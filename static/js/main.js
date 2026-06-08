/**
 * htmforge.nepidesk.de · main.js
 * - Parallax (Hero)
 * - Scroll Reveal + Typewriter (IntersectionObserver)
 * - Stack bar animation
 * - Toast auto-dismiss
 * - Clipboard copy
 * - Header shadow on scroll
 */

// ── Parallax ──────────────────────────────────────────────
(function initParallax() {
  const layers = document.querySelectorAll('[data-speed]');
  if (!layers.length) return;
  let ticking = false;
  function apply() {
    const y = window.scrollY;
    layers.forEach(el => {
      el.style.transform = `translateY(${y * (parseFloat(el.dataset.speed) || 0.3)}px)`;
    });
    ticking = false;
  }
  window.addEventListener('scroll', () => {
    if (!ticking) { requestAnimationFrame(apply); ticking = true; }
  }, { passive: true });
})();


// ── Typewriter ────────────────────────────────────────────
(function initTypewriter() {
  // Each .typewriter element has data-typewriter="Text to type"
  // Inside: <span class="typewriter-text"> + <span class="typewriter-cursor">
  const CHAR_DELAY = 55;   // ms per character
  const START_DELAY = 200; // ms after entering viewport

  function type(el) {
    const text    = el.dataset.typewriter || '';
    const display = el.querySelector('.typewriter-text');
    const cursor  = el.querySelector('.typewriter-cursor');
    if (!display || !text) return;

    let i = 0;
    display.textContent = '';

    setTimeout(() => {
      const interval = setInterval(() => {
        display.textContent += text[i];
        i++;
        if (i >= text.length) {
          clearInterval(interval);
          // keep cursor blinking — looks nice
        }
      }, CHAR_DELAY);
    }, START_DELAY);
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      type(entry.target);
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('.typewriter').forEach(el => observer.observe(el));
})();


// ── Scroll Reveal ─────────────────────────────────────────
(function initReveal() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el    = entry.target;
      const delay = parseInt(el.dataset.delay) || 0;
      setTimeout(() => el.classList.add('visible'), delay);

      // Stack bar: set CSS var from inline style width, trigger transition
      const fill = el.querySelector('.stack-bar-fill');
      if (fill) {
        const target = fill.style.width;          // e.g. "90%"
        fill.style.width = '0%';                  // reset first
        setTimeout(() => { fill.style.width = target; }, delay + 80);
      }

      observer.unobserve(el);
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
})();


// ── Toast auto-dismiss ────────────────────────────────────
document.body.addEventListener('htmx:afterSwap', () => {
  const toast = document.querySelector('#toast-slot .toast');
  if (!toast) return;
  const ms = parseInt(toast.dataset.duration) || 2500;
  setTimeout(() => {
    toast.style.transition = 'opacity .3s, transform .3s';
    toast.style.opacity    = '0';
    toast.style.transform  = 'translateY(8px)';
    setTimeout(() => toast.remove(), 320);
  }, ms);
});


// ── Clipboard copy ────────────────────────────────────────
document.body.addEventListener('click', e => {
  const btn = e.target.closest('.svc-copy');
  if (!btn) return;
  const url = btn.dataset.url;
  if (!url) return;
  navigator.clipboard.writeText(url).catch(() => {});
});


// ── Header shadow on scroll ───────────────────────────────
(function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (ticking) return;
    requestAnimationFrame(() => {
      header.style.boxShadow = window.scrollY > 20
        ? '0 8px 40px rgba(0,0,0,.7)'
        : 'none';
      ticking = false;
    });
    ticking = true;
  }, { passive: true });
})();