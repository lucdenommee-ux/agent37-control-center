from core.registry_manager import RegistryManager
from core.pipeline_launcher import PipelineLauncher
from integrations.github_manager import GitHubManager

class Agent37:

    def __init__(self):

        self.registry = RegistryManager()
        self.pipeline = PipelineLauncher()
        self.github = GitHubManager()

    def create_repo(self, name):

        self.github.create_repo(name)

    def run_pipeline(self, script):

        self.pipeline.run_pipeline(script)

    def start(self):

        print("Agent 37 Control Center running")


if __name__ == "__main__":

    agent = Agent37()
    agent.start()

