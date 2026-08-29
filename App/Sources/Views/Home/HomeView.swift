import SwiftUI

struct HomeView: View {
    @EnvironmentObject private var progress: ProgressService
    @EnvironmentObject private var settings: SettingsService

    @State private var course: Course?
    @State private var loadError: String?

    private var weekSummaries: [Week] { course?.weeks ?? [] }
    private var prerequisites: [Topic] { course?.prerequisites ?? [] }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    heroCard
                    prereqCard
                    weekList
                    attributionCard
                }
                .padding()
            }
            .background(Theme.background)
            .navigationTitle("Precalc Prep")
            .task { loadCourse() }
        }
    }

    private var heroCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(course?.title ?? "Loading…")
                        .font(.title2.weight(.bold))
                    Text(course?.institution ?? "")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
                Spacer()
                Image(systemName: "function")
                    .font(.system(size: 36))
                    .foregroundStyle(Theme.accent)
            }
            ProgressView(value: progress.overallCompletion) {
                Text("Course progress")
                    .font(.caption.weight(.semibold))
            } currentValueLabel: {
                Text("\(Int(progress.overallCompletion * 100))%")
                    .font(.caption.monospacedDigit())
            }
            .tint(Theme.accent)
            HStack {
                if let slug = settings.lastLessonSlug, let topic = course.flatMap({ (_: Course) -> Topic? in ContentService.shared.topic(bySlug: slug) }) {
                    NavigationLink {
                        LessonView(topic: topic)
                    } label: {
                        Label(topic.title, systemImage: "play.circle.fill")
                            .lineLimit(1)
                            .truncationMode(.tail)
                            .frame(maxWidth: .infinity, alignment: .center)
                    }
                    .buttonStyle(.borderedProminent)
                    .controlSize(.regular)
                } else {
                    NavigationLink {
                        TopicsView()
                    } label: {
                        Label("Start the course", systemImage: "play.circle.fill")
                            .lineLimit(1)
                            .truncationMode(.tail)
                            .frame(maxWidth: .infinity, alignment: .center)
                    }
                    .buttonStyle(.borderedProminent)
                    .controlSize(.regular)
                }
            }
        }
        .cardStyle()
    }

    private var prereqCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            SectionHeader(
                title: "Bridge from geometry",
                subtitle: "These six topics fill the two years of math you missed. Do these first if anything in Week 1 looks unfamiliar.",
                systemImage: "arrow.up.right.circle"
            )
            ForEach(prerequisites) { topic in
                NavigationLink {
                    LessonView(topic: topic)
                } label: {
                    HStack(alignment: .top, spacing: 12) {
                        Image(systemName: "circle.grid.cross")
                            .font(.title3)
                            .foregroundStyle(Theme.accent)
                            .frame(width: 32)
                        VStack(alignment: .leading, spacing: 2) {
                            Text(topic.title).font(.subheadline.weight(.semibold))
                            Text(topic.summary).font(.caption).foregroundStyle(.secondary).lineLimit(2)
                            HStack(spacing: 6) {
                                Image(systemName: "clock").font(.caption2)
                                Text("\(topic.estimatedMinutes) min").font(.caption2)
                            }
                            .foregroundStyle(.tertiary)
                        }
                        Spacer()
                        Image(systemName: "chevron.right").font(.caption).foregroundStyle(.tertiary)
                    }
                    .padding(.vertical, 6)
                }
                .buttonStyle(.plain)
                if topic.slug != prerequisites.last?.slug { Divider() }
            }
        }
        .cardStyle()
    }

    private var weekList: some View {
        VStack(alignment: .leading, spacing: 12) {
            SectionHeader(
                title: "7-week course",
                subtitle: "Matches the Champlain College CCO syllabus.",
                systemImage: "calendar"
            )
            ForEach(weekSummaries) { week in
                NavigationLink {
                    WeekDetailView(week: week)
                } label: {
                    WeekRow(week: week, progress: progress)
                }
                .buttonStyle(.plain)
            }
        }
    }

    private var attributionCard: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text("Course content")
                .font(.subheadline.weight(.semibold))
            Text("All topics, worked examples, and step-by-step walkthroughs in this app are based on three open-licensed textbooks:")
                .font(.caption)
                .foregroundStyle(.secondary)
            ForEach((course?.textbooks ?? []), id: \.self) { src in
                let s = TextbookSource(rawValue: src.rawValue) ?? .openstaxAbramson
                Text("• \(s.displayName) (\(s.licenseName))")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }
            Text("Topic structure and learning objectives follow the Champlain College CCO Precalculus 7-week outline.")
                .font(.caption2)
                .foregroundStyle(.secondary)
        }
        .cardStyle()
    }

    private func loadCourse() {
        do {
            course = try ContentService.shared.loadCourse()
        } catch {
            loadError = error.localizedDescription
        }
    }
}

struct WeekRow: View {
    let week: Week
    let progress: ProgressService

    private var completed: Int {
        week.topics.filter { progress.progress(for: $0.slug).lessonRead }.count
    }

    var body: some View {
        HStack(alignment: .center, spacing: 12) {
            ZStack {
                Circle()
                    .fill(Theme.accent.opacity(0.15))
                    .frame(width: 44, height: 44)
                Text("\(week.number)")
                    .font(.headline.weight(.bold))
                    .foregroundStyle(Theme.accent)
            }
            VStack(alignment: .leading, spacing: 4) {
                Text(week.title).font(.subheadline.weight(.semibold))
                Text(week.summary).font(.caption).foregroundStyle(.secondary).lineLimit(2)
                HStack(spacing: 6) {
                    Image(systemName: "list.bullet").font(.caption2)
                    Text("\(week.topics.count) topics").font(.caption2)
                    Text("·").font(.caption2)
                    Image(systemName: "checkmark").font(.caption2)
                    Text("\(completed) done").font(.caption2)
                }
                .foregroundStyle(.tertiary)
            }
            Spacer()
            Image(systemName: "chevron.right").font(.caption).foregroundStyle(.tertiary)
        }
        .padding(10)
        .background(Theme.card, in: RoundedRectangle(cornerRadius: 12))
    }
}
