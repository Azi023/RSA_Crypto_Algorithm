# performance_analysis.py
import time
import psutil

def measure_performance(func, *args, **kwargs):
    process = psutil.Process()
    cpu_start = process.cpu_times()
    mem_start = process.memory_info().rss
    time_start = time.time()

    # Execute the target function
    result = func(*args, **kwargs)

    time_end = time.time()
    cpu_end = process.cpu_times()
    mem_end = process.memory_info().rss

    cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)
    mem_usage = (mem_end - mem_start) / (1024 * 1024)  # Convert to MB
    elapsed_time = time_end - time_start

    metrics = {
        'elapsed_time': elapsed_time,
        'cpu_time': cpu_time,
        'memory_usage': mem_usage
    }
    return result, metrics
