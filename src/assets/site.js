// Theory pages: collapse the topic list on small screens and
// highlight the current section in "On this page".
(function () {
  var details = document.querySelector(".sidebar-details");
  var narrow = window.matchMedia("(max-width: 56rem)");
  function syncSidebar() {
    if (details) details.open = !narrow.matches;
  }
  syncSidebar();
  narrow.addEventListener("change", syncSidebar);

  // On phones, close "On this page" after picking a section.
  document.querySelectorAll(".narrow-nav a").forEach(function (a) {
    a.addEventListener("click", function () { a.closest("details").open = false; });
  });

  var links = Array.prototype.slice.call(document.querySelectorAll(".toc .toc-list a"));
  if (!links.length || !("IntersectionObserver" in window)) return;
  var ids = links.map(function (a) { return a.getAttribute("href").slice(1); });
  var headings = ids.map(function (id) { return document.getElementById(id); }).filter(Boolean);

  function setActive(id) {
    links.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + id); });
  }
  var observer = new IntersectionObserver(function () {
    // The active section is the last heading above the upper third of the viewport.
    var line = window.innerHeight / 3;
    var current = headings[0];
    headings.forEach(function (h) { if (h.getBoundingClientRect().top < line) current = h; });
    if (current) setActive(current.id);
  }, { rootMargin: "0px 0px -60% 0px", threshold: [0, 1] });
  headings.forEach(function (h) { observer.observe(h); });
})();
