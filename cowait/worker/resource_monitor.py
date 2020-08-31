import time
import psutil


class ResourceMonitor():
    def __init__(self):
        self.last_net = psutil.net_io_counters()
        self.last_disk = psutil.disk_io_counters()
        self.last_time = time.time()

    def stats(self):
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(percpu=True)
        net = psutil.net_io_counters()
        disk = psutil.disk_io_counters()
        ctime = time.time()
        stats = {
            'dt': round(ctime - self.last_time, 3),
            'cpu': [ round(c / 100.0, 3) for c in cpu ],
            'mem': round(1.0 - mem.available / mem.total, 3),
            'net': [
                net.bytes_recv - self.last_net.bytes_recv,  # read
                net.bytes_sent - self.last_net.bytes_sent,  # write
            ],
            'disk': [
                disk.read_bytes - self.last_disk.read_bytes,  # read
                disk.write_bytes - self.last_disk.write_bytes,  # write
            ],
        }
        self.last_net = net
        self.last_disk = disk
        self.last_time = ctime
        return stats
