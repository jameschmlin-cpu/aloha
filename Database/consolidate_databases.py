# -*- coding: utf-8 -*-
import sqlite3
import os

def find_genesis_base():
    if "GENESIS_HOME" in os.environ:
        return os.environ["GENESIS_HOME"]
    current = os.path.abspath(__file__)
    while True:
        parent, name = os.path.split(current)
        if name.lower() == "genesis" or os.path.exists(os.path.join(current, "Genesis_Map.json")):
            return current
        if not name:
            break
        current = parent
    return r"C:\Genesis"

GENESIS_BASE = find_genesis_base()
master_db_path = os.path.join(GENESIS_BASE, "Database", "Genesis_DFMEA.db")
rules_db_path = os.path.join(GENESIS_BASE, "Genesis_Core", "Vault", "DFMEA_Rules.db")

print(f"Master Database: {master_db_path}")
print(f"Rules Database: {rules_db_path}")

# Connect to master
conn_master = sqlite3.connect(master_db_path)
cur_master = conn_master.cursor()

# Ensure Rules table exists in master
cur_master.execute("""
    CREATE TABLE IF NOT EXISTS Rules (
        error_code TEXT PRIMARY KEY,
        solution TEXT
    )
""")

# Ensure dfmea_matrix exists with unified columns
cur_master.execute("""
    CREATE TABLE IF NOT EXISTS dfmea_matrix (
        id TEXT PRIMARY KEY,
        problem_point TEXT,
        failure_mode TEXT,
        severity INTEGER,
        occurrence INTEGER DEFAULT 1,
        detection INTEGER DEFAULT 1,
        root_cause TEXT,
        prevention TEXT,
        corrective TEXT,
        version_index INTEGER DEFAULT 1,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Add occurrence/detection columns if table already existed without them
try:
    cur_master.execute("ALTER TABLE dfmea_matrix ADD COLUMN occurrence INTEGER DEFAULT 1")
    print("Added occurrence column to dfmea_matrix")
except Exception:
    pass

try:
    cur_master.execute("ALTER TABLE dfmea_matrix ADD COLUMN detection INTEGER DEFAULT 1")
    print("Added detection column to dfmea_matrix")
except Exception:
    pass

# Ensure Failure_Mode_Library exists
cur_master.execute("""
    CREATE TABLE IF NOT EXISTS Failure_Mode_Library (
        err_id TEXT PRIMARY KEY,
        mode TEXT,
        root_cause TEXT,
        prevention TEXT
    )
""")

# Copy data from rules_db if it exists
if os.path.exists(rules_db_path):
    print("Reading data from rules database...")
    conn_rules = sqlite3.connect(rules_db_path)
    cur_rules = conn_rules.cursor()
    
    # Copy Rules
    try:
        cur_rules.execute("SELECT error_code, solution FROM Rules")
        for row in cur_rules.fetchall():
            cur_master.execute("INSERT OR REPLACE INTO Rules (error_code, solution) VALUES (?, ?)", row)
        print("Rules copied.")
    except Exception as e:
        print(f"Error copying Rules: {e}")
        
    # Copy Failure_Mode_Library
    try:
        cur_rules.execute("SELECT err_id, mode, root_cause, prevention FROM Failure_Mode_Library")
        for row in cur_rules.fetchall():
            cur_master.execute("INSERT OR REPLACE INTO Failure_Mode_Library (err_id, mode, root_cause, prevention) VALUES (?, ?, ?, ?)", row)
        print("Failure_Mode_Library copied.")
    except Exception as e:
        print(f"Error copying Failure_Mode_Library: {e}")
        
    # Copy dfmea_matrix
    try:
        cur_rules.execute("SELECT id, failure, mode, severity, root_cause, prevention, corrective FROM dfmea_matrix")
        for row in cur_rules.fetchall():
            # map failure -> problem_point, mode -> failure_mode
            cur_master.execute("""
                INSERT OR REPLACE INTO dfmea_matrix 
                (id, problem_point, failure_mode, severity, root_cause, prevention, corrective) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, row)
        print("dfmea_matrix copied.")
    except Exception as e:
        print(f"Error copying dfmea_matrix: {e}")
        
    conn_rules.close()

conn_master.commit()
conn_master.close()
print("Database consolidation completed successfully!")
