# Precalc Prep — iOS app for Champlain CCO Precalculus

A complete iOS study app for the Champlain College CCO 7-week precalculus course
(algebra & trigonometry). It bridges the two years of high-school math you
missed, then walks you through the syllabus with interactive graphs, worked
examples, step-by-step solutions, YouTube videos, quizzes, and an AI tutor
powered by Groq.

## Curriculum sources

Every topic in the app is built on the structure and learning objectives of the
three textbooks listed on the course outline:

| Book | Author(s) | Year | License | Used for |
| --- | --- | --- | --- | --- |
| [Precalculus: An Investigation of Functions](https://math.libretexts.org/Bookshelves/Precalculus/Book%3A_Precalculus__An_Investigation_of_Functions_(Lippman_and_Rasmussen)) | Lippman & Rasmussen | 2017 | CC BY-NC-SA 4.0 | Weeks 1–6 |
| [Trigonometry](https://math.libretexts.org/Bookshelves/Precalculus/Trigonometry_(Yoshiwara)) | Yoshiwara | 2018 | CC BY-NC-SA 4.0 | Weeks 2, 6, 7 |
| [Algebra & Trigonometry](https://openstax.org/books/algebra-and-trigonometry) | Abramson et al. (OpenStax) | 2021 | CC BY 4.0 | All weeks (and prerequisites) |

Each topic, example, and quiz question in the app cites the section it comes
from. Tap the **Sources** card at the bottom of any lesson to open the original
page in your browser.

This is a non-commercial study app; LibreTexts' CC BY-NC-SA license is honored.

## What the app includes

- **7-week course** — every topic in the Champlain CCO outline, with the same
  titles and pacing. Two bonus topics round out the knowledge base:
  *Conic Sections* and *Sequences & Series*.
- **6 prerequisite lessons** — Algebra Essentials, Exponents & Scientific
  Notation, Radicals, Polynomials & Factoring, Rational Expressions, Coordinate
  Graphs. These bridge the two years you missed.
- **Interactive graphs** — typed in math (`sin(x)`, `x^2 - 4`, `exp(-x)`,
  `log(x)`, `pow(x, 2)`, etc.) plotted on a Canvas-based engine with smart
  tick spacing.
- **Worked examples** — every example names its source textbook.
- **Step-by-step solutions** — reveal one step at a time, with explanations.
- **YouTube videos** — embedded in-app, sourced from Khan Academy, 3Blue1Brown,
  and the Organic Chemistry Tutor.
- **Practice quizzes** — **10 questions per topic**, multiple-choice,
  true/false, and free-response with instant feedback and source citations.
- **Hint button** — every question has up to **3 progressive hints** that nudge
  you toward the right answer without giving it away. Tap "Show hint (1/3)",
  then (2/3), then (3/3) for the most help.
- **AI Tutor** — chat that calls Groq's `llama-3.1-8b-instant` (configurable).
  Your key is stored in the iOS Keychain; nothing is logged server-side.
- **Tools** — a custom plotter, an interactive unit circle, and a searchable
  formula sheet.
- **Progress tracking** — local-only, on-device, via `UserDefaults`.

**Current totals:** 38 topics, 384 practice questions, 1,152 hints — all
regenerated from a single Python source (`build_curriculum.py` +
`practice_questions.py`) so the content is auditable.

## Building

You need **Xcode 15 or later** with the iOS 17 SDK installed.

```bash
# 1. Install xcodegen if you don't have it (you do on this machine)
brew install xcodegen

# 2. From the project root, generate the Xcode project
cd "PrecalcPrep"
xcodegen generate

# 3. Open in Xcode
open PrecalcPrep.xcodeproj
```

Then pick the **PrecalcPrep** scheme and the **iPhone 15** (or any iOS 17)
simulator, and press ⌘R.

> If you don't use xcodegen, the project.pbxproj is already committed so you
> can `open PrecalcPrep.xcodeproj` directly.

## Configuring the AI Tutor

1. Get a free key at [console.groq.com](https://console.groq.com).
2. In the app, open the **Settings** tab → **AI Tutor (Groq API key)**.
3. Paste the key, tap **Save key**. It's stored in the iOS Keychain on this
   device only.
5. Open the **AI Tutor** tab and start chatting.

The app sends system + conversation messages to
`https://api.groq.com/openai/v1/chat/completions` and renders the reply.

## Project layout

```
PrecalcPrep/
├── App/
│   ├── Info.plist
│   ├── Resources/
│   │   ├── Assets.xcassets/
│   │   └── Content/
│   │       └── course.json          # the full curriculum
│   └── Sources/
│       ├── App/                     # @main app entry
│       ├── Models/                  # Course, Week, Topic, Lesson…
│       ├── Services/                # Content, Settings, Progress, Keychain, Groq
│       ├── Theme/                   # colors & shared modifiers
│       ├── Utilities/               # ExpressionParser
│       └── Views/
│           ├── Components/          # YouTubePlayer, MathBlock, citations, etc.
│           ├── Graph/               # GraphView (Canvas + expression engine)
│           ├── Home/                # Home, Topics, WeekDetail, Tools
│           ├── Lesson/              # LessonView
│           ├── Quiz/                # QuizView
│           ├── Settings/            # SettingsView
│           └── Tutor/               # TutorView (AI chat)
├── build_curriculum.py              # regenerates course.json
├── project.yml                      # xcodegen spec
└── PrecalcPrep.xcodeproj            # generated
```

## Editing the curriculum

The full curriculum lives in `App/Resources/Content/course.json`. To make
edits easier, it's generated by `build_curriculum.py` (week structure) plus
`practice_questions.py` (the 384-question bank) from a single Python
source-of-truth. Helper functions: `topic()`, `lesson()`, `example()`,
`step_by_step()`, `mc()`, `tf()`, `fr()`.

To rebuild after editing:

```bash
python3 build_curriculum.py
```

If you change the source-textbook URLs, update `TextbookSource.baseURL` in
`App/Sources/Models/CourseModels.swift`.

### Adding practice questions

The `practice_questions.py` file is organized by week. Each topic has its own
list of 10 questions built with the `q(...)` helper:

```python
q("Your prompt?",
  ["Choice A", "Choice B", "Choice C", "Choice D"],
  "2",                                  # index of the correct choice
  "Why this is the right answer.",
  src(OS, "Ch 1.1"),
  ["First hint (gentle nudge).",
   "Second hint (more specific).",
   "Third hint (very close to answer)."]),
```

Hints are **optional but recommended** — 3 progressive hints per question is
the standard. If you have fewer, the others are skipped; if you have none, the
hint button doesn't appear.

## Notes on math rendering

LaTeX is rendered as Unicode (e.g. `\\sqrt{x}` becomes `√x`, `\\theta` becomes
`θ`, `\\le` becomes `≤`). A native MathJax-style renderer is a future
enhancement; for now, the source math is shown verbatim in a serif monospaced
block that you can select and copy.

## Privacy

The app does not send anything to a server except:

- Outbound calls to `api.groq.com` for AI Tutor chats, when you initiate them.
- Standard outbound HTTPS to `youtube.com` and `youtu.be` for embedded videos.

The Groq API key is stored in the iOS Keychain. The app does not collect
analytics, track usage, or sync data to any backend.

## Attribution

- Course topic structure and learning objectives follow the Champlain College
  CCO Precalculus 7-week outline.
- All textbook references are clickable in-app and link to the official
  LibreTexts and OpenStax pages.
- LibreTexts books are CC BY-NC-SA 4.0; OpenStax is CC BY 4.0. This study
  app is consistent with both licenses.
