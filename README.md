# Resource Monitor  
A lightweight and convenient resource monitoring tool built on psutil and CodeCarbon.  
It tracks CPU/GPU/RAM energy consumption, execution time, system load, and network usage during code execution.

ResourceMonitor supports two output modes:

1. **Silent Mode** – only prints a clean summary report  
2. **Log Mode** – prints full CodeCarbon logging output during execution

Users can freely configure:
- Whether to show CodeCarbon logs  
- CodeCarbon reporting interval (seconds)  
- Whether to save collected energy data as a CSV file  

---

## Features

- CPU / GPU / RAM energy tracking (kWh)
- CPU / GPU / RAM usage statistics (average and peak)
- Network traffic (sent/received)
- Execution time measurement

---

## Installation

```bash
pip install -r requirements.txt
````

---

## Quick Start

```python
from ResourceMonitor import ResourceMonitor

monitor = ResourceMonitor()
monitor.start()

# ... your code ...

monitor.stop()
```

---

## Example Output (Silent Mode)

```
======================================
Resources Monitor Report:
Execution Time: 12.626897 seconds
Total Energy: 0.000119 kWh
  • CPU : 0.000072 kWh (Power: 42.5 W)
  • GPU : 0.000013 kWh (Power: 9.9 W)
  • RAM : 0.000034 kWh (Power: 20.0 W)
CPU Usage: Avg 5.45% | Max 17.50%
Memory Usage: Avg 46.55% | Max 46.70%
Network: Sent 22.43 KB | Recv 30.92 KB
======================================
```

---

## Demo Scripts

### **Demo 1 — Silent Mode (Only Summary Output)**

```python
from ResourceMonitor import ResourceMonitor

monitor = ResourceMonitor()
monitor.start()

print(sum(range(1_000_001)))

monitor.stop()
```

---

### **Demo 2 — Log Mode (Show CodeCarbon Logs)**

```python
from ResourceMonitor import ResourceMonitor

monitor = ResourceMonitor()
monitor.start(
    output_interval=5,          # Capture CodeCarbon logs every 5 seconds
    show_codecarbon_logs=True,  # Display CodeCarbon logs
    export_csv=True             # Save data to csv
    )

import time
for i in range(1, 4):
    time.sleep(5)
    print(f"[Program Output] Step {i}/3 completed.")

monitor.stop()
```

Running this script produces full CodeCarbon logs such as:

```
[codecarbon INFO @ 12:03:41] [setup] RAM Tracking...
[codecarbon INFO @ 12:03:41] [setup] CPU Tracking...
[codecarbon INFO @ 12:03:44] CPU Model on constant consumption mode: 13th Gen Intel(R) Core(TM) i9-13900H
[codecarbon INFO @ 12:03:44] [setup] GPU Tracking...
[codecarbon INFO @ 12:03:44] Tracking Nvidia GPU via pynvml
[codecarbon INFO @ 12:03:44] The below tracking methods have been set up:
                RAM Tracking Method: RAM power estimation model
                CPU Tracking Method: global constant
                GPU Tracking Method: pynvml
            
[codecarbon INFO @ 12:03:44] >>> Tracker's metadata:
[codecarbon INFO @ 12:03:44]   Platform system: Windows-10-10.0.26100-SP0
[codecarbon INFO @ 12:03:44]   Python version: 3.10.11
[codecarbon INFO @ 12:03:44]   CodeCarbon version: 3.1.0
[codecarbon INFO @ 12:03:44]   Available RAM : 31.730 GB
[codecarbon INFO @ 12:03:44]   CPU count: 20 thread(s) in 20 physical CPU(s)
[codecarbon INFO @ 12:03:44]   CPU model: 13th Gen Intel(R) Core(TM) i9-13900H
[codecarbon INFO @ 12:03:44]   GPU count: 1
[codecarbon INFO @ 12:03:44]   GPU model: 1 x NVIDIA GeForce RTX 4060 Laptop GPU
[codecarbon INFO @ 12:03:47] Emissions data (if any) will be saved to file C:\Users\Hongw\PycharmProjects\Resource-Monitor\emissions.csv
[Program Output] Step 1/3 completed.
[codecarbon INFO @ 12:03:52] Energy consumed for RAM : 0.000028 kWh. RAM Power : 20.0 W
[codecarbon INFO @ 12:03:52] Delta energy consumed for CPU with constant : 0.000059 kWh, power : 42.5 W
[codecarbon INFO @ 12:03:52] Energy consumed for All CPU : 0.000059 kWh
[codecarbon INFO @ 12:03:52] Energy consumed for all GPUs : 0.000008 kWh. Total GPU Power : 6.011307758819215 W
[codecarbon INFO @ 12:03:52] 0.000095 kWh of electricity and 0.000000 L of water were used since the beginning.
[Program Output] Step 2/3 completed.
[codecarbon INFO @ 12:03:57] Energy consumed for RAM : 0.000056 kWh. RAM Power : 20.0 W
[codecarbon INFO @ 12:03:57] Delta energy consumed for CPU with constant : 0.000059 kWh, power : 42.5 W
[codecarbon INFO @ 12:03:57] Energy consumed for All CPU : 0.000118 kWh
[codecarbon INFO @ 12:03:57] Energy consumed for all GPUs : 0.000021 kWh. Total GPU Power : 8.811019932084283 W
[codecarbon INFO @ 12:03:57] 0.000195 kWh of electricity and 0.000000 L of water were used since the beginning.
[codecarbon INFO @ 12:04:03] Energy consumed for RAM : 0.000083 kWh. RAM Power : 20.0 W
[codecarbon INFO @ 12:04:03] Delta energy consumed for CPU with constant : 0.000059 kWh, power : 42.5 W
[codecarbon INFO @ 12:04:03] Energy consumed for All CPU : 0.000177 kWh
[codecarbon INFO @ 12:04:03] Energy consumed for all GPUs : 0.000044 kWh. Total GPU Power : 16.598015554973085 W
[codecarbon INFO @ 12:04:03] 0.000305 kWh of electricity and 0.000000 L of water were used since the beginning.
[Program Output] Step 3/3 completed.
[codecarbon INFO @ 12:04:03] Energy consumed for RAM : 0.000085 kWh. RAM Power : 20.0 W
[codecarbon INFO @ 12:04:03] Delta energy consumed for CPU with constant : 0.000003 kWh, power : 42.5 W
[codecarbon INFO @ 12:04:03] Energy consumed for All CPU : 0.000180 kWh
[codecarbon INFO @ 12:04:03] Energy consumed for all GPUs : 0.000045 kWh. Total GPU Power : 29.584723234701567 W
[codecarbon INFO @ 12:04:03] 0.000310 kWh of electricity and 0.000000 L of water were used since the beginning.

======================================
Resources Monitor Report:
Execution Time: 21.839347 seconds
Total Energy: 0.000310 kWh
  • CPU : 0.000180 kWh (Power: 42.5 W)
  • GPU : 0.000045 kWh (Power: 29.6 W)
  • RAM : 0.000085 kWh (Power: 20.0 W)
CPU Usage: Avg 5.07% | Max 14.80%
Memory Usage: Avg 49.47% | Max 49.70%
Network: Sent 50.18 KB | Recv 315.63 KB
======================================

```

---

EOD