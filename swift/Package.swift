// swift-tools-version: 6.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "dates_diff_demo",
    platforms: [
        .macOS(.v14)
    ],
    dependencies: [
      .package(url: "https://github.com/rensbreur/SwiftTUI", branch: "main"),
    ],
    targets: [
        .executableTarget(
            name: "DatesDiffDemo", dependencies: [.product(name: "SwiftTUI", package: "SwiftTUI")]
        ),
        .testTarget(
            name: "DatesDiffDemoTests",
            dependencies: ["DatesDiffDemo"],
            path: "Tests",
            resources: [
                .copy("SampleData")
            ]
        ),

    ]
)
