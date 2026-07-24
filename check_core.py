import os
import json

target_files = [
    r"C:\Genesis\SDK\nodes\node_a.py",
    r"C:\Genesis\SDK\nodes\node_b.py",
    r"C:\Genesis\SDK\nodes\node_c.py",
    r"C:\Genesis\SDK\nodes\node_d.py",
    r"C:\Genesis\SDK\sandbox\executor.py"
]

report = {}
for path in target_files:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                report[path] = {
                    "line_count": len(content.splitlines()),
                    "has_logic": "def " in content or "class " in content,
                    "preview": content[:150]
                }
        except Exception as e:
            report[path] = {"error": str(e)}
    else:
        report[path] = {"error": "File not found"}

print(json.dumps(report, indent=4))