#ifndef BANGSAEN_SEC_H
#define BANGSAEN_SEC_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#if defined(_WIN32) || defined(_WIN64)
#include <windows.h>
#endif

// Cross-Compiler Intrinsics Header Fix (MSVC vs GCC/Clang)
#if defined(_MSC_VER)
    #include <intrin.h>
    #include <immintrin.h>
#elif defined(__GNUC__) || defined(__clang__)
    #if defined(__x86_64__) || defined(_M_X64)
        #include <x86intrin.h>
        #include <immintrin.h>
    #endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    char tenant_key[128];
    char session_token[256];
    uint64_t token_issued_at;
    uint32_t offline_validity_sec;
    bool is_attested;
    uint32_t koopman_space_dim;
} BangsaenCloudContext;

typedef struct {
    double zeroization_time_ns;
    uint64_t cpu_cycles;
    size_t bytes_cleared;
    bool hardware_flush_executed;
} BangsaenMetrics;

bool bangsaen_sec_init_cloud_context(BangsaenCloudContext* ctx, const char* tenant_key, uint32_t offline_days);
bool bangsaen_sec_verify_attestation(BangsaenCloudContext* ctx);
BangsaenMetrics bangsaen_sec_destroy_and_contaminate(void* target_ptr, size_t size);

#ifdef __cplusplus
}
#endif

#endif // BANGSAEN_SEC_H