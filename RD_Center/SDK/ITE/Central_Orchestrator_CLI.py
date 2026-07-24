import sqlite3


import subprocess



DB_PATH = r"C:\Genesis\Database\System_Core.db"



def run_cmd(cmd):

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    return result.stdout



def search_node(name):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT name, path, function_desc FROM file_registry WHERE name LIKE ?", ('%'+name+'%',))

    results = cursor.fetchall()

    conn.close()

    return results



if __name__ == "__main__":

    print("=== AI 中央調度器 (CLI 介面) ===")

    while True:

        query = input("\n請輸入要管理的程式關鍵字 (或輸入 exit 離開): ")

        if query.lower() == 'exit': break

        

        nodes = search_node(query)

        if nodes:

            for i, node in enumerate(nodes):

                print(f"[{i}] {node[0]} | 路徑: {node[1]} | 描述: {node[2]}")

            

            choice = input("\n選擇節點編號進行操作 (或按 Enter 跳過): ")

            if choice.isdigit():

                target = nodes[int(choice)]

                print(f"選定節點: {target[0]}")

                # 這裡準備掛載自動檢測器指令

                # 例如: run_cmd(f"python {target[1]} --check")

        else:

            print("查無此節點。")