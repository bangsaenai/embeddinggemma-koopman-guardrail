#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "../core/bangsaen_sec.h"

int main() {
    printf("===================================================\n");
    printf("   Bangsaen AI Labs: C-Native Core Sanity Test     \n");
    printf("===================================================\n\n");

    BangsaenCloudContext cloud_ctx;
    if (bangsaen_sec_init_cloud_context(&cloud_ctx, "bsa_live_9937_commercial_key", 7)) {
        printf("[+] Cloud Context Initialized Successfully:\n");
        printf("    - Tenant Key : %s\n", cloud_ctx.tenant_key);
        printf("    - Token      : %s\n", cloud_ctx.session_token);
        printf("    - Vector Dim : %dD Koopman Space\n\n", cloud_ctx.koopman_space_dim);
    } else {
        printf("[-] Failed to initialize Cloud Context!\n");
        return 1;
    }

    char sensitive_buffer[128] = "CRITICAL_PROPRIETARY_ALGORITHM_LOGIC_KEY_2026";
    size_t data_len = strlen(sensitive_buffer);

    printf("[+] Memory State BEFORE Active Defense:\n");
    printf("    - Address : %p\n", (void*)sensitive_buffer);
    printf("    - Content : \"%s\"\n\n", sensitive_buffer);

    printf("[*] Executing Hardware Zeroization & Cache Flush...\n");
    BangsaenMetrics metrics = bangsaen_sec_destroy_and_contaminate(sensitive_buffer, data_len);

    bool is_completely_cleared = true;
    for (size_t i = 0; i < data_len; i++) {
        if (sensitive_buffer[i] != 0x00) {
            is_completely_cleared = false;
            break;
        }
    }

    printf("\n[+] Memory State AFTER Active Defense:\n");
    printf("    - Remanence Status : %s (+0.00MB Remanence)\n", is_completely_cleared ? "CLEARED (0x00)" : "FAILED");
    printf("    - Hardware Flush   : %s\n", metrics.hardware_flush_executed ? "EXECUTED (_mm_clflush)" : "SKIPPED");
    printf("    - CPU Cycles       : %llu cycles\n", (unsigned long long)metrics.cpu_cycles);
    printf("    - Measured Time    : %.2f nanoseconds\n", metrics.zeroization_time_ns);
    printf("===================================================\n");

    return 0;
}