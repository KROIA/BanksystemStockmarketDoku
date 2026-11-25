// Visitor stats and reader feedback.
// - GoatCounter (dashboard: bsmdocs.goatcounter.com) counts page views. No cookies; previews on
//   127.0.0.1 aren't counted. Searches show up there as "search: <words>" or
//   "search (no results): <words>".
// - A "?" next to every section heading and a button at the end of each page open the Tally
//   form X54X74. Its hidden fields get the page address and the section heading.
//   The Tally script loads on the first click only; if it's blocked, the form opens in a new tab.
(function () {
  const gc = document.createElement("script");
  gc.async = true;
  gc.src = "https://gc.zgo.at/count.js";
  gc.dataset.goatcounter = "https://bsmdocs.goatcounter.com/count";
  document.head.append(gc);

  // A search counts when the search box loses focus or Enter is pressed (result clicked, Esc, ...)
  const box = document.querySelector(".md-search__input");
  box?.addEventListener("change", () => {
    const q = box.value.trim().toLowerCase().slice(0, 60);
    if (q.length < 2 || !window.goatcounter?.count) return;
    const none = !document.querySelector(".md-search-result__item");
    goatcounter.count({ path: (none ? "search (no results): " : "search: ") + q, title: "Search", event: true });
  });

  const article = document.querySelector(".md-content__inner");
  if (!article || document.querySelector("img.hero")) return;   // no feedback buttons on the home page

  const FORM = "X54X74";
  const t = document.documentElement.lang.startsWith("de")
    ? { section: "Ist in diesem Abschnitt etwas unklar oder fehlt etwas?",
        page: "Ist auf dieser Seite etwas unklar oder fehlt etwas?", button: "Sag es uns", whole: "(ganze Seite)" }
    : { section: "Something unclear or missing in this section?",
        page: "Something unclear or missing on this page?", button: "Tell us", whole: "(whole page)" };
  const ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h4v3a1 1 0 0 0 1 1h.5c.25 0 .5-.1.7-.29L13.9 18H20a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zm0 2h16v12h-6.92L10 19.08V16H4zm8.19 1.5c-.89 0-1.6.18-2.14.54-.55.36-.83.96-.78 1.65h1.97c0-.28.1-.49.26-.63.2-.14.42-.21.69-.21.31 0 .58.08.76.26.18.17.27.39.27.69 0 .28-.08.53-.22.74-.17.22-.38.4-.64.54-.52.32-.86.6-1.07.84-.19.24-.29.58-.29 1.08h2c0-.28.05-.5.14-.68.09-.17.26-.32.52-.47.46-.21.84-.49 1.13-.85.29-.37.44-.76.44-1.2q0-1.05-.81-1.68c-.54-.41-1.29-.62-2.23-.62M11 12v2h2v-2z"/></svg>';

  let tally;   // Promise for the Tally script
  function link(section, cls, html, title) {
    const fields = { page: location.origin + location.pathname, section };
    const a = document.createElement("a");
    a.className = cls;
    a.href = `https://tally.so/r/${FORM}?` + new URLSearchParams(fields);
    a.target = "_blank";
    a.rel = "noopener";
    a.innerHTML = html;
    if (title) { a.title = title; a.setAttribute("aria-label", title); }
    a.addEventListener("click", e => {
      e.preventDefault();
      tally ??= new Promise((ok, fail) => {
        const s = document.createElement("script");
        s.src = "https://tally.so/widgets/embed.js";
        s.onload = ok;
        s.onerror = fail;
        document.head.append(s);
      });
      tally.then(() => Tally.openPopup(FORM, { layout: "modal", width: 600, hiddenFields: fields }),
                 () => open(a.href, "_blank", "noopener"));
    });
    return a;
  }

  for (const h of article.querySelectorAll(":scope > h2[id]"))
    h.append(link(h.textContent.replace(/¶$/, "").trim(), "feedback-icon", ICON, t.section));

  const end = document.createElement("p");
  end.className = "feedback-end";
  end.append(t.page + " ", link(t.whole, "md-button", ICON + t.button));
  article.append(end);
})();
