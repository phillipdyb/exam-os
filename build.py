#!/usr/bin/env python3
"""Build the static site into dist/.

Usage: python3 build.py

Theory articles live in src/theory/<slug>.html as HTML fragments.
Exam and quiz content lives in data/*.py. No dependencies beyond the stdlib.
"""
import html
import json
import re
import shutil
from pathlib import Path

from data.exams import EXAMS
from data.quiz import QUESTIONS

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"

SITE_NAME = "Operating Systems"
COURSE = "IDATT2202"

# Order matters: this is the reading order of the theory section.
TOPICS = [
    ("introduction", "What an operating system is", "Lecture 1"),
    ("kernel", "The kernel abstraction", "Lecture 2"),
    ("programming-interface", "The programming interface", "Lecture 3"),
    ("threads", "Concurrency and threads", "Lecture 4"),
    ("address-translation", "Address translation", "Lecture 5"),
    ("virtual-memory", "Caching and virtual memory", "Lecture 6"),
    ("synchronisation", "Synchronisation", "Lecture 7"),
    ("deadlock", "Multi-object synchronisation and deadlock", "Lecture 8"),
    ("scheduling", "Scheduling", "Lecture 9"),
    ("file-systems", "Storage and file systems", "Lecture 10"),
    ("security", "Security", "Lecture 12"),
    ("c-for-the-exam", "C for the exam", "Course page"),
]
TOPIC_TITLES = {slug: title for slug, title, _ in TOPICS}

esc = html.escape


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------------------------------------------------------------- layout

def nav_link(root, href, label, current):
    attr = ' aria-current="page"' if current else ""
    return f'<a href="{root}{href}"{attr}>{label}</a>'


def page(*, title, root, section, body, sidebar="", toc="", scripts=(), wide=False):
    nav = "".join([
        nav_link(root, "theory/", "Theory", section == "theory"),
        nav_link(root, "quiz/", "Quiz", section == "quiz"),
        nav_link(root, "exams/", "Earlier exams", section == "exams"),
    ])
    full_title = f"{title} – {SITE_NAME}" if title != SITE_NAME else f"{SITE_NAME} – {COURSE}"
    layout_class = "layout"
    if sidebar:
        layout_class += " has-sidebar"
    if toc:
        layout_class += " has-toc"
    if wide:
        layout_class += " is-wide"
    sidebar_html = f'<aside class="sidebar" aria-label="Topics">{sidebar}</aside>' if sidebar else ""
    toc_html = f'<aside class="toc" aria-label="On this page">{toc}</aside>' if toc else ""
    script_tags = "".join(f'<script src="{root}assets/{s}" defer></script>' for s in scripts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="Exam preparation for {COURSE} Operating Systems at NTNU: theory, quiz and earlier exams with solutions.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%231d5b66'/%3E%3Ctext x='16' y='22' font-family='monospace' font-size='15' fill='white' text-anchor='middle'%3E$_%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{root}assets/style.css">
{script_tags}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="site-header-inner">
    <a class="brand" href="{root}index.html"><span class="brand-prompt" aria-hidden="true">$</span> {SITE_NAME} <span class="brand-course">{COURSE}</span></a>
    <nav class="site-nav" aria-label="Main">{nav}</nav>
  </div>
</header>
<div class="{layout_class}">
{sidebar_html}
<main id="main" class="main">
{body}
</main>
{toc_html}
</div>
<footer class="site-footer">
  <p>Study notes for {COURSE} Operating Systems at NTNU, built only from the course material. Not an official course page.
  Part of <a href="https://philz.no/">philz.no</a>.</p>
</footer>
</body>
</html>
"""


def topics_sidebar(root, current=None):
    items = []
    for slug, title, lecture in TOPICS:
        attr = ' aria-current="page"' if slug == current else ""
        items.append(f'<li><a href="{root}theory/{slug}.html"{attr}>{esc(title)}</a></li>')
    return (
        '<details class="sidebar-details" open><summary>Topics</summary>'
        f'<ol class="sidebar-list">{"".join(items)}</ol></details>'
    )


def build_toc(body_html):
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
    if not heads:
        return ""
    items = "".join(f'<li><a href="#{hid}">{text}</a></li>' for hid, text in heads)
    return f'<p class="toc-title">On this page</p><ol class="toc-list">{items}</ol>'


def narrow_nav(label, inner):
    """Collapsible page navigation shown only on narrow screens."""
    return f'<details class="narrow-nav"><summary>{label}</summary>{inner}</details>'


def add_heading_ids(body_html):
    def repl(m):
        text = m.group(1)
        plain = re.sub(r"<[^>]+>", "", text)
        return f'<h2 id="{slugify(plain)}">{text}</h2>'
    return re.sub(r"<h2>(.*?)</h2>", repl, body_html)


def manhead(left, middle, right):
    return (
        '<div class="manhead" aria-hidden="true">'
        f'<span>{esc(left)}</span><span>{esc(middle)}</span><span>{esc(right)}</span></div>'
    )


# ---------------------------------------------------------------- exam index

def exam_refs_by_topic():
    refs = {slug: [] for slug, _, _ in TOPICS}
    for exam in EXAMS:
        for q in exam["questions"]:
            for t in q.get("topics", []):
                refs[t].append((exam, q))
    return refs


def exam_ref_list(root, refs):
    if not refs:
        return ""
    items = []
    for exam, q in refs:
        items.append(
            f'<li><a href="{root}exams/{exam["year"]}.html#q{q["n"]}">'
            f'{exam["year"]}, question {q["n"]}</a> – {esc(q["title"])}</li>'
        )
    return (
        '<section class="on-exam" aria-labelledby="on-exam-title">'
        '<h2 id="on-exam-title">On earlier exams</h2>'
        f'<ul>{"".join(items)}</ul></section>'
    )


# ---------------------------------------------------------------- pages

def build_home(refs):
    root = ""
    rows = []
    for slug, title, lecture in TOPICS:
        n = len(refs[slug])
        exam_cell = f"{n} question{'s' if n != 1 else ''}" if n else "–"
        rows.append(
            f'<tr><td><a href="theory/{slug}.html">{esc(title)}</a></td>'
            f"<td class=\"col-source\">{esc(lecture)}</td><td class=\"num nowrap\">{exam_cell}</td></tr>"
        )
    total_q = len(QUESTIONS) + sum(
        1 for e in EXAMS for q in e["questions"] if q["type"] == "mc"
    )
    body = f"""
{manhead(COURSE, "Operating Systems", "Exam notes")}
<h1>Operating Systems</h1>
<p class="lede">Notes, practice questions and earlier exams for {COURSE} at NTNU. Everything here is taken from the course material: the lecture slides, the in-class exercises and the exams from 2023 to 2025.</p>

<dl class="sections">
  <div><dt><a href="theory/">Theory</a></dt>
  <dd>{len(TOPICS)} articles that follow the lectures, from the kernel abstraction to security. Each ends with the exam questions it covers.</dd></div>
  <div><dt><a href="quiz/">Quiz</a></dt>
  <dd>{total_q} multiple-choice questions with explanations. Pick a topic or mix them all.</dd></div>
  <div><dt><a href="exams/">Earlier exams</a></dt>
  <dd>The 2023, 2024 and 2025 exams with the course's suggested solutions.</dd></div>
</dl>

<h2 id="topics">Topics</h2>
<table class="topic-table">
<thead><tr><th scope="col">Topic</th><th scope="col" class="col-source">Source</th><th scope="col" class="num">On exams</th></tr></thead>
<tbody>{"".join(rows)}</tbody>
</table>

<h2 id="the-exam">About the exam</h2>
<p>The earlier exams were 3-hour written exams in Inspera with no printed or hand-written support material; only a specific basic calculator was allowed (2023). Questions are in English, and you can answer in English or Norwegian. Each exam opens with 15–20 multiple-choice questions worth 2 marks each, followed by fill-in tasks (page replacement, scheduling, address translation), short C programs and written explanations. No points are deducted for wrong multiple-choice answers.</p>
<p>The course expects you to read, understand and write simple C programs. See <a href="theory/c-for-the-exam.html">C for the exam</a> for the list.</p>
"""
    write("index.html", page(title=SITE_NAME, root=root, section="home", body=body))


def build_theory(refs):
    root = "../"
    # Index
    items = []
    for i, (slug, title, lecture) in enumerate(TOPICS, 1):
        frag = (SRC / "theory" / f"{slug}.html").read_text()
        m = re.search(r'<p class="summary">(.*?)</p>', frag, re.S)
        summary = m.group(1).strip() if m else ""
        items.append(
            f'<li><a href="{slug}.html">{esc(title)}</a>'
            f'<span class="topic-source">{esc(lecture)}</span>'
            f"<p>{summary}</p></li>"
        )
    body = f"""
{manhead(COURSE, "Theory", "Contents")}
<h1>Theory</h1>
<p class="lede">The articles follow the lecture order. Each one sums up the slides and exercises for that lecture and links to the exam questions that tested it.</p>
<ol class="topic-index">{"".join(items)}</ol>
"""
    write("theory/index.html", page(
        title="Theory", root=root, section="theory", body=body,
        sidebar=topics_sidebar(root)))

    # Articles
    for i, (slug, title, lecture) in enumerate(TOPICS):
        frag = (SRC / "theory" / f"{slug}.html").read_text()
        frag = add_heading_ids(frag)
        prev_link = next_link = ""
        if i > 0:
            ps, pt, _ = TOPICS[i - 1]
            prev_link = f'<a class="pager-prev" href="{ps}.html"><span>Previous</span>{esc(pt)}</a>'
        if i < len(TOPICS) - 1:
            ns, nt, _ = TOPICS[i + 1]
            next_link = f'<a class="pager-next" href="{ns}.html"><span>Next</span>{esc(nt)}</a>'
        quiz_count = sum(1 for q in all_quiz_questions() if q["topic"] == slug)
        quiz_link = (
            f'<p class="practice"><a href="{root}quiz/?topic={slug}">Practise this topic in the quiz</a> ({quiz_count} questions)</p>'
            if quiz_count else ""
        )
        body = f"""
<article class="article">
{manhead(COURSE, title, lecture)}
<h1>{esc(title)}</h1>
{narrow_nav("On this page", build_toc(frag).split("</p>", 1)[1]) if build_toc(frag) else ""}
{frag}
{exam_ref_list(root, refs[slug])}
{quiz_link}
</article>
<nav class="pager" aria-label="Topics">{prev_link}{next_link}</nav>
"""
        toc = build_toc(frag)
        write(f"theory/{slug}.html", page(
            title=title, root=root, section="theory", body=body,
            sidebar=topics_sidebar(root, slug), toc=toc, scripts=("site.js",)))


def mc_options_html(qid, options, answer):
    lis = []
    for i, opt in enumerate(options):
        correct = ' data-correct' if i == answer else ""
        lis.append(f'<li><button type="button" class="option"{correct}>{opt}</button></li>')
    return f'<ol class="options" type="A" data-qid="{qid}">{"".join(lis)}</ol>'


def build_exams():
    root = "../"
    rows = []
    for exam in EXAMS:
        mc = sum(1 for q in exam["questions"] if q["type"] == "mc")
        rows.append(
            f'<tr><td><a href="{exam["year"]}.html">Autumn {exam["year"]}</a></td>'
            f'<td>{esc(exam["date"])}</td><td class="num">{len(exam["questions"])}</td>'
            f'<td class="num">{mc}</td></tr>'
        )
    body = f"""
{manhead(COURSE, "Earlier exams", "2023–2025")}
<h1>Earlier exams</h1>
<p class="lede">Each exam is shown question by question. Multiple-choice questions can be answered directly on the page. Open questions have the course's suggested solution behind a <em>Show solution</em> button, so you can write your own answer first.</p>
<table class="topic-table">
<thead><tr><th scope="col">Exam</th><th scope="col">Date</th><th scope="col" class="num">Questions</th><th scope="col" class="num">Multiple choice</th></tr></thead>
<tbody>{"".join(rows)}</tbody>
</table>
<h2 id="how-to-use">How to use them</h2>
<p>Set a 3-hour timer and do one exam in one sitting, without notes. Then go through the solutions and read the theory articles for the questions you missed. Each article lists the exam questions that cover it.</p>
<p>The 2023 and 2025 exams share several questions with each other and with 2024 (trap, thread abstraction, yielding, false sharing, page replacement). Expect the same kinds of questions again.</p>
"""
    write("exams/index.html", page(title="Earlier exams", root=root, section="exams", body=body))

    for exam in EXAMS:
        parts = []
        for q in exam["questions"]:
            topics = " ".join(
                f'<a href="{root}theory/{t}.html">{esc(TOPIC_TITLES[t])}</a>' for t in q.get("topics", [])
            )
            meta = f'<p class="q-meta"><span>{q["marks"]} marks</span>'
            if topics:
                meta += f'<span>Read: {topics}</span>'
            meta += "</p>"
            inner = f'<div class="q-prompt">{q["prompt"]}</div>'
            if q["type"] == "mc":
                inner += mc_options_html(f'{exam["year"]}-{q["n"]}', q["options"], q["answer"])
                if q.get("why"):
                    inner += f'<div class="explain" hidden><p>{q["why"]}</p></div>'
            if q.get("solution"):
                label = "Show solution"
                inner += (
                    f'<details class="solution"><summary>{label}</summary>'
                    f'<div class="solution-body">{q["solution"]}</div></details>'
                )
            parts.append(
                f'<section class="question" id="q{q["n"]}" aria-labelledby="q{q["n"]}-t">'
                f'<h2 id="q{q["n"]}-t"><span class="q-num">{q["n"]}</span> {esc(q["title"])}</h2>'
                f"{meta}{inner}</section>"
            )
        jump = "".join(
            f'<li><a href="#q{q["n"]}">{q["n"]}</a></li>' for q in exam["questions"]
        )
        body = f"""
{manhead(COURSE, f"Exam autumn {exam['year']}", exam["date"])}
<h1>Exam, autumn {exam["year"]}</h1>
<p class="lede">{esc(exam["intro"])}</p>
<div class="exam-tools">
  <p class="score" aria-live="polite" data-total="{sum(1 for q in exam["questions"] if q["type"] == "mc")}"></p>
  <button type="button" class="button-quiet" data-action="reset">Clear my answers</button>
</div>
{narrow_nav("Jump to a question", f'<ol class="jump-list">{jump}</ol>')}
{"".join(parts)}
"""
        toc = f'<p class="toc-title">Questions</p><ol class="jump-list">{jump}</ol>'
        write(f"exams/{exam['year']}.html", page(
            title=f"Exam autumn {exam['year']}", root=root, section="exams",
            body=body, toc=toc, scripts=("exam.js",)))


def all_quiz_questions():
    qs = []
    for q in QUESTIONS:
        qs.append(dict(q))
    for exam in EXAMS:
        for q in exam["questions"]:
            if q["type"] != "mc":
                continue
            topics = q.get("topics") or ["introduction"]
            qs.append({
                "topic": topics[0],
                "q": q["prompt"],
                "options": q["options"],
                "answer": q["answer"],
                "explain": q.get("why", ""),
                "source": f'Exam {exam["year"]}, question {q["n"]}',
                "href": f'exams/{exam["year"]}.html#q{q["n"]}',
            })
    return qs


def build_quiz():
    root = "../"
    qs = all_quiz_questions()
    counts = {slug: 0 for slug, _, _ in TOPICS}
    for q in qs:
        counts[q["topic"]] += 1
    topic_opts = "".join(
        f'<label class="check"><input type="checkbox" name="topic" value="{slug}" checked> {esc(title)} <span class="count">{counts[slug]}</span></label>'
        for slug, title, _ in TOPICS if counts[slug]
    )
    data = json.dumps({
        "questions": qs,
        "topics": {slug: title for slug, title, _ in TOPICS},
    }, ensure_ascii=False).replace("</", "<\\/")
    body = f"""
{manhead(COURSE, "Quiz", f"{len(qs)} questions")}
<h1>Quiz</h1>
<div id="quiz-setup">
<p class="lede">Multiple-choice questions from the lectures, exercises and earlier exams. You get the answer and a short explanation after each question.</p>
<form class="quiz-form" id="quiz-form">
  <fieldset>
    <legend>Topics</legend>
    <p class="fieldset-actions"><button type="button" class="link-button" data-select="all">Select all</button> <button type="button" class="link-button" data-select="none">Clear</button></p>
    <div class="check-grid">{topic_opts}</div>
  </fieldset>
  <fieldset>
    <legend>Questions</legend>
    <div class="radio-row">
      <label class="check"><input type="radio" name="count" value="10" checked> 10</label>
      <label class="check"><input type="radio" name="count" value="20"> 20</label>
      <label class="check"><input type="radio" name="count" value="all"> All selected</label>
    </div>
    <label class="check"><input type="checkbox" name="examOnly"> Only questions from earlier exams</label>
  </fieldset>
  <p class="form-actions"><button type="submit" class="button">Start quiz</button> <span class="form-hint" id="pool-hint" aria-live="polite"></span></p>
</form>
</div>
<div id="quiz-run" hidden></div>
<noscript><p>The quiz needs JavaScript. The <a href="{root}exams/">earlier exams</a> work without it.</p></noscript>
<script type="application/json" id="quiz-data">{data}</script>
"""
    write("quiz/index.html", page(
        title="Quiz", root=root, section="quiz", body=body, scripts=("quiz.js",)))


def write(rel, content):
    content = re.sub(r"<table(?=[\s>])", '<div class="table-wrap"><table', content)
    content = content.replace("</table>", "</table></div>")
    path = DIST / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(SRC / "assets", DIST / "assets")
    refs = exam_refs_by_topic()
    build_home(refs)
    build_theory(refs)
    build_exams()
    build_quiz()
    n_pages = len(list(DIST.rglob("*.html")))
    print(f"Built {n_pages} pages into {DIST.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
