"""
Fetch a Fantasy Premier League mini-league gameweek and print a compact stats brief.

Stdlib only -- no pip install needed. Run:
    py fpl_brief.py --league 979533              # latest finished gameweek
    py fpl_brief.py --league 979533 --gw 7       # a specific gameweek
    py fpl_brief.py --league 979533 --out brief.md

Paste the output into Claude along with the house-style prompt.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://fantasy.premierleague.com/api"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) fpl-brief/1.0"}
DELAY = 0.4          # polite gap between requests
CACHE = Path(__file__).parent / ".cache"

CHIP_NAMES = {"3xc": "Triple Captain", "bboost": "Bench Boost",
              "freehit": "Free Hit", "wildcard": "Wildcard"}


def fetch(path, cache_as=None, retries=3):
    """GET a JSON endpoint. Returns None on 404. Caches to disk if cache_as given."""
    if cache_as:
        cached = CACHE / cache_as
        if cached.exists():
            return json.loads(cached.read_text(encoding="utf-8"))

    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(BASE + path, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            time.sleep(DELAY)
            if cache_as:
                CACHE.mkdir(exist_ok=True)
                (CACHE / cache_as).write_text(json.dumps(data), encoding="utf-8")
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            last = e
            time.sleep(2 ** attempt)
        except Exception as e:
            last = e
            time.sleep(2 ** attempt)
    raise RuntimeError("failed after %d attempts: %s (%s)" % (retries, path, last))


def emit(lines, path):
    text = "\n".join(lines)
    sys.stdout.reconfigure(encoding="utf-8")   # team names contain apostrophes/emoji
    print(text)
    if path:
        Path(path).write_text(text, encoding="utf-8")
        print("\n[written to %s]" % path, file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--league", type=int, required=True)
    ap.add_argument("--gw", type=int, help="gameweek (default: latest finished)")
    ap.add_argument("--out", help="write the brief to this file as well as stdout")
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args()

    if args.no_cache and CACHE.exists():
        for f in CACHE.iterdir():
            f.unlink()

    out = []
    say = out.append

    # ---- 1. bootstrap: the lookup table everything joins against -----------
    bs = fetch("/bootstrap-static/", cache_as="bootstrap.json")
    players = {e["id"]: e for e in bs["elements"]}
    teams = {t["id"]: t["short_name"] for t in bs["teams"]}
    events = {e["id"]: e for e in bs["events"]}

    def pname(pid):
        p = players.get(pid)
        if not p:
            return "#%s" % pid
        return "%s (%s)" % (p["web_name"], teams.get(p["team"], "?"))

    finished = [e["id"] for e in bs["events"] if e["finished"]]
    gw = args.gw or (max(finished) if finished else None)

    # ---- 2. the league -----------------------------------------------------
    lg = fetch("/leagues-classic/%d/standings/" % args.league)
    if lg is None:
        sys.exit("league %d not found" % args.league)

    # Pre-GW1 the members sit in new_entries with no points; afterwards they
    # move to standings.results. Read whichever is populated.
    rows = lg["standings"]["results"]
    preseason = not rows
    if preseason:
        rows = [{"entry": r["entry"],
                 "entry_name": r["entry_name"],
                 "player_name": "%s %s" % (r["player_first_name"], r["player_last_name"]),
                 "joined_time": r["joined_time"]}
                for r in lg["new_entries"]["results"]]

    say("# %s -- data brief" % lg["league"]["name"])
    say("")

    if gw is None or preseason:
        say("**Status:** pre-season, no gameweek finished. %d managers joined." % len(rows))
        say("")
        say("## Managers")
        say("")
        for r in sorted(rows, key=lambda r: r.get("joined_time", "")):
            say("- **%s** -- %s (entry %s, joined %s)"
                % (r["entry_name"], r["player_name"], r["entry"],
                   r.get("joined_time", "")[:10]))
        say("")
        nxt = next((e for e in bs["events"] if e.get("is_next")), None)
        if nxt:
            say("GW%d deadline: %s. Squads only become readable once it passes -- "
                "rerun then for the season preview." % (nxt["id"], nxt["deadline_time"]))
        emit(out, args.out)
        return

    ev = events[gw]
    say("**Gameweek %d** | game average %s | highest score in the game %s"
        % (gw, ev.get("average_entry_score"), ev.get("highest_score")))
    nxt = next((e for e in bs["events"] if e.get("is_next")), None)
    if nxt:
        say("Next deadline: GW%d, %s" % (nxt["id"], nxt["deadline_time"]))
    say("")

    # ---- 3. live points for every player this GW ---------------------------
    live = fetch("/event/%d/live/" % gw, cache_as="live_%d.json" % gw)
    lpts = {e["id"]: e["stats"]["total_points"] for e in live["elements"]}
    lstats = {e["id"]: e["stats"] for e in live["elements"]}

    # ---- 4. per-manager detail --------------------------------------------
    managers = []
    for r in rows:
        eid = r["entry"]
        hist = fetch("/entry/%d/history/" % eid)
        picks = fetch("/entry/%d/event/%d/picks/" % (eid, gw))
        trans = fetch("/entry/%d/transfers/" % eid) or []

        row = next((c for c in hist["current"] if c["event"] == gw), None)
        if row is None:
            continue

        chip = next((c["name"] for c in hist.get("chips", []) if c["event"] == gw), None)
        chips_used = [(CHIP_NAMES.get(c["name"], c["name"]), c["event"])
                      for c in hist.get("chips", [])]

        cap = vice = None
        bench = []
        if picks:
            for p in picks["picks"]:
                if p["is_captain"]:
                    cap = p
                elif p["is_vice_captain"]:
                    vice = p
                if p["multiplier"] == 0:
                    bench.append(p)

        managers.append({
            "name": r["entry_name"], "who": r.get("player_name", ""),
            "pts": row["points"], "hit": row["event_transfers_cost"],
            "net": row["points"] - row["event_transfers_cost"],
            "total": row["total_points"], "bench": row["points_on_bench"],
            "n_trans": row["event_transfers"],
            "rank": r.get("rank"), "last_rank": r.get("last_rank"),
            "overall": row["overall_rank"], "value": row["value"] / 10.0,
            "chip": CHIP_NAMES.get(chip, chip), "chips_used": chips_used,
            "cap": cap, "vice": vice, "bench_players": bench,
            "trans": [t for t in trans if t["event"] == gw],
            "autosubs": picks.get("automatic_subs", []) if picks else [],
        })

    if not managers:
        say("No manager data for GW%d yet." % gw)
        emit(out, args.out)
        return

    managers.sort(key=lambda m: -m["net"])

    # ---- 5. the brief -----------------------------------------------------
    say("## Table")
    say("")
    say("| Pos | Team | Manager | GW | Hit | Net | Total | Moved |")
    say("|---|---|---|---|---|---|---|---|")
    for m in managers:
        move = ""
        if m["rank"] and m["last_rank"]:
            d = m["last_rank"] - m["rank"]
            move = "+%d" % d if d > 0 else (str(d) if d < 0 else "=")
        say("| %s | %s | %s | %d | %s | %d | %d | %s |"
            % (m["rank"] or "-", m["name"], m["who"], m["pts"],
               "-%d" % m["hit"] if m["hit"] else "0", m["net"], m["total"], move))
    say("")
    avg = sum(m["net"] for m in managers) / float(len(managers))
    say("League average this GW: %.1f (game average %s)"
        % (avg, ev.get("average_entry_score")))
    say("")

    say("## Manager by manager")
    say("")
    for m in managers:
        say("### %s -- %s" % (m["name"], m["who"]))
        if m["hit"]:
            say("- Score: %d, minus a %dpt hit for %d transfers = **%d**"
                % (m["pts"], m["hit"], m["n_trans"], m["net"]))
        else:
            say("- Score: %d (%d transfers, no hit)" % (m["pts"], m["n_trans"]))
        if m["chip"]:
            say("- **Chip played: %s**" % m["chip"])
        if m["cap"]:
            cid = m["cap"]["element"]
            raw, mult = lpts.get(cid, 0), m["cap"]["multiplier"]
            st = lstats.get(cid, {})
            say("- Captain: %s -- returned %dpts (x%d = %d)"
                % (pname(cid), raw, mult, raw * mult))
            say("  - %s mins, %sG %sA, bonus %s"
                % (st.get("minutes", 0), st.get("goals_scored", 0),
                   st.get("assists", 0), st.get("bonus", 0)))
        if m["vice"]:
            say("- Vice: %s -- %dpts" % (pname(m["vice"]["element"]),
                                         lpts.get(m["vice"]["element"], 0)))
        bench_detail = ""
        if m["bench_players"]:
            bench_detail = " (%s)" % ", ".join(
                "%s %d" % (pname(b["element"]), lpts.get(b["element"], 0))
                for b in m["bench_players"])
        say("- Points left on bench: **%d**%s" % (m["bench"], bench_detail))
        for t in m["trans"]:
            i, o = t["element_in"], t["element_out"]
            say("- Transfer: OUT %s (%dpts this GW) -> IN %s (%dpts this GW), made %s"
                % (pname(o), lpts.get(o, 0), pname(i), lpts.get(i, 0), t["time"][:16]))
        for a in m["autosubs"]:
            say("- Auto-sub: %s out, %s in"
                % (pname(a["element_out"]), pname(a["element_in"])))
        say("- Squad value %.1fm, overall rank %s" % (m["value"], "{:,}".format(m["overall"])))
        if m["chips_used"]:
            say("- Chips used so far: %s"
                % ", ".join("%s (GW%d)" % (n, e) for n, e in m["chips_used"]))
        say("")

    say("## Headlines")
    say("")
    say("- Best: **%s** with %d" % (managers[0]["name"], managers[0]["net"]))
    say("- Worst: **%s** with %d" % (managers[-1]["name"], managers[-1]["net"]))
    benched = max(managers, key=lambda m: m["bench"])
    say("- Most points benched: **%s** (%d)" % (benched["name"], benched["bench"]))
    hits = [m for m in managers if m["hit"]]
    if hits:
        say("- Took hits: %s" % ", ".join("%s (-%d)" % (m["name"], m["hit"]) for m in hits))
    caps = [m for m in managers if m["cap"]]
    if caps:
        wc = min(caps, key=lambda m: lpts.get(m["cap"]["element"], 0))
        say("- Worst captain: **%s** with %s on %d"
            % (wc["name"], pname(wc["cap"]["element"]), lpts.get(wc["cap"]["element"], 0)))
    game_avg = ev.get("average_entry_score") or 0
    beat = [m["name"] for m in managers if m["net"] > game_avg]
    say("- Beat the game average (%s): %s" % (game_avg, ", ".join(beat) if beat else "nobody"))

    emit(out, args.out)


if __name__ == "__main__":
    main()
