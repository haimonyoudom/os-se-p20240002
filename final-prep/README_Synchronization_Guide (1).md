# Synchronization & Deadlock Worksheet Guide

> Study notes based on the uploaded worksheet.

## Table of Contents

1. Semaphore Basics
2. wait() and signal()
3. Binary vs Counting Semaphores
4. Producer–Consumer Pattern
5. Mutual Exclusion
6. Race Conditions
7. Ordering Constraints
8. Deadlock
9. Common Semaphore Patterns
10. How to Solve Semaphore Questions
11. Exam Checklist

---

# 1. Semaphore Basics

A **semaphore** is an integer used to synchronize processes or threads accessing shared resources.

Two operations:

```text
wait(S)
signal(S)
```

## wait(S)

- If `S > 0`
  - decrement `S`
  - continue execution
- If `S == 0`
  - block until another process calls `signal(S)`.

## signal(S)

```text
S++
```

If another process is waiting, one waiting process is awakened.

---

# 2. Binary vs Counting Semaphores

## Binary Semaphore

```text
Semaphore mutex = 1;
```

Used for **mutual exclusion**.

```text
wait(mutex)

Critical Section

signal(mutex)
```

## Counting Semaphore

```text
Semaphore empty = N;
```

Used when multiple identical resources exist.

---

# 3. Producer–Consumer Pattern

Typical semaphores:

```text
Semaphore empty = BufferSize;
Semaphore full = 0;
Semaphore mutex = 1;
```

Producer:

```text
Produce

wait(empty)
wait(mutex)

Insert Item

signal(mutex)
signal(full)
```

Consumer:

```text
wait(full)
wait(mutex)

Remove Item

signal(mutex)
signal(empty)

Consume
```

Always call `wait(empty)` **before** `wait(mutex)` to avoid deadlock.

---

# 4. Mutual Exclusion

Whenever multiple processes modify one shared variable:

- counter
- buffer
- queue
- balance

Protect it:

```text
wait(mutex)

modify shared data

signal(mutex)
```

---

# 5. Race Condition

Occurs when multiple processes read and write shared data simultaneously.

Example:

```text
counter++
```

Without synchronization the final value may be incorrect.

---

# 6. Ordering Constraints

If **A must happen before B**:

```text
Semaphore s = 0;
```

Process 1

```text
A
signal(s)
```

Process 2

```text
wait(s)
B
```

---

# 7. Deadlock

Deadlock occurs when processes wait forever for each other.

Bad example:

```text
P1:
wait(A)
wait(B)

P2:
wait(B)
wait(A)
```

Avoid by acquiring resources in the **same order**.

---

# 8. Common Semaphore Patterns

## Mutual Exclusion

```text
wait(mutex)
Critical Section
signal(mutex)
```

## Producer–Consumer

```text
wait(empty)
wait(mutex)
Insert
signal(mutex)
signal(full)
```

## Ordering

```text
wait(s)
Task
signal(next)
```

---

# 9. How to Solve Semaphore Questions

## Step 1

Identify the shared resource.

→ Use `mutex`.

## Step 2

Is there limited capacity?

→ Use a counting semaphore.

## Step 3

Does one action have to happen before another?

→ Use a semaphore initialized to **0**.

## Step 4

Check for deadlock.

All processes should acquire resources in the same order.

---

# 10. Exam Checklist

- ✅ Shared variable → `mutex`
- ✅ Buffer → `empty`, `full`, `mutex`
- ✅ Ordering constraint → semaphore starts at `0`
- ✅ Limited resources → counting semaphore
- ✅ Deadlock prevention → consistent wait order

---

# Quick Reference

| Situation | Semaphore |
|-----------|-----------|
| Mutual exclusion | `mutex = 1` |
| Buffer slots | `empty = N` |
| Items available | `full = 0` |
| A before B | semaphore = `0` |
| One process at a time | Binary semaphore |
| Multiple resources | Counting semaphore |
