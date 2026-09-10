(function () {
  function fitSlideContent() {
    var slide = document.querySelector('.slide');
    var content = slide && slide.querySelector('.slide-content');
    var navigation = document.querySelector('.nav');
    if (!slide || !content) return;

    slide.style.overflowY = 'hidden';
    content.style.zoom = '1';

    var contentRect = content.getBoundingClientRect();
    var slideRect = slide.getBoundingClientRect();
    var navigationHeight = navigation ? navigation.getBoundingClientRect().height + 28 : 32;
    var availableHeight = slideRect.height - (contentRect.top - slideRect.top) - navigationHeight;
    var availableWidth = slideRect.width - (contentRect.left - slideRect.left) - 24;
    var heightScale = availableHeight / contentRect.height;
    var widthScale = availableWidth / contentRect.width;
    var scale = Math.min(heightScale, widthScale, 1.35);

    content.style.zoom = scale.toFixed(3);

    for (var pass = 0; pass < 3; pass += 1) {
      var fittedRect = content.getBoundingClientRect();
      var fittedBottom = fittedRect.bottom - slideRect.top;
      var bottomLimit = slideRect.height - navigationHeight;
      if (fittedBottom <= bottomLimit) break;
      scale *= (bottomLimit - (fittedRect.top - slideRect.top)) / fittedRect.height;
      content.style.zoom = Math.max(0.35, scale).toFixed(3);
    }
  }

  function scheduleFit() {
    window.requestAnimationFrame(fitSlideContent);
  }

  window.addEventListener('load', scheduleFit);
  window.addEventListener('resize', scheduleFit);
  if (document.fonts) document.fonts.ready.then(scheduleFit);
})();
