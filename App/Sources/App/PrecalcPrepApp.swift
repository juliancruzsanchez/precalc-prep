import SwiftUI

@main
struct PrecalcPrepApp: App {
    @StateObject private var progress = ProgressService()
    @StateObject private var settings = SettingsService()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(progress)
                .environmentObject(settings)
                .preferredColorScheme(settings.colorSchemePreference.colorScheme)
                .tint(Theme.accent)
        }
    }
}

struct RootView: View {
    @EnvironmentObject private var settings: SettingsService
    @State private var selectedTab: AppTab = .home

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem { Label("Home", systemImage: "house.fill") }
                .tag(AppTab.home)

            TopicsView()
                .tabItem { Label("Topics", systemImage: "list.bullet.rectangle.fill") }
                .tag(AppTab.topics)

            ToolsView()
                .tabItem { Label("Tools", systemImage: "function") }
                .tag(AppTab.tools)

            TutorView()
                .tabItem { Label(TutorPersona.callToAction, systemImage: "bubble.left.and.bubble.right.fill") }
                .tag(AppTab.tutor)

            SettingsView()
                .tabItem { Label("Settings", systemImage: "gear") }
                .tag(AppTab.settings)
        }
    }
}

enum AppTab: Hashable {
    case home, topics, tools, tutor, settings
}
