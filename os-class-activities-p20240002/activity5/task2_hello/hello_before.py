
import threading
import time
import random

output_lock = threading.Lock()   # only for clean terminal output (NOT for ordering)

def process1():
    """Prints H and E"""
    time.sleep(random.uniform(0, 0.05))   # random startup delay
    with output_lock:
        print("H", end='', flush=True)
    time.sleep(random.uniform(0, 0.02))
    with output_lock:
        print("E", end='', flush=True)

def process2():
    """Prints L and L"""
    time.sleep(random.uniform(0, 0.05))   # random startup delay
    with output_lock:
        print("L", end='', flush=True)
    time.sleep(random.uniform(0, 0.02))
    with output_lock:
        print("L", end='', flush=True)

def process3():
    """Prints O"""
    time.sleep(random.uniform(0, 0.05))   # random startup delay
    with output_lock:
        print("O", end='', flush=True)


if __name__ == "__main__":
    print("=== Task 2A: HELLO WITHOUT Semaphores ===")
    print("Running 5 times to show non-deterministic ordering:\n")

    for run in range(1, 6):
        print(f"Run {run}: ", end='', flush=True)

        t1 = threading.Thread(target=process1)
        t2 = threading.Thread(target=process2)
        t3 = threading.Thread(target=process3)

        # Start all threads simultaneously – no ordering control
        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        print()   # newline after each run

    print("\n← The order above is unpredictable. "
          "Letters may not spell HELLO!")