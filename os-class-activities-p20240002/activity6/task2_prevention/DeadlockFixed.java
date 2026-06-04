import java.util.concurrent.Semaphore;

class AccountSafe {
    String name;
    int balance;

    AccountSafe(String name, int balance) {
        this.name = name;
        this.balance = balance;
    }
}

class SafeTransfer {
    static Semaphore mutex = new Semaphore(1); // single global mutex, initialized to 1

    static void transfer(AccountSafe from, AccountSafe to, int amount) {
        try {
            System.out.println(Thread.currentThread().getName()
                    + " requesting mutex to transfer " + amount
                    + " from " + from.name + " to " + to.name);

            mutex.acquire(); // only one transfer at a time
            try {
                System.out.println(Thread.currentThread().getName()
                        + " acquired mutex");

                Thread.sleep(100); // simulate processing time

                from.balance -= amount;
                to.balance += amount;

                System.out.println(Thread.currentThread().getName()
                        + " transferred " + amount
                        + " from " + from.name + " to " + to.name
                        + " | " + from.name + ": " + from.balance
                        + ", " + to.name + ": " + to.balance);
            } finally {
                mutex.release(); // always release, even on error
                System.out.println(Thread.currentThread().getName()
                        + " released mutex");
            }

        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

public class DeadlockFixed {
    public static void main(String[] args) throws InterruptedException {
        AccountSafe accountA = new AccountSafe("Account-A", 1000);
        AccountSafe accountB = new AccountSafe("Account-B", 1000);
        int startingTotal = accountA.balance + accountB.balance;

        System.out.println("=== Deadlock Prevention using Single Semaphore Mutex ===");
        System.out.println("Starting balance - Account-A: " + accountA.balance
                + ", Account-B: " + accountB.balance);
        System.out.println("Starting total: " + startingTotal);
        System.out.println();

        Thread t1 = new Thread(
                () -> SafeTransfer.transfer(accountA, accountB, 100), "Thread-1");
        Thread t2 = new Thread(
                () -> SafeTransfer.transfer(accountB, accountA, 200), "Thread-2");

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        int finalTotal = accountA.balance + accountB.balance;

        System.out.println();
        System.out.println("=== Results ===");
        System.out.println("Final Account-A: " + accountA.balance);
        System.out.println("Final Account-B: " + accountB.balance);
        System.out.println("Final total: " + finalTotal);
        System.out.println("Starting total: " + startingTotal);
        System.out.println("Balance preserved: " + (startingTotal == finalTotal));
        System.out.println();
        System.out.println("No deadlock occurred");
    }
}