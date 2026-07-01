import time
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
        self.nodes = {}
        
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

    # Mark node and job as busy/running
        node.status = "busy"
        job["status"] = "running"
        job["agent"] = node.node_id

    # Execute the job
        response = self.communication.send_job(
            node.node_id,
            job_id,
            job["command"]
    )

        result = response["result"]

    # Mark node idle again
        node.status = "idle"

    # Immediately update the coordinator with the new status
        heartbeat = node.heartbeat()
        self.receive_heartbeat(heartbeat)

    # Job completed successfully
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
    
    def check_cluster_health(self):
        """
        Check node health and recover jobs from failed nodes.
        """
        offline_nodes = self.registry.check_node_health()

        for node_id in offline_nodes:
            print(f"Node '{node_id}' marked OFFLINE")
            self.recover_jobs(node_id)
    
    def recover_jobs(self, node_id):
        """
        Recover unfinished jobs assigned to a failed node.
        """

        print(f"Recovering jobs from '{node_id}'...")

        for job_id, job in self.jobs.items():

            if job["agent"] == node_id and job["status"] != "running":

                print(f"Recovering job '{job_id}'")

            # Reset the job
                job["status"] = "pending"
                job["agent"] = None

                
            # Reassign the job
                try:
                    self.assign_job(job_id)
                    print(f"Job '{job_id}' reassigned successfully.")
                except RuntimeError as e:
                     print(f"Recovery failed for '{job_id}': {e}")
    
    
    def receive_heartbeat(self, heartbeat):
        """
        Process a heartbeat received from a node.
        """
        node_id = heartbeat["node_id"]
        status = heartbeat["status"]

        self.registry.heartbeat(
            heartbeat["node_id"],
            heartbeat["status"],
            heartbeat["timestamp"]
        )

        print(f"Heartbeat received from {node_id} ({status})")
    