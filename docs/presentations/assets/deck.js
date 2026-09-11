/* Zoom is fixed via CSS media queries (see deck.css) so every slide renders at the
   same scale. Per-slide auto-fit zoom was removed because it computed a different
   scale per slide's content, making the deck appear to zoom in/out while navigating. */

(function () {
  var MAX_COL_WIDTH = 280;
  var MIN_COL_WIDTH = 130;
  var STEP = 10;

  function addColumnsUntilNoScroll() {
    var slide = document.querySelector('.slide');
    if (!slide) return;
    var grids = slide.querySelectorAll('.challenge-grid');
    if (!grids.length) return;

    var width = MAX_COL_WIDTH;
    setMinColumnWidth(grids, width);

    // Narrowing the minimum column width lets auto-fit place another column,
    // shortening the grid instead of leaving the slide needing a scrollbar.
    while (slide.scrollHeight > slide.clientHeight + 1 && width > MIN_COL_WIDTH) {
      width -= STEP;
      setMinColumnWidth(grids, width);
    }
  }

  function setMinColumnWidth(grids, width) {
    grids.forEach(function (grid) {
      grid.style.setProperty('--challenge-min-col', width + 'px');
    });
  }

  function scheduleFit() {
    window.requestAnimationFrame(addColumnsUntilNoScroll);
  }

  window.addEventListener('load', scheduleFit);
  window.addEventListener('resize', scheduleFit);
  if (document.fonts) document.fonts.ready.then(scheduleFit);
})();
