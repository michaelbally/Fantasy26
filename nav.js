/*
  Saggy Dads Pro League — shared navigation.

  Every page loads this file, so the menu only ever lives here.
  Each new gameweek: change LATEST_GW below. That's the only edit.
*/
(function () {
  var LATEST_GW = 7;

  var nav = document.getElementById('site-nav');
  if (!nav) return;

  // Work out which page we're on, e.g. "gw3", "stats", "index".
  var page = location.pathname.split('/').pop().replace(/\.html$/, '') || 'index';
  var gwMatch = /^gw(\d+)$/.exec(page);
  var currentGw = gwMatch ? parseInt(gwMatch[1], 10) : null;

  function active(isActive) {
    return isActive ? ' is-active' : '';
  }

  var chips = '';
  for (var n = 1; n <= LATEST_GW; n++) {
    chips += '<a href="gw' + n + '.html"' +
      (n === currentGw ? ' class="is-active"' : '') + '>GW' + n + '</a>';
  }

  nav.innerHTML =
    '<div class="site-nav__inner">' +
      '<a href="index.html" class="site-nav__link' + active(page === 'index') + '">Latest</a>' +
      '<details class="site-nav__dropdown">' +
        '<summary class="site-nav__link' + active(currentGw !== null) + '">Gameweeks</summary>' +
        '<div class="site-nav__panel">' + chips + '</div>' +
      '</details>' +
      '<a href="stats.html" class="site-nav__link' + active(page === 'stats') + '">Stats</a>' +
      '<a href="managers.html" class="site-nav__link' + active(page === 'managers') + '">Managers</a>' +
      '<a href="hall-of-fame.html" class="site-nav__link' + active(page === 'hall-of-fame') + '">Hall of Fame</a>' +
    '</div>';

  // Close the gameweek dropdown when clicking outside it.
  document.addEventListener('click', function (e) {
    var open = nav.querySelector('.site-nav__dropdown[open]');
    if (open && !open.contains(e.target)) open.removeAttribute('open');
  });
})();
