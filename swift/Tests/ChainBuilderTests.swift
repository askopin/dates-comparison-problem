@testable import DatesDiffDemo
import Foundation
import Testing

struct ChainBuilderTests {
    @Test func processesEmptyList() throws {
        let response: EventsResponse = try EventsResponse.sample(filename: "empty")
        let sut = ChainBuilder()
        sut.calendar = Calendar(hoursFromGMT: 0)

        let chains = sut.process(response: response)

        #expect(chains.isEmpty)
    }

    @Test func processesListWithSingleEvent() throws {
        let response: EventsResponse = try EventsResponse.sample(filename: "single")
        let sut = ChainBuilder()
        sut.calendar = Calendar(hoursFromGMT: 0)

        let chains = sut.process(response: response)
        
        #expect(chains.count == 1)
        #expect(chains[0].events.count == 1)
    }

    @Test func isIndependentOfResponseOrder() throws {
        let missorted_response: EventsResponse = try EventsResponse.sample(filename: "missorted")
        let reference_response: EventsResponse = try EventsResponse.sample(filename: "multi")
        let sut = ChainBuilder()

        sut.calendar = Calendar(hoursFromGMT: 0)
        let missorted_chains = sut.process(response: missorted_response)
        let reference_chains = sut.process(response: reference_response)
        #expect(missorted_chains == reference_chains)
    }

    @Test func chainsShapeDependsOnTimezone() throws {
        let response: EventsResponse = try EventsResponse.sample(filename: "multi")
        let sut = ChainBuilder()

        sut.calendar = Calendar(hoursFromGMT: -4)
        var chains = sut.process(response: response)
        #expect(chains[0].events.map {$0.id} == [10, 1])

        
        sut.calendar = Calendar(hoursFromGMT: 0)
        chains = sut.process(response: response)
        #expect(chains[0].events.map {$0.id} == [10])
    }
}

