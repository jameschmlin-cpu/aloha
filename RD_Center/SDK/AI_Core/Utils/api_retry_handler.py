import time
import random
from google.api_core import exceptions

def call_gemini_api_with_backoff(api_func, *args, **kwargs):
    max_retries = 5
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            # 執行 SDK 呼叫
            return api_func(*args, **kwargs)
        except exceptions.ResourceExhausted:
            # 若觸發 429 限制，進行指數退避
            delay = (base_delay * (2 ** attempt)) + (random.uniform(0, 1))
            print(f"偵測到流量限制，進入退避模式：等待 {delay:.2f} 秒後重試...")
            time.sleep(delay)
        except Exception as e:
            # 非流量限制的錯誤，直接拋出
            raise e
            
    raise Exception("已達最大重試次數，請檢查 Node C 節點狀態。")