# Changelog

All notable changes to Precalc Prep are documented here. Dates are in YYYY-MM-DD.

## [Unreleased]

### Added
- Initial release of Precalc Prep — a SwiftUI iOS app for the Champlain
  College CCO MATH 130 Precalculus course (7-week format).
- 38 lessons: 6 prerequisites (catch-up from geometry) + 7 weekly lessons
  including two bonus topics (Conic Sections, Sequences & Series).
- 384 practice questions with 3 progressive hints each (1,152 total hints).
- Interactive Canvas-based graph engine with a custom recursive-descent
  expression parser (handles `sin`, `cos`, `tan`, `exp`, `ln`, `log`,
  `sqrt`, `^`, etc.).
- Step-by-step problem solver with one-at-a-time reveal.
- Embedded YouTube videos (37 total) sourced from Khan Academy, 3Blue1Brown,
  and the Organic Chemistry Tutor.
- AI Tutor that calls Groq's `llama-3.1-8b-instant` chat-completions endpoint.
  API key is stored in the iOS Keychain, never sent elsewhere.
- Tools tab with a custom plotter, an interactive unit circle, and a
  formula reference.
- Local-only progress tracking via `UserDefaults`.

### Sources
All course content is grounded in the three required textbooks from the
course outline:
- Lippman & Rasmussen, *Precalculus: An Investigation of Functions*
  (LibreTexts, 2017) — CC BY-NC-SA 4.0
- Yoshiwara, *Trigonometry* (LibreTexts, 2018) — CC BY-NC-SA 4.0
- Abramson et al., *Algebra & Trigonometry* (OpenStax, 2021) — CC BY 4.0

Every topic, example, and quiz question cites the section it draws from.
This is a non-commercial study app; LibreTexts' CC BY-NC-SA license is honored.

### Build / Run
- Xcode 15+ with iOS 17 SDK
- `xcodegen generate` then open `PrecalcPrep.xcodeproj` in Xcode
- Target any iPhone simulator and press ⌘R
