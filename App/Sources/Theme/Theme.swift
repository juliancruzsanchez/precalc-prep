import SwiftUI

enum Theme {
    static let accent = Color(red: 0.243, green: 0.498, blue: 0.910)
    static let accentSoft = Color(red: 0.243, green: 0.498, blue: 0.910).opacity(0.12)
    static let success = Color(red: 0.18, green: 0.65, blue: 0.39)
    static let warning = Color(red: 0.93, green: 0.62, blue: 0.13)
    static let danger = Color(red: 0.86, green: 0.21, blue: 0.27)
    static let card = Color(.secondarySystemGroupedBackground)
    static let background = Color(.systemGroupedBackground)

    /// Math-style serif font. Uses New York (the iOS system serif), which is
    /// optimized for reading at body sizes. Use `compact: true` for inline /
    /// step-by-step lines; the default for full equations.
    static func mathFont(compact: Bool) -> Font {
        if compact {
            return .system(.callout, design: .serif)
        } else {
            return .system(.body, design: .serif)
        }
    }
}

struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(16)
            .background(Theme.card, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: 16, style: .continuous)
                    .stroke(Color.primary.opacity(0.05), lineWidth: 1)
            )
    }
}

extension View {
    func cardStyle() -> some View { modifier(CardStyle()) }
}

struct SectionHeader: View {
    let title: String
    var subtitle: String? = nil
    var systemImage: String? = nil

    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 8) {
            if let systemImage {
                Image(systemName: systemImage)
                    .foregroundStyle(Theme.accent)
            }
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.title2.weight(.semibold))
                if let subtitle {
                    Text(subtitle)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
            }
            Spacer()
        }
    }
}
