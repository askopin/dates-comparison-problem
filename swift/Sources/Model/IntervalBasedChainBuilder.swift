import Foundation

struct IntervalBasedChainBuilder {
    let minChainInterval: TimeInterval
    let maxChainInterval: TimeInterval

    init (
        minChainInterval: TimeInterval = 0,
        maxChainInterval: TimeInterval = 24 * 60 * 60
    ){
        self.minChainInterval = minChainInterval
        self.maxChainInterval = maxChainInterval
    }

    func process(response: EventsResponse) -> [EventChain] {
        let events = response.events.sorted { $0.start < $1.start }

        let chains: [[Event]] = events.reduce(into: []) { chains, event in
            let insertIndex = chains.firstIndex(where: { chain in
                guard let lastEvent = chain.last else {
                    assertionFailure("empty chains should never exist")
                    return false
                }

                let dateDiff = lastEvent.end.distance(to: event.start)
                return dateDiff >= minChainInterval && dateDiff < maxChainInterval
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
