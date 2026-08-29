import Foundation

struct ChatMessage: Identifiable, Hashable {
    enum Role: String { case system, user, assistant }
    let id = UUID()
    let role: Role
    var content: String
}

enum GroqError: LocalizedError {
    case missingAPIKey
    case http(Int)
    case decoding(String)
    case empty

    var errorDescription: String? {
        switch self {
        case .missingAPIKey: return "Add your Groq API key in Settings → \(TutorPersona.displayName)."
        case .http(let code): return "Groq returned HTTP \(code)."
        case .decoding(let msg): return "Could not parse Groq response: \(msg)"
        case .empty: return "Groq returned an empty response."
        }
    }
}

/// Lightweight Groq Chat Completions client. Defaults to a fast, cheap model.
final class GroqService {
    private let endpoint = URL(string: "https://api.groq.com/openai/v1/chat/completions")!
    private let session: URLSession

    init(session: URLSession = .shared) {
        self.session = session
    }

    func send(messages: [ChatMessage], model: String = "llama-3.1-8b-instant") async throws -> String {
        guard let apiKey = KeychainService.loadGroqKey(), !apiKey.isEmpty else {
            throw GroqError.missingAPIKey
        }

        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.timeoutInterval = 60

        let payload: [String: Any] = [
            "model": model,
            "messages": messages.map {
                [
                    "role": $0.role.rawValue,
                    "content": $0.content,
                ]
            },
            "temperature": 0.2,
            "max_tokens": 1024,
        ]
        request.httpBody = try JSONSerialization.data(withJSONObject: payload)

        let (data, response) = try await session.data(for: request)
        guard let http = response as? HTTPURLResponse else { throw GroqError.empty }
        guard (200..<300).contains(http.statusCode) else {
            let body = String(data: data, encoding: .utf8) ?? ""
            throw GroqError.http(http.statusCode)
        }

        struct Response: Decodable {
            struct Choice: Decodable {
                struct Message: Decodable { let role: String; let content: String }
                let message: Message
            }
            let choices: [Choice]
        }

        do {
            let decoded = try JSONDecoder().decode(Response.self, from: data)
            guard let content = decoded.choices.first?.message.content, !content.isEmpty else {
                throw GroqError.empty
            }
            return content
        } catch {
            throw GroqError.decoding(String(describing: error))
        }
    }
}
