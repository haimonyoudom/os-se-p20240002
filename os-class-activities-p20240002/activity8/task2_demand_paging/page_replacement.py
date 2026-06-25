# Part 2B - Demand Paging Simulator (FIFO & LRU)
# Student: Monyoudom | ID: p20240002 | a=2, b=0

from collections import deque

FRAMES = 3

def run_fifo(name, reference_string):
    frames  = []          # current pages in memory (ordered by load time)
    faults  = 0
    queue   = deque()     # tracks load order for eviction

    print(f"=== FIFO — {name} ===")
    for page in reference_string:
        if page in frames:
            status = "HIT  "
        else:
            faults += 1
            status  = "FAULT"
            if len(frames) < FRAMES:
                frames.append(page)
                queue.append(page)
            else:
                evict = queue.popleft()
                frames[frames.index(evict)] = page
                queue.append(page)

        display = [str(p) for p in frames] + ['_'] * (FRAMES - len(frames))
        evicted = "" if status == "HIT  " else f"  evicted: {queue[-1] if status == 'HIT  ' else ''}"
        print(f"  Ref {page} | {status} | frames: [{', '.join(display)}]")

    print(f"  Total FIFO faults: {faults}")
    print()
    return faults


def run_lru(name, reference_string):
    frames  = []          # current pages in memory
    faults  = 0
    recency = []          # tracks recency: index 0 = most recent

    print(f"=== LRU — {name} ===")
    for page in reference_string:
        if page in frames:
            status = "HIT  "
            # Update recency on hit
            recency.remove(page)
            recency.insert(0, page)
        else:
            faults += 1
            status  = "FAULT"
            if len(frames) < FRAMES:
                frames.append(page)
            else:
                # Evict least recently used (last in recency list)
                evict = recency[-1]
                frames[frames.index(evict)] = page
                recency.remove(evict)
            recency.insert(0, page)

        display = [str(p) for p in frames] + ['_'] * (FRAMES - len(frames))
        print(f"  Ref {page} | {status} | frames: [{', '.join(display)}]")

    print(f"  Total LRU faults: {faults}")
    print()
    return faults


# ── Strings ────────────────────────────────────────────────────────
my_string   = [2, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3]       # Part 2A (a=2 so first 7 → 2)
full_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3,
               2, 1, 2, 0, 1, 7, 0, 1]                     # Full lecture string

print("=" * 55)
print("Part 2B — Demand Paging Simulator")
print(f"Frames: {FRAMES}")
print("=" * 55)
print()

# ── Run on MY string ───────────────────────────────────────────────
print(f"My string: {my_string}")
print()
f1 = run_fifo("My string", my_string)
l1 = run_lru ("My string", my_string)
print(f"  My string  →  FIFO faults: {f1}  |  LRU faults: {l1}")
print()

# ── Run on FULL lecture string ─────────────────────────────────────
print("-" * 55)
print(f"Full lecture string: {full_string}")
print()
f2 = run_fifo("Full lecture string", full_string)
l2 = run_lru ("Full lecture string", full_string)
print(f"  Full string  →  FIFO faults: {f2}  |  LRU faults: {l2}")
print("=" * 55)