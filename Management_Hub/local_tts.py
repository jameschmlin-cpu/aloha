# -*- coding: utf-8 -*-
# 檔案：C:\Genesis\Management_Hub\local_tts.py
# 狀態：本機 SAPI5 語音合成腳本 (100% 離線運作)

import sys
import win32com.client

def main():
    if len(sys.argv) < 3:
        print("Usage: python local_tts.py <text> <output_path>")
        sys.exit(1)
        
    text = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        # 建立 SAPI5 語音合成引擎
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        
        # 尋找內建的台灣繁體中文語音 (Hanhan 或 Yating)
        voices = speaker.GetVoices()
        for i in range(voices.Count):
            voice = voices.Item(i)
            desc = voice.GetDescription().lower()
            if "chinese" in desc or "hanhan" in desc or "yating" in desc or "繁體" in desc:
                speaker.Voice = voice
                break
                
        # 寫入 Wave 音訊檔
        filestream = win32com.client.Dispatch("SAPI.SpFileStream")
        filestream.Open(output_path, 3, False)  # 3 = SSFMCreateForWrite
        speaker.AudioOutputStream = filestream
        speaker.Speak(text)
        filestream.Close()
        print("SUCCESS")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
