# 設定路徑
$Source = "C:\Genesis"
$Destination = "D:\SystemBackUp\ITE_Mirror_Genesis"

# 建立鏡像同步 (若目標存在則覆寫，若不存在則建立)
# -MIR 參數強制鏡像：確保來源與目標完全一致，多餘檔案會被刪除
robocopy $Source $Destination /MIR /R:3 /W:5 /NP /TEE /LOG:C:\Genesis_Backup_Log.txt

# 輸出完成 Hash 檢查點
$Hash = (Get-ChildItem $Destination -Recurse | Get-FileHash -Algorithm SHA256 | Measure-Object).Count
Write-Host "鏡像備份完成。總計檔案數: $Hash"
Write-Host "日誌已生成於 C:\Genesis_Backup_Log.txt"