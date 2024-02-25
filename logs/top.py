from nvitop import Device
import psutil

devices = Device.all()

def get_system_usage():
    # cpu_usage = psutil.cpu_percent()
    cpu_usage = sum(psutil.cpu_percent(percpu=True))
    # ram_usage = psutil.virtual_memory().percent
    ram_usage = psutil.virtual_memory().used / (1024.0 ** 3)

    device = Device.all()[0]

    gpu_memory_total = device.memory_total()
    gpu_memory_used = device.memory_used()
    gpu_usage = round((gpu_memory_used / gpu_memory_total) * 100, 2)
    gpu_util = device.gpu_utilization()

    return cpu_usage, ram_usage, gpu_usage, gpu_util