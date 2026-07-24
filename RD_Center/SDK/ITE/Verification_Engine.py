
import hashlib

def get_self_hash():
    with open(__file__, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

print(f"VERIFICATION_ENGINE_ONLINE | Self-Hash: {get_self_hash()}")
