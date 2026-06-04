
import threading

# ── Semaphores ────────────────────────────────────────────────────────────────
start_he = threading.Semaphore(1)   # Process 1 is allowed to start immediately
after_e  = threading.Semaphore(0)   # Process 2 blocked until Process 1 signals
after_ll = threading.Semaphore(0)   # Process 3 blocked until Process 2 signals

# Lock used only so each letter prints cleanly (not for ordering)
print_lock = threading.Lock()

def process1():
    """
    Prints H then E.
    Waits on start_he (allowed = 1 so it starts right away).
    Signals after_e when done so Process 2 can proceed.
    """
    start_he.acquire()          # wait for permission to start (immediate)
    with print_lock:
        print("H", end='', flush=True)
    with print_lock:
        print("E", end='', flush=True)
    after_e.release()           # tell Process 2 it can print now


def process2():
    """
    Prints L then L.
    Must wait for Process 1 to finish (after_e starts at 0).
    Signals after_ll when done so Process 3 can proceed.
    """
    after_e.acquire()           # block until Process 1 signals
    with print_lock:
        print("L", end='', flush=True)
    with print_lock:
        print("L", end='', flush=True)
    after_ll.release()          # tell Process 3 it can print now


def process3():
    """
    Prints O.
    Must wait for Process 2 to finish (after_ll starts at 0).
    """
    after_ll.acquire()          # block until Process 2 signals
    with print_lock:
        print("O", end='', flush=True)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Task 2B: HELLO WITH Semaphores ===")
    print("Running 5 times to confirm deterministic ordering:\n")

    for run in range(1, 6):
        # Reset semaphores for each run
        start_he = threading.Semaphore(1)
        after_e  = threading.Semaphore(0)
        after_ll = threading.Semaphore(0)

        # Recreate threads capturing current semaphore values via closures
        def make_p1(s_start, s_after):
            def p1():
                s_start.acquire()
                with print_lock:
                    print("H", end='', flush=True)
                with print_lock:
                    print("E", end='', flush=True)
                s_after.release()
            return p1

        def make_p2(s_wait, s_after):
            def p2():
                s_wait.acquire()
                with print_lock:
                    print("L", end='', flush=True)
                with print_lock:
                    print("L", end='', flush=True)
                s_after.release()
            return p2

        def make_p3(s_wait):
            def p3():
                s_wait.acquire()
                with print_lock:
                    print("O", end='', flush=True)
            return p3

        t1 = threading.Thread(target=make_p1(start_he, after_e))
        t2 = threading.Thread(target=make_p2(after_e, after_ll))
        t3 = threading.Thread(target=make_p3(after_ll))

        print(f"Run {run}: ", end='', flush=True)

        # Start all threads – semaphores enforce the correct order
        t1.start(); t2.start(); t3.start()
        t1.join();  t2.join();  t3.join()

        print()   # newline

    print("\n← Always HELLO! Semaphores guarantee correct ordering.")