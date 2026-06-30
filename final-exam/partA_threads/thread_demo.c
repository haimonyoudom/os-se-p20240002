#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_THREADS 4

void *worker(void *arg) {
    int id = *(int *)arg;
    int result = id * 10;
    printf("Thread %d: tid=%lu, result=%d\n", id, pthread_self(), result);
    sleep(5);          // ← stays alive so we can capture it
    int *ret = malloc(sizeof(int));
    *ret = result;
    return ret;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];
    int total = 0;

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

    printf("Main: all threads done. Total = %d\n", total);
    return 0;
}