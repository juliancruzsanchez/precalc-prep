import SwiftUI

/// A monospaced, well-spaced block used to display math expressions.
/// LaTeX rendering is intentionally a future enhancement — we render the source text
/// verbatim with light punctuation cleanup, so what you see is the actual expression.
struct MathBlock: View {
    let text: String
    var compact: Bool = false

    var body: some View {
        Text(formatMath(text))
            .font(.system(compact ? .footnote : .body, design: .serif))
            .padding(.vertical, compact ? 4 : 8)
            .padding(.horizontal, compact ? 8 : 12)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(Color.primary.opacity(0.05), in: RoundedRectangle(cornerRadius: 8))
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
        VStack(alignment: .leading, spacing: 8) {
            Text(example.title).font(.headline)
            VStack(alignment: .leading, spacing: 4) {
                Text("Problem").font(.caption.weight(.semibold)).foregroundStyle(.secondary)
                Text(example.problem)
            }
            DisclosureGroup(isExpanded: $revealed) {
                VStack(alignment: .leading, spacing: 8) {
                    ForEach(Array(example.steps.enumerated()), id: \.offset) { idx, step in
                        HStack(alignment: .top, spacing: 8) {
                            Text("\(idx + 1).")
                                .font(.subheadline.weight(.semibold))
                                .foregroundStyle(.secondary)
                            Text(step)
                                .font(.subheadline)
                        }
                    }
                    VStack(alignment: .leading, spacing: 4) {
                        Text("Answer").font(.caption.weight(.semibold)).foregroundStyle(.secondary)
                        Text(example.solution).font(.body.weight(.semibold)).foregroundStyle(Theme.success)
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
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(problem.title).font(.headline)
                Spacer()
                Text("\(revealedCount)/\(problem.steps.count) steps")
                    .font(.caption.monospacedDigit())
                    .foregroundStyle(.secondary)
            }
            Text(problem.prompt)
                .font(.subheadline)
                .foregroundStyle(.secondary)

            VStack(alignment: .leading, spacing: 8) {
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
                            if isRevealed {
                                MathBlock(text: step.math, compact: true)
                                Text(step.explanation)
                                    .font(.footnote)
                                    .foregroundStyle(.secondary)
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
        .cardStyle()
    }
}
