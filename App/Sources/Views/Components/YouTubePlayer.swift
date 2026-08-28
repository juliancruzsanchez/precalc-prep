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
struct LocalVideoPlayer: View {
    let videoID: String
    @State private var player: AVPlayer?

    var body: some View {
        ZStack {
            Color.black
            if let player {
                PlayerLayerView(player: player)
            } else {
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
        }
        .task(id: videoID) {
            let url = Bundle.main.url(
                forResource: videoID,
                withExtension: "mp4"
            )
            if let url {
                let item = AVPlayerItem(url: url)
                let p = AVPlayer(playerItem: item)
                p.isMuted = false
                p.actionAtItemEnd = .none
                player = p
            } else {
                player = nil
            }
        }
        .onDisappear {
            // Pause when the page scrolls offscreen so we don't leak audio
            // from videos the user has already swiped past.
            player?.pause()
        }
    }
}

/// Back-compat alias — LessonView still calls `YouTubeEmbed(videoID:)`.
/// The actual sizing (frame) is applied by the caller (VideoCard), so
/// the player can't be collapsed to zero by SwiftUI layout negotiation.
typealias YouTubeEmbed = LocalVideoPlayer
