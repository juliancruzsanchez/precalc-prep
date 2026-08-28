import Foundation

enum ContentError: LocalizedError {
    case fileNotFound
    case decodeFailed(String)

    var errorDescription: String? {
        switch self {
        case .fileNotFound: return "Could not locate the curriculum file in the app bundle."
        case .decodeFailed(let reason): return "Could not decode curriculum: \(reason)"
        }
    }
}

final class ContentService {
    static let shared = ContentService()

    private var cached: Course?

    func loadCourse() throws -> Course {
        if let cached { return cached }
        guard let url = Bundle.main.url(forResource: "course", withExtension: "json") else {
            throw ContentError.fileNotFound
        }
        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        do {
            let course = try decoder.decode(Course.self, from: data)
            cached = course
            return course
        } catch {
            throw ContentError.decodeFailed(String(describing: error))
        }
    }

    func topic(bySlug slug: String) -> Topic? {
        guard let course = try? loadCourse() else { return nil }
        if let pre = course.prerequisites?.first(where: { $0.slug == slug }) { return pre }
        for week in course.weeks {
            if let t = week.topics.first(where: { $0.slug == slug }) { return t }
        }
        return nil
    }

    func parentWeek(forTopicSlug slug: String) -> Week? {
        guard let course = try? loadCourse() else { return nil }
        return course.weeks.first { $0.topics.contains { $0.slug == slug } }
    }
}
