import subprocess

class GitHubManager:

    def create_repo(self, name):
        print(f"Creating repo: {name}")
        subprocess.run(["gh", "repo", "create", name, "--public"])

    def clone_repo(self, repo_url):
        subprocess.run(["git", "clone", repo_url])

    def push_changes(self, message="auto commit"):
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", message])
        subprocess.run(["git", "push"])


