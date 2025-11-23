from ResourceMonitor import ResourceMonitor

monitor = ResourceMonitor()

monitor.start()

print(sum(range(1_000_001)))

monitor.stop()