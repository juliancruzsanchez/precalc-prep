import SwiftUI

struct LessonView: View {
    let topic: Topic

    @EnvironmentObject private var progress: ProgressService
    @EnvironmentObject private var settings: SettingsService

    @State private var showingQuiz = false

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                header

                objectivesCard

                ExplanationBlock(explanation: topic.lesson.explanation)

                if let plots = topic.lesson.graphPlots, !plots.isEmpty {
                    SectionHeader(title: "Interactive graphs", systemImage: "chart.xyaxis.line")
                    ForEach(plots) { plot in
                        if let xr = plot.xRange, let yr = plot.yRange {
                            GraphView(
                                title: plot.title,
                                expression: plot.expression,
                                domainX: xr,
                                domainY: yr,
                                note: plot.note
                            )
                        }
                    }
                }

                if !topic.lesson.examples.isEmpty {
                    SectionHeader(title: "Worked examples", systemImage: "list.bullet.rectangle")
                    ForEach(topic.lesson.examples, id: \.title) { ex in
                        WorkedExampleView(example: ex)
                    }
                }

                if !topic.lesson.stepByStep.isEmpty {
                    SectionHeader(title: "Step-by-step", systemImage: "list.number")
                    ForEach(topic.lesson.stepByStep, id: \.title) { prob in
                        StepByStepView(problem: prob)
                    }
                }

                if !topic.lesson.videos.isEmpty {
                    SectionHeader(title: "Videos", systemImage: "play.rectangle")
                    ForEach(topic.lesson.videos) { v in
                        VideoCard(video: v, topicSlug: topic.slug)
                    }
                }

                practiceCard

                SourceListView(citations: topic.sources)
            }
            .padding()
        }
        .navigationTitle(topic.title)
        .navigationBarTitleDisplayMode(.inline)
        .onAppear { settings.lastLessonSlug = topic.slug }
        .sheet(isPresented: $showingQuiz) {
            NavigationStack {
                QuizView(topicSlug: topic.slug, questions: topic.lesson.practice)
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(topic.summary)
                .font(.subheadline)
                .foregroundStyle(.secondary)
            HStack(spacing: 12) {
                Label("\(topic.estimatedMinutes) min", systemImage: "clock")
                let p = progress.progress(for: topic.slug)
                if p.lessonRead {
                    Label("Started", systemImage: "book.fill")
                        .foregroundStyle(Theme.success)
                }
            }
            .font(.caption)
            .foregroundStyle(.secondary)
        }
    }

    private var objectivesCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Learning objectives").font(.headline)
            ForEach(topic.lesson.objectives, id: \.self) { obj in
                HStack(alignment: .top, spacing: 8) {
                    Image(systemName: "target")
                        .foregroundStyle(Theme.accent)
                    Text(obj).font(.subheadline)
                }
            }
        }
        .cardStyle()
    }

    private var practiceCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                SectionHeader(title: "Practice", systemImage: "pencil.and.list.clipboard")
                Spacer()
            }
            Text("\(topic.lesson.practice.count) questions. Get instant feedback and step-by-step explanations.")
                .font(.subheadline)
                .foregroundStyle(.secondary)
            Button {
                progress.markLessonRead(slug: topic.slug)
                showingQuiz = true
            } label: {
                Label("Start practice quiz", systemImage: "play.fill")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)
        }
        .cardStyle()
    }
}

struct VideoCard: View {
    let video: VideoResource
    let topicSlug: String
    @EnvironmentObject private var progress: ProgressService
    @State private var didCount = false

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            YouTubeEmbed(videoID: video.youtubeId)
            VStack(alignment: .leading, spacing: 2) {
                Text(video.title).font(.subheadline.weight(.semibold))
                Text(video.channel).font(.caption).foregroundStyle(.secondary)
                if let source = video.source {
                    SourceCitationView(citation: source, compact: true)
                }
            }
        }
        .cardStyle()
        .onAppear {
            if !didCount {
                progress.incrementVideo(slug: topicSlug)
                didCount = true
            }
        }
    }
}
