import time
import psutil
import threading
from codecarbon import EmissionsTracker
import logging
logging.getLogger("codecarbon").addFilter(lambda record: record.levelno != logging.WARNING)


class ResourceMonitor:
    """
    A resource monitor for tracking resource consumption during code execution.

    Usage:
        monitor = ResourceMonitor()
        monitor.start(
            output_interval=60,           # Capture CodeCarbon output interval in seconds
            show_codecarbon_logs=False,   # Display the CodeCarbon log
            save_to_file=True             # Save the data as csv
        )
        # ... run your code ...
        monitor.stop()
    """

    def __init__(self, interval=1.0):
        """
        Initialize the monitor.

        Args:
            interval (float): Sampling interval for CPU/memory in seconds (default: 1.0).
        """
        self.interval = interval
        self._reset()

    def _reset(self):
        """Reset internal state."""
        self.start_time = None
        self.running = False
        self.cpu_usage = []
        self.memory_usage = []
        self.network_sent = []
        self.network_recv = []
        self.monitor_thread = None
        self.tracker = None
        self.start_network_io = None

    def _monitor_resources(self):
        """Background thread to sample system resources."""
        while self.running:
            current_time = time.time() - self.start_time
            self.cpu_usage.append((current_time, psutil.cpu_percent()))
            self.memory_usage.append((current_time, psutil.virtual_memory().percent))

            net_io = psutil.net_io_counters()
            sent = net_io.bytes_sent - self.start_network_io.bytes_sent
            recv = net_io.bytes_recv - self.start_network_io.bytes_recv
            self.network_sent.append((current_time, sent))
            self.network_recv.append((current_time, recv))

            time.sleep(self.interval)

    def start(self, output_interval=60, show_codecarbon_logs=False, export_csv=False):
        """Start monitoring resources and energy consumption."""
        if self.running:
            raise RuntimeError("Monitor is already running.")

        self.start_time = time.time()
        self.start_network_io = psutil.net_io_counters()
        self.running = True

        if show_codecarbon_logs is False:
            logging.getLogger("codecarbon").addFilter(lambda record: record.levelno != logging.INFO)

        # Start CodeCarbon tracker (handles CPU/GPU/RAM power estimation)
        self.tracker = EmissionsTracker(
            save_to_file=export_csv,
            measure_power_secs=output_interval
        )
        self.tracker.start()

        # Start background sampling thread
        self.monitor_thread = threading.Thread(target=self._monitor_resources)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop(self):
        """Stop monitoring and print detailed report including CPU/RAM/GPU breakdown."""
        if not self.running:
            raise RuntimeError("Monitor was not started.")

        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)

        duration = time.time() - self.start_time

        # Initialize all energy/power values
        total_energy = 0.0
        cpu_energy = gpu_energy = ram_energy = 0.0
        cpu_power = gpu_power = ram_power = 0.0

        # Extract detailed data from CodeCarbon
        if self.tracker:
            self.tracker.stop()
            final = getattr(self.tracker, 'final_emissions_data', None)
            if final:
                total_energy = getattr(final, 'energy_consumed', 0.0)
                cpu_energy = getattr(final, 'cpu_energy', 0.0)
                gpu_energy = getattr(final, 'gpu_energy', 0.0)
                ram_energy = getattr(final, 'ram_energy', 0.0)
                cpu_power = getattr(final, 'cpu_power', 0.0)
                gpu_power = getattr(final, 'gpu_power', 0.0)
                ram_power = getattr(final, 'ram_power', 0.0)

        # Print main report
        print("\n" + "=" * 38)
        print(f"Resources Monitor Report:")
        print(f"Execution Time: {duration:.6f} seconds")
        print(f"Total Energy: {total_energy:.6f} kWh")
        print(f"  • CPU : {cpu_energy:.6f} kWh (Power: {cpu_power:.1f} W)")
        print(f"  • GPU : {gpu_energy:.6f} kWh (Power: {gpu_power:.1f} W)")
        print(f"  • RAM : {ram_energy:.6f} kWh (Power: {ram_power:.1f} W)")

        # Resource usage stats
        if self.cpu_usage:
            avg_cpu = sum(x[1] for x in self.cpu_usage) / len(self.cpu_usage)
            max_cpu = max(x[1] for x in self.cpu_usage)
            print(f"CPU Usage: Avg {avg_cpu:.2f}% | Max {max_cpu:.2f}%")

        if self.memory_usage:
            avg_mem = sum(x[1] for x in self.memory_usage) / len(self.memory_usage)
            max_mem = max(x[1] for x in self.memory_usage)
            print(f"Memory Usage: Avg {avg_mem:.2f}% | Max {max_mem:.2f}%")

        if self.network_sent and self.network_recv:
            total_sent = self.network_sent[-1][1]
            total_recv = self.network_recv[-1][1]
            print(f"Network: Sent {total_sent / 1024:.2f} KB | Recv {total_recv / 1024:.2f} KB")

        print("=" * 38)

        self._reset()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()