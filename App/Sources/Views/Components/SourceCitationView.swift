import SwiftUI

struct SourceCitationView: View {
    let citation: SourceCitation
    var compact: Bool = false

    var body: some View {
        HStack(alignment: .top, spacing: 8) {
            Image(systemName: "book.closed")
                .foregroundStyle(Theme.accent)
                .font(.caption)
                .padding(.top, 2)
            VStack(alignment: .leading, spacing: 2) {
                Text(citation.displayLabel)
                    .font(.caption)
                    .foregroundStyle(.primary)
                Text(citation.source.licenseName)
                    .font(.caption2)
                    .foregroundStyle(.secondary)
                if !compact, let url = citation.url {
                    Link(destination: url) {
                        HStack(spacing: 4) {
                            Image(systemName: "link")
                            Text("Read in the source textbook")
                        }
                        .font(.caption2)
                    }
                }
            }
        }
        .padding(10)
        .background(Theme.accentSoft, in: RoundedRectangle(cornerRadius: 8))
    }
}

struct SourceListView: View {
    let citations: [SourceCitation]

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text("Sources")
                .font(.subheadline.weight(.semibold))
                .foregroundStyle(.secondary)
            ForEach(citations, id: \.self) { SourceCitationView(citation: $0, compact: true) }
        }
    }
}
