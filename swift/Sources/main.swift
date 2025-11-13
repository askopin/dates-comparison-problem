
import Foundation
import SwiftTUI

guard  CommandLine.arguments.count > 1 else {
    print("Input not specified")
    exit(1)
}

let fileName: String = CommandLine.arguments[1]
let fileUrl = URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appending(path: fileName, directoryHint: .notDirectory)

Application(rootView: RootView(viewModel: RootViewModel(dataSourceURL: fileUrl, chainBuilder: ChainBuilder()))).start()
