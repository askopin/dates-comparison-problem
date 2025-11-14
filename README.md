# Chaining dates problem

## Introduction

Couple of months ago I've been on an interview, and as a "homework" I was asked to solve a following problem:
There is a list of events scattered across the globe, each has its start and time. Required to build a chains of events so that in each chain next event starts on same date previous one ends, and display the result in a fancy way (which is out of scope of the article). Edge cases like overlapping events are also out of scope.

Sounds simple, but while discussing a solution we were struggle to have a common understanding of what doest it mean for two things to happen at one day in different places. I tried 

So, we have a list that looks like this (order is not guaranteed):
```
{
  "events": [
    {"id": 2, "start": "2026-01-01T18:00:00Z", "end": "2026-01-02T06:00:00Z" },
    {"id": 1, "start": "2025-12-31T18:00:00Z", "end": "2026-01-01T06:00:00Z" },
    {"id": 3, "start": "2026-01-05T14:00:00Z", "end": "2026-01-06T13:00:00Z" }
  ]
}
```
and as a result should have something that has a following structure
```
[
    [
        {"id": 1, "start": "2025-12-31T18:00:00Z", "end": "2026-01-01T06:00:00Z" },
        {"id": 2, "start": "2026-01-01T18:00:00Z", "end": "2026-01-02T06:00:00Z" },
    ],
    [
        {"id": 3, "start": "2026-01-05T14:00:00Z", "end": "2026-01-06T13:00:00Z" }
    ]
]
```

## Naive solution

The most obvious approach (and also the one suggested by the interviewers) is to just compare dates using calendar or compare strings produced using date formatter:

```
class ChainBuilder {
    
    func process(response: EventsResponse) -> [EventChain] {
        let calendar = Calendar.current
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
```

The huge issue of this solution (or any similar one) is that it uses current timezone of the user to calculate the result and as user travels across the world visiting our events grouping may change.
![gif](images/terminal_render.gif)

## Why it behaves so weird

Lets assume that we have two events: 
    - Event 1: `{start: 2025-12-31T18:00:00Z, end: 2026-01-01T06:00:00Z}`
    - Event 2: `{start: 2026-01-01T18:00:00Z, end: 2026-01-02T06:00:00Z}`

Then we have the following imaginary timeline, each tick corresponds to six hours:
![image](images/timeline.png)

In order to start counting days, we need to put the origin point on the line aka specify timezone. Lets assume that our user starts in UK
![image](images/same_day_case.png)

Then first event ends at 6AM Jan 1st and second one starts at 6PM same day.
But what if our user lives in the New Zealand?

![image](images/different_days_case.png)
Then first event ends at 6APM Dec 31st and second one starts at 6AM Jan 1st, so we should not chain them! 

And what if first event takes place in London but second one in Wellington? Should split the chain while customer changes flights somewhere in east Asia?

## Conclusion

As any poorly defined task it lacks good solution, as for me personally the least frustrating approach is to just chain events if time between them is within a certain threshold.  
But even calculating the difference could be not as straightforward.

**What was intentionally ignored here:**
- Daylight Saving Time
- leap days/hours/seconds
- time inconsistencies in distributed systems
- gravitation effects, extreme velocity and other consequences of living in a curved space-time 
- everything else from the list: https://zenodo.org/records/17070518

Kudos to Rens Breur for easy way to build terminal UI: https://github.com/rensbreur/SwiftTUI

 