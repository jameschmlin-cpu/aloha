# C:\Genesis\Headquarter\RD\Automated_Skill_Harvester.py
import os
import ast
import yaml

def parse_python_file(file_path):
    """
    使用 AST 解析 Python 檔案中的類別與方法結構
    """
    source = None
    encodings = ["utf-8", "cp950", "gb18030", "latin-1"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                source = f.read()
            break
        except UnicodeDecodeError:
            continue

    if source is None:
        print(f"[Error] 無法以已知編碼讀取檔案 {file_path}")
        return []

    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"[Error] 無法解析檔案 {file_path}: {e}")
        return []

    harvested_skills = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_doc = ast.get_docstring(node) or "未提供類別描述。"
            
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    # 排除建構子與私有方法
                    if item.name.startswith("_"):
                        continue
                    
                    method_doc = ast.get_docstring(item) or "未提供方法描述。"
                    args = []
                    for arg in item.args.args:
                        if arg.arg == "self":
                            continue
                        # 獲取型態標註
                        arg_type = "Any"
                        if arg.annotation:
                            if isinstance(arg.annotation, ast.Name):
                                arg_type = arg.annotation.id
                            elif isinstance(arg.annotation, ast.Constant):
                                arg_type = str(arg.annotation.value)
                        args.append({
                            "name": arg.arg,
                            "type": arg_type
                        })
                    
                    methods.append({
                        "name": item.name,
                        "description": method_doc.strip(),
                        "parameters": args
                    })
            
            harvested_skills.append({
                "skill_name": class_name,
                "description": class_doc.strip(),
                "methods": methods
            })
            
    return harvested_skills

def harvest_skills():
    rd_dir = r"C:\Genesis\Headquarter\RD"
    registry_path = r"C:\Genesis\Headquarter\Skills_Registry.yaml"
    
    print("[System] 正在進行 AST 自主技能收割 (Skill Harvesting)...")
    
    new_skills = []
    # 遍歷 RD 目錄下的所有 Python 檔案
    for file_name in os.listdir(rd_dir):
        if file_name.endswith(".py") and file_name != "Automated_Skill_Harvester.py":
            file_path = os.path.join(rd_dir, file_name)
            skills = parse_python_file(file_path)
            for skill in skills:
                new_skills.append(skill)
                # 寫入單個 Skill 的 YAML 設定檔
                skill_yaml_path = os.path.join(rd_dir, f"Skill_{skill['skill_name']}.yaml")
                config = {
                    "skill_name": skill["skill_name"],
                    "class_name": skill["skill_name"],
                    "description": skill["description"],
                    "methods": skill["methods"],
                    "auto_mount": True,
                    "status": "READY"
                }
                with open(skill_yaml_path, "w", encoding="utf-8") as sf:
                    yaml.dump(config, sf, allow_unicode=True, sort_keys=False)
                print(f"[HARVESTED] 成功收割積木屬性：{skill['skill_name']} -> {os.path.basename(skill_yaml_path)}")

    if not new_skills:
        print("[System] 未偵測到新積木。")
        return

    # 註冊至 Skills_Registry.yaml
    try:
        if os.path.exists(registry_path):
            with open(registry_path, "r", encoding="utf-8") as rf:
                registry = yaml.safe_load(rf) or {}
        else:
            registry = {}
        
        if "RD_Node" not in registry or not isinstance(registry["RD_Node"], list):
            registry["RD_Node"] = []
            
        updated = False
        for skill in new_skills:
            if skill["skill_name"] not in registry["RD_Node"]:
                registry["RD_Node"].append(skill["skill_name"])
                updated = True
                print(f"[REGISTRY] 自動註冊新技能 {skill['skill_name']} 至 RD_Node")
                
        if updated:
            with open(registry_path, "w", encoding="utf-8") as wf:
                yaml.dump(registry, wf, allow_unicode=True, sort_keys=False)
            print("[System] Skills_Registry.yaml 更新成功。")
        else:
            print("[System] 技能註冊表已是最新狀態。")
            
    except Exception as e:
        print(f"[Error] 註冊至 Skills_Registry.yaml 失敗: {e}")

if __name__ == "__main__":
    harvest_skills()