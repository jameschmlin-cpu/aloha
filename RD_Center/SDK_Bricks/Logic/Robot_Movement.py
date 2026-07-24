# -*- coding: utf-8 -*-
# Compiled Brick: Robot_Movement.py
# Category: Logic (Motion Control)

import time
import sys
import os

GENESIS_BASE = r"C:\Genesis"
LOG_FILE = os.path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log")

def write_log(level, msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{level}] [{timestamp}] [Robot_Movement] {msg}\n"
    print(log_line.strip())
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass

class RobotMovementBrick:
    def run(self):
        write_log("INFO", "Initializing multi-axis industrial robot arm trajectory planner...")
        time.sleep(0.5)

        # 6-Axis Target Joint Angles (degrees)
        target_joints = [45.0, -30.0, 90.0, 0.0, 45.0, 180.0]
        current_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        max_speed_deg_sec = 60.0
        time_step = 0.2

        write_log("INFO", f"Target Coordinates: Joint1={target_joints[0]}°, Joint2={target_joints[1]}°, Joint3={target_joints[2]}°")
        
        # Simulating Trajectory Interpolation
        steps = 5
        for s in range(1, steps + 1):
            fraction = s / steps
            for i in range(6):
                current_joints[i] = round(target_joints[i] * fraction, 2)
            
            # Safety Checks
            # Joint 3 angle must not exceed mechanical safety limits (e.g. 110 degrees)
            if abs(current_joints[2]) > 100.0:
                write_log("WARNING", f"Safety Margin Warning: Joint 3 angle ({current_joints[2]}°) is close to hardware limit (110.0°)")
            
            # Check for ground crash collision (simulation: joint2 + joint3 must remain positive)
            kinematic_height = current_joints[1] + current_joints[2]
            if kinematic_height < -45.0:
                write_log("CRITICAL", f"Motion Halted: Collision Envelope Violated (Kinematic Height: {kinematic_height})")
                return False

            write_log("INFO", f"Step {s}/{steps}: Moving Joint Positions: {current_joints}")
            time.sleep(0.3)

        write_log("SUCCESS", "Trajectory execution completed. Mechanical brakes engaged. Robot arm locked in Target Position.")
        return True

if __name__ == "__main__":
    brick = RobotMovementBrick()
    success = brick.run()
    sys.exit(0 if success else 1)
