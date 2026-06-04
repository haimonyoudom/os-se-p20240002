
import threading
import time
import random

# ── Buffer configuration ─────────────────────────────────────────────────────
BUFFER_CAPACITY = 100          # 100 particles = 50 pairs
MAX_PAIRS       = BUFFER_CAPACITY // 2

# ── Semaphores ───────────────────────────────────────────────────────────────
empty_pairs = threading.Semaphore(MAX_PAIRS)   # 50 free pair-slots
full_pairs  = threading.Semaphore(0)           # 0 pairs ready initially
mutex       = threading.Semaphore(1)           # mutual exclusion

# ── Shared state (protected by mutex) ────────────────────────────────────────
buffer: list[str] = []
produced_count = 0
packaged_count = 0
error_occurred = False

# ── Producer ─────────────────────────────────────────────────────────────────
def producer(machine_id: int):
    global produced_count, error_occurred
    pair_id = 0

    while not error_occurred:
        pair_id += 1
        p1 = f"M{machine_id}-{pair_id}-P1"
        p2 = f"M{machine_id}-{pair_id}-P2"

        # ── SEMAPHORE: wait for a free pair-slot ─────────────────────────────
        empty_pairs.acquire()
        if error_occurred:
            break

        # ── MUTEX: enter critical section ────────────────────────────────────
        mutex.acquire()

        # Safety check (should never trigger with correct semaphore logic)
        if len(buffer) + 2 > BUFFER_CAPACITY:
            print(f"\nThe producing machine is broken")
            error_occurred = True
            mutex.release()
            break

        buffer.append(p1)
        buffer.append(p2)
        produced_count += 1

        # ── MUTEX: leave critical section ─────────────────────────────────────
        mutex.release()

        # ── SEMAPHORE: notify consumer that one more pair is ready ────────────
        full_pairs.release()

        time.sleep(random.uniform(0.01, 0.04))   # simulate production time


# ── Consumer ─────────────────────────────────────────────────────────────────
def consumer():
    global packaged_count, error_occurred

    while not error_occurred:
        # ── SEMAPHORE: wait until at least one complete pair is in the buffer ─
        full_pairs.acquire()
        if error_occurred:
            break

        # ── MUTEX: enter critical section ─────────────────────────────────────
        mutex.acquire()

        # Safety check (should never trigger with correct semaphore logic)
        if len(buffer) < 2:
            print(f"\nThe packaging machine is broken")
            error_occurred = True
            mutex.release()
            break

        p1 = buffer.pop(0)
        p2 = buffer.pop(0)

        # Verify both particles belong to the same pair
        parts1 = p1.split('-')   # ['M<id>', '<pair_id>', 'P1']
        parts2 = p2.split('-')   # ['M<id>', '<pair_id>', 'P2']

        if parts1[0] != parts2[0] or parts1[1] != parts2[1]:
            print(f"\nPairs are incorrect")
            print(f"  Packaged: {p1}  +  {p2}  ← mismatched!")
            error_occurred = True
            mutex.release()
            break

        packaged_count += 1

        # ── MUTEX: leave critical section ─────────────────────────────────────
        mutex.release()

        # ── SEMAPHORE: free one pair-slot for producers ───────────────────────
        empty_pairs.release()

        time.sleep(random.uniform(0.01, 0.03))   # simulate packaging time


# ── Status printer ────────────────────────────────────────────────────────────
def status_printer():
    while not error_occurred:
        print(
            f"\rProduced pairs: {produced_count:4d} | "
            f"Packaged pairs: {packaged_count:4d} | "
            f"Buffer particles: {len(buffer):3d}",
            end='', flush=True
        )
        time.sleep(0.2)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    NUM_PRODUCERS = 4

    print("=== Task 1B: Particle Buffer WITH Semaphores ===")
    print(f"Producers: {NUM_PRODUCERS}  |  Consumer: 1  |  "
          f"Buffer capacity: {BUFFER_CAPACITY} particles ({MAX_PAIRS} pairs)")
    print("Semaphores: empty_pairs=50, full_pairs=0, mutex=1")
    print("Press Ctrl+C to stop.\n")

    # Status printer
    t_status = threading.Thread(target=status_printer, daemon=True)
    t_status.start()

    # Producers
    producer_threads = []
    for mid in range(1, NUM_PRODUCERS + 1):
        t = threading.Thread(target=producer, args=(mid,), daemon=True)
        producer_threads.append(t)
        t.start()

    # Consumer
    t_consumer = threading.Thread(target=consumer, daemon=True)
    t_consumer.start()

    try:
        # Run until manually stopped or an error occurs
        t_consumer.join()
        for t in producer_threads:
            t.join(timeout=1.0)
    except KeyboardInterrupt:
        print(f"\n\nManually stopped.")

    print(f"\n--- Simulation ended ---")
    print(f"Final: Produced pairs: {produced_count} | "
          f"Packaged pairs: {packaged_count} | "
          f"Buffer particles: {len(buffer)}")
    if not error_occurred:
        print("No errors detected – semaphores worked correctly!")