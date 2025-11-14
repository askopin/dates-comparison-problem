@testable import DatesDiffDemo
import Foundation
import Testing

struct IntervalBasedChainBuilderTests {
     @Test func processesEmptyList() throws {
        let response: EventsResponse = try EventsResponse.sample(filename: "empty")
        let sut = IntervalBasedChainBuilder()

        let chains = sut.process(response: response)

        #expect(chains.isEmpty)
    }

    @Test func processesListWithSingleEvent() throws {
        let response: EventsResponse = try EventsResponse.sample(filename: "single")
        let sut = IntervalBasedChainBuilder()

        let chains = sut.process(response: response)
        
        #expect(chains.count == 1)
        #expect(chains[0].events.count == 1)
    }

    @Test func isIndependentOfResponseOrder() throws {
        let missorted_response: EventsResponse = try EventsResponse.sample(filename: "missorted")
        let reference_response: EventsResponse = try EventsResponse.sample(filename: "multi")
        let sut = IntervalBasedChainBuilder()

        let missorted_chains = sut.process(response: missorted_response)
        let reference_chains = sut.process(response: reference_response)
        #expect(missorted_chains == reference_chains)
    }

    @Test func notChainsIntersectingEvents() throws {
        let response: EventsResponse = try EventsResponse.sample(filename: "intersecting")
        let sut = IntervalBasedChainBuilder()

        let chains = sut.process(response: response)

        #expect(chains.count == 3)
    }

    @Test func chainsEventsWithExactMatch() throws {
        let response: EventsResponse = try EventsResponse.sample(filename: "exact_match")
        let sut = IntervalBasedChainBuilder()

        let chains = sut.process(response: response)

        #expect(chains.count == 1)
    }
}