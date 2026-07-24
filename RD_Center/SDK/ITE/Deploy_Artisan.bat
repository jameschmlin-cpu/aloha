@echo off
echo [狀態] 正在部署工匠模組...
:: 寫入 Python 檔案
(
echo import os
echo import shutil
echo.
echo class Artisan:
echo     def create_file(self, path, content^):
echo         if os.path.exists(path^): return "⚠️ 警告: 檔案存在"
echo         with open(path, 'w', encoding='utf-8'^) as f: f.write(content^)
echo         return "✅ 已建立: " + path
echo.
echo     def move_to_archive(self, path^):
echo         archive_dir = r"C:\ITE\Archive\Cold_Storage"
echo         if not os.path.exists(archive_dir^): os.makedirs(archive_dir^)
echo         dest = os.path.join(archive_dir, os.path.basename(path^) + ".archived"^)
echo         shutil.move(path, dest^)
echo         return "✅ 已封存至: " + dest
) > C:\ITE\Imperial_Artisan.py

echo [狀態] 工匠模組部署完成。
pause