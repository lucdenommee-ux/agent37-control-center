
import json
from pathlib import Path
from datetime import datetime

REGISTRY_FILE = Path("config/agent_registry.json")
RUNTIME_FILE = Path("state/runtime_state.json")


class BootstrapController:
    def __init__(self):
        self.registry_file = REGISTRY_FILE
        self.runtime_file = RUNTIME_FILE

    def _load_json(self, path: Path):
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, path: Path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_registry(self):
        return self._load_json(self.registry_file)

    def save_registry(self, data):
        self._save_json(self.registry_file, data)

    def load_runtime(self):
        return self._load_json(self.runtime_file)

    def save_runtime(self, data):
        self._save_json(self.runtime_file, data)

    def ensure_runtime_file(self):
        if not self.runtime_file.exists():
            self.save_runtime({
                "system_status": "ACTIVE",
                "last_bootstrap": None,
                "active_jobs": [],
                "failed_jobs": [],
                "last_registry_sync": None
            })

    def agent_exists(self, agent_id: str) -> bool:
        registry = self.load_registry()
        agents = registry.get("agents", [])
        return any(agent.get("agent_id") == agent_id for agent in agents)

    def get_agent(self, agent_id: str):
        registry = self.load_registry()
        agents = registry.get("agents", [])
        for agent in agents:
            if agent.get("agent_id") == agent_id:
                return agent
        return None

    def reserve_agent(self, agent_spec: dict):
        registry = self.load_registry()
        agents = registry.setdefault("agents", [])

        if self.agent_exists(agent_spec["agent_id"]):
            return {
                "success": False,
                "reason": "duplicate_agent_id",
                "agent_id": agent_spec["agent_id"]
            }

        agent_spec["creation_state"] = "RESERVED"
        agent_spec["created_at"] = datetime.utcnow().isoformat()
        agent_spec["updated_at"] = datetime.utcnow().isoformat()
        agents.append(agent_spec)
        self.save_registry(registry)

        return {
            "success": True,
            "reason": "reserved",
            "agent_id": agent_spec["agent_id"]
        }

    def update_agent_state(self, agent_id: str, state: str, status: str = None, last_error: str = None):
        registry = self.load_registry()
        agents = registry.get("agents", [])

        for agent in agents:
            if agent.get("agent_id") == agent_id:
                agent["creation_state"] = state
                agent["updated_at"] = datetime.utcnow().isoformat()
                if status:
                    agent["status"] = status
                if last_error is not None:
                    agent["last_error"] = last_error
                self.save_registry(registry)
                return True

        return False

    def log_runtime_event(self, job_type: str, payload: dict, success: bool = True, error: str = None):
        runtime = self.load_runtime()
        self.ensure_runtime_file()
        runtime = self.load_runtime()

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "job_type": job_type,
            "payload": payload,
            "success": success,
            "error": error
        }

        if success:
            runtime.setdefault("active_jobs", []).append(event)
        else:
            runtime.setdefault("failed_jobs", []).append(event)

        runtime["last_bootstrap"] = datetime.utcnow().isoformat()
        runtime["last_registry_sync"] = datetime.utcnow().isoformat()
        self.save_runtime(runtime)

    def build_bootstrap_packet(self, agent_id: str, agent_name: str, prompt: str, reporting_target: str, system_block: str):
        return {
            "message_type": "BOOTSTRAP_REQUEST",
            "timestamp": datetime.utcnow().isoformat(),
            "agent_spec": {
                "agent_id": agent_id,
                "agent_name": agent_name,
                "agent_role": agent_name,
                "parent_agent": reporting_target,
                "system_block": system_block,
                "status": "INITIALIZING",
                "reporting_target": reporting_target
            },
            "provisioning_spec": {
                "creation_mode": "NEW_CHAT",
                "chat_target": "LAB_6_RUNTIME",
                "prompt_payload": prompt,
                "timeout_seconds": 90
            }
        }

    def commit_success(self, agent_id: str):
        self.update_agent_state(agent_id, state="ACTIVE", status="ACTIVE", last_error=None)
        self.log_runtime_event("bootstrap_success", {"agent_id": agent_id}, success=True)

    def commit_failure(self, agent_id: str, error: str):
        self.update_agent_state(agent_id, state="FAILED", status="FAILED", last_error=error)
        self.log_runtime_event("bootstrap_failure", {"agent_id": agent_id}, success=False, error=error)


Envoyé de Yahoo Courriel pour iPhone




