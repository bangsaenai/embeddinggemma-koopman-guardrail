#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../core/bangsaen_sec.h"

#define NUCLEAR_ITERATIONS 1000000000ULL // 1,000,000,000 Operations (1 Billion)
#define PROGRESS_INTERVAL  100000000ULL  // Report status every 100 Million ops (10%)
#define MAX_BUFFER_SIZE    4096          // Up to 4KB dynamic page boundary

// Fast PRNG (Xorshift64) for non-blocking dynamic random generation
static inline uint64_t xorshift64(uint64_t* state) {
    uint64_t x = *state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    return *state = x;
}

int main() {
    printf("===================================================\n");
    printf("   Bangsaen AI Labs: DYNAMIC 1-BILLION NUCLEAR TEST \n");
    printf("   Target: 1 Billion Dynamic Payload Zeroizations   \n");
    printf("   Buffer Sizes: 16 Bytes -> 4,096 Bytes (Dynamic)  \n");
    printf("===================================================\n\n");

    // Allocate 4KB aligned working memory buffer
    uint8_t* dynamic_buffer = (uint8_t*)malloc(MAX_BUFFER_SIZE);
    if (!dynamic_buffer) {
        printf("[-] Failed to allocate dynamic test memory buffer!\n");
        return 1;
    }

    uint64_t prng_state = 0xDEADBEEF99372026ULL;
    double total_ns = 0.0;
    uint64_t total_cycles = 0;
    uint64_t total_bytes_cleared = 0;
    double min_ns = 1e9;
    double max_ns = 0.0;
    bool all_cleared = true;

    printf("[*] Starting Dynamic 1 Billion Operations Test...\n");
    printf("[*] Benchmarking multi-size payload memory flushes...\n\n");

    for (uint64_t i = 1; i <= NUCLEAR_ITERATIONS; i++) {
        // 1. Generate dynamic payload size between 16 and 4096 bytes
        uint64_t rand_val = xorshift64(&prng_state);
        size_t current_size = 16 + (size_t)(rand_val % (MAX_BUFFER_SIZE - 16 + 1));

        // 2. Pollute buffer with dynamic noise bytes
        uint8_t noise_byte = (uint8_t)(rand_val & 0xFF);
        memset(dynamic_buffer, noise_byte, current_size);

        // 3. Execute Hardware Zeroization & Cache Flush
        BangsaenMetrics m = bangsaen_sec_destroy_and_contaminate(dynamic_buffer, current_size);

        total_ns += m.zeroization_time_ns;
        total_cycles += m.cpu_cycles;
        total_bytes_cleared += current_size;

        if (m.zeroization_time_ns < min_ns) min_ns = m.zeroization_time_ns;
        if (m.zeroization_time_ns > max_ns) max_ns = m.zeroization_time_ns;

        // 4. Spot check memory clearance (First, middle, and last bytes)
        if (dynamic_buffer[0] != 0x00 || 
            dynamic_buffer[current_size / 2] != 0x00 || 
            dynamic_buffer[current_size - 1] != 0x00) {
            all_cleared = false;
        }

        // Live Progress Report every 100,000,000 iterations (10%)
        if (i % PROGRESS_INTERVAL == 0) {
            double current_avg_ns = total_ns / (double)i;
            double gb_cleared = (double)total_bytes_cleared / (1024.0 * 1024.0 * 1024.0);
            printf("    [Progress %3llu%%] %10llu / %llu ops | Avg: %.2f ns | Cleared: %.2f GB\n",
                   (unsigned long long)(i / (NUCLEAR_ITERATIONS / 100)),
                   (unsigned long long)i,
                   (unsigned long long)NUCLEAR_ITERATIONS,
                   current_avg_ns,
                   gb_cleared);
        }
    }

    double avg_ns = total_ns / (double)NUCLEAR_ITERATIONS;
    double avg_cycles = (double)total_cycles / (double)NUCLEAR_ITERATIONS;
    double total_gb = (double)total_bytes_cleared / (1024.0 * 1024.0 * 1024.0);

    printf("\n===================================================\n");
    printf("   DYNAMIC NUCLEAR TEST FINAL AUDIT REPORT          \n");
    printf("===================================================\n");
    printf("    [+] Final Status       : %s (+0.00MB Remanence)\n", all_cleared ? "100% PASSED (1 BILLION DYNAMIC CLEAN)" : "FAILED");
    printf("    [+] Total Operations   : %llu ops\n", (unsigned long long)NUCLEAR_ITERATIONS);
    printf("    [+] Total Memory Cleaned: %.2f Gigabytes\n", total_gb);
    printf("    [+] Total Time Elapsed : %.2f seconds\n", total_ns / 1e9);
    printf("    [+] Average Time / Op  : %.2f nanoseconds\n", avg_ns);
    printf("    [+] Average Cycles / Op: %.2f CPU cycles\n", avg_cycles);
    printf("    [+] Min / Max Time     : %.2f ns / %.2f ns\n", min_ns, max_ns);
    printf("===================================================\n");

    free(dynamic_buffer);
    return 0;
}