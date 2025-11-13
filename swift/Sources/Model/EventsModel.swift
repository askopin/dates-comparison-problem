import Foundation

struct EventChain: Identifiable, Equatable {
    let id: String
    let events: [Event]

    init(events: [Event]) {
        self.events = events
        self.id = events.map { String($0.id) }.joined(separator: "|")
    }
}

struct Event: Decodable, Identifiable, Equatable {
    let id: Int
    let start: Date
    let end: Date
}

struct EventsResponse: Decodable {
    let events: [Event]
}
