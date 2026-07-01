"""
Reproduces the job_id bug in agent.py without needing scheduler.py or
key_manager.py (which aren't present and would crash on import anyway).

Run: python test_gcon_bugs.py
"""

from agent import GCONAgent


def test_job_id_conflated_with_node_id():
    agent = GCONAgent(node_id="node-1")

    # Two different "jobs" run on the same agent.
    result_a = agent.execute_job("echo hello")
    result_b = agent.execute_job("echo world")

    print("Job A reported job_id:", result_a["job_id"])
    print("Job B reported job_id:", result_b["job_id"])

    # Expected: each execution reports its own job_id.
    # Actual: both report "node-1", because self.job_id is set once
    # in __init__ and never changes.
    assert result_a["job_id"] == result_b["job_id"] == "node-1", (
        "job_id no longer conflated with node_id — bug may already be fixed"
    )
    print("CONFIRMED BUG: both jobs report job_id='node-1' instead of "
          "their own identity. Receipts generated from these results are "
          "indistinguishable by job.")


if __name__ == "__main__":
    test_job_id_conflated_with_node_id()