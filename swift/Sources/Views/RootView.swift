
import SwiftTUI

struct RootView: View {
    @ObservedObject var viewModel: RootViewModel

    var body: some View {
        if viewModel.chains.isEmpty {
            Text(viewModel.message)
            Button("Reload data") {
                viewModel.reloadData()
            }
            .bold()
            .background(.red)

        } else {
            VStack {
                zoneSelector
                chainList
            }
             .border(.rounded)
        }
    }

    var zoneSelector: some View {
        VStack(spacing: 1) {
            Text("Timezone:")
                .bold()
            HStack {
                ForEach(viewModel.timezones) { zone in
                    Button(
                        action: { },
                        hover: { viewModel.select(timezone: zone) }, 
                        label: { Text(zone.displayValue(alignmentWidth: 6)) }
                    )
                }
                Spacer()
            }
            .bold()
        }
        .border(.rounded)
    }

    var chainList: some View {
        HStack {
            ForEach(viewModel.chains) { chain in
                VStack {
                    ForEach(chain.events) { event in 
                        Text("\(event.displayValue)")
                    }
                    Spacer()
                }
                .border(.rounded)
            }
        }
    }
}

