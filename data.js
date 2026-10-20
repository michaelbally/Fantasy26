/*
  Saggy Dads Pro League - season data.

  The manager cards read this file, and so does the form column on new gameweek pages.
  Each new gameweek: add one more object to "gameweeks" (copy the last one and edit).

  pts    = gameweek score after any hit      hit   = points lost to a transfer hit
  tr     = transfers counted by FPL          bench = points left on the bench
  cap    = captain's return, already doubled by = captain
  chip   = chip played that week (only present when one was)
  globalAvg = FPL-wide average score (null where we don't have it)
*/
window.LEAGUE = {
  "managers": [
      {
          "id": "simon",
          "name": "Simon Edwards",
          "team": "Pending Moderation",
          "titles": 3,
          "runnersUp": 2,
          "seasons": 8,
          "tagline": "Led the table for the first six gameweeks and treats a transfer as a last resort."
      },
      {
          "id": "ball",
          "name": "Michael Ball",
          "team": "Sao Baulo",
          "titles": 1,
          "runnersUp": 1,
          "seasons": 5,
          "tagline": "The quiet assassin: tidy squad, tiny bench, no fuss."
      },
      {
          "id": "xavier",
          "name": "Joel Xavier",
          "team": "Jianguo FC",
          "titles": 1,
          "runnersUp": 2,
          "seasons": 5,
          "tagline": "Wildcard pioneer with a complicated relationship with Bruno Fernandes."
      },
      {
          "id": "desmond",
          "name": "Michael Desmond",
          "team": "Tony Yeboah's Eye",
          "titles": 1,
          "runnersUp": 0,
          "seasons": 4,
          "tagline": "Lives and dies by the armband: 46 points one week, 4 the next."
      },
      {
          "id": "dring",
          "name": "Daniel Dring",
          "team": "The Two Time",
          "titles": 2,
          "runnersUp": 0,
          "seasons": 4,
          "tagline": "A bench full of points and a team sheet full of questions."
      },
      {
          "id": "kane",
          "name": "Jonathan Kane",
          "team": "Real Moat",
          "titles": 0,
          "runnersUp": 1,
          "seasons": 4,
          "tagline": "Respectable scores, a long stay at the bottom, and the league record for points left on the bench."
      }
  ],
  "gameweeks": [
    {
      "gw": 1, "globalAvg": null,
      "awards": {},
      "results": {
        "simon": {"pts": 57, "hit": 0, "tr": 0, "bench": 7, "cap": 4, "by": "Haaland"},
        "ball": {"pts": 52, "hit": 0, "tr": 0, "bench": 8, "cap": 4, "by": "Haaland"},
        "dring": {"pts": 51, "hit": 0, "tr": 0, "bench": 15, "cap": 4, "by": "Haaland"},
        "desmond": {"pts": 48, "hit": 0, "tr": 0, "bench": 13, "cap": 4, "by": "B.Fernandes"},
        "xavier": {"pts": 39, "hit": 0, "tr": 0, "bench": 6, "cap": 4, "by": "B.Fernandes"},
        "kane": {"pts": 39, "hit": 0, "tr": 0, "bench": 9, "cap": 4, "by": "Haaland"}
      }
    },
    {
      "gw": 2, "globalAvg": null,
      "awards": {},
      "results": {
        "simon": {"pts": 103, "hit": 0, "tr": 0, "bench": 13, "cap": 26, "by": "Haaland"},
        "desmond": {"pts": 97, "hit": 4, "tr": 2, "bench": 1, "cap": 46, "by": "B.Fernandes"},
        "xavier": {"pts": 88, "hit": 0, "tr": 1, "bench": 8, "cap": 46, "by": "B.Fernandes"},
        "dring": {"pts": 75, "hit": 0, "tr": 1, "bench": 19, "cap": 26, "by": "Haaland"},
        "kane": {"pts": 69, "hit": 0, "tr": 0, "bench": 9, "cap": 26, "by": "Haaland"},
        "ball": {"pts": 65, "hit": 0, "tr": 1, "bench": 4, "cap": 26, "by": "Haaland"}
      }
    },
    {
      "gw": 3, "globalAvg": 51,
      "awards": {},
      "results": {
        "xavier": {"pts": 70, "hit": 0, "tr": 0, "bench": 11, "cap": 18, "by": "Haaland", "chip": "Wildcard"},
        "ball": {"pts": 70, "hit": 0, "tr": 1, "bench": 6, "cap": 18, "by": "Haaland"},
        "kane": {"pts": 62, "hit": 0, "tr": 2, "bench": 10, "cap": 18, "by": "Haaland"},
        "dring": {"pts": 56, "hit": 0, "tr": 0, "bench": 14, "cap": 18, "by": "Haaland"},
        "desmond": {"pts": 48, "hit": 0, "tr": 1, "bench": 2, "cap": 4, "by": "B.Fernandes"},
        "simon": {"pts": 41, "hit": 0, "tr": 0, "bench": 11, "cap": 18, "by": "Haaland"}
      }
    },
    {
      "gw": 4, "globalAvg": 69,
      "awards": {},
      "results": {
        "ball": {"pts": 74, "hit": 0, "tr": 1, "bench": 1, "cap": 18, "by": "Haaland"},
        "simon": {"pts": 72, "hit": 0, "tr": 0, "bench": 3, "cap": 18, "by": "Haaland"},
        "desmond": {"pts": 64, "hit": 0, "tr": 1, "bench": 14, "cap": 10, "by": "Palmer"},
        "kane": {"pts": 64, "hit": 4, "tr": 2, "bench": 10, "cap": 16, "by": "Rogers"},
        "dring": {"pts": 57, "hit": 0, "tr": 0, "bench": 7, "cap": 18, "by": "Haaland"},
        "xavier": {"pts": 55, "hit": 0, "tr": 1, "bench": 17, "cap": 4, "by": "Isak"}
      }
    },
    {
      "gw": 5, "globalAvg": 48,
      "awards": {},
      "results": {
        "simon": {"pts": 52, "hit": 0, "tr": 3, "bench": 18, "cap": 12, "by": "Haaland"},
        "xavier": {"pts": 46, "hit": 0, "tr": 1, "bench": 7, "cap": 12, "by": "Haaland"},
        "dring": {"pts": 43, "hit": 0, "tr": 0, "bench": 11, "cap": 12, "by": "Haaland"},
        "kane": {"pts": 40, "hit": 4, "tr": 2, "bench": 31, "cap": 12, "by": "Haaland"},
        "ball": {"pts": 38, "hit": 0, "tr": 1, "bench": 7, "cap": 12, "by": "Haaland"},
        "desmond": {"pts": 28, "hit": 0, "tr": 1, "bench": 5, "cap": 4, "by": "Palmer"}
      }
    },
    {
      "gw": 6, "globalAvg": 58,
      "awards": {},
      "results": {
        "ball": {"pts": 69, "hit": 0, "tr": 1, "bench": 13, "cap": 12, "by": "Haaland"},
        "xavier": {"pts": 59, "hit": 0, "tr": 1, "bench": 6, "cap": 2, "by": "B.Fernandes"},
        "desmond": {"pts": 56, "hit": 0, "tr": 1, "bench": 14, "cap": 18, "by": "Rogers"},
        "simon": {"pts": 55, "hit": 0, "tr": 0, "bench": 4, "cap": 12, "by": "Haaland"},
        "kane": {"pts": 46, "hit": 0, "tr": 0, "bench": 19, "cap": 12, "by": "Haaland", "chip": "Wildcard"},
        "dring": {"pts": 42, "hit": 0, "tr": 0, "bench": 9, "cap": 12, "by": "Haaland"}
      }
    },
    {
      "gw": 7, "globalAvg": 59,
      "awards": {"transferOfTheWeek": ["desmond"], "transferFlop": [], "captainsPick": [], "armbandOfShame": ["desmond"], "benchWarmer": ["kane"], "tidiestBench": ["ball"]},
      "results": {
        "ball": {"pts": 78, "hit": 0, "tr": 1, "bench": 2, "cap": 26, "by": "Haaland"},
        "kane": {"pts": 70, "hit": 0, "tr": 0, "bench": 18, "cap": 26, "by": "Haaland"},
        "xavier": {"pts": 63, "hit": 0, "tr": 1, "bench": 15, "cap": 26, "by": "Haaland"},
        "simon": {"pts": 61, "hit": 0, "tr": 0, "bench": 5, "cap": 26, "by": "Haaland"},
        "dring": {"pts": 60, "hit": 0, "tr": 0, "bench": 14, "cap": 26, "by": "Haaland"},
        "desmond": {"pts": 53, "hit": 0, "tr": 1, "bench": 3, "cap": 4, "by": "Palmer"}
      }
    }
  ]
};
