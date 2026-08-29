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
    @State private var videoPagerHeight: CGFloat = VideoCard.minCardHeight

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
                            .frame(maxWidth: .infinity)
                        }
                    }
                }

                if !topic.lesson.examples.isEmpty {
                    SectionHeader(title: "Worked examples", systemImage: "list.bullet.rectangle")
                    ForEach(topic.lesson.examples, id: \.title) { ex in
                        WorkedExampleView(example: ex)
                            .frame(maxWidth: .infinity)
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
                        // Pager with fixed height to ensure proper swipe behavior
                        TabView(selection: $walkthroughPage) {
                            ForEach(Array(topic.lesson.stepByStep.enumerated()), id: \.element.title) { idx, prob in
                                StepByStepCard(problem: prob)
                                    .tag(idx)
                            }
                        }
                        .tabViewStyle(.page(indexDisplayMode: .never))
                        .frame(height: 380)
                        // Custom dots for navigation feedback
                        .overlay(alignment: .bottom) {
                            if topic.lesson.stepByStep.count > 1 {
                                PageIndicator(count: topic.lesson.stepByStep.count, current: walkthroughPage)
                                    .padding(.bottom, 12)
                            }
                        }
                    }
                    .frame(maxWidth: .infinity)
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
                        // Pager. Height follows the tallest card (measured via
                        // `PageContentHeightKey`) so the attribution card always
                        // sits above the reserved page-indicator strip instead of
                        // spilling underneath the dots.
                        TabView(selection: $videoPage) {
                            ForEach(Array(topic.lesson.videos.enumerated()), id: \.element.youtubeId) { idx, v in
                                VideoCard(video: v, topicSlug: topic.slug)
                                    .tag(idx)
                            }
                        }
                        .tabViewStyle(.page(indexDisplayMode: .never))
                        .frame(height: videoPagerHeight)
                        // Custom dots instead of the system indicator, which is
                        // invisible over light backgrounds.
                        .overlay(alignment: .bottom) {
                            if topic.lesson.videos.count > 1 {
                                PageIndicator(count: topic.lesson.videos.count, current: videoPage)
                                    .padding(.bottom, 10)
                                    .allowsHitTesting(false)
                            }
                        }
                        .onPreferenceChange(PageContentHeightKey.self) { height in
                            videoPagerHeight = max(height, VideoCard.minCardHeight)
                        }
                    }
                    .frame(maxWidth: .infinity)
                }

                practiceCard

                SourceListView(citations: topic.sources)
            }
            .padding()
        }
        .navigationTitle(topic.title)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            // Liquid-glass chat circle in the navigation bar. Tapping opens
            // Ms. Kaya (the AI tutor) for the current lesson. The shape is a
            // plain circle — no text, no capsule — so it reads as an icon
            // affordance rather than a call-to-action pill. `.ultraThinMaterial`
            // gives it the frosted glass look; the soft white stroke + inner
            // highlight sell the "liquid glass" edge.
            ToolbarItem(placement: .topBarTrailing) {
                Button {
                    showingTutor = true
                } label: {
                    Image(systemName: "bubble.left.and.bubble.right.fill")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundStyle(Theme.accent)
                        .frame(width: 36, height: 36)
                        .background(
                            Circle()
                                .fill(.ultraThinMaterial)
                        )
                        .overlay(
                            Circle()
                                .stroke(Color.white.opacity(0.55), lineWidth: 0.7)
                        )
                        .overlay(
                            // Subtle inner highlight along the top — the
                            // "liquid" cue: a thin arc that catches light.
                            Circle()
                                .stroke(
                                    LinearGradient(
                                        colors: [
                                            Color.white.opacity(0.55),
                                            Color.white.opacity(0.0)
                                        ],
                                        startPoint: .top,
                                        endPoint: .center
                                    ),
                                    lineWidth: 0.7
                                )
                                .blendMode(.plusLighter)
                        )
                        .shadow(color: Color.black.opacity(0.08), radius: 4, x: 0, y: 2)
                }
                .buttonStyle(.plain)
                .accessibilityLabel(TutorPersona.callToAction)
            }
        }
        .onAppear { settings.lastLessonSlug = topic.slug }
        .onReceive(NotificationCenter.default.publisher(for: .dismissTutorView)) { _ in
            showingTutor = false
        }
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
        .frame(maxWidth: .infinity, alignment: .leading)
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
        .frame(maxWidth: .infinity, alignment: .leading)
        .cardStyle()
    }
}

/// Video card: video plays full width (edge-to-edge inside the card), the
/// title / channel / source sit underneath. The card sizes to its content and
/// reports its natural height through `PageContentHeightKey` so the parent
/// pager grows to fit (video + text + the strip reserved for the page dots) —
/// which keeps the page indicator from ever overlapping the attribution card.
struct VideoCard: View {
    let video: VideoResource
    let topicSlug: String
    @EnvironmentObject private var progress: ProgressService
    @State private var didCount = false

    /// Minimum video height. At ~390pt wide (iPhone portrait) the natural
    /// 16:9 height is ~219pt; we round up to 240 so the video is clearly
    /// visible and not squeezed. Hard-coded instead of `.aspectRatio` /
    /// GeometryReader because both kept collapsing inside the paged TabView.
    static let videoHeight: CGFloat = 240
    /// Space reserved at the bottom of the card for the TabView page dots.
    static let pageIndicatorPadding: CGFloat = 36
    /// Fallback minimum card height in case the preference measurement hasn't
    /// arrived yet — never lets the pager collapse the video away.
    static let minCardHeight: CGFloat = videoHeight + 120 + pageIndicatorPadding

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Full-width video, explicit height. No aspect-ratio modifier,
            // no GeometryReader — just a fixed frame so the AVPlayerLayer
            // always has a real, non-zero size to fill.
            YouTubeEmbed(videoID: video.youtubeId)
                .frame(maxWidth: .infinity)
                .frame(height: Self.videoHeight)
                .clipped()

            // Text + attribution. Sizes to its content (titles and citation
            // labels wrap freely) instead of a fixed height, so the citation
            // card can never overflow into the page-indicator strip below.
            VStack(alignment: .leading, spacing: 6) {
                Text(video.title)
                    .font(.subheadline.weight(.semibold))
                    .lineLimit(2)
                    .multilineTextAlignment(.leading)
                    .fixedSize(horizontal: false, vertical: true)
                Text(video.channel)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
                if let source = video.source {
                    SourceCitationView(citation: source, compact: true)
                }
            }
            .padding(14)
            // Reserve room for the page dots at the bottom of the pager.
            .padding(.bottom, Self.pageIndicatorPadding)
            .fixedSize(horizontal: false, vertical: true)
        }
        .background(Theme.card, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .stroke(Color.primary.opacity(0.05), lineWidth: 1)
        )
        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        // Report our natural height so the parent TabView can size to fit.
        .background(
            GeometryReader { proxy in
                Color.clear.preference(key: PageContentHeightKey.self, value: proxy.size.height)
            }
        )
        .onAppear {
            if !didCount {
                progress.incrementVideo(slug: topicSlug)
                didCount = true
            }
        }
    }
}
