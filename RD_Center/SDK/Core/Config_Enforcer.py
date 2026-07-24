import os

CONFIG = {'DB': r'C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db'}

def enforce_paths():

    if not os.path.exists(os.path.dirname(CONFIG['DB'])): os.makedirs(os.path.dirname(CONFIG['DB']))

    with open(CONFIG['DB'], 'a'): pass