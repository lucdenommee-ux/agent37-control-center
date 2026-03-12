class TaskRouter:

    def route(self, task):

        if task["type"] == "repo_create":
            return "github_manager"

        if task["type"] == "pipeline":
            return "pipeline_launcher"

        if task["type"] == "file_event":
            return "watcher"

        return "unknown"


