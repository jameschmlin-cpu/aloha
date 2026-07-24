while($true) {
    $cmd = Get-Content 'C:\Genesis\Node_Command_Stream.pipe' -Tail 1
    if ($cmd -ne 'INIT_LINK_SUCCESS' -and $cmd -ne '') {
        Write-Host '==> 執行指令: ' -ForegroundColor Yellow -NoNewline
        Write-Host $cmd
        Invoke-Expression $cmd
        Set-Content -Path 'C:\Genesis\Node_Command_Stream.pipe' -Value ''
    }
    Start-Sleep -Milliseconds 500
}
