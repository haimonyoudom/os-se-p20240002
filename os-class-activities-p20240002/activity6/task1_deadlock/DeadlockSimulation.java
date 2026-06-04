import java.util.concurrent.Semaphore;
import java.util.concurrent.atomic.AtomicBoolean;

class Account {
    String name;
    int balance;
    Semaphore lock = new Semaphore(1);

    Account(String name, int balance) {
        this.name = name;
        this.balance = balance;
    }
}

class Transfer {
    static void transfer(Account from, Account to, int amount, AtomicBoolean done) {
        try {
            System.out.println(Thread.currentThread().getName()
                    + " trying to lock FROM " + from.name);
            from.lock.acquire();
            System.out.println(Thread.currentThread().getName()
                    + " locked FROM " + from.name + " | now waiting for " + to.name);

            Thread.sleep(100); // force context switch so deadlock is likely

            System.out.println(Thread.currentThread().getName()
                    + " trying to lock TO " + to.name);
            to.lock.acquire();
            System.out.println(Thread.currentThread().getName()
                    + " locked TO " + to.name);

            from.balance -= amount;
            to.balance += amount;

            System.out.println(Thread.currentThread().getName()
                    + " transfer of " + amount + " completed: "
                    + from.name + " -> " + to.name);

            to.lock.release();
            from.lock.release();
            done.set(true);
        } catch (InterruptedException e) {
            System.out.println(Thread.currentThread().getName() + " was interrupted.");
        }
    }
}

public class DeadlockSimulation {
    public static void main(String[] args) throws InterruptedException {
        Account accountA = new Account("Account-A", 1000);
        Account accountB = new Account("Account-B", 1000);

        System.out.println("=== Deadlock Simulation ===");
        System.out.println("Starting balance - Account-A: " + accountA.balance
                + ", Account-B: " + accountB.balance);
        System.out.println("Starting total: " + (accountA.balance + accountB.balance));
        System.out.println();

        AtomicBoolean t1Done = new AtomicBoolean(false);
        AtomicBoolean t2Done = new AtomicBoolean(false);

        Thread t1 = new Thread(
                () -> Transfer.transfer(accountA, accountB, 100, t1Done), "Thread-1");
        Thread t2 = new Thread(
                () -> Transfer.transfer(accountB, accountA, 200, t2Done), "Thread-2");

        t1.setDaemon(true);
        t2.setDaemon(true);

        t1.start();
        t2.start();

        // Watchdog: wait up to 3 seconds for both transfers
        long deadline = System.currentTimeMillis() + 3000;
        while (System.currentTimeMillis() < deadline) {
            if (t1Done.get() && t2Done.get()) break;
            Thread.sleep(200);
        }

        boolean deadlocked = !t1Done.get() || !t2Done.get();

        if (deadlocked) {
            System.out.println();
            System.out.println("Deadlock detected: transactions are stuck");
            System.out.println();
            if (!t1Done.get()) System.out.println("Thread-1 is waiting for Account-B");
            if (!t2Done.get()) System.out.println("Thread-2 is waiting for Account-A");
            System.out.println();
            System.out.println("Current balances (transfers did NOT complete):");
            System.out.println("  Account-A: " + accountA.balance);
            System.out.println("  Account-B: " + accountB.balance);
        } else {
            System.out.println("Final Account-A: " + accountA.balance);
            System.out.println("Final Account-B: " + accountB.balance);
            System.out.println("Final total: " + (accountA.balance + accountB.balance));
        }
    }
}