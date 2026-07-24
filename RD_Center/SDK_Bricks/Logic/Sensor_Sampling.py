# -*- coding: utf-8 -*-
# Compiled Brick: Sensor_Sampling.py
# Category: Logic (Telemetry & Diagnostics)

import time
import sys
import os
import random
import sqlite3

GENESIS_BASE = r"C:\Genesis"
LOG_FILE = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")
DB_FILE = os.path.join(GENESIS_BASE, "Database", "Sensor_Data.db")

def write_log(level, msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{level}] [{timestamp}] [Sensor_Sampling] {msg}\n"
    print(log_line.strip())
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass

class SensorSamplingBrick:
    def run(self):
        write_log("INFO", "Initializing digital sensor input channel...")
        
        # Ensure database and table exist
        try:
            os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
            conn = sqlite3.connect(DB_FILE, timeout=5.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sensor_readings (
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    sensor_id TEXT,
                    vibration REAL,
                    voltage REAL,
                    temperature REAL
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            write_log("ERROR", f"Failed to initialize database: {e}")
            return False

        # Run 5 sampling cycles
        sensor_id = "SEN_MAIN_VALVE_01"
        for cycle in range(1, 6):
            vibration = round(random.uniform(10.0, 50.0), 2)
            voltage = round(random.uniform(215.0, 245.0), 1)
            temperature = round(random.uniform(45.0, 85.0), 1)

            write_log("INFO", f"Sample #{cycle}: Vibration={vibration}Hz, Voltage={voltage}V, Temperature={temperature}°C")

            # Check threshold bounds
            if temperature > 80.0:
                write_log("WARNING", f"High thermal threshold exceeded: {temperature}°C (Limit: 80.0°C)")
            if voltage > 240.0:
                write_log("WARNING", f"Overvoltage spike detected: {voltage}V (Limit: 240.0V)")

            # Save to SQLite database
            try:
                conn = sqlite3.connect(DB_FILE, timeout=5.0)
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute(
                    "INSERT INTO sensor_readings (sensor_id, vibration, voltage, temperature) VALUES (?, ?, ?, ?)",
                    (sensor_id, vibration, voltage, temperature)
                )
                conn.commit()
                conn.close()
            except Exception as ex:
                write_log("ERROR", f"Failed to commit metrics to database: {ex}")

            time.sleep(0.3)

        write_log("SUCCESS", "Sensor scan transaction sequence finished. Data synced to Database.")
        return True

if __name__ == "__main__":
    brick = SensorSamplingBrick()
    success = brick.run()
    sys.exit(0 if success else 1)
