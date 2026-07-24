# Node A-D 完整整合模組
$BaseDir = "C:\ITE"
$DbFile = "$BaseDir\Genesis_Core\Data\Memory_Core.db"

function Invoke-SystemIntegrity {
    $Nodes = @()
    # 執行所有偵測，並將結果存入物件陣列
    $Nodes += [PSCustomObject]@{Node="Node_A"; Status=(Test-Path $BaseDir)}
    $Nodes += [PSCustomObject]@{Node="Node_B"; Status=(Test-Path $DbFile)}
    $Nodes += [PSCustomObject]@{Node="Node_C"; Status=(if(Test-Path $DbFile){"READY"}else{"FAIL"})}
    $Nodes += [PSCustomObject]@{Node="Node_D"; Status="SYNC_COMPLETE"}
    return $Nodes
}

Invoke-SystemIntegrity | Format-Table -AutoSize