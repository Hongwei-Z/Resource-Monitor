from ResourceMonitor import ResourceMonitor
import time

monitor = ResourceMonitor()

monitor.start(
    output_interval=5,          # Display CodeCarbon logs every 5 seconds
    show_codecarbon_logs=True,  # Display CodeCarbon logs
    export_csv=True             # Save data to csv
    )

for i in range(1, 4):
    time.sleep(5)
    print(f"[Program Output] Step {i}/3 completed.")

monitor.stop()