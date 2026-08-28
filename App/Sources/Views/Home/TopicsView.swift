import SwiftUI

struct TopicsView: View {
    @EnvironmentObject private var progress: ProgressService
    @State private var course: Course?

    var body: some View {
        NavigationStack {
            List {
                if let course {
                    if let prereqs = course.prerequisites, !prereqs.isEmpty {
                        Section("Prerequisites (catch-up)") {
                            ForEach(prereqs) { topic in
                                NavigationLink {
                                    LessonView(topic: topic)
                                } label: {
                                    topicRow(topic)
                                }
                            }
                        }
                    }
                    ForEach(course.weeks) { week in
                        Section("Week \(week.number) — \(week.title)") {
                            ForEach(week.topics) { topic in
                                NavigationLink {
                                    LessonView(topic: topic)
                                } label: {
                                    topicRow(topic)
                                }
                            }
                        }
                    }
                } else {
                    Text("Loading course…")
                }
            }
            .listStyle(.insetGrouped)
            .navigationTitle("Topics")
            .task {
                course = try? ContentService.shared.loadCourse()
            }
        }
    }

    @ViewBuilder
    private func topicRow(_ topic: Topic) -> some View {
        let p = progress.progress(for: topic.slug)
        HStack(alignment: .center, spacing: 10) {
            Image(systemName: p.lessonRead ? "checkmark.circle.fill" : "circle")
                .foregroundStyle(p.lessonRead ? Theme.success : .secondary)
            VStack(alignment: .leading, spacing: 2) {
                Text(topic.title)
                Text("\(topic.estimatedMinutes) min · \(topic.lesson.practice.count) practice Qs")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }
        }
    }
}

struct WeekDetailView: View {
    let week: Week
    @EnvironmentObject private var progress: ProgressService

    var body: some View {
        List {
            Section {
                Text(week.summary)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
            Section("Topics") {
                ForEach(week.topics) { topic in
                    NavigationLink {
                        LessonView(topic: topic)
                    } label: {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(topic.title).font(.body.weight(.medium))
                            Text(topic.summary)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                            HStack(spacing: 6) {
                                Label("\(topic.estimatedMinutes) min", systemImage: "clock")
                                Label("\(topic.lesson.practice.count) Qs", systemImage: "pencil")
                            }
                            .font(.caption2)
                            .foregroundStyle(.tertiary)
                        }
                        .padding(.vertical, 4)
                    }
                }
            }
            Section("Sources for this week") {
                ForEach(week.sources, id: \.self) { src in
                    SourceCitationView(citation: src, compact: true)
                }
            }
        }
        .listStyle(.insetGrouped)
        .navigationTitle("Week \(week.number)")
    }
}
