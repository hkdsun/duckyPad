$hexPath = $args[0]
$hexWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($hexPath)
$outputPath = [System.IO.Path]::Combine([System.IO.Path]::GetDirectoryName($hexPath), $hexWithoutExt + ".dfu")
$dfuseExePath = Resolve-Path -Path ".\firmware\hex2dfu\hex2dfu.exe"

Write-Output "Executing $dfuseExePath with the following arguments:"
Write-Output "Input file: $hexPath"
Write-Output "Output file: $outputPath"

$process = Start-Process -PassThru -FilePath $dfuseExePath -ArgumentList "$hexPath $outputPath" -Wait
if($process.ExitCode -eq 1) {
    Write-Output "Conversion to DFU failed."
    exit 1
}

Write-Output "Conversion to DFU succeeded."
Write-Output "Uploading $outputPath to device."

Write-Output -NoNewLine 'Put device in DFU mode and press any key to continue...';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');

$dfuseCommandExe = "C:\Program Files (x86)\STMicroelectronics\Software\DfuSe v3.0.6\Bin\DfuSeCommand.exe"
$process = Start-Process -PassThru -FilePath $dfuseCommandExe -ArgumentList " -c -d --fn $outputPath" -Wait
if($process.ExitCode -eq 1) {
    Write-Output "Uploading to device failed."
    exit 1
}

Write-Output "All done."
exit 0
