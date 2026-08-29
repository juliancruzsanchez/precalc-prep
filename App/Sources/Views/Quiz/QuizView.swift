import SwiftUI

struct QuizView: View {
    let topicSlug: String
    let questions: [QuizQuestion]

    @EnvironmentObject private var progress: ProgressService
    @Environment(\.dismiss) private var dismiss

    @State private var currentIndex: Int = 0
    @State private var selectedAnswer: String? = nil
    @State private var showResult: Bool = false
    @State private var correctCount: Int = 0
    @State private var wrongIndices: [Int] = []
    @State private var hintsRevealed: Int = 0

    private var current: QuizQuestion? {
        guard questions.indices.contains(currentIndex) else { return nil }
        return questions[currentIndex]
    }

    private var isFinished: Bool { currentIndex >= questions.count }

    var body: some View {
        Group {
            if isFinished {
                finishedView
            } else if let q = current {
                questionView(q)
            } else {
                Text("No questions available.")
            }
        }
        .navigationTitle("Practice Quiz")
        .navigationBarTitleDisplayMode(.inline)
    }

    private func questionView(_ q: QuizQuestion) -> some View {
        VStack(alignment: .leading, spacing: 16) {
            ProgressView(value: Double(currentIndex), total: Double(questions.count))
                .tint(Theme.accent)

            Text("Question \(currentIndex + 1) of \(questions.count)")
                .font(.caption.weight(.semibold))
                .foregroundStyle(.secondary)

            Text(q.prompt)
                .font(.title3.weight(.medium))
                .frame(maxWidth: .infinity, alignment: .leading)

            VStack(spacing: 10) {
                if let choices = q.choices {
                    ForEach(Array(choices.enumerated()), id: \.offset) { idx, choice in
                        choiceButton(idx: idx, text: choice, question: q)
                    }
                } else {
                    Text(TutorPersona.quizFreeResponseNote)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
            }

            hintSection(for: q)

            if showResult, let sel = selectedAnswer {
                explanationCard(q: q, userChoice: sel)
            }

            Spacer()

            HStack {
                Button("Skip") {
                    selectedAnswer = nil
                    showResult = false
                    hintsRevealed = 0
                    currentIndex += 1
                }
                .buttonStyle(.bordered)
                Spacer()
                if showResult {
                    Button(currentIndex == questions.count - 1 ? "Finish" : "Next") {
                        showResult = false
                        selectedAnswer = nil
                        hintsRevealed = 0
                        currentIndex += 1
                    }
                    .buttonStyle(.borderedProminent)
                } else {
                    Button("Check") {
                        showResult = true
                        if selectedAnswer == q.answer {
                            correctCount += 1
                        } else {
                            wrongIndices.append(currentIndex)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(selectedAnswer == nil && q.kind != .freeResponse)
                }
            }
        }
        .padding()
    }

    @ViewBuilder
    private func hintSection(for q: QuizQuestion) -> some View {
        let available = q.hints.count
        if available == 0 { EmptyView() } else {
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Label("Need a hint?", systemImage: "lightbulb")
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(.secondary)
                    Spacer()
                    if !showResult {
                        Button {
                            withAnimation(.easeInOut(duration: 0.2)) {
                                hintsRevealed = min(hintsRevealed + 1, available)
                            }
                        } label: {
                            HStack(spacing: 4) {
                                Image(systemName: "lightbulb.fill")
                                Text(hintsRevealed >= available ? "No more hints" : "Show hint (\(hintsRevealed + 1)/\(available))")
                            }
                        }
                        .buttonStyle(.bordered)
                        .controlSize(.small)
                        .disabled(hintsRevealed >= available)
                    }
                }
                ForEach(Array(q.hints.prefix(hintsRevealed).enumerated()), id: \.offset) { idx, hint in
                    HStack(alignment: .top, spacing: 8) {
                        Text("💡")
                            .font(.subheadline)
                        Text(hint)
                            .font(.subheadline)
                            .foregroundStyle(.primary)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    .padding(10)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Theme.warning.opacity(0.12), in: RoundedRectangle(cornerRadius: 8))
                }
            }
        }
    }

    @ViewBuilder
    private func choiceButton(idx: Int, text: String, question: QuizQuestion) -> some View {
        let isSelected = selectedAnswer == "\(idx)"
        let isCorrect = question.answer == "\(idx)"
        let showState = showResult
        let bg: Color = {
            if showState {
                if isCorrect { return Theme.success.opacity(0.18) }
                if isSelected { return Theme.danger.opacity(0.18) }
                return Color.secondary.opacity(0.08)
            }
            if isSelected { return Theme.accent.opacity(0.18) }
            return Color.secondary.opacity(0.06)
        }()
        Button {
            if !showResult { selectedAnswer = "\(idx)" }
        } label: {
            HStack {
                Text(["A", "B", "C", "D", "E"][safe: idx] ?? "\(idx + 1)")
                    .font(.subheadline.weight(.bold))
                    .frame(width: 28, height: 28)
                    .background(Color.primary.opacity(0.1), in: Circle())
                Text(text)
                    .multilineTextAlignment(.leading)
                Spacer()
                if showState && isCorrect {
                    Image(systemName: "checkmark.circle.fill").foregroundStyle(Theme.success)
                } else if showState && isSelected && !isCorrect {
                    Image(systemName: "xmark.circle.fill").foregroundStyle(Theme.danger)
                }
            }
            .padding(.vertical, 12)
            .padding(.horizontal, 12)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(bg, in: RoundedRectangle(cornerRadius: 12))
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(showState && (isSelected || isCorrect) ? Color.primary.opacity(0.3) : Color.clear, lineWidth: 1)
            )
        }
        .buttonStyle(.plain)
        .disabled(showResult)
    }

    @ViewBuilder
    private func explanationCard(q: QuizQuestion, userChoice: String) -> some View {
        let isRight = userChoice == q.answer
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: isRight ? "checkmark.seal.fill" : "exclamationmark.triangle.fill")
                    .foregroundStyle(isRight ? Theme.success : Theme.danger)
                Text(isRight ? "Correct" : "Not quite")
                    .font(.headline)
            }
            Text(q.explanation)
                .font(.subheadline)
            SourceCitationView(citation: q.source, compact: true)
        }
        .padding(12)
        .background(
            (isRight ? Theme.success : Theme.danger).opacity(0.08),
            in: RoundedRectangle(cornerRadius: 12)
        )
    }

    private var finishedView: some View {
        let total = questions.count
        let percent = total == 0 ? 0 : Int(Double(correctCount) / Double(total) * 100)
        return VStack(spacing: 16) {
            Spacer()
            Image(systemName: percent >= 80 ? "trophy.fill" : (percent >= 50 ? "hand.thumbsup.fill" : "book.fill"))
                .font(.system(size: 64))
                .foregroundStyle(percent >= 80 ? Theme.warning : Theme.accent)
            Text("Quiz complete")
                .font(.title.weight(.bold))
            Text("\(correctCount) out of \(total) correct (\(percent)%)")
                .font(.headline)
                .foregroundStyle(.secondary)
            if !wrongIndices.isEmpty {
                VStack(alignment: .leading, spacing: 6) {
                    Text("Review these questions:")
                        .font(.subheadline.weight(.semibold))
                    ForEach(wrongIndices, id: \.self) { idx in
                        if questions.indices.contains(idx) {
                            Text("• \(questions[idx].prompt)")
                                .font(.footnote)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(Theme.danger.opacity(0.08), in: RoundedRectangle(cornerRadius: 12))
            }
            Spacer()
            HStack {
                Button("Close") { dismiss() }
                    .buttonStyle(.bordered)
                Spacer()
                Button("Try again") {
                    currentIndex = 0
                    selectedAnswer = nil
                    showResult = false
                    correctCount = 0
                    wrongIndices = []
                    hintsRevealed = 0
                }
                .buttonStyle(.borderedProminent)
            }
        }
        .padding()
        .onAppear {
            progress.recordQuiz(slug: topicSlug, correct: correctCount, total: total)
        }
    }
}

private extension Array {
    subscript(safe index: Int) -> Element? {
        indices.contains(index) ? self[index] : nil
    }
}
