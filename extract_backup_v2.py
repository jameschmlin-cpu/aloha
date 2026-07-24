import sqlite3
import os

def final_recovery():
    db_path = r"C:\Genesis\Database\Unified_Empire_Memory.db"
    backup_id = "SYSTEM_BACKUP_20260714"
    output_path = r"C:\Genesis\restored_backup.txt"
    
    # 確保輸出目錄存在
    if not os.path.exists(r"C:\Genesis"):
        os.makedirs(r"C:\Genesis")
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 精準鎖定查詢
        cursor.execute("SELECT content FROM backups WHERE id = ?", (backup_id,))
        row = cursor.fetchone()
        
        if row:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(row[0])
            print(f"[SUCCESS] 備份 {backup_id} 已成功還原至 {output_path}")
        else:
            print(f"[ERROR] 路徑正確，但資料庫中找不到 ID: {backup_id}")
            
        conn.close()
    except Exception as e:
        print(f"[FATAL] 讀取失敗: {e}")

if __name__ == "__main__":
    final_recovery()