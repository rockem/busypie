from threading import Thread

from backports.asyncio import runners


class RunnerThread(Thread):

    def __init__(self, main, *, debug=False):
        super().__init__()
        self.result = None
        self.exception = None
        self.main = main
        self.debug = debug

    def run(self):
        try:
            self.result = runners.run(self.main, debug=self.debug)
        except BaseException as e:
            self.exception = e


def run(main, *, debug=False):
    """
    Since we're using asyncio loop to run wait() in irder to be compatible with async calls,
    here we also run each wait in a different thread to allow nested calls to wait()
    """
    thread = RunnerThread(main, debug=debug)
    thread.start()
    thread.join()
    if thread.exception:
        raise thread.exception
    return thread.result
