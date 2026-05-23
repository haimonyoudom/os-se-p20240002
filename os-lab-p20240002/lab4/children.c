#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
    pid_t pids[3];
    int i;

    printf("Parent PID: %d\n", getpid());

    // Create 3 child processes
    for (i = 0; i < 3; i++) {
        pids[i] = fork();

        if (pids[i] == 0) {
            // Child process
            printf("Child %d PID: %d - sleeping 15 seconds\n", i+1, getpid());
            sleep(15);
            printf("Child %d done\n", i+1);
            exit(0);
        }
    }

    // Parent waits for all 3 children
    printf("Parent waiting for all 3 children...\n");
    printf("Run: ps --forest -e | grep -A5 <PARENT_PID>\n");

    for (i = 0; i < 3; i++) {
        int status;
        pid_t done = wait(&status);
        printf("Parent: child PID %d finished\n", done);
    }

    printf("All children done - no zombies!\n");
    return 0;
}
