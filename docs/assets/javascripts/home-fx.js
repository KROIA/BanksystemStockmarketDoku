// Home page effects: the hero picture scrolls slower than the page (parallax), the feature
// cards lift and tilt toward the mouse, and the sections below the first screen slide in.
// Runs only on the page with the hero picture, and not at all when the visitor asks for
// reduced motion. Without this script the page simply shows everything at once.
(function () {
  const hero = document.querySelector("img.hero");
  if (!hero || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  document.body.classList.add("home-fx");

  // Parallax: the picture is drawn 12% larger and moves inside its frame while it is on screen
  const frame = hero.parentElement;
  let queued = false;
  const parallax = () => {
    queued = false;
    const r = frame.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;
    const p = (innerHeight - r.top) / (innerHeight + r.height);   // 0 entering, 1 leaving
    hero.style.setProperty("--hero-shift", ((p - 0.5) * r.height * 0.1).toFixed(1) + "px");
  };
  addEventListener("scroll", () => {
    if (!queued) { queued = true; requestAnimationFrame(parallax); }
  }, { passive: true });
  parallax();

  // Cards tilt toward the mouse, with a soft glare where the pointer is
  const cards = document.querySelectorAll(".grid.cards > ul > li");
  if (matchMedia("(hover: hover) and (pointer: fine)").matches) {
    cards.forEach(card => {
      card.addEventListener("mousemove", e => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        card.style.setProperty("--rx", ((0.5 - y) * 8).toFixed(2) + "deg");
        card.style.setProperty("--ry", ((x - 0.5) * 8).toFixed(2) + "deg");
        card.style.setProperty("--gx", (x * 100).toFixed(1) + "%");
        card.style.setProperty("--gy", (y * 100).toFixed(1) + "%");
      });
      card.addEventListener("mouseleave", () => {
        card.style.removeProperty("--rx");
        card.style.removeProperty("--ry");
      });
    });
  }

  // Slide in: only what starts below the first screen; cards in a row follow each other
  const seen = new IntersectionObserver(entries => entries.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add("is-visible"); seen.unobserve(en.target); }
  }), { threshold: 0.15 });
  const blocks = [...document.querySelectorAll(".md-content__inner > :not(h1):not(.grid)")];
  [...blocks, ...cards].forEach(el => {
    if (el.getBoundingClientRect().top < innerHeight) return;
    if (el.matches("li")) el.style.setProperty("--delay", [...el.parentElement.children].indexOf(el) * 0.1 + "s");
    el.classList.add("reveal");
    seen.observe(el);
  });
})();
