class Dashboard:
    """
    Display GCON cluster metrics in a human-readable format.
    """

    def __init__(self, collector, summary):
        self.collector = collector
        self.summary = summary

    def display(self):
        """
        Display the current cluster dashboard.
        """

        # Collect latest metrics
        node_metrics = self.collector.collect_node_metrics()
        job_metrics = self.collector.collect_job_metrics()

        # Generate summaries
        cluster = self.summary.cluster_summary()

        nodes = cluster["nodes"]
        jobs = cluster["jobs"]
        resources = cluster["resources"]

        print("=" * 60)
        print("              GCON CLUSTER DASHBOARD")
        print("=" * 60)

        #
        # Node Information
        #
        print("\nNODES")
        print("-" * 60)

        for node in node_metrics:

            cpu = node["cpu"] if node["cpu"] is not None else "N/A"
            memory = node["memory"] if node["memory"] is not None else "N/A"

            print(
                f"{node['node_id']:<12}"
                f"{node['status']:<10}"
                f"CPU: {cpu}%   "
                f"MEM: {memory}%   "
                f"Jobs: {node['running_jobs']}"
            )

        #
        # Job Information
        #
        print("\nJOBS")
        print("-" * 60)

        for job in job_metrics:

            print(
                f"{job['job_id']:<12}"
                f"{job['status']:<12}"
                f"{job['agent']}"
            )

        #
        # Cluster Summary
        #
        print("\nCLUSTER SUMMARY")
        print("-" * 60)

        print(f"Total Nodes      : {nodes['total_nodes']}")
        print(f"Busy Nodes       : {nodes['busy_nodes']}")
        print(f"Idle Nodes       : {nodes['idle_nodes']}")
        print(f"Offline Nodes    : {nodes['offline_nodes']}")

        print()

        print(f"Total Jobs       : {jobs['total_jobs']}")
        print(f"Pending Jobs     : {jobs['pending_jobs']}")
        print(f"Running Jobs     : {jobs['running_jobs']}")
        print(f"Completed Jobs   : {jobs['completed_jobs']}")
        print(f"Failed Jobs      : {jobs['failed_jobs']}")

        print()

        print(f"Average CPU      : {resources['average_cpu']}%")
        print(f"Average Memory   : {resources['average_memory']}%")

        print("=" * 60)