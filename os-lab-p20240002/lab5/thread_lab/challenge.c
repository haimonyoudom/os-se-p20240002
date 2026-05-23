#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <signal.h>

// Global flag
volatile sig_atomic_t keep_running = 1;

// Signal handler
void handle_sigint(int sig) {
    printf("\nSIGINT received. Stopping threads...\n");
    keep_running = 0;
}

// Worker thread function
void* worker(void* arg) {
    pthread_t tid = pthread_self();

    while (keep_running) {
        printf("Thread %lu is running...\n", (unsigned long)tid);
        sleep(1);
    }

    printf("Thread %lu exiting...\n", (unsigned long)tid);
    pthread_exit(NULL);
}

int main() {
    pthread_t t1, t2;

    // Set up SIGINT handler
    signal(SIGINT, handle_sigint);

    // Create threads
    if (pthread_create(&t1, NULL, worker, NULL) != 0) {
        perror("Failed to create thread 1");
        return 1;
    }

    if (pthread_create(&t2, NULL, worker, NULL) != 0) {
        perror("Failed to create thread 2");
        return 1;
    }

    // Wait for threads to finish
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("All threads cleanly exited. Goodbye.\n");

    return 0;
}
