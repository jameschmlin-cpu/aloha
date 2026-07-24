# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template

import sqlite3




app = Flask(__name__, template_folder='templates')

DB_PATH = r"C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db"



@app.route('/')

def index():

    return render_template('dashboard.html')



@app.route('/api/data')

def get_data():

    try:

        conn = sqlite3.connect(DB_PATH)

        # 實體查詢資料庫最新的兩筆狀態，確保數據流動

        cursor = conn.execute("SELECT service_name, status FROM State_Table ORDER BY id DESC LIMIT 2")

        rows = cursor.fetchall()

        conn.close()

        

        # 轉換為前端可讀的數據格式

        return jsonify({

            "status": "Online",

            "case_count": 85,

            "node_count": 34,

            "logs": rows

        })

    except Exception as e:

        return jsonify({"status": "Error", "message": str(e)})



if __name__ == "__main__":

    app.run(port=5000, debug=True)