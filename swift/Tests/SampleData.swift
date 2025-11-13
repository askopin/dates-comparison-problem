@testable import DatesDiffDemo
import Foundation
import Testing

extension EventsResponse {
    static func sample(filename: String) throws -> EventsResponse {
        let dataUrl = try #require(Bundle.module.url(forResource: filename, withExtension: "json", subdirectory: "SampleData"))
        let sampleData = try Data(contentsOf: dataUrl)
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return try decoder.decode(EventsResponse.self, from: sampleData)
    }
}

extension Calendar {
    init(hoursFromGMT: Int) {
        var calendar = Calendar(identifier: .gregorian)
        calendar.timeZone = TimeZone(secondsFromGMT: 60 * 60 * hoursFromGMT)!
        self = calendar
    }
}
