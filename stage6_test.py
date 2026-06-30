from network import GCONNetwork
from coordinator import GCONCoordinator
from agent import GCONAgent
from node import GCONNode

print("=" * 60)
print("        GCON STAGE 6 - SCHEDULING TEST")
print("=" * 60)


coordinator = GCONCoordinator()

node1 = GCONAgent("node-001")
node2 = GCONAgent("node-002")
node3 = GCONAgent("node-003")

coordinator.register_agent(node1)
coordinator.register_agent(node2)
coordinator.register_agent(node3)

heartbeat = node1.heartbeat()
coordinator.receive_heartbeat(heartbeat)

heartbeat = node2.heartbeat()
coordinator.receive_heartbeat(heartbeat)

heartbeat = node3.heartbeat()
coordinator.receive_heartbeat(heartbeat)

info = coordinator.registry.get_node_info("node-001")

print("\n=== HEARTBEAT TEST ===")
print(f"Node: node-001")
print(f"Status: {info['status']}")
print(f"Last Seen: {info['last_seen']}")


print("\nRegistered Nodes:")
print(coordinator.registry.list_nodes())

# --------------------------------------------------
# Submit a job
# --------------------------------------------------

coordinator.submit_job(
    "job-001",
    "echo Stage 6 Scheduler Working"
)

print("\nSubmitting job...")

result = coordinator.assign_job("job-001")

# --------------------------------------------------
# Results
# --------------------------------------------------

print("\n=== JOB RESULT ===")
print(result)

print("\n=== NODE STATUS ===")

for node_id in coordinator.registry.list_nodes():
    node = coordinator.registry.get_node(node_id)
    print(f"{node.job_id}: {node.status}")

print("\n=== JOB STATUS ===")
print(coordinator.get_job_status("job-001"))

print("\nStage 6 Scheduler Test Complete.")


import time

print("\nWaiting for heartbeat timeout...")
time.sleep(12)
print("\n=== BEFORE HEALTH CHECK ===")

for node_id in coordinator.registry.list_nodes():
    info = coordinator.registry.get_node_info(node_id)
    print(
        node_id,
        "| status =", info["status"],
        "| last_seen =", info["last_seen"]
    )


coordinator.registry.check_node_health()

print("\n=== SCHEDULER FAILURE TEST ===")

try:
    coordinator.submit_job(
        "job-002",
        "echo This job should not run"
    )

    coordinator.assign_job("job-002")

except RuntimeError as e:
    print(e)

print("\n=== AFTER HEALTH CHECK ===")

for node_id in coordinator.registry.list_nodes():
    info = coordinator.registry.get_node_info(node_id)
    print(
        node_id,
        "| status =", info["status"],
        "| last_seen =", info["last_seen"]
    )


print("\n=== NODE HEALTH ===")

for node_id in coordinator.registry.list_nodes():
    info = coordinator.registry.get_node_info(node_id)

    print(node_id, "->", info["status"])