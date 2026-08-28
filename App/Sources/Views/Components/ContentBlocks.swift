import SwiftUI

/// Preference key used to measure the natural height of a tab's content so the
/// parent `TabView(.page)` can grow to fit it instead of clipping.
struct PageContentHeightKey: PreferenceKey {
    static var defaultValue: CGFloat = 0
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())
    }
}

/// A serif-styled, well-spaced block used to display math expressions.
/// Uses the system "New York" serif at math-appropriate sizing so equations
/// read as math, not body text. LaTeX rendering is intentionally a future
/// enhancement — we render the source text verbatim with light punctuation
/// cleanup, so what you see is the actual expression.
struct MathBlock: View {
    let text: String
    var compact: Bool = false
    var italic: Bool = true

    var body: some View {
        Text(formatMath(text))
            .font(Theme.mathFont(compact: compact))
            .italic(italic)
            .padding(.vertical, compact ? 6 : 10)
            .padding(.horizontal, compact ? 10 : 14)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                Theme.accentSoft.opacity(0.5),
                in: RoundedRectangle(cornerRadius: 10)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(Theme.accent.opacity(0.15), lineWidth: 1)
            )
            .textSelection(.enabled)
    }

    /// Replaces a few common LaTeX-y tokens with their Unicode equivalents so the
    /// text reads naturally on iOS. Anything we don't recognize stays as-is.
    private func formatMath(_ s: String) -> String {
        s.replacingOccurrences(of: "\\sqrt", with: "√")
         .replacingOccurrences(of: "\\pi", with: "π")
         .replacingOccurrences(of: "\\theta", with: "θ")
         .replacingOccurrences(of: "\\alpha", with: "α")
         .replacingOccurrences(of: "\\beta", with: "β")
         .replacingOccurrences(of: "\\gamma", with: "γ")
         .replacingOccurrences(of: "\\le", with: "≤")
         .replacingOccurrences(of: "\\ge", with: "≥")
         .replacingOccurrences(of: "\\ne", with: "≠")
         .replacingOccurrences(of: "\\to", with: "→")
         .replacingOccurrences(of: "\\cdot", with: "·")
         .replacingOccurrences(of: "\\times", with: "×")
         .replacingOccurrences(of: "\\div", with: "÷")
         .replacingOccurrences(of: "\\pm", with: "±")
         .replacingOccurrences(of: "\\infty", with: "∞")
         .replacingOccurrences(of: "{", with: "")
         .replacingOccurrences(of: "}", with: "")
    }
}

struct ExplanationBlock: View {
    let explanation: Explanation

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(explanation.intro)
                .font(.body)
            ForEach(explanation.sections) { section in
                VStack(alignment: .leading, spacing: 6) {
                    Text(section.heading)
                        .font(.headline)
                    Text(section.body)
                        .font(.body)
                        .foregroundStyle(.primary)
                    if let bullets = section.bullets, !bullets.isEmpty {
                        VStack(alignment: .leading, spacing: 4) {
                            ForEach(bullets, id: \.self) { bullet in
                                HStack(alignment: .top, spacing: 8) {
                                    Text("•").foregroundStyle(.secondary)
                                    Text(bullet)
                                        .font(.subheadline)
                                        .foregroundStyle(.primary)
                                }
                            }
                        }
                        .padding(.leading, 4)
                    }
                }
            }
        }
        .cardStyle()
    }
}

struct WorkedExampleView: View {
    let example: WorkedExample
    @State private var revealed = false

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(example.title)
                .font(.headline)
                .fixedSize(horizontal: false, vertical: true)

            VStack(alignment: .leading, spacing: 6) {
                Text("PROBLEM")
                    .font(.caption2.weight(.bold))
                    .tracking(0.8)
                    .foregroundStyle(.secondary)
                MathBlock(text: example.problem)
            }

            DisclosureGroup(isExpanded: $revealed) {
                VStack(alignment: .leading, spacing: 10) {
                    ForEach(Array(example.steps.enumerated()), id: \.offset) { idx, step in
                        HStack(alignment: .top, spacing: 8) {
                            Text("\(idx + 1).")
                                .font(Theme.mathFont(compact: true).weight(.semibold))
                                .foregroundStyle(Theme.accent)
                                .frame(width: 22, alignment: .trailing)
                            Text(step)
                                .font(.subheadline)
                                .fixedSize(horizontal: false, vertical: true)
                        }
                    }
                    VStack(alignment: .leading, spacing: 6) {
                        Text("ANSWER")
                            .font(.caption2.weight(.bold))
                            .tracking(0.8)
                            .foregroundStyle(.secondary)
                        MathBlock(text: example.solution)
                    }
                    .padding(.top, 4)
                    SourceCitationView(citation: example.source, compact: true)
                }
                .padding(.top, 6)
            } label: {
                Text(revealed ? "Hide solution" : "Show solution")
                    .font(.subheadline.weight(.medium))
                    .foregroundStyle(Theme.accent)
            }
        }
        .cardStyle()
    }
}

struct StepByStepView: View {
    let problem: StepByStepProblem
    @State private var revealedCount: Int = 0

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Title + step counter — title wraps freely so the equation is never truncated.
            VStack(alignment: .leading, spacing: 6) {
                HStack(alignment: .firstTextBaseline) {
                    Text(problem.title)
                        .font(Theme.mathFont(compact: false).weight(.semibold))
                        .lineLimit(nil)
                        .multilineTextAlignment(.leading)
                        .fixedSize(horizontal: false, vertical: true)
                    Spacer(minLength: 8)
                    Text("\(revealedCount)/\(problem.steps.count) steps")
                        .font(.caption.monospacedDigit())
                        .foregroundStyle(.secondary)
                }
                Text(problem.prompt)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(nil)
                    .fixedSize(horizontal: false, vertical: true)
            }

            VStack(alignment: .leading, spacing: 10) {
                ForEach(Array(problem.steps.enumerated()), id: \.offset) { idx, step in
                    let isRevealed = idx < revealedCount
                    HStack(alignment: .top, spacing: 10) {
                        ZStack {
                            Circle()
                                .fill(isRevealed ? Theme.accent : Color.secondary.opacity(0.2))
                                .frame(width: 26, height: 26)
                            Text("\(idx + 1)")
                                .font(.caption.weight(.bold))
                                .foregroundStyle(.white)
                        }
                        VStack(alignment: .leading, spacing: 4) {
                            Text(step.label)
                                .font(.subheadline.weight(.semibold))
                                .fixedSize(horizontal: false, vertical: true)
                            if isRevealed {
                                MathBlock(text: step.math, compact: true)
                                Text(step.explanation)
                                    .font(.footnote)
                                    .foregroundStyle(.secondary)
                                    .fixedSize(horizontal: false, vertical: true)
                            } else {
                                Text("Tap 'Next step' to reveal")
                                    .font(.footnote)
                                    .foregroundStyle(.tertiary)
                            }
                        }
                    }
                }
            }

            HStack {
                Button {
                    if revealedCount > 0 { revealedCount -= 1 }
                } label: {
                    Label("Previous", systemImage: "chevron.left")
                }
                .buttonStyle(.bordered)
                .disabled(revealedCount == 0)
                Spacer()
                Button {
                    if revealedCount < problem.steps.count { revealedCount += 1 }
                } label: {
                    Label(revealedCount == problem.steps.count ? "Done" : "Next step", systemImage: "chevron.right")
                        .labelStyle(.titleAndIcon)
                }
                .buttonStyle(.borderedProminent)
                .disabled(revealedCount == problem.steps.count)
            }

            SourceCitationView(citation: problem.source, compact: true)
        }
        // Bottom padding reserves space for the TabView page indicator so it
        // never overlaps the last step. Reported in the height preference so
        // the parent TabView grows to fit content + indicator.
        .padding(.bottom, 36)
        // Allow the card to grow with its content (no fixed height clipping).
        .fixedSize(horizontal: false, vertical: true)
        // Report our natural height to the parent so the paged TabView can size to fit.
        .background(
            GeometryReader { proxy in
                Color.clear.preference(key: PageContentHeightKey.self, value: proxy.size.height)
            }
        )
    }
}
