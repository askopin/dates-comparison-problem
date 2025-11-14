import Foundation

class ChainBuilder {
    var calendar = Calendar(identifier: .gregorian)

    func process(response: EventsResponse) -> [EventChain] {
        let events = response.events.sorted { $0.start < $1.start }

        let chains: [[Event]] = events.reduce(into: []) { chains, event in
            let insertIndex = chains.firstIndex(where: { chain in
                 guard let lastEvent = chain.last else {
                    assertionFailure("empty chains should never exist")
                    return false
                }

                return calendar.isDate(lastEvent.end, inSameDayAs: event.start)
            })

            if let insertIndex {
                chains[insertIndex].append(event)
            } else {
                chains.append([event])
            }
        }

        return chains.map { EventChain(events: $0) }
    }
}
