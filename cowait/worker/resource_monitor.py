import os
import psutil


class ResourceMonitor():
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.cpu_cores = psutil.cpu_count()
        self.total_memory = psutil.virtual_memory().total
        self.process.cpu_percent()  # initial cpu reading

    def stats(self):
        with self.process.oneshot():
            cpu = self.process.cpu_percent()
            mem = self.process.memory_full_info()
            io = self.process.io_counters()
            fds = self.process.num_fds()

        stats = {
            'cpu': [
                round(cpu / 100.0, 3),
                self.cpu_cores,
            ],
            'mem': [
                mem.uss,  # used
                self.total_memory,  # total
            ],
            'io': [
                io.read_chars,  # read
                io.write_chars,  # write
            ],
            'iops': [
                io.read_count,  # read
                io.write_count,  # write
            ],
            'fds': fds,
        }
        return stats
