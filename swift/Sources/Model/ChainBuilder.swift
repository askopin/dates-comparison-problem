import Foundation


class ChainBuilder {
    var calendar = Calendar(identifier: .gregorian)

    func process(response: EventsResponse) -> [EventChain] {
        let events = response.events.sorted { $0.start < $1.start }

        let chains: [[Event]] = events.reduce(into: []) { acc, event in
            for (index, chain) in acc.enumerated() {
                guard let lastEvent = chain.last else {
                    assertionFailure("empty chains should never exist")
                    continue
                }
                
                if calendar.isDate(lastEvent.end, inSameDayAs: event.start) {
                    acc[index].append(event)
                    return
                }
            }

            acc.append([event])
        }

        return chains.map { EventChain(events: $0) }
    }
}
