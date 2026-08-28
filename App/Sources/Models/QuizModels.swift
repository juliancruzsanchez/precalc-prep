import Foundation

enum QuizQuestionKind: String, Codable {
    case multipleChoice = "mc"
    case trueFalse = "tf"
    case freeResponse = "fr"
}

struct QuizQuestion: Codable, Hashable, Identifiable {
    var id: String { UUID().uuidString }
    let kind: QuizQuestionKind
    let prompt: String
    let choices: [String]?
    let answer: String          // index for mc/tf, exact string for fr
    let explanation: String
    let source: SourceCitation
    let hints: [String]         // 0–3 progressive hints

    enum CodingKeys: String, CodingKey {
        case kind, prompt, choices, answer, explanation, source, hints
    }

    init(kind: QuizQuestionKind,
         prompt: String,
         choices: [String]?,
         answer: String,
         explanation: String,
         source: SourceCitation,
         hints: [String] = []) {
        self.kind = kind
        self.prompt = prompt
        self.choices = choices
        self.answer = answer
        self.explanation = explanation
        self.source = source
        self.hints = hints
    }

    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        self.kind = try c.decode(QuizQuestionKind.self, forKey: .kind)
        self.prompt = try c.decode(String.self, forKey: .prompt)
        self.choices = try c.decodeIfPresent([String].self, forKey: .choices)
        self.answer = try c.decode(String.self, forKey: .answer)
        self.explanation = try c.decode(String.self, forKey: .explanation)
        self.source = try c.decode(SourceCitation.self, forKey: .source)
        self.hints = try c.decodeIfPresent([String].self, forKey: .hints) ?? []
    }
}

struct Quiz: Codable, Hashable, Identifiable {
    let id: String
    let title: String
    let questions: [QuizQuestion]
}
