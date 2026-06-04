import threading
import time

# Initial semaphore values
a = threading.Semaphore(1)
b = threading.Semaphore(0)
c = threading.Semaphore(0)
d = threading.Semaphore(5)

def process1():
    while True:
        d.acquire() 
        a.acquire()      # wait(a)
        print("H", end="", flush=True)
        print("E", end="", flush=True)
        b.release()      # signal(b)
        b.release()      # signal(b)

def process2():
    while True:
        b.acquire()      # wait(b)
        print("L", end="", flush=True)
        c.release()      # signal(c)

def process3():
    while True:
        c.acquire()      # wait(c)
        c.acquire()      # wait(c)
        print("O", end="", flush=True)
        print()          # newline after HELLO
        a.release()      # signal(a)
        

# Create threads
t1 = threading.Thread(target=process1, daemon=True)
t2 = threading.Thread(target=process2, daemon=True)
t3 = threading.Thread(target=process3, daemon=True)

# Start threads
t1.start()
t2.start()
t3.start()

# Keep main thread alive
while True:
    time.sleep(1)