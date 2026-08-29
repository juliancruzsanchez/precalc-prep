import SwiftUI
import AVFoundation

/// UIView wrapper around an AVPlayerLayer. The layer is the view's backing
/// layer, so the video automatically fills the view's bounds — no
/// SwiftUI intrinsic-size negotiation required. This is critical inside
/// paged TabViews where aspect-ratio / GeometryReader-based sizing kept
/// collapsing the video to zero height.
struct PlayerLayerView: UIViewRepresentable {
    let player: AVPlayer

    func makeUIView(context: Context) -> PlayerContainerView {
        let view = PlayerContainerView()
        view.player = player
        view.backgroundColor = .black
        return view
    }

    func updateUIView(_ uiView: PlayerContainerView, context: Context) {
        uiView.player = player
    }

    final class PlayerContainerView: UIView {
        override static var layerClass: AnyClass { AVPlayerLayer.self }
        var playerLayer: AVPlayerLayer { layer as! AVPlayerLayer }

        var player: AVPlayer? {
            get { playerLayer.player }
            set { playerLayer.player = newValue }
        }

        override init(frame: CGRect) {
            super.init(frame: frame)
            playerLayer.videoGravity = .resizeAspect
        }

        required init?(coder: NSCoder) {
            super.init(coder: coder)
            playerLayer.videoGravity = .resizeAspect
        }
    }
}

/// Local MP4 player. Videos live at `Videos/{youtubeId}.mp4` in the app
/// bundle (Git LFS tracked) and play via an embedded AVPlayerLayer.
/// Local MP4 player. Videos live at `Videos/{youtubeId}.mp4` in the app
/// bundle (Git LFS tracked) and play via an embedded AVPlayerLayer.
///
/// The raw AVPlayerLayer has no built-in transport controls, so the playback
/// UI below is layered on top in SwiftUI: tap anywhere to play/pause, a
/// center play button while paused, and a scrubber with timestamps at the
/// bottom. Controls are small and kept to the video's own area so they never
/// fight the paging swipes of the surrounding TabView.
struct LocalVideoPlayer: View {
    let videoID: String
    @State private var player: AVPlayer?
    @State private var timeObserver: Any?
    @State private var isPlaying = false
    @State private var isScrubbing = false
    @State private var currentTime: Double = 0
    @State private var duration: Double = 0

    var body: some View {
        ZStack {
            Color.black
            if let player {
                PlayerLayerView(player: player)
                    .contentShape(Rectangle())
                    .onTapGesture { togglePlayPause() }
            } else {
                missingFile
            }

            if player != nil {
                controls
            }
        }
        .task(id: videoID) {
            guard let url = Bundle.main.url(
                forResource: videoID,
                withExtension: "mp4"
            ) else {
                player = nil
                return
            }
            let item = AVPlayerItem(url: url)
            let p = AVPlayer(playerItem: item)
            p.isMuted = false
            p.actionAtItemEnd = .pause
            player = p

            let interval = CMTime(seconds: 0.25, preferredTimescale: 600)
            let token = p.addPeriodicTimeObserver(
                forInterval: interval,
                queue: .main
            ) { [weak p] time in
                guard !isScrubbing, let p else { return }
                currentTime = time.seconds
                let d = p.currentItem?.duration.seconds ?? 0
                if d.isFinite, d > 0 { duration = d }
                isPlaying = p.timeControlStatus == .playing
            }
            timeObserver = token

            // Auto-play as soon as the item is ready. Without this the
            // first frame renders (the "thumbnail") but playback never
            // starts — the user has to tap, and on the paged TabView the
            // tap can be eaten by the swipe gesture.
            try? await Task.sleep(nanoseconds: 200_000_000)
            p.play()
        }
        .onDisappear {
            // Pause when the page scrolls offscreen so we don't leak audio
            // from videos the user has already swiped past.
            removeTimeObserver()
            player?.pause()
        }
    }

    // MARK: - Controls

    /// Center play button while paused, plus a bottom transport bar
    /// (play/pause, scrubber, timestamps) that's always available.
    private var controls: some View {
        ZStack {
            if !isPlaying {
                Button {
                    togglePlayPause()
                } label: {
                    Image(systemName: "play.fill")
                        .font(.system(size: 40))
                        .foregroundStyle(.white)
                        .padding(22)
                        .background(.black.opacity(0.45), in: Circle())
                }
                .buttonStyle(.plain)
                .transition(.opacity)
            }

            VStack {
                Spacer()
                HStack(spacing: 10) {
                    Button {
                        togglePlayPause()
                    } label: {
                        Image(systemName: isPlaying ? "pause.fill" : "play.fill")
                            .font(.system(size: 16, weight: .semibold))
                            .foregroundStyle(.white)
                            .frame(width: 36, height: 36)
                    }
                    .buttonStyle(.plain)

                    Text(timeString(currentTime))
                        .font(.caption.monospacedDigit())
                        .foregroundStyle(.white)
                        .frame(minWidth: 40, alignment: .leading)

                    Slider(
                        value: $currentTime,
                        in: 0...max(duration, 0.01),
                        onEditingChanged: { editing in
                            isScrubbing = editing
                            if !editing {
                                player?.seek(
                                    to: CMTime(seconds: currentTime, preferredTimescale: 600),
                                    toleranceBefore: .zero,
                                    toleranceAfter: .zero
                                )
                            }
                        }
                    )
                    .tint(.white)

                    Text(timeString(duration))
                        .font(.caption.monospacedDigit())
                        .foregroundStyle(.white)
                        .frame(minWidth: 40, alignment: .trailing)
                }
                .padding(.horizontal, 8)
                .padding(.top, 20)
                .padding(.bottom, 6)
                .background(
                    LinearGradient(
                        colors: [.clear, .black.opacity(0.55)],
                        startPoint: .top,
                        endPoint: .bottom
                    )
                )
            }
        }
    }

    private var missingFile: some View {
        VStack(spacing: 8) {
            Image(systemName: "exclamationmark.triangle.fill")
                .font(.title2)
                .foregroundStyle(.yellow)
            Text("Video file missing")
                .font(.caption)
                .foregroundStyle(.white)
            Text(videoID)
                .font(.caption2.monospaced())
                .foregroundStyle(.white.opacity(0.6))
        }
    }

    // MARK: - Playback

    private func togglePlayPause() {
        guard let player else { return }
        if player.timeControlStatus == .playing {
            player.pause()
            isPlaying = false
        } else {
            // Replaying from the end restarts from the beginning.
            let now = player.currentTime().seconds
            let dur = player.currentItem?.duration.seconds ?? 0
            if dur.isFinite, dur > 0, now >= dur - 0.5 {
                player.seek(to: .zero)
            }
            player.play()
            isPlaying = true
        }
    }

    private func removeTimeObserver() {
        guard let token = timeObserver, let player else { return }
        player.removeTimeObserver(token)
        timeObserver = nil
    }

    private func timeString(_ t: Double) -> String {
        guard t.isFinite, t >= 0 else { return "0:00" }
        let total = Int(t)
        return "\(total / 60):" + String(format: "%02d", total % 60)
    }
}

/// Back-compat alias — LessonView still calls `YouTubeEmbed(videoID:)`.
/// The actual sizing (frame) is applied by the caller (VideoCard), so
/// the player can't be collapsed to zero by SwiftUI layout negotiation.
typealias YouTubeEmbed = LocalVideoPlayer
