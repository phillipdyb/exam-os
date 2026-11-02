// Quiz: pick topics and a number of questions, answer one at a time,
// get the explanation straight away, review mistakes at the end.
(function () {
  var data = JSON.parse(document.getElementById("quiz-data").textContent);
  var root = "../";
  var form = document.getElementById("quiz-form");
  var setup = document.getElementById("quiz-setup");
  var run = document.getElementById("quiz-run");
  var hint = document.getElementById("pool-hint");
  var letters = "ABCDEFGH";

  var state = null;

  // Preselect a topic from ?topic=slug (links from theory articles).
  var params = new URLSearchParams(location.search);
  var preset = params.get("topic");
  if (preset && data.topics[preset]) {
    form.querySelectorAll('input[name="topic"]').forEach(function (cb) {
      cb.checked = cb.value === preset;
    });
  }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function pool() {
    var topics = {};
    form.querySelectorAll('input[name="topic"]:checked').forEach(function (cb) { topics[cb.value] = true; });
    var examOnly = form.examOnly.checked;
    return data.questions.filter(function (q) {
      return topics[q.topic] && (!examOnly || q.href);
    });
  }

  function updateHint() {
    var n = pool().length;
    var submit = form.querySelector('[type="submit"]');
    submit.disabled = n === 0;
    hint.textContent = n === 0 ? "Select at least one topic." : n + " questions match.";
  }
  form.addEventListener("change", updateHint);
  form.querySelectorAll("[data-select]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var on = btn.dataset.select === "all";
      form.querySelectorAll('input[name="topic"]').forEach(function (cb) { cb.checked = on; });
      updateHint();
    });
  });
  updateHint();

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var count = form.count.value;
    var qs = shuffle(pool());
    if (count !== "all") qs = qs.slice(0, Number(count));
    start(qs);
  });

  function start(questions) {
    state = {
      questions: questions.map(function (q) {
        var order = shuffle(q.options.map(function (_, i) { return i; }));
        return { q: q, order: order, choice: null };
      }),
      index: 0
    };
    setup.hidden = true;
    run.hidden = false;
    show();
  }

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function show() {
    var item = state.questions[state.index];
    var q = item.q;
    var n = state.questions.length;
    run.innerHTML = "";

    var progress = el("div", "quiz-progress");
    progress.appendChild(el("span", "", "Question " + (state.index + 1) + " of " + n));
    var right = state.questions.filter(function (x) { return x.choice !== null && x.order[x.choice] === x.q.answer; }).length;
    var answered = state.questions.filter(function (x) { return x.choice !== null; }).length;
    progress.appendChild(el("span", "", right + " of " + answered + " right"));
    run.appendChild(progress);

    var bar = el("div", "progress-bar");
    var fill = el("span");
    fill.style.width = (100 * answered / n) + "%";
    bar.appendChild(fill);
    run.appendChild(bar);

    run.appendChild(el("p", "quiz-topic", data.topics[q.topic]));
    var question = el("div", "quiz-question", q.q);
    question.id = "quiz-q";
    run.appendChild(question);

    var list = el("ol", "options");
    list.setAttribute("aria-labelledby", "quiz-q");
    item.order.forEach(function (optIndex, pos) {
      var li = el("li");
      var b = el("button", "option", q.options[optIndex]);
      b.type = "button";
      b.addEventListener("click", function () { answer(pos); });
      li.appendChild(b);
      list.appendChild(li);
    });
    run.appendChild(list);

    var feedback = el("div");
    feedback.setAttribute("aria-live", "polite");
    run.appendChild(feedback);

    var nav = el("div", "quiz-nav");
    var quit = el("button", "button-quiet", "End quiz");
    quit.type = "button";
    quit.addEventListener("click", finish);
    var next = el("button", "button", state.index + 1 < n ? "Next question" : "See results");
    next.type = "button";
    next.hidden = true;
    next.addEventListener("click", advance);
    nav.appendChild(quit);
    nav.appendChild(next);
    run.appendChild(nav);

    if (item.choice !== null) render(item, list, feedback, next);
    else list.querySelector(".option").focus({ preventScroll: true });
    run.scrollIntoView({ block: "start" });
  }

  function answer(pos) {
    var item = state.questions[state.index];
    if (item.choice !== null) return;
    item.choice = pos;
    show();
  }

  function render(item, list, feedback, next) {
    var buttons = list.querySelectorAll(".option");
    var correctPos = item.order.indexOf(item.q.answer);
    buttons.forEach(function (b, pos) {
      b.disabled = true;
      if (pos === correctPos) {
        b.classList.add("is-right");
        b.appendChild(el("span", "verdict", pos === item.choice ? "Your answer, correct" : "Correct answer"));
      } else if (pos === item.choice) {
        b.classList.add("is-wrong");
        b.appendChild(el("span", "verdict", "Your answer"));
      }
    });
    var isRight = item.choice === correctPos;
    var box = el("div", "explain");
    var verdict = isRight ? "Correct." : "Not quite. The answer is " + letters[correctPos] + ".";
    box.appendChild(el("p", "", "<strong>" + verdict + "</strong> " + (item.q.explain || "")));
    var src = item.q.href
      ? 'From <a href="' + root + item.q.href + '">' + item.q.source + "</a>"
      : "From " + item.q.source;
    box.appendChild(el("p", "source", src + '. Read more in <a href="' + root + "theory/" + item.q.topic + '.html">' + data.topics[item.q.topic] + "</a>."));
    feedback.appendChild(box);
    next.hidden = false;
    next.focus({ preventScroll: true });
  }

  function advance() {
    if (state.index + 1 < state.questions.length) {
      state.index++;
      show();
    } else {
      finish();
    }
  }

  function finish() {
    state.done = true;
    var answered = state.questions.filter(function (x) { return x.choice !== null; });
    var wrong = answered.filter(function (x) { return x.order[x.choice] !== x.q.answer; });
    var right = answered.length - wrong.length;
    run.innerHTML = "";
    run.appendChild(el("h2", "", "Results"));
    run.appendChild(el("p", "result-score", right + " <small>of " + answered.length + " right</small>"));
    if (answered.length < state.questions.length) {
      run.appendChild(el("p", "", "You stopped after " + answered.length + " of " + state.questions.length + " questions."));
    }

    var actions = el("p", "form-actions");
    if (wrong.length) {
      var retry = el("button", "button", "Practise the " + wrong.length + " I missed");
      retry.type = "button";
      retry.addEventListener("click", function () { start(wrong.map(function (x) { return x.q; })); });
      actions.appendChild(retry);
    }
    var again = el("button", wrong.length ? "button-quiet" : "button", "Start a new quiz");
    again.type = "button";
    again.addEventListener("click", function () {
      run.hidden = true;
      setup.hidden = false;
      updateHint();
      setup.scrollIntoView({ block: "start" });
    });
    actions.appendChild(again);
    run.appendChild(actions);

    if (wrong.length) {
      run.appendChild(el("h3", "", "Questions you missed"));
      var list = el("ol", "result-list");
      wrong.forEach(function (x) {
        var li = el("li");
        li.appendChild(el("div", "rl-q", x.q.q));
        li.appendChild(el("span", "rl-a", "Answer: " + x.q.options[x.q.answer]));
        list.appendChild(li);
      });
      run.appendChild(list);
    } else if (answered.length) {
      run.appendChild(el("p", "", "No mistakes this round."));
    }
    run.scrollIntoView({ block: "start" });
  }

  // Keyboard: A–D or 1–4 to answer, Enter or N for the next question.
  document.addEventListener("keydown", function (e) {
    if (!state || state.done || run.hidden || e.metaKey || e.ctrlKey || e.altKey) return;
    var item = state.questions[state.index];
    if (!item) return;
    var k = e.key.toUpperCase();
    var pos = letters.indexOf(k);
    if (pos === -1 && /^[1-8]$/.test(k)) pos = Number(k) - 1;
    if (item.choice === null && pos >= 0 && pos < item.order.length) {
      e.preventDefault();
      answer(pos);
    } else if (item.choice !== null && k === "N") {
      e.preventDefault();
      advance();
    }
  });
})();
