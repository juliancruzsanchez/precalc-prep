import Foundation
import SwiftUI

enum ColorSchemePreference: String, CaseIterable, Identifiable {
    case system, light, dark
    var id: String { rawValue }
    var label: String {
        switch self {
        case .system: return "Match system"
        case .light: return "Always light"
        case .dark: return "Always dark"
        }
    }
    var colorScheme: ColorScheme? {
        switch self {
        case .system: return nil
        case .light: return .light
        case .dark: return .dark
        }
    }
}

final class SettingsService: ObservableObject {
    private static let colorSchemeKey = "settings.colorScheme"
    private static let lastLessonSlugKey = "settings.lastLessonSlug"

    @Published var colorSchemePreference: ColorSchemePreference {
        didSet {
            UserDefaults.standard.set(colorSchemePreference.rawValue, forKey: Self.colorSchemeKey)
        }
    }

    @Published var lastLessonSlug: String? {
        didSet {
            UserDefaults.standard.set(lastLessonSlug, forKey: Self.lastLessonSlugKey)
        }
    }

    init() {
        let raw = UserDefaults.standard.string(forKey: Self.colorSchemeKey) ?? ColorSchemePreference.system.rawValue
        self.colorSchemePreference = ColorSchemePreference(rawValue: raw) ?? .system
        self.lastLessonSlug = UserDefaults.standard.string(forKey: Self.lastLessonSlugKey)
    }
}
