# Remove directories if they exist
$paths = @(
    "build/app/windows"
)

foreach ($path in $paths) {
    if (Test-Path -Path $path) {
        Remove-Item -Path $path -Recurse -Force
    }
}

# Execute the Briefcase commands
briefcase create
briefcase build
briefcase package --adhoc-sign
briefcase run
