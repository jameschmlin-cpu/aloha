import importlib.util

def mount_skill(skill_name, agent_instance):
    """
    動態將圖書館內的邏輯掛載到 Agent 身上
    """
    path = rf"C:\Genesis\.agents\library\skill_{skill_name}.py"
    spec = importlib.util.spec_from_file_location(skill_name, path)
    skill_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(skill_module)
    
    # 將技能邏輯綁定到 Agent 物件上
    setattr(agent_instance, skill_name, skill_module.execute)
    print(f"[System] 已將 {skill_name} 掛載至 {agent_instance.name}")

def emit_event(event_name, data):
    print(f'[Bus] 發送事件: {event_name} | 數據: {data}')