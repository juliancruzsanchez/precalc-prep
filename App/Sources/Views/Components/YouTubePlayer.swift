import SwiftUI
import WebKit

struct YouTubePlayer: UIViewRepresentable {
    let videoID: String
    @Binding var isPlaying: Bool

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []
        let view = WKWebView(frame: .zero, configuration: config)
        view.scrollView.isScrollEnabled = false
        view.backgroundColor = .black
        view.isOpaque = false
        loadContent(into: view)
        return view
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        loadContent(into: uiView)
    }

    private func loadContent(into view: WKWebView) {
        let html = """
        <!doctype html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                html, body { margin: 0; padding: 0; background: #000; height: 100%; width: 100%; }
                iframe { display: block; width: 100%; height: 100%; border: 0; }
            </style>
        </head>
        <body>
            <iframe
                src="https://www.youtube-nocookie.com/embed/\(videoID)?playsinline=1&rel=0&modestbranding=1"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen></iframe>
        </body>
        </html>
        """
        view.loadHTMLString(html, baseURL: URL(string: "https://www.youtube-nocookie.com"))
    }
}

/// Lightweight wrapper so the player only loads when the cell is on screen.
/// Renders full-width, edge-to-edge, with a 16:9 aspect ratio and no on-video
/// overlays (no position indicator, no debug text).
struct YouTubeEmbed: View {
    let videoID: String
    @State private var isPlaying = false

    var body: some View {
        YouTubePlayer(videoID: videoID, isPlaying: $isPlaying)
            .aspectRatio(16/9, contentMode: .fill)
            .background(Color.black)
    }
}
