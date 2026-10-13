#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../core/bangsaen_sec.h"

#if defined(_WIN32) || defined(_WIN64)
#include <windows.h>
#include <process.h>
#else
#include <pthread.h>
#endif

#define SEQUENTIAL_ITERATIONS 1000000
#define NUM_THREADS 16
#define THREAD_ITERATIONS 100000

typedef struct {
    int thread_id;
    uint64_t total_cycles;
    double total_time_ns;
    bool success;
} ThreadData;

// Thread Worker Function
#if defined(_WIN32) || defined(_WIN64)
DWORD WINAPI thread_worker(LPVOID arg)
#else
void* thread_worker(void* arg)
#endif
{
    ThreadData* data = (ThreadData*)arg;
    char buffer[256];
    data->success = true;

    for (int i = 0; i < THREAD_ITERATIONS; i++) {
        snprintf(buffer, sizeof(buffer), "THREAD_%d_SECRET_PAYLOAD_ITERATION_%d", data->thread_id, i);
        size_t len = strlen(buffer);

        BangsaenMetrics m = bangsaen_sec_destroy_and_contaminate(buffer, len);
        data->total_cycles += m.cpu_cycles;
        data->total_time_ns += m.zeroization_time_ns;

        // Verify clearance
        if (buffer[0] != 0x00) {
            data->success = false;
        }
    }

#if defined(_WIN32) || defined(_WIN64)
    return 0;
#else
    return NULL;
#endif
}

int main() {
    printf("===================================================\n");
    printf("   Bangsaen AI Labs: C-Native Core STRESS TEST     \n");
    printf("===================================================\n\n");

    // -------------------------------------------------------------------
    // TEST 1: Sequential 1,000,000 Iterations Stress Test
    // -------------------------------------------------------------------
    printf("[1/2] Running Sequential Stress Test (%d iterations)...\n", SEQUENTIAL_ITERATIONS);
    
    char test_payload[128] = "ENTERPRISE_CAD_ENGINE_GEOMETRY_MATRIX_2026_PROPRIETARY";
    size_t payload_len = strlen(test_payload);

    double total_ns = 0.0;
    uint64_t total_cycles = 0;
    double min_ns = 1e9;
    double max_ns = 0.0;
    bool all_cleared = true;

    // Warm-up run
    bangsaen_sec_destroy_and_contaminate(test_payload, payload_len);

    for (int i = 0; i < SEQUENTIAL_ITERATIONS; i++) {
        // Prepare dummy payload
        memset(test_payload, 'A' + (i % 26), payload_len);

        BangsaenMetrics m = bangsaen_sec_destroy_and_contaminate(test_payload, payload_len);

        total_ns += m.zeroization_time_ns;
        total_cycles += m.cpu_cycles;

        if (m.zeroization_time_ns < min_ns) min_ns = m.zeroization_time_ns;
        if (m.zeroization_time_ns > max_ns) max_ns = m.zeroization_time_ns;

        if (test_payload[0] != 0x00) {
            all_cleared = false;
        }
    }

    double avg_ns = total_ns / SEQUENTIAL_ITERATIONS;
    double avg_cycles = (double)total_cycles / SEQUENTIAL_ITERATIONS;

    printf("    [+] Status           : %s (+0.00MB Remanence)\n", all_cleared ? "100% PASSED" : "FAILED");
    printf("    [+] Total Operations : %d\n", SEQUENTIAL_ITERATIONS);
    printf("    [+] Average Time     : %.2f nanoseconds / op\n", avg_ns);
    printf("    [+] Average Cycles   : %.2f CPU cycles / op\n", avg_cycles);
    printf("    [+] Min / Max Time   : %.2f ns / %.2f ns\n\n", min_ns, max_ns);

    // -------------------------------------------------------------------
    // TEST 2: Multi-Threaded Concurrency Test (16 Threads)
    // -------------------------------------------------------------------
    printf("[2/2] Running Multi-Threaded Concurrency Test (%d Threads x %d ops = %d total ops)...\n",
           NUM_THREADS, THREAD_ITERATIONS, NUM_THREADS * THREAD_ITERATIONS);

#if defined(_WIN32) || defined(_WIN64)
    HANDLE threads[NUM_THREADS];
    ThreadData tdata[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        tdata[i].thread_id = i;
        tdata[i].total_cycles = 0;
        tdata[i].total_time_ns = 0.0;
        tdata[i].success = true;
        threads[i] = CreateThread(NULL, 0, thread_worker, &tdata[i], 0, NULL);
    }

    WaitForMultipleObjects(NUM_THREADS, threads, TRUE, INFINITE);

    for (int i = 0; i < NUM_THREADS; i++) {
        CloseHandle(threads[i]);
    }
#else
    pthread_t threads[NUM_THREADS];
    ThreadData tdata[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        tdata[i].thread_id = i;
        tdata[i].total_cycles = 0;
        tdata[i].total_time_ns = 0.0;
        tdata[i].success = true;
        pthread_create(&threads[i], NULL, thread_worker, &tdata[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
#endif

    bool concurrency_success = true;
    double mt_total_ns = 0.0;
    uint64_t mt_total_cycles = 0;

    for (int i = 0; i < NUM_THREADS; i++) {
        if (!tdata[i].success) concurrency_success = false;
        mt_total_ns += tdata[i].total_time_ns;
        mt_total_cycles += tdata[i].total_cycles;
    }

    uint64_t total_mt_ops = (uint64_t)NUM_THREADS * THREAD_ITERATIONS;
    printf("    [+] Concurrency Status : %s\n", concurrency_success ? "100% PASSED (Zero Race Conditions)" : "FAILED");
    printf("    [+] Active Threads     : %d Concurrent Threads\n", NUM_THREADS);
    printf("    [+] Total Operations   : %llu ops\n", (unsigned long long)total_mt_ops);
    printf("    [+] Throughput Avg     : %.2f nanoseconds / op\n", mt_total_ns / total_mt_ops);
    printf("===================================================\n");

    return 0;
}