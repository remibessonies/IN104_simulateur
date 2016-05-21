import time
class Deadline:

    def __init__(self, time):
        self.time = time

    def until(self):
        return self.time - time.time()
