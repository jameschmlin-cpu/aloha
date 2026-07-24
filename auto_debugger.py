# C:\Genesis\auto_debugger.py
import os
import sys
import ast
import hashlib
import psutil

class GenesisDebugger:
    def __init__(self, target_path: str):
        self.target_path = target_path

    def calculate_hash(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def ast_safety_check(self, file_path: str) -> bool:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                node = ast.parse(f.read(), filename=file_path)
            # 進行上下文感知風險審查
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name):
                    if subnode.func.id == "system":
                        raise ValueError("檢測到不安全的系統調用，請使用 psutil。")
            return True
        except Exception as e:
            print(f"[AST 錯誤攔截]: {e}")
            return False

    def monitor_processes(self):
        print("[psutil 監控中] 當前系統行程狀態：")
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            if 'docker' in proc.info['name'].lower() or 'python' in proc.info['name'].lower():
                print(f"PID: {proc.info['pid']} | 名稱: {proc.info['name']} | CPU%: {proc.info['cpu_percent']}")

if __name__ == "__main__":
    debugger = GenesisDebugger(r"C:\Genesis")
    debugger.monitor_processes()