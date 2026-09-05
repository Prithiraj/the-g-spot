'use strict';
// Progressive enhancements only. All information and outbound links work without JS.
(() => {
  const dialog = document.querySelector('#lightbox');
  const triggers = [...document.querySelectorAll('.gallery-trigger')];
  let active = 0;
  let previousFocus = null;
  if (dialog && typeof dialog.showModal === 'function' && triggers.length) {
    const image = dialog.querySelector('#lightbox-image');
    const caption = dialog.querySelector('#lightbox-caption');
    const count = dialog.querySelector('#lightbox-count');
    function show(index) {
      active = (index + triggers.length) % triggers.length;
      const trigger = triggers[active];
      image.src = trigger.href;
      image.alt = trigger.querySelector('img').alt;
      caption.textContent = ['The wooden bar, signs and memorabilia.', 'A look out onto the patio.', 'The G Spot. on North Scenic Highway.'][active];
      count.textContent = `${String(active + 1).padStart(2, '0')} / ${String(triggers.length).padStart(2, '0')}`;
    }
    triggers.forEach((trigger, index) => {
      trigger.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
        event.preventDefault();
        previousFocus = trigger;
        show(index);
        dialog.showModal();
        document.body.classList.add('dialog-open');
        dialog.querySelector('.lightbox-close').focus();
      });
    });
    dialog.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
    dialog.querySelector('.lightbox-previous').addEventListener('click', () => show(active - 1));
    dialog.querySelector('.lightbox-next').addEventListener('click', () => show(active + 1));
    dialog.addEventListener('keydown', event => {
      if (event.key === 'ArrowRight') { event.preventDefault(); show(active + 1); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); show(active - 1); }
    });
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const box = dialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('dialog-open');
      previousFocus?.focus({ preventScroll: true });
    });
  }
  const copy = document.querySelector('.copy-address');
  const status = document.querySelector('#copy-status');
  if (copy && status && window.isSecureContext && navigator.clipboard?.writeText) {
    copy.hidden = false;
    copy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText('The G Spot., 3825 N Scenic Hwy, Lake Wales, FL 33898');
        status.textContent = 'Address copied. See you on Scenic Highway.';
      } catch {
        status.textContent = 'Copy unavailable. Select the address above, or use Get directions.';
      }
    });
  }
  const links = [...document.querySelectorAll('.main-nav a')];
  if ('IntersectionObserver' in window && links.length) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        links.forEach(link => {
          if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      }
    }, { rootMargin: '-18% 0px -55% 0px', threshold: 0 });
    links.forEach(link => { const section = document.querySelector(link.hash); if (section) observer.observe(section); });
    const hero = document.querySelector('#top');
    if (hero) observer.observe(hero);
  }
})();
