# Category: Core
import time
class OpenHarness:
    def execute_with_retry(self, task, retries=3):
        for i in range(retries):
            try:
                return task()
            except Exception:
                time.sleep(1)
        return False
