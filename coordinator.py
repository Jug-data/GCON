from agent import GCONAgent
from receipt import ReceiptManager
from verifier import ExecutionVerifier

class GCONCoordinator:
    """
    Coordinates GCON agents, job execution, and receipt management.
    """
    def __init__(self, network):
        self.network = network
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

        if job_id not in self.jobs:
            raise ValueError(f"Job '{job_id}' does not exist.")
        job =self.jobs[job_id]
        
        result = self.network.send_job(job["command"])

        job["status"] = "completed"
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