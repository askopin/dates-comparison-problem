import Foundation

class RootViewModel: ObservableObject {
    let dataSourceURL: URL
    var response: EventsResponse?
    let chainBuilder: NaiveChainBuilder
    let timezones: [UserTimeZone] 
    var currentTimezone: UserTimeZone

    @Published private(set) var chains: [EventChain] = []
    @Published private(set) var message: String = "No data"

    init(dataSourceURL: URL, chainBuilder: NaiveChainBuilder = NaiveChainBuilder()) {
        self.dataSourceURL = dataSourceURL
        self.chainBuilder = chainBuilder
        let timezones = Array(-12...12).map { UserTimeZone(rawValue: $0) }
        currentTimezone = timezones[0]
        self.timezones = timezones

        reloadData()
    }

    func reloadData() {
        guard let data = try? Data(contentsOf: dataSourceURL) else {
            message = "File not exists: \(dataSourceURL.absoluteString)"
            return
        }

        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        response = try? decoder.decode(EventsResponse.self, from: data)

        if response == nil {
            message = "Unable to decode data"
            return
        }

        select(timezone: currentTimezone)
    }

    func select(timezone: UserTimeZone) {
        guard let response else {
            return
        }

        var calendar = Calendar(identifier: .gregorian)
        calendar.timeZone = TimeZone(secondsFromGMT: -60 * 60 * timezone.rawValue) ?? .current
        chainBuilder.calendar = calendar
        currentTimezone = timezone
        self.chains = chainBuilder.process(response: response)
        
        if chains.count == 0 {
            message = "No data"
        }
    }
}

extension Event {
    static let dateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.timeZone = TimeZone(secondsFromGMT: 0)
        formatter.dateFormat = "dd.MM HH:mm"
        return formatter
    }()

    var displayValue: String {
        "\(Self.dateFormatter.string(from: start)) - \(Self.dateFormatter.string(from: end))"
    }
}

struct UserTimeZone: Identifiable {
    let rawValue: Int
    var id: Int { self.rawValue }

    func displayValue(alignmentWidth: Int) -> String {
        let strValue = String(rawValue)
        let spaceCount = (alignmentWidth - strValue.count) / 2
        let spacer = String(repeating: Character(" "), count: spaceCount)
        return "\(spacer)\(strValue)\(spacer)"
    }
}