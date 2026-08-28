import SwiftUI

struct LessonView: View {
    let topic: Topic

    @EnvironmentObject private var progress: ProgressService
    @EnvironmentObject private var settings: SettingsService

    @State private var showingQuiz = false
    @State private var walkthroughPage = 0
    @State private var videoPage = 0
    @State private var showingTutor = false
    @State private var walkthroughHeight: CGFloat = 360

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
                    VStack(alignment: .leading, spacing: 12) {
                        HStack {
                            SectionHeader(title: "Step-by-step walkthroughs", systemImage: "list.number")
                            Spacer()
                            if topic.lesson.stepByStep.count > 1 {
                                Text("\(walkthroughPage + 1) of \(topic.lesson.stepByStep.count)")
                                    .font(.caption.monospacedDigit())
                                    .foregroundStyle(.secondary)
                            }
                        }
                        // Pager. The TabView height grows with the tallest page so
                        // content is never clipped and the card keeps its rounded
                        // corners. We measure each page's intrinsic height via
                        // `PageContentHeightKey` (see ContentBlocks).
                        TabView(selection: $walkthroughPage) {
                            ForEach(Array(topic.lesson.stepByStep.enumerated()), id: \.element.title) { idx, prob in
                                StepByStepView(problem: prob)
                                    .padding(.horizontal, 2)
                                    .tag(idx)
                            }
                        }
                        .tabViewStyle(.page(indexDisplayMode: .always))
                        .frame(height: walkthroughHeight)
                        .onPreferenceChange(PageContentHeightKey.self) { height in
                            // Add a little breathing room so the page indicator
                            // and bottom padding don't crowd the last step.
                            walkthroughHeight = max(height + 8, 320)
                        }
                    }
                }

                if !topic.lesson.videos.isEmpty {
                    VStack(alignment: .leading, spacing: 12) {
                        HStack {
                            SectionHeader(title: "Videos", systemImage: "play.rectangle")
                            Spacer()
                            if topic.lesson.videos.count > 1 {
                                Text("\(videoPage + 1) of \(topic.lesson.videos.count)")
                                    .font(.caption.monospacedDigit())
                                    .foregroundStyle(.secondary)
                            }
                        }
                        // Pager. The TabView height grows with the tallest page so
                        // content is never clipped.
                        TabView(selection: $videoPage) {
                            ForEach(Array(topic.lesson.videos.enumerated()), id: \.element.youtubeId) { idx, v in
                                VideoCard(video: v, topicSlug: topic.slug)
                                    .tag(idx)
                            }
                        }
                        .tabViewStyle(.page(indexDisplayMode: .always))
                    }
                }

                practiceCard

                SourceListView(citations: topic.sources)
            }
            .padding()
        }
        .navigationTitle(topic.title)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            // AI chat button on the right of the navigation bar.
            ToolbarItem(placement: .topBarTrailing) {
                Button {
                    showingTutor = true
                } label: {
                    Label("Ask AI", systemImage: "bubble.left.and.bubble.right.fill")
                        .labelStyle(.titleAndIcon)
                }
                .buttonStyle(.borderedProminent)
                .tint(Theme.accent)
                .controlSize(.small)
            }
        }
        .onAppear { settings.lastLessonSlug = topic.slug }
        .sheet(isPresented: $showingQuiz) {
            NavigationStack {
                QuizView(topicSlug: topic.slug, questions: topic.lesson.practice)
            }
        }
        .sheet(isPresented: $showingTutor) {
            NavigationStack {
                TutorView(context: .init(topic: topic))
            }
        }
    }

    // MARK: - Header

    private var header: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(topic.summary)
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .fixedSize(horizontal: false, vertical: true)
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

    // MARK: - Cards

    private var objectivesCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Learning objectives").font(.headline)
            ForEach(topic.lesson.objectives, id: \.self) { obj in
                HStack(alignment: .top, spacing: 8) {
                    Image(systemName: "target")
                        .foregroundStyle(Theme.accent)
                    Text(obj).font(.subheadline)
                        .fixedSize(horizontal: false, vertical: true)
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

/// Video card: video plays full width (edge-to-edge inside the card), the
/// title / channel / source sit underneath. The page indicator from the parent
/// `TabView` sits below this card, so it can never overlap the video itself.
struct VideoCard: View {
    let video: VideoResource
    let topicSlug: String
    @EnvironmentObject private var progress: ProgressService
    @State private var didCount = false

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Full-width video, no padding, no on-video overlay.
            YouTubeEmbed(videoID: video.youtubeId)
                .frame(maxWidth: .infinity)

            VStack(alignment: .leading, spacing: 4) {
                Text(video.title)
                    .font(.subheadline.weight(.semibold))
                    .fixedSize(horizontal: false, vertical: true)
                Text(video.channel)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                if let source = video.source {
                    SourceCitationView(citation: source, compact: true)
                }
            }
            .padding(14)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .background(Theme.card, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .stroke(Color.primary.opacity(0.05), lineWidth: 1)
        )
        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        .onAppear {
            if !didCount {
                progress.incrementVideo(slug: topicSlug)
                didCount = true
            }
        }
    }
}
