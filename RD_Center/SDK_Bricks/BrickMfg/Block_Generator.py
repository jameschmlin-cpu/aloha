
import os
import hashlib

def create_block(block_id):
    content = f"BLOCK_DATA_{block_id}"
    sha256 = hashlib.sha256(content.encode()).hexdigest()
    
    file_path = os.path.join(r"C:\Genesis", f"block_{block_id}.txt")
    with open(file_path, "w") as f:
        f.write(f"Content: {content}\nHash: {sha256}")
    return file_path

if __name__ == "__main__":
    for i in range(1, 4):
        path = create_block(i)
        print(f"Created: {path}")

