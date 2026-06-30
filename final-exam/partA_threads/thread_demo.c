#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_THREADS 4
#define EXTRA_THREADS 3

void *worker(void *arg) {
    int id = *(int *)arg;
    int result = id * 10;
    printf("Thread %d: tid=%lu, result=%d\n", id, pthread_self(), result);
    sleep(5);
    int *ret = malloc(sizeof(int));
    *ret = result;
    return ret;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];
    int total = 0;

    // Original 4 workers
    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        int *res;
        pthread_join(threads[i], (void **)&res);
        total += *res;
        free(res);
    }
    printf("Main: original threads done. Total = %d\n", total);

    // 3 extra workers start AFTER originals joined
    printf("Starting 3 extra workers...\n");
    pthread_t extra[EXTRA_THREADS];
    int extra_ids[EXTRA_THREADS];
    for (int i = 0; i < EXTRA_THREADS; i++) {
        extra_ids[i] = NUM_THREADS + i + 1;
        pthread_create(&extra[i], NULL, worker, &extra_ids[i]);
    }

    // Capture LWPs while extra workers are alive
    sleep(2);
    system("ps -eLf | grep thread_demo | grep -v grep");

    for (int i = 0; i < EXTRA_THREADS; i++) {
        int *res;
        pthread_join(&extra[i], (void **)&res);
        free(res);
    }
    printf("Main: all done.\n");
    return 0;
}
