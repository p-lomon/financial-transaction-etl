import subprocess
import time
import signal
import sys

# Paths to your scripts
PRODUCER_SCRIPT = "./kafka/producer/transaction_producer.py"
CONSUMER_SCRIPT = "./kafka/consumer/postgres_consumer.py"

# Store subprocess references
producer_proc = None
consumer_proc = None


def start_processes():
    global producer_proc, consumer_proc
    print("Starting Kafka Producer and Consumer...")

    producer_proc = subprocess.Popen(["python", PRODUCER_SCRIPT])
    print("Starting Kafka Producer...")
    time.sleep(10)  # Give producer time to warm up (optional)

    consumer_proc = subprocess.Popen(["python", CONSUMER_SCRIPT])


def stop_processes():
    print("\n Stopping processes...")
    if producer_proc:
        producer_proc.terminate()
    if consumer_proc:
        consumer_proc.terminate()

    # Wait for processes to exit
    if producer_proc:
        producer_proc.wait()
    if consumer_proc:
        consumer_proc.wait()

    print("All processes stopped.")


def signal_handler(sig, frame):
    stop_processes()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        start_processes()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_processes()
