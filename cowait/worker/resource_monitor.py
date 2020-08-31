import os
import time
import psutil


class ResourceMonitor():
    def __init__(self):
        self.last_time = time.time()
        self.process = psutil.Process(os.getpid())
        self.last_io = self.process.io_counters()

    def stats(self):
        cpu = self.process.cpu_percent()
        mem = self.process.memory_full_info()
        io = self.process.io_counters()
        ctime = time.time()
        stats = {
            'dt': round(ctime - self.last_time, 3),
            'cpu': round(cpu / 100.0, 3),
            'mem': [
                mem.uss,  # used
                psutil.virtual_memory().total,  # total
            ],
            'io': [
                io.read_bytes - self.last_io.read_bytes,  # read
                io.write_bytes - self.last_io.write_bytes,  # write
            ],
        }
        self.last_io = io
        self.last_time = ctime
        return stats
