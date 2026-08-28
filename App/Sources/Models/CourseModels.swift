import Foundation

// MARK: - Source attribution

enum TextbookSource: String, Codable, Hashable {
    case lippmanRasmussen = "lippman_rasmussen"
    case yoshiwara = "yoshiwara"
    case openstaxAbramson = "openstax_abramson"

    var displayName: String {
        switch self {
        case .lippmanRasmussen: return "Lippman & Rasmussen, Precalculus: An Investigation of Functions (LibreTexts, 2017)"
        case .yoshiwara: return "Yoshiwara, Trigonometry (LibreTexts, 2018)"
        case .openstaxAbramson: return "Abramson et al., Algebra & Trigonometry (OpenStax, 2021)"
        }
    }

    var licenseName: String {
        switch self {
        case .lippmanRasmussen, .yoshiwara: return "CC BY-NC-SA 4.0"
        case .openstaxAbramson: return "CC BY 4.0"
        }
    }

    var baseURL: String {
        switch self {
        case .lippmanRasmussen:
            return "https://math.libretexts.org/Bookshelves/Precalculus/Book%3A_Precalculus__An_Investigation_of_Functions_(Lippman_and_Rasmussen)"
        case .yoshiwara:
            return "https://math.libretexts.org/Bookshelves/Precalculus/Trigonometry_(Yoshiwara)"
        case .openstaxAbramson:
            return "https://openstax.org/books/algebra-and-trigonometry/pages"
        }
    }
}

struct SourceCitation: Codable, Hashable {
    let source: TextbookSource
    let chapter: String?
    let section: String?
    let urlPath: String?

    var displayLabel: String {
        var parts: [String] = [source.displayName]
        if let chapter { parts.append(chapter) }
        if let section { parts.append(section) }
        return parts.joined(separator: " — ")
    }

    var url: URL? {
        guard var components = URLComponents(string: source.baseURL) else { return nil }
        if let urlPath {
            components.path = urlPath.hasPrefix("/") ? urlPath : "/" + urlPath
        }
        return components.url
    }
}

// MARK: - Curriculum hierarchy

struct Course: Codable, Hashable {
    let id: String
    let title: String
    let institution: String
    let weeks: [Week]
    let prerequisites: [Topic]?
    let textbooks: [TextbookSource]
}

struct Week: Codable, Hashable, Identifiable {
    var id: String { "week-\(number)" }
    let number: Int
    let title: String
    let summary: String
    let topics: [Topic]
    let sources: [SourceCitation]
}

struct Topic: Codable, Hashable, Identifiable {
    var id: String { slug }
    let slug: String
    let title: String
    let summary: String
    let estimatedMinutes: Int
    let lesson: Lesson
    let sources: [SourceCitation]
}

struct Lesson: Codable, Hashable {
    let objectives: [String]
    let explanation: Explanation
    let examples: [WorkedExample]
    let stepByStep: [StepByStepProblem]
    let videos: [VideoResource]
    let practice: [QuizQuestion]
    let graphPlots: [GraphPlot]?
    let keyFormulas: [KeyFormula]?
}

struct Explanation: Codable, Hashable {
    let intro: String
    let sections: [ExplanationSection]
}

struct ExplanationSection: Codable, Hashable, Identifiable {
    var id: String { heading }
    let heading: String
    let body: String
    let bullets: [String]?
}

struct WorkedExample: Codable, Hashable, Identifiable {
    var id: String { UUID().uuidString }
    let title: String
    let problem: String
    let solution: String
    let steps: [String]
    let source: SourceCitation
}

struct StepByStepProblem: Codable, Hashable, Identifiable {
    var id: String { UUID().uuidString }
    let title: String
    let prompt: String
    let steps: [Step]
    let source: SourceCitation
}

struct Step: Codable, Hashable, Identifiable {
    var id: String { UUID().uuidString }
    let label: String
    let math: String
    let explanation: String
}

struct VideoResource: Codable, Hashable, Identifiable {
    var id: String { youtubeId }
    let youtubeId: String
    let title: String
    let channel: String
    let source: SourceCitation?
    let durationSeconds: Int?
}

struct KeyFormula: Codable, Hashable, Identifiable {
    var id: String { UUID().uuidString }
    let name: String
    let latex: String
    let whenToUse: String?
}

struct GraphPlot: Codable, Hashable, Identifiable {
    var id: String { UUID().uuidString }
    let title: String
    let expression: String
    /// Two-element array [min, max] in JSON; deserialized into a ClosedRange.
    let domainX: [Double]
    let domainY: [Double]
    let note: String?

    var xRange: ClosedRange<Double>? {
        guard domainX.count == 2, domainX[0] <= domainX[1] else { return nil }
        return domainX[0]...domainX[1]
    }

    var yRange: ClosedRange<Double>? {
        guard domainY.count == 2, domainY[0] <= domainY[1] else { return nil }
        return domainY[0]...domainY[1]
    }
}
