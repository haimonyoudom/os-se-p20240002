# CPU Scheduling Algorithms — Exam Study Guide

## 1. Core Formulas (Memorize These First)

| Term | Formula |
|---|---|
| **Turnaround Time (TAT)** | Completion Time (CT) − Arrival Time (AT) |
| **Waiting Time (WAT)** | Turnaround Time (TAT) − Burst Time (BT) |
| **Response Time (RT)** | Time of first CPU allocation − Arrival Time (AT) |
| **Completion Time (CT)** | Time at which process finishes execution (read from Gantt chart) |
| **Average TAT** | Sum of all TAT ÷ number of processes |
| **Average WAT** | Sum of all WAT ÷ number of processes |

> **Shortcut relationship:** TAT = WAT + BT, and CT = AT + TAT

---

## 2. FCFS (First Come First Serve)

- **Non-preemptive.** Processes run strictly in order of arrival.
- Simple but causes the **convoy effect** (short processes stuck behind long ones).

**Steps to solve:**
1. Sort processes by Arrival Time.
2. Run each process to completion in that order (no interruption).
3. CT of process = max(AT, CT of previous process) + BT.
4. Compute TAT and WAT.

**Example:**

| Process | AT | BT |
|---|---|---|
| P1 | 0 | 5 |
| P2 | 1 | 3 |
| P3 | 2 | 8 |
| P4 | 3 | 6 |

Gantt Chart:
```
| P1 | P2 | P3  | P4  |
0    5    8     16    22
```

| Process | AT | BT | CT | TAT (CT-AT) | WAT (TAT-BT) |
|---|---|---|---|---|---|
| P1 | 0 | 5 | 5 | 5 | 0 |
| P2 | 1 | 3 | 8 | 7 | 4 |
| P3 | 2 | 8 | 16 | 14 | 6 |
| P4 | 3 | 6 | 22 | 19 | 13 |

Avg TAT = (5+7+14+19)/4 = **11.25**
Avg WAT = (0+4+6+13)/4 = **5.75**

---

## 3. SJN / SJF (Shortest Job Next / Shortest Job First)

- **Non-preemptive.** Among the processes that have **already arrived**, pick the one with the **smallest burst time** to run next.
- Optimal for minimizing average waiting time (non-preemptive case) but can cause **starvation** of long processes.

**Steps to solve:**
1. At each decision point, look only at processes that have arrived (AT ≤ current time) and haven't run yet.
2. Pick the smallest BT among them (tie → earliest AT, or given order).
3. Run it fully (no interruption), then repeat.

**Example:**

| Process | AT | BT |
|---|---|---|
| P1 | 0 | 7 |
| P2 | 1 | 4 |
| P3 | 2 | 1 |
| P4 | 3 | 4 |

- t=0: only P1 available → run P1 (0–7)
- t=7: P2, P3, P4 all arrived. Shortest = P3 (1) → run P3 (7–8)
- t=8: remaining P2(4), P4(4) → tie, pick earliest arrival P2 → run P2 (8–12)
- t=12: run P4 (12–16)

Gantt Chart:
```
| P1    | P3 | P2   | P4   |
0       7    8      12     16
```

| Process | AT | BT | CT | TAT | WAT |
|---|---|---|---|---|---|
| P1 | 0 | 7 | 7 | 7 | 0 |
| P3 | 2 | 1 | 8 | 6 | 5 |
| P2 | 1 | 4 | 12 | 11 | 7 |
| P4 | 3 | 4 | 16 | 13 | 9 |

Avg TAT = (7+6+11+13)/4 = **9.25**
Avg WAT = (0+5+7+9)/4 = **5.25**

---

## 4. SRT / SRTF (Shortest Remaining Time First)

- **Preemptive** version of SJN.
- At every time unit (or every new arrival), check if the newly arrived process has a **shorter remaining burst time** than the currently running process. If so, **preempt** and switch to it.
- Best average WAT/TAT theoretically, but high overhead from frequent context switching + starvation risk.

**Steps to solve:**
1. Track **remaining time** for every process, not just original BT.
2. At each new arrival (or each time tick), compare remaining time of running process vs. new arrival.
3. Always run whichever available process has the smallest remaining time.
4. CT = the time the remaining time hits 0.

**Example:**

| Process | AT | BT |
|---|---|---|
| P1 | 0 | 8 |
| P2 | 1 | 4 |
| P3 | 2 | 9 |
| P4 | 3 | 5 |

- t=0: only P1 → run P1
- t=1: P2 arrives (rem=4) vs P1 rem=7 → switch to P2
- t=2: P3 arrives (rem=9), P2 rem=3 is smallest → keep P2
- t=3: P4 arrives (rem=5), P2 rem=2 is smallest → keep P2
- t=5: P2 finishes (CT=5). Compare P1(7), P3(9), P4(5) → run P4
- t=10: P4 finishes (CT=10). Compare P1(7), P3(9) → run P1
- t=17: P1 finishes (CT=17). Run P3
- t=26: P3 finishes (CT=26)

Gantt Chart:
```
| P1 | P2   | P4    | P1     | P3      |
0    1      5       10       17        26
```

| Process | AT | BT | CT | TAT | WAT |
|---|---|---|---|---|---|
| P1 | 0 | 8 | 17 | 17 | 9 |
| P2 | 1 | 4 | 5 | 4 | 0 |
| P3 | 2 | 9 | 26 | 24 | 15 |
| P4 | 3 | 5 | 10 | 7 | 2 |

Avg TAT = (17+4+24+7)/4 = **13**
Avg WAT = (9+0+15+2)/4 = **6.5**

---

## 5. RR (Round Robin)

- **Preemptive**, uses a fixed **time quantum (TQ)**.
- Every process gets the CPU for at most TQ time, then goes to the **back of the ready queue** if not finished.
- Fair and good for time-sharing systems, but performance depends heavily on TQ size (too small → high overhead; too large → behaves like FCFS).
**Easy Method (Exam Trick)**

For every turn, ask these four questions:

Who is at the front of the queue?
Run for one Time Quantum (or until finished).
Did any new process arrive during this time? Add them to the queue.
If the current process isn't finished, move it to the back.

Repeat until every process has burst time = 0.
**Steps to solve:**
1. Maintain a ready queue in arrival order.
2. Pop front process, run for min(remaining time, TQ).
3. If new processes arrived during that slice, add them to the queue **before** re-adding the just-run process (if it still has remaining time).
4. Repeat until all remaining times = 0.

**Example (TQ = 2):**

| Process | AT | BT |
|---|---|---|
| P1 | 0 | 5 |
| P2 | 1 | 3 |
| P3 | 2 | 1 |
| P4 | 3 | 2 |

Queue trace:
- t=0: Queue=[P1]. Run P1 (0–2), rem=3. P2 arrived at t=1 → Queue=[P2,P1]
- t=2: P3 arrives(t=2). Queue=[P2,P3,P1]. Run P2 (2–4), rem=1. P4 arrives at t=3 → Queue=[P3,P1,P4,P2]
- t=4: Run P3 (4–5), rem=0 → done (CT=5). Queue=[P1,P4,P2]
- t=5: Run P1 (5–7), rem=1. Queue=[P4,P2,P1]
- t=7: Run P4 (7–9), rem=0 → done (CT=9). Queue=[P2,P1]
- t=9: Run P2 (9–10), rem=0 → done (CT=10). Queue=[P1]
- t=10: Run P1 (10–11), rem=0 → done (CT=11)

Gantt Chart:
```
| P1 | P2 | P3 | P1 | P4 | P2 | P1 |
0    2    4    5    7    9    10   11
```

| Process | AT | BT | CT | TAT | WAT |
|---|---|---|---|---|---|
| P1 | 0 | 5 | 11 | 11 | 6 |
| P2 | 1 | 3 | 10 | 9 | 6 |
| P3 | 2 | 1 | 5 | 3 | 2 |
| P4 | 3 | 2 | 9 | 6 | 4 |

Avg TAT = (11+9+3+6)/4 = **7.25**
Avg WAT = (6+6+2+4)/4 = **4.5**

---

## 6. MLQ (Multi-Level Queue)

- Ready queue is **split into separate queues** based on process type/priority (e.g., System, Interactive, Batch).
- Each queue can have **its own scheduling algorithm** (e.g., top queue = RR, bottom queue = FCFS).
- Queues themselves are scheduled with **fixed priority** (higher queue always runs first, lower queue starves) or **time-slicing between queues** (each queue gets a % of CPU time).
- **No movement between queues** (this is the key difference from Multilevel Feedback Queue, which does allow movement).

**Key exam points:**
- Draw the queue structure: e.g.
  ```
  Queue 1 (System, highest priority) → FCFS
  Queue 2 (Interactive)              → RR (TQ=2)
  Queue 3 (Batch, lowest priority)   → FCFS
  ```
- If **fixed priority scheduling between queues**: Queue 1 processes must ALL finish before Queue 2 is looked at, and so on.
- If asked to compute TAT/WAT: solve each queue's Gantt chart internally using its own algorithm, respecting the priority order between queues.
- Common exam trap: mixing up which algorithm applies to which queue — always double check the question's queue assignment before scheduling.

---

## 7. Quick Comparison Table

| Algorithm | Preemptive? | Selection Criteria | Starvation Risk | Best For |
|---|---|---|---|---|
| FCFS | No | Arrival order | Low (but convoy effect) | Simple batch systems |
| SJN/SJF | No | Shortest burst time | High (long jobs) | Minimizing avg WAT (non-preemptive) |
| SRT | Yes | Shortest remaining time | High (long jobs) | Minimizing avg WAT (preemptive) |
| RR | Yes (by TQ) | Fixed time slice | None | Time-sharing/interactive systems |
| MLQ | Depends per queue | Fixed queue assignment | High for low-priority queues | Systems with distinct process categories |

---

## 8. Exam Checklist

- [ ] Always double-check whether the question wants **arrival times considered** — if all AT=0, every algorithm simplifies a lot.
- [ ] For SJN and SRT, only consider processes that have **already arrived** when picking next process.
- [ ] For SRT and RR, always track **remaining time**, not original burst time.
- [ ] Draw the **Gantt chart** first — it makes CT/TAT/WAT calculation almost mechanical.
- [ ] Double check: **TAT = WAT + BT** as a sanity check on every row.
- [ ] For RR, be careful with tie-breaking when a process finishes and a new one arrives at the exact same time — convention is usually: **newly arrived process is added to queue before the just-preempted process**.
- [ ] For MLQ, confirm whether it's **fixed priority** or **time-sliced between queues** before scheduling.
