import sqlite3

def recovery_via_repair_node():
    db_path = r"C:\Genesis\Database\Unified_Empire_Memory.db"
    # 使用系統修復標籤進行提取
    target_id = "REPAIR_CHECK"
    output_path = r"C:\Genesis\recovered_data_via_repair.txt"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 直接提取 REPAIR_CHECK 的 payload
        cursor.execute("SELECT payload FROM data WHERE union_id = ?", (target_id,))
        row = cursor.fetchone()
        
        if row:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(row[0])
            print(f"[SUCCESS] 數據已從 REPAIR_CHECK 節點還原至 {output_path}")
            # 強制列印前 100 字元以便進行快速校驗
            print(f"[PREVIEW]: {row[0][:100]}")
        else:
            print("[CRITICAL] REPAIR_CHECK 節點內無數據，請確認是否已發生物理崩潰。")
            
        conn.close()
    except Exception as e:
        print(f"[FATAL] 讀取失敗: {e}")

if __name__ == "__main__":
    recovery_via_repair_node()