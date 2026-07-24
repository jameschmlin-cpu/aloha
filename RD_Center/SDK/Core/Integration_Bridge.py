import requests
class SystemBridge:
    def link_ollama(self):
        try:
            r = requests.post('http://localhost:11434/api/generate', json={'model': 'llama3', 'prompt': 'test'}, timeout=5)
            return r.status_code == 200
        except: return False