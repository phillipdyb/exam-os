# Operating Systems – IDATT2202 exam notes

A static study site with theory, a quiz and earlier exams (2023–2025), built only from the course material.

## Build

    python3 build.py

Writes the site to `dist/` (not committed). No dependencies beyond Python 3.

## Publish

Pushing to `main` builds and deploys the site to GitHub Pages via `.github/workflows/pages.yml`.
One-time setup: in the repository on GitHub, go to Settings → Pages and set Source to **GitHub Actions**.
To use a custom domain (e.g. a philz.no subdomain), add it under Settings → Pages → Custom domain
and point a CNAME record for it to `phillipdyb.github.io`.

## Where things are

- `src/theory/*.html` – theory articles (HTML fragments; `<h2>` headings become the "On this page" list)
- `data/exams.py` – the three exams, answers and suggested solutions
- `data/quiz.py` – quiz questions from lectures and exercises (exam multiple-choice questions are added automatically)
- `src/assets/` – CSS and the small scripts for the quiz and exam pages
- `build.py` – layout, navigation and page generation; the topic list and order live in `TOPICS`

The source PDFs in `ignore/` are not tracked by git.
