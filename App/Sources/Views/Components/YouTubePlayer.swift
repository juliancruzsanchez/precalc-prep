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
                html, body { margin: 0; padding: 0; background: #000; height: 100%; }
                .wrap { position: relative; padding-top: 56.25%; height: 0; overflow: hidden; }
                iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
            </style>
        </head>
        <body>
            <div class="wrap">
                <iframe
                    src="https://www.youtube-nocookie.com/embed/\(videoID)?playsinline=1&rel=0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowfullscreen></iframe>
            </div>
        </body>
        </html>
        """
        view.loadHTMLString(html, baseURL: URL(string: "https://www.youtube-nocookie.com"))
    }
}

/// Lightweight wrapper so the player only loads when the cell is on screen.
struct YouTubeEmbed: View {
    let videoID: String
    @State private var isPlaying = false

    var body: some View {
        ZStack(alignment: .bottomTrailing) {
            YouTubePlayer(videoID: videoID, isPlaying: $isPlaying)
                .aspectRatio(16/9, contentMode: .fit)
                .background(Color.black)
            Text(videoID)
                .font(.caption2.monospaced())
                .foregroundStyle(.white.opacity(0.6))
                .padding(6)
        }
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}
