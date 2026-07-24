$code = @"

# -*- coding: utf-8 -*-

import os

import shutil



class Artisan:

    def create_file(self, path, content):

        if os.path.exists(path): return "警告: 檔案已存在"

        with open(path, 'w', encoding='utf-8') as f:

            f.write(content)

        return "✅ 已建立: " + path



    def move_to_archive(self, path):

        archive_dir = r"C:\Genesis\Archive\Cold_Storage"

        if not os.path.exists(archive_dir): os.makedirs(archive_dir)

        dest = os.path.join(archive_dir, os.path.basename(path) + ".archived")

        shutil.move(path, dest)

        return "✅ 已封存至: " + dest

"@

$code | Out-File -FilePath C:\Genesis\Imperial_Artisan.py -Encoding utf8