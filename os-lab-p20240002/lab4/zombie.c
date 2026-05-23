#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // Child process
        printf("Child PID: %d - exiting now\n", getpid());
        exit(0);
    } else {
        // Parent process
        printf("Parent PID: %d - sleeping 10 seconds...\n", getpid());
        printf("Check zombie now: ps aux | grep Z\n");
        sleep(10);

        // Call wait() to collect child
        int status;
        wait(&status);
        printf("Parent called wait() - zombie should be gone now\n");
        printf("Check again: ps aux | grep Z\n");
        sleep(5);
    }
    return 0;
}