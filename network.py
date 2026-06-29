class GCONNetwork:
    """
    Simulated GCON network.
    """

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def send_job(self, command):
        """
        Send a job through the network.
        """

        return self.dispatcher.dispatch(command)