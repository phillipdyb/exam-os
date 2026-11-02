// Earlier exams: answer multiple-choice questions on the page.
// Answers are remembered in localStorage so you can come back to an exam.
(function () {
  var key = "os-exam:" + location.pathname;
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem(key)) || {}; } catch (e) { saved = {}; }

  var scoreEl = document.querySelector(".score");
  var total = scoreEl ? Number(scoreEl.dataset.total) : 0;
  var lists = Array.prototype.slice.call(document.querySelectorAll(".options"));

  function store() {
    try { localStorage.setItem(key, JSON.stringify(saved)); } catch (e) { /* private mode */ }
  }

  function updateScore() {
    if (!scoreEl) return;
    var answered = 0, right = 0;
    Object.keys(saved).forEach(function (qid) {
      answered++;
      if (saved[qid].right) right++;
    });
    if (!answered) {
      scoreEl.textContent = total + " multiple-choice questions. Click an option to answer.";
      return;
    }
    scoreEl.innerHTML = "<strong>" + right + " of " + answered + "</strong> right so far, " +
      (total - answered) + " multiple-choice left.";
  }

  function markJump(list, isRight) {
    var section = list.closest(".question");
    if (!section) return;
    document.querySelectorAll('.jump-list a[href="#' + section.id + '"]').forEach(function (link) {
      link.classList.toggle("is-right", isRight === true);
      link.classList.toggle("is-wrong", isRight === false);
    });
  }

  function reveal(list, chosenIndex) {
    var buttons = Array.prototype.slice.call(list.querySelectorAll(".option"));
    var chosen = buttons[chosenIndex];
    var isRight = chosen.hasAttribute("data-correct");
    buttons.forEach(function (b) {
      b.disabled = true;
      if (b.hasAttribute("data-correct")) {
        b.classList.add("is-right");
        addVerdict(b, b === chosen ? "Your answer, correct" : "Correct answer");
      }
    });
    if (!isRight) {
      chosen.classList.add("is-wrong");
      addVerdict(chosen, "Your answer");
    }
    var explain = list.nextElementSibling;
    if (explain && explain.classList.contains("explain")) explain.hidden = false;
    markJump(list, isRight);
    return isRight;
  }

  function addVerdict(button, text) {
    var v = document.createElement("span");
    v.className = "verdict";
    v.textContent = text;
    button.appendChild(v);
  }

  lists.forEach(function (list) {
    var qid = list.dataset.qid;
    var buttons = Array.prototype.slice.call(list.querySelectorAll(".option"));
    buttons.forEach(function (b, i) {
      b.addEventListener("click", function () {
        if (saved[qid]) return;
        var right = reveal(list, i);
        saved[qid] = { choice: i, right: right };
        store();
        updateScore();
      });
    });
    if (saved[qid]) reveal(list, saved[qid].choice);
  });

  // On phones, close the question list after jumping so the question is visible.
  document.querySelectorAll(".narrow-nav a").forEach(function (a) {
    a.addEventListener("click", function () { a.closest("details").open = false; });
  });

  var reset = document.querySelector('[data-action="reset"]');
  if (reset) {
    reset.addEventListener("click", function () {
      saved = {};
      store();
      lists.forEach(function (list) {
        list.querySelectorAll(".option").forEach(function (b) {
          b.disabled = false;
          b.classList.remove("is-right", "is-wrong");
          var v = b.querySelector(".verdict");
          if (v) v.remove();
        });
        var explain = list.nextElementSibling;
        if (explain && explain.classList.contains("explain")) explain.hidden = true;
        markJump(list, null);
      });
      updateScore();
    });
  }

  updateScore();
})();
