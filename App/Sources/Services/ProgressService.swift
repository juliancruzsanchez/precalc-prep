import Foundation

struct TopicProgress: Codable, Hashable {
    var lessonRead: Bool = false
    var examplesViewed: Int = 0
    var stepByStepsCompleted: Int = 0
    var videosWatched: Int = 0
    var quizAttempts: Int = 0
    var quizCorrect: Int = 0
    var quizTotal: Int = 0
    var lastVisited: Date?

    var quizScorePercent: Double {
        guard quizTotal > 0 else { return 0 }
        return Double(quizCorrect) / Double(quizTotal) * 100
    }
}

final class ProgressService: ObservableObject {
    private static let storageKey = "progress.v1"

    @Published private(set) var byTopic: [String: TopicProgress] = [:]

    init() {
        if let data = UserDefaults.standard.data(forKey: Self.storageKey),
           let decoded = try? JSONDecoder().decode([String: TopicProgress].self, from: data) {
            self.byTopic = decoded
        }
    }

    private func save() {
        if let data = try? JSONEncoder().encode(byTopic) {
            UserDefaults.standard.set(data, forKey: Self.storageKey)
        }
    }

    func progress(for slug: String) -> TopicProgress {
        byTopic[slug] ?? TopicProgress()
    }

    func ensureEntry(for slug: String) {
        if byTopic[slug] == nil {
            byTopic[slug] = TopicProgress()
        }
    }

    func markLessonRead(slug: String) {
        ensureEntry(for: slug)
        byTopic[slug]?.lessonRead = true
        byTopic[slug]?.lastVisited = Date()
        save()
    }

    func incrementExample(slug: String) {
        ensureEntry(for: slug)
        byTopic[slug]?.examplesViewed += 1
        save()
    }

    func incrementStep(slug: String) {
        ensureEntry(for: slug)
        byTopic[slug]?.stepByStepsCompleted += 1
        save()
    }

    func incrementVideo(slug: String) {
        ensureEntry(for: slug)
        byTopic[slug]?.videosWatched += 1
        save()
    }

    func recordQuiz(slug: String, correct: Int, total: Int) {
        ensureEntry(for: slug)
        byTopic[slug]?.quizAttempts += 1
        byTopic[slug]?.quizCorrect += correct
        byTopic[slug]?.quizTotal += total
        save()
    }

    var overallCompletion: Double {
        guard let course = try? ContentService.shared.loadCourse() else { return 0 }
        let allSlugs: [String] = (course.prerequisites ?? []).map(\.slug)
            + course.weeks.flatMap { $0.topics.map(\.slug) }
        guard !allSlugs.isEmpty else { return 0 }
        let readCount = allSlugs.filter { byTopic[$0]?.lessonRead == true }.count
        return Double(readCount) / Double(allSlugs.count)
    }
}
