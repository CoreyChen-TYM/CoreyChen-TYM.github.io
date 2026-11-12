(() => {
  const viewer = document.createElement('dialog');
  viewer.className = 'image-viewer';
  viewer.setAttribute('aria-label', 'Enlarged image');

  const image = document.createElement('img');
  const close = document.createElement('button');
  close.type = 'button';
  close.className = 'image-viewer-close';
  close.textContent = '×';
  close.setAttribute('aria-label', 'Close image');
  viewer.append(image, close);
  document.body.append(viewer);

  document.querySelectorAll('article figure a, .journal-project a, a[data-preview]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      image.src = link.href;
      image.alt = link.querySelector('img')?.alt || link.textContent.trim();
      viewer.showModal();
    });
  });

  // Clicking the enlarged image, its surrounding space, or the button closes it.
  viewer.addEventListener('click', () => viewer.close());
  viewer.addEventListener('close', () => image.removeAttribute('src'));
})();
