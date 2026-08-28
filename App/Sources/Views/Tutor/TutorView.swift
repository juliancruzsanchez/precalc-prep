import SwiftUI

/// Context the AI tutor uses to keep answers relevant to the current unit.
/// Pass this in from any lesson / unit / topic so the tutor knows what the
/// user is studying and can pull the right definitions, examples, and pitfalls.
struct TutorContext: Hashable {
    let title: String
    let summary: String
    let objectives: [String]
    let topicSlug: String?
    let weekTitle: String?

    init(topic: Topic, weekTitle: String? = nil) {
        self.title = topic.title
        self.summary = topic.summary
        self.objectives = topic.lesson.objectives
        self.topicSlug = topic.slug
        self.weekTitle = weekTitle
    }

    /// System-prompt section that grounds the tutor in the current unit.
    var systemContextBlock: String {
        var lines: [String] = ["Current unit the student is studying: \"\(title)\"." ]
        if let weekTitle { lines.append("Course position: \(weekTitle).") }
        if !summary.isEmpty { lines.append("Unit summary: \(summary)") }
        if !objectives.isEmpty {
            lines.append("Learning objectives:")
            for obj in objectives { lines.append("- \(obj)") }
        }
        lines.append("Keep every answer tightly relevant to this unit. If the student asks something off-topic, briefly answer but steer them back to \"\(title)\".")
        return lines.joined(separator: "\n")
    }

    /// First few suggested prompts tailored to the current unit.
    var suggestedPrompts: [String] {
        var prompts: [String] = [
            "Explain \(title) like I'm seeing it for the first time.",
            "Walk me through a worked example for \(title).",
            "What's the most common mistake students make in \(title)?"
        ]
        if let first = objectives.first {
            prompts.append("Help me master this objective: \(first)")
        }
        return prompts
    }
}

struct TutorView: View {
    /// Optional unit context. When present, the tutor shows a context banner
    /// and grounds its answers in the current lesson.
    var context: TutorContext? = nil

    @State private var messages: [ChatMessage] = []
    @State private var input: String = ""
    @State private var isSending = false
    @State private var error: String?
    @State private var keyPresent: Bool = KeychainService.loadGroqKey() != nil

    @FocusState private var inputFocused: Bool

    private let groq = GroqService()

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                if let context {
                    contextBanner(context)
                }
                if !keyPresent {
                    missingKeyBanner
                }
                ScrollViewReader { proxy in
                    ScrollView {
                        VStack(alignment: .leading, spacing: 12) {
                            if messages.isEmpty {
                                emptyState
                            } else {
                                ForEach(messages) { msg in
                                    MessageBubble(message: msg)
                                        .id(msg.id)
                                }
                            }
                            if let error {
                                Text(error)
                                    .font(.caption)
                                    .foregroundStyle(Theme.danger)
                                    .padding(.horizontal)
                            }
                        }
                        .padding()
                    }
                    .onChange(of: messages.count) { _, _ in
                        if let last = messages.last {
                            withAnimation { proxy.scrollTo(last.id, anchor: .bottom) }
                        }
                    }
                }

                Divider()
                inputBar
            }
            .navigationTitle(context?.title ?? "AI Tutor")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Menu {
                        Button("Clear chat", role: .destructive) {
                            messages.removeAll()
                            error = nil
                        }
                    } label: {
                        Image(systemName: "ellipsis.circle")
                    }
                }
            }
        }
    }

    // MARK: - Context banner

    private func contextBanner(_ ctx: TutorContext) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(alignment: .top, spacing: 8) {
                Image(systemName: "graduationcap.fill")
                    .foregroundStyle(.white)
                    .padding(8)
                    .background(Theme.accent, in: Circle())
                VStack(alignment: .leading, spacing: 2) {
                    HStack(spacing: 6) {
                        Text("Asking about")
                            .font(.caption2.weight(.bold))
                            .tracking(0.6)
                            .foregroundStyle(.secondary)
                        if let weekTitle = ctx.weekTitle {
                            Text("·")
                                .foregroundStyle(.tertiary)
                            Text(weekTitle)
                                .font(.caption2.weight(.semibold))
                                .foregroundStyle(Theme.accent)
                        }
                    }
                    Text(ctx.title)
                        .font(.subheadline.weight(.semibold))
                        .lineLimit(nil)
                        .fixedSize(horizontal: false, vertical: true)
                    if !ctx.summary.isEmpty {
                        Text(ctx.summary)
                            .font(.caption)
                            .foregroundStyle(.secondary)
                            .lineLimit(3)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }
                Spacer(minLength: 0)
            }
            if !ctx.objectives.isEmpty {
                DisclosureGroup {
                    VStack(alignment: .leading, spacing: 4) {
                        ForEach(ctx.objectives, id: \.self) { obj in
                            HStack(alignment: .top, spacing: 6) {
                                Text("•").foregroundStyle(.secondary)
                                Text(obj)
                                    .font(.caption)
                                    .foregroundStyle(.primary)
                                    .fixedSize(horizontal: false, vertical: true)
                            }
                        }
                    }
                    .padding(.top, 4)
                } label: {
                    Text("Unit objectives (\(ctx.objectives.count))")
                        .font(.caption.weight(.semibold))
                        .foregroundStyle(Theme.accent)
                }
            }
        }
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Theme.accentSoft, in: RoundedRectangle(cornerRadius: 12))
        .padding(.horizontal)
        .padding(.top, 8)
    }

    // MARK: - Empty / missing key

    private var emptyState: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(context == nil
                 ? "Ask anything about precalculus."
                 : "Ask anything about \(context!.title).")
                .font(.headline)
                .fixedSize(horizontal: false, vertical: true)
            Text(context == nil
                 ? "I can walk you through a step-by-step solution, give you another worked example, or quiz you on a topic. Add your Groq API key in Settings to start chatting."
                 : "I'll keep every answer grounded in this unit's objectives. Add your Groq API key in Settings if you haven't yet.")
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .fixedSize(horizontal: false, vertical: true)
            Text("Suggested prompts:")
                .font(.caption.weight(.semibold))
                .foregroundStyle(.secondary)
            ForEach(currentSuggestedPrompts, id: \.self) { p in
                Button {
                    input = p
                    send()
                } label: {
                    HStack {
                        Image(systemName: "sparkles")
                        Text(p)
                            .multilineTextAlignment(.leading)
                            .fixedSize(horizontal: false, vertical: true)
                        Spacer()
                    }
                    .font(.subheadline)
                    .padding(.vertical, 8)
                    .padding(.horizontal, 12)
                    .background(Theme.accentSoft, in: RoundedRectangle(cornerRadius: 10))
                }
                .buttonStyle(.plain)
            }
        }
    }

    private var currentSuggestedPrompts: [String] {
        context?.suggestedPrompts ?? defaultSuggestedPrompts
    }

    private let defaultSuggestedPrompts = [
        "Explain how to use the Law of Sines step by step.",
        "What's the difference between sin⁻¹ and csc?",
        "Give me a practice problem on rational expressions and walk me through it.",
        "How do I find the asymptotes of a rational function?",
    ]

    private var missingKeyBanner: some View {
        HStack(alignment: .top, spacing: 8) {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundStyle(Theme.warning)
            VStack(alignment: .leading, spacing: 2) {
                Text("Add your Groq API key")
                    .font(.subheadline.weight(.semibold))
                Text("In Settings → AI Tutor, paste a key from console.groq.com. It's stored securely in the iOS Keychain.")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
        .padding(10)
        .background(Theme.warning.opacity(0.12))
    }

    private var inputBar: some View {
        HStack(alignment: .bottom, spacing: 8) {
            TextField("Ask a precalculus question…", text: $input, axis: .vertical)
                .lineLimit(1...4)
                .textFieldStyle(.plain)
                .focused($inputFocused)
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
                .background(Theme.card, in: RoundedRectangle(cornerRadius: 18))
            Button {
                send()
            } label: {
                if isSending {
                    ProgressView().padding(8)
                } else {
                    Image(systemName: "arrow.up.circle.fill")
                        .font(.system(size: 30))
                        .foregroundStyle(canSend ? Theme.accent : Color.secondary.opacity(0.5))
                }
            }
            .disabled(!canSend)
        }
        .padding(8)
    }

    private var canSend: Bool { !isSending && !input.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && keyPresent }

    private func send() {
        let prompt = input.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !prompt.isEmpty, keyPresent else { return }
        let userMsg = ChatMessage(role: .user, content: prompt)
        messages.append(userMsg)
        input = ""
        error = nil
        isSending = true
        Task {
            do {
                var systemPrompt = """
                You are a patient, accurate precalculus tutor. Follow these rules:
                - Solve step by step. Show every algebraic step.
                - Use proper mathematical notation.
                - Cite which topic the answer relates to (functions, trig, logs, etc.).
                - If the user is confused, re-explain the underlying concept before solving.
                - Never invent theorems or formulas. If you're unsure, say so.
                - Encourage the user; remind them they're rebuilding a strong foundation.
                - Keep answers focused and not too long. Use LaTeX-style notation like \\(x^2 + 1\\).
                """
                if let context {
                    systemPrompt += "\n\n" + context.systemContextBlock
                }
                var history: [ChatMessage] = [ChatMessage(role: .system, content: systemPrompt)]
                history.append(contentsOf: messages)
                let reply = try await groq.send(messages: history)
                messages.append(ChatMessage(role: .assistant, content: reply))
            } catch let e as GroqError {
                error = e.errorDescription
            } catch {
                self.error = error.localizedDescription
            }
            isSending = false
        }
    }
}

struct MessageBubble: View {
    let message: ChatMessage

    private var isUser: Bool { message.role == .user }

    var body: some View {
        HStack(alignment: .top, spacing: 8) {
            if isUser { Spacer(minLength: 40) }
            if !isUser {
                Image(systemName: "sparkles")
                    .foregroundStyle(.white)
                    .padding(8)
                    .background(Theme.accent, in: Circle())
            }
            VStack(alignment: isUser ? .trailing : .leading, spacing: 2) {
                Text(message.content)
                    .font(.body)
                    .padding(12)
                    .background(isUser ? Theme.accent : Theme.card, in: RoundedRectangle(cornerRadius: 14))
                    .foregroundStyle(isUser ? .white : .primary)
                    .textSelection(.enabled)
            }
            if isUser {
                Image(systemName: "person.fill")
                    .foregroundStyle(.white)
                    .padding(8)
                    .background(Color.secondary, in: Circle())
            } else { Spacer(minLength: 40) }
        }
    }
}
