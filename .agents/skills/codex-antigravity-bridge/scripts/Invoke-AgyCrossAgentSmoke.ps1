[CmdletBinding()]
param(
    [string]$Workspace = (Get-Location).Path,
    [string]$AgyPath,
    [string]$Marker = 'CROSS-AGENT-AGY-SMOKE',
    [ValidateRange(10, 600)]
    [int]$TimeoutSeconds = 90,
    [switch]$TestReadFile,
    [string]$TestRelativeFilePath = '.agents/skills/README.md'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$workspacePath = [System.IO.Path]::GetFullPath($Workspace)
if (-not (Test-Path -LiteralPath $workspacePath -PathType Container)) {
    throw "Workspace does not exist: $workspacePath"
}

if ([string]::IsNullOrWhiteSpace($AgyPath)) {
    $agyCommand = Get-Command agy -ErrorAction SilentlyContinue
    if ($null -ne $agyCommand) {
        $AgyPath = $agyCommand.Source
    } else {
        $AgyPath = Join-Path $env:LOCALAPPDATA 'agy\bin\agy.exe'
    }
}
if (-not (Test-Path -LiteralPath $AgyPath -PathType Leaf)) {
    throw "agy executable not found: $AgyPath"
}

$prompt = if ($TestReadFile) {
    $targetFile = [System.IO.Path]::Combine($workspacePath, $TestRelativeFilePath)
    "CROSS_AGENT_READFILE_TEST marker=$Marker. Read the first 5 lines of '$targetFile'. Reply with exactly: AGY_READFILE_OK:$Marker"
} else {
    "CROSS_AGENT_SMOKE_TEST marker=$Marker. Do not use tools. Reply with exactly: AGY_HANDSHAKE_OK:$Marker"
}

$startInfo = [System.Diagnostics.ProcessStartInfo]::new()
$startInfo.FileName = $AgyPath
$startInfo.WorkingDirectory = $workspacePath
$startInfo.UseShellExecute = $false
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$startInfo.CreateNoWindow = $true

$arguments = @('--add-dir', $workspacePath, '--print', '--sandbox', '--print-timeout', "${TimeoutSeconds}s", '-p', $prompt)
if ($startInfo.PSObject.Properties.Name -contains 'ArgumentList') {
    foreach ($argument in $arguments) { [void]$startInfo.ArgumentList.Add($argument) }
} else {
    $startInfo.Arguments = ($arguments | ForEach-Object {
        if ($_ -match '[\s"]') { '"{0}"' -f ($_ -replace '"', '\"') } else { $_ }
    }) -join ' '
}

$process = [System.Diagnostics.Process]::new()
$process.StartInfo = $startInfo

$stdoutBuilder = [System.Text.StringBuilder]::new()
$stderrBuilder = [System.Text.StringBuilder]::new()

$process.OutputDataReceived += [System.Diagnostics.DataReceivedEventHandler]{
    param($sender, $eventArgs)
    if ($null -ne $eventArgs.Data) { [void]$stdoutBuilder.AppendLine($eventArgs.Data) }
}
$process.ErrorDataReceived += [System.Diagnostics.DataReceivedEventHandler]{
    param($sender, $eventArgs)
    if ($null -ne $eventArgs.Data) { [void]$stderrBuilder.AppendLine($eventArgs.Data) }
}

[void]$process.Start()
$process.BeginOutputReadLine()
$process.BeginErrorReadLine()

$processCompleted = $process.WaitForExit($TimeoutSeconds * 1000)
if (-not $processCompleted) {
    try { $process.Kill() } catch {}
    throw "agy smoke test timed out after $TimeoutSeconds seconds."
}

$exitCode = $process.ExitCode
$stdoutText = $stdoutBuilder.ToString()
$stderrText = $stderrBuilder.ToString()

$expectedToken = if ($TestReadFile) { "AGY_READFILE_OK:$Marker" } else { "AGY_HANDSHAKE_OK:$Marker" }
$passed = ($exitCode -eq 0) -and ($stdoutText.Contains($expectedToken))

$result = [ordered]@{
    testType = if ($TestReadFile) { 'read_file' } else { 'handshake' }
    passed = $passed
    exitCode = $exitCode
    expectedToken = $expectedToken
    receivedExpectedToken = $stdoutText.Contains($expectedToken)
    rawStdout = $stdoutText.Trim()
    rawStderr = $stderrText.Trim()
}

$result | ConvertTo-Json -Depth 4
if (-not $passed) { exit 1 } else { exit 0 }
