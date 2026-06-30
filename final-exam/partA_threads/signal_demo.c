#include <stdio.h>
#include <signal.h>
#include <unistd.h>

void handler(int sig) {
    printf("\nCaught signal %d — cleaning up and exiting.\n", sig);
    _exit(0);
}

int main() {
    signal(SIGINT, handler);
    signal(SIGTERM, handler);
    printf("Running. Press Ctrl+C to exit.\n");
    while (1) {
        printf("looping...\n");
        sleep(1);
    }
}
