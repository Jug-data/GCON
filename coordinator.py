from agent import GCONAgent
from receipt import ReceiptManager
from verifier import ExecutionVerifier
from Noderegistry import NodeRegistry
from scheduler import Scheduler
from communication import CommunicationManager

class GCONCoordinator:
    """
    Coordinates GCON agents, job execution, and receipt management.
    """
    def __init__(self, network=None):
        self.network = network
        self.registry = NodeRegistry()
        self.scheduler = Scheduler(self.registry)
        self.communication = CommunicationManager()
        self.agents = {}
        self.jobs = {}
        self.receipts = {}
        
        print("GCON Coordinator initialized.")
        
    def register_agent(self, node):
        """
        Register a GCON agent with the coordinator.
        """
        self.registry.register(node)
        self.communication.register_node(node)

        print(f"Node '{node.node_id}' registered successfully.")
    
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

        response = self.communication.send_job(
        node.node_id,
        job["command"]
)
        result = response["result"]
        
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
    