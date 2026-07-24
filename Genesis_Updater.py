import git
import os

def self_update():
    repo_url = "https://github.com/YourRepo/Genesis-Core.git"
    repo_dir = r"C:\Genesis\Core_Repo"
    
    if not os.path.exists(repo_dir):
        git.Repo.clone_from(repo_url, repo_dir)
    else:
        repo = git.Repo(repo_dir)
        repo.remotes.origin.pull()
    print("核心邏輯與決策表已更新完畢。")

if __name__ == "__main__":
    self_update()