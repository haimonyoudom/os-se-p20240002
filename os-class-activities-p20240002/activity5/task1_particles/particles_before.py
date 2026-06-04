
import threading
import time
import random

# ── Shared state ────────────────────────────────────────────────────────────
BUFFER_CAPACITY = 100          # max particles (50 pairs)
buffer: list[str] = []         # shared buffer  ← NO lock protecting this
produced_count = 0
packaged_count = 0
error_occurred = False         # set to True to stop all threads

# ── Producer (UNSAFE) ───────────────────────────────────────────────────────
def producer(machine_id: int):
    global produced_count, error_occurred
    pair_id = 0

    while not error_occurred:
        pair_id += 1
        p1 = f"M{machine_id}-{pair_id}-P1"
        p2 = f"M{machine_id}-{pair_id}-P2"

        # ⚠ Check buffer space WITHOUT a mutex – another thread can sneak in
        if len(buffer) + 2 > BUFFER_CAPACITY:
            print(f"\nThe producing machine is broken")
            print(f"  Machine {machine_id} tried to add to a full buffer "
                  f"(size={len(buffer)})")
            error_occurred = True
            break

        # ⚠ Deliberate gap between P1 and P2 appends to expose the race condition.
        #   Another producer can append its P1 here, interleaving particles.
        buffer.append(p1)
        time.sleep(0.003)       # <── race window: other threads run here
        buffer.append(p2)

        produced_count += 1
        time.sleep(random.uniform(0.005, 0.02))


# ── Consumer (UNSAFE) ───────────────────────────────────────────────────────
def consumer():
    global packaged_count, error_occurred

    while not error_occurred:
        time.sleep(0.015)

        # ⚠ Check count WITHOUT a mutex
        if len(buffer) < 2:
            print(f"\nThe packaging machine is broken")
            print(f"  Consumer tried to fetch from an empty buffer")
            error_occurred = True
            break

        # ⚠ Pop two items – they may belong to different pairs
        p1 = buffer.pop(0)
        p2 = buffer.pop(0)

        # Verify pair identity
        parts1 = p1.split('-')   # [machine, pair_id, P1]
        parts2 = p2.split('-')   # [machine, pair_id, P2]

        if parts1[0] != parts2[0] or parts1[1] != parts2[1]:
            print(f"\nPairs are incorrect")
            print(f"  Packaged: {p1}  +  {p2}  ← mismatched!")
            error_occurred = True
            break

        packaged_count += 1


# ── Status printer ───────────────────────────────────────────────────────────
def status_printer():
    while not error_occurred:
        print(
            f"\rProduced pairs: {produced_count:4d} | "
            f"Packaged pairs: {packaged_count:4d} | "
            f"Buffer particles: {len(buffer):3d}",
            end='', flush=True
        )
        time.sleep(0.1)


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Task 1A: Particle Buffer WITHOUT Semaphores ===")
    print("Running with 4 producers and 1 consumer (no synchronisation)...")
    print("Expect a race-condition error to appear shortly.\n")

    # Start status printer first
    t_status = threading.Thread(target=status_printer, daemon=True)
    t_status.start()

    # Start producers
    producer_threads = []
    for mid in range(1, 5):            # 4 producer machines
        t = threading.Thread(target=producer, args=(mid,), daemon=True)
        producer_threads.append(t)
        t.start()

    # Start consumer
    t_consumer = threading.Thread(target=consumer, daemon=True)
    t_consumer.start()

    # Wait for all workers to finish (they stop when error_occurred = True)
    t_consumer.join()
    for t in producer_threads:
        t.join(timeout=1.0)

    print(f"\n--- Simulation ended ---")
    print(f"Final: Produced pairs: {produced_count} | "
          f"Packaged pairs: {packaged_count} | "
          f"Buffer particles: {len(buffer)}")