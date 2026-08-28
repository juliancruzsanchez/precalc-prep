import SwiftUI

struct SettingsView: View {
    @EnvironmentObject private var settings: SettingsService
    @State private var groqKey: String = ""
    @State private var keyStatus: String? = nil
    @State private var savingKey: Bool = false
    @State private var keyPresent: Bool = KeychainService.loadGroqKey() != nil

    var body: some View {
        NavigationStack {
            Form {
                Section("Appearance") {
                    Picker("Theme", selection: $settings.colorSchemePreference) {
                        ForEach(ColorSchemePreference.allCases) { p in
                            Text(p.label).tag(p)
                        }
                    }
                }
                Section {
                    SecureField("gsk_…", text: $groqKey)
                        .autocorrectionDisabled()
                        .textInputAutocapitalization(.never)
                    HStack {
                        Button(keyPresent ? "Replace key" : "Save key") {
                            saveKey()
                        }
                        .buttonStyle(.borderedProminent)
                        .disabled(groqKey.isEmpty || savingKey)
                        if keyPresent {
                            Button("Remove", role: .destructive) {
                                removeKey()
                            }
                            .buttonStyle(.bordered)
                        }
                        Spacer()
                    }
                    if let s = keyStatus {
                        Text(s).font(.caption).foregroundStyle(.secondary)
                    }
                    Text("Get a free key at console.groq.com. It is stored only in the iOS Keychain on this device, and only sent to api.groq.com when you chat.")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                } header: {
                    Text("AI Tutor (Groq API key)")
                } footer: {
                    Text("The app uses llama-3.1-8b-instant by default for fast, low-cost answers.")
                }

                Section("About") {
                    LabeledContent("Version", value: appVersion)
                    LabeledContent("Build", value: appBuild)
                    Link(destination: URL(string: "https://openstax.org/books/algebra-and-trigonometry")!) {
                        Label("OpenStax Algebra & Trigonometry", systemImage: "book")
                    }
                    Link(destination: URL(string: "https://math.libretexts.org/Bookshelves/Precalculus/Book%3A_Precalculus__An_Investigation_of_Functions_(Lippman_and_Rasmussen)")!) {
                        Label("Lippman & Rasmussen, LibreTexts", systemImage: "book")
                    }
                    Link(destination: URL(string: "https://math.libretexts.org/Bookshelves/Precalculus/Trigonometry_(Yoshiwara)")!) {
                        Label("Yoshiwara, LibreTexts", systemImage: "book")
                    }
                }

                Section("Licenses") {
                    Text("Course topic structure and learning objectives follow the Champlain College CCO Precalculus 7-week outline.")
                        .font(.caption)
                    Text("All content is original teaching prose. The app links to and cites the three required textbooks (Lippman & Rasmussen 2017, Yoshiwara 2018, Abramson et al. 2021).")
                        .font(.caption)
                    Text("LibreTexts books are CC BY-NC-SA 4.0; OpenStax is CC BY 4.0. This non-commercial study app is consistent with both licenses.")
                        .font(.caption)
                }
            }
            .navigationTitle("Settings")
        }
    }

    private var appVersion: String {
        Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0"
    }

    private var appBuild: String {
        Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "1"
    }

    private func saveKey() {
        savingKey = true
        do {
            try KeychainService.saveGroqKey(groqKey)
            keyPresent = true
            keyStatus = "Saved."
            groqKey = ""
        } catch {
            keyStatus = "Could not save: \(error.localizedDescription)"
        }
        savingKey = false
    }

    private func removeKey() {
        KeychainService.deleteGroqKey()
        keyPresent = false
        keyStatus = "Removed."
    }
}
