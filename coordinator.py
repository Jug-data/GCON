from agent import GCONAgent
from receipt import ReceiptManager
from verifier import ExecutionVerifier
from Noderegistry import NodeRegistry
from scheduler import Scheduler


class GCONCoordinator:
    """
    Coordinates GCON agents, job execution, and receipt management.
    """
    def __init__(self, network=None):
        self.network = network
        self.registry = NodeRegistry()
        self.scheduler = Scheduler(self.registry)
        self.agents = {}
        self.jobs = {}
        self.receipts = {}
        print("GCON Coordinator initialized.")
        
    def register_agent(self, agent):
        """
        Register a GCON agent with the coordinator.
        """
        if not isinstance(agent, GCONAgent):
           raise TypeError("Expected a GCONAgent instance.")
        self.agents[agent.job_id] = agent
        self.registry.register(agent)

        print(f"Agent '{agent.job_id}' registered successfully.")
    
    def submit_job(self, job_id, command):
        """
        Submit a new job to the coordinator.
        """

        if job_id in self.jobs:
            raise ValueError(f"Job '{job_id}' already exists.")

        self.jobs[job_id] = {
            "command": command,
            "status": "pending",
            "agent": None
    }

        print(f"Job '{job_id}' submitted successfully.")
    
    def assign_job(self, job_id):
        """
        Assign a job to an available node and execute it.
        """

        if job_id not in self.jobs:
            raise ValueError(f"Job '{job_id}' does not exist.")

        job = self.jobs[job_id]

        node = self.scheduler.select_node()

        if node is None:
            raise RuntimeError("No available nodes to execute the job.")

        node.status = "busy"

        result = node.execute_job(job["command"])
        node.status = "idle"

        job["status"] = "completed"
        job["agent"] = node.node_id 
        job["result"] = result

        return result
    
    def receive_receipt(self, job_id, receipt):
        """
        Store a receipt for a completed job.
        """

        if job_id not in self.jobs:
            raise ValueError(f"Job '{job_id}' does not exist.")

        self.receipts[job_id] = receipt

        print(f"Receipt received for job '{job_id}'.")
        
    def get_job_status(self, job_id):
        """
        Get the current status of a job.
        """

        if job_id not in self.jobs:
            raise ValueError(f"Job '{job_id}' does not exist.")

        return self.jobs[job_id]
    
    
    def receive_heartbeat(self, heartbeat):
        """
        Process a heartbeat received from a node.
        """

        node_id = heartbeat["node_id"]
        status = heartbeat["status"]

        self.registry.heartbeat(node_id, status)

        print(f"Heartbeat received from '{node_id}' ({status})")
    