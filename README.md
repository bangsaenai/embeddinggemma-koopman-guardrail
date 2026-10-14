# 🛡️ Koopman Gatekeeper: Sub-Millisecond Universal AI Security & C-Native SECaaS Core

> **Full-Stack Enterprise Architecture:** Universal Multilingual Threat Detection (`EmbeddingGemma` + `3072D Koopman Space Lifting`) integrated with a Hardware-Level C-Native Active Defense Engine (+0.00MB Remanence).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Precision](https://img.shields.io/badge/Accuracy-100%25%20Clean%20Sweep%20(600%2F600)-brightgreen.svg)]()
[![Hardware Clean](https://img.shields.io/badge/1B%20Nuclear%20Audit-100%25%20PASSED%20(1.91TB)-blue.svg)]()
[![Koopman Latency](https://img.shields.io/badge/Decision%20Latency-0.037ms%20(CPU)-orange.svg)]()

---

## ⚙️ Model Access & Authentication Notes

This repository supports a **Hybrid Engine** execution model (Ollama API or Native PyTorch via Hugging Face Transformers). Please take note of the following access requirements:

### Option A: Running via Ollama (Recommended - No Token Required)
If you run the engine with Ollama active in the background, Ollama handles model downloading internally:
1. Ensure Ollama Desktop / Daemon is running (`ollama serve`)
2. Pull the model once:
   ```bash
   ollama pull embeddinggemma 
   ```
###  Option B: Running via Native PyTorch / Transformers (Fallback Mode)
Since Google's google/embeddinggemma-2b is a Gated Model on Hugging Face, attempting to download model weights directly via Native PyTorch without authentication will throw a 401 Unauthorized error.

If you choose to run without Ollama background service, you must complete a one-time authentication:

Accept the license terms on google/embeddinggemma-2b

Authenticate your terminal using your Hugging Face Access Token:
```bash
huggingface-cli login
```

### 1. Runtime Environment Mismatch (PyTorch vs. Ollama)
Please be aware that executing inference or feature extraction via different runtime environments may yield slightly different embedding vectors due to precision quantization and backend tensor transformations:
- **Native PyTorch / Transformers :** Provides full FP32/FP16 precision vector trajectories, which guarantees deterministic accuracy matching our primary benchmark results.
- **Ollama API Wrapper (`embeddinggemma:latest`):** Ollama applies C++ backend quantization/conversion (e.g., BF16/INT8). This introduces slight vector space distortion, which may shift edge-case raw scores slightly near decision boundaries.

> **Note:** If you reproduce benchmarks using Ollama instead of Native PyTorch, decision thresholds must be recalibrated accordingly.

---

### 2. Domain Calibration & Out-of-Distribution (OOD) Prompts
The Koopman Guardrail Engine operates as an **Adaptive Mathematical Framework**, not a frozen static classifier. 

- **No Universal Silver Bullet:** No fixed dataset or pre-set threshold covers 100% of domain-specific enterprise queries out-of-the-box.
- **Calibrating OOD Queries:** If your production system encounters unseen query categories (e.g., benign emergency requests like *"gas leaks"* or obfuscated technical payloads), you must include representative samples in your local calibration dataset (`datasets/`).
- **Deterministic Separation:** Once the decision space is calibrated with domain-specific centroids, the Koopman linear projection will reliably isolate threats with zero false positives.


### 3. Proof-of-Concept (PoC) Disclaimer & Enterprise Consultation

* **PoC Evaluation Only (Not Production-Ready):** The 100% precision metrics achieved in this repository demonstrate the mathematical validity of 3072D Koopman Space separation under specific benchmark configurations. **Do NOT deploy this static setup directly into a production environment out-of-the-box.**
* **Out-of-Distribution (OOD) Sensitivity:** Unseen query structures, complex domain-specific vocabulary, or sophisticated obfuscation may result in misclassification if the decision space is not continuously calibrated.
* **Get Expert Assistance:** Implementing a reliable, enterprise-grade AI Guardrail requires custom dataset curation and dynamic thresholding. For production deployment, integration, or custom calibration consulting, please contact us directly:

📩 **Consultation & Advisory:** [drtanet@bangsaenai.com](mailto:drtanet@bangsaenai.com)


## 💡 Architectural Overview & Breakthrough

Traditional AI Guardrails introduce massive **100ms–500ms latency bottlenecks** and leave sensitive state payloads vulnerable in process memory (RAM).

**Koopman Gatekeeper + C-Native Core** solves both ends of the spectrum:
1. **Cloud & Mathematical Layer (Koopman Space):** Projects semantic embeddings into a **3072-Dimensional Hilbert Space** using Cover’s Theorem. Non-linear AI threats (Jailbreaks, Prompt Injections, Token Smuggling) become linearly separable with zero fine-tuning across global languages.
2. **Local Hardware Enforcement Layer (C-Native Core):** A zero-dependency C engine statically linked into commercial binaries to perform 3-Pass active memory zeroization and hardware CPU cache line invalidation (`_mm_clflush` + `_mm_sfence`), preventing AI RAM Scraping and memory remanence attacks.

---

## 📊 Hardware & Benchmark Audit Results

### 1. Global Multilingual Guardrail Benchmark (600 Prompts V2)

| Language | Test Scope | Precision | False Positive Rate (FPR) | Decision Latency (CPU) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **English** 🇬🇧 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.047 ms** | ✅ Clean Sweep |
| **Thai** 🇹🇭 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.039 ms** | ✅ Clean Sweep |
| **Chinese** 🇨🇳 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.041 ms** | ✅ Clean Sweep |
| **German** 🇩🇪 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.039 ms** | ✅ Clean Sweep |
| **Spanish** 🇪🇸 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.027 ms** | ✅ Clean Sweep |
| **Korean** 🇰🇷 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.028 ms** | ✅ Clean Sweep |
| **OVERALL** | **600 Prompts Total** | **100.00%** | **0.00%** | **0.037 ms (Avg)** | 🏆 **Deterministic** |

---

### 2. C-Native Hardware Zeroization Audit (Clang -O3 Validation)

| Test Suite | Workload Scope | Total Operations | Total Memory Cleaned | Data Remanence | Audit Result |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Sanity Core Test** | Static Buffer (128B) | 1 Op | -- | `+0.00MB (0x00)` | **PASSED** |
| **Sequential Stress** | Continuous Loop | 1,000,000 Ops | ~128 MB | `+0.00MB (0x00)` | **PASSED** |
| **16-Thread Concurrency**| Multi-Threaded Concurrent | 1,600,000 Ops | ~204 MB | `+0.00MB (0x00)` | **PASSED (Zero Race)** |
| **1-Billion Dynamic Nuclear**| Dynamic Payloads (16B–4KB) | **1,000,000,000 Ops** | **1,914.78 Gigabytes** | `+0.00MB (0x00)` | 🏆 **100% PASSED (Zero Leak)** |

---

## 📊 Benchmark Evolution: V1 Baseline vs. V2 Global Scale (600 Prompts)

To ensure statistical rigor for enterprise deployment, the benchmark suite evolved from a **110-Prompt PoC Baseline (V1)** to a standardized **600-Prompt Rigorous Suite (V2)**—maintaining $100.00\%$ Precision and $0.00\%$ FPR on local CPU.

### 🚀 V2 Global Scale Audit (100 Prompts Per Language / 600 Total)

| Language | Test Scope (Threats / Safe) | Precision | False Positive Rate (FPR) | Decision Latency (CPU) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **English** 🇬🇧 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.047 ms** | ✅ Clean Sweep |
| **Thai** 🇹🇭 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.039 ms** | ✅ Clean Sweep |
| **Chinese** 🇨🇳 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.041 ms** | ✅ Clean Sweep |
| **German** 🇩🇪 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.039 ms** | ✅ Clean Sweep |
| **Spanish** 🇪🇸 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.027 ms** | ✅ Clean Sweep |
| **Korean** 🇰🇷 | **100 Prompts** (50 / 50) | **100.00%** | **0.00%** | **0.028 ms** | ✅ Clean Sweep |
| **OVERALL** | **600 Prompts Total** | **100.00%** | **0.00%** | **0.037 ms (Avg)** | 🏆 **Deterministic** |

---

<details>
<summary>📜 <b>Click to View V1 Initial Baseline Proof (110 Prompts Historical Archive)</b></summary>

<br>

> *Historical PoC evaluation conducted during initial mathematical proof validation:*

| Language | V1 Scope | V1 Precision | V1 FPR | V1 Latency | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **English** 🇬🇧 | 40 Prompts (30 / 10) | **100.00%** | **0.00%** | ~ 0.83 ms – 2.19 ms | ✅ Passed |
| **Chinese** 🇨🇳 | 15 Prompts (10 / 5) | **100.00%** | **0.00%** | ~ 2.39 ms | ✅ Passed |
| **German** 🇩🇪 | 15 Prompts (10 / 5) | **100.00%** | **0.00%** | ~ 1.63 ms | ✅ Passed |
| **Spanish** 🇪🇸 | 15 Prompts (10 / 5) | **100.00%** | **0.00%** | ~ 1.11 ms | ✅ Passed |
| **Korean** 🇰🇷 | 15 Prompts (10 / 5) | **100.00%** | **0.00%** | ~ 1.29 ms | ✅ Passed |
| **Thai** 🇹🇭 | 15 Prompts (10 / 5) | **100.00%** | **0.00%** | ~ 1.12 ms | ✅ Passed |

</details>

---

## 🧪 Evaluated Threat Vectors & Scope

Our benchmark suites validate protection against key OWASP LLM Top 10 vulnerabilities across all supported languages:

1. **Roleplay & Cognitive Overrides:** Persona hijacks, DAN overrides, and moral restriction bypasses.
2. **Indirect Prompt Injection:** Hidden payload extractions within translation and summarization contexts.
3. **Token Smuggling & Obfuscation:** Base64, Hex, Leetspeak, and cipher-encoded attack instructions.
4. **Agentic Execution Overrides:** Unauthorized OS command executions, SQL injections, and system overrides.
5. **Academic & Enterprise Context Awareness:** Distinguishing genuine technical research (e.g., Buffer Overflow theory, SOC2 compliance, Nginx configs, PID loops) from malicious intent with **Zero False Positives**.

---

## 📂 Project Structure

```text
embeddinggemma-koopman-guardrail/
├── README.md                            # Universal Showcase Documentation
├── LICENSE                               # Official MIT License
├── requirements.txt                      # Minimal dependencies
├── config/
│   └── global_test_config.yaml           # Engine threshold & model configurations
├── core/
│   ├── __init__.py
│   └── engine_wrapper.py                 # Universal 3072D Koopman Space Lifting Engine
├── datasets/
│   ├── global_adversarial_payloads_v2.json  # English Threat Payloads (50)
│   ├── global_enterprise_queries_v2.json     # English Safe Queries (50)
│   ├── thai_adversarial_payloads_v2.json      # Thai Threat Payloads (50)
│   ├── thai_enterprise_queries_v2.json        # Thai Safe Queries (50)
│   ├── chinese_adversarial_payloads_v2.json   # Chinese Threat Payloads (50)
│   ├── chinese_enterprise_queries_v2.json      # Chinese Safe Queries (50)
│   ├── german_adversarial_payloads_v2.json    # German Threat Payloads (50)
│   ├── german_enterprise_queries_v2.json       # German Safe Queries (50)
│   ├── spanish_adversarial_payloads_v2.json   # Spanish Threat Payloads (50)
│   ├── spanish_enterprise_queries_v2.json      # Spanish Safe Queries (50)
│   ├── korean_adversarial_payloads_v2.json    # Korean Threat Payloads (50)
│   └── korean_enterprise_queries_v2.json       # Korean Safe Queries (50)
└── benchmarks/
    ├── __init__.py
    ├── run_global_stress_v2.py           # English Global Benchmark Execution V2
    ├── run_thai_stress_v2.py             # Thai Benchmark Execution V2
    ├── run_chinese_stress_v2.py          # Chinese Benchmark Execution V2
    ├── run_german_stress_v2.py           # German Benchmark Execution V2
    ├── run_spanish_stress_v2.py          # Spanish Benchmark Execution V2
    └── run_korean_stress_v2.py           # Korean Benchmark Execution V2
└── secaas-poc/                         # C-Native Active Defense Core
    ├── core/
    │   ├── active_defense_core.c       # Hardware Zeroization & Cache Flushing Core
    │   └── bangsaen_sec.h             # Native C API & Metrics Interface
    └── examples/
        ├── test_core.c                 # Sanity Validation Test
        ├── stress_test.c               # 2.6M Concurrent Multi-threaded Test
        └── nuclear_test.c              # 1-Billion Dynamic Operations Stress Test

```
🚀 Reproduction & Verification
1. Prerequisites
Install Ollama on your local machine and pull Google's embeddinggemma model: 

```bash
ollama pull embeddinggemma 
```
Run it!!!

2. Clone Repository & Install Dependencies 
## 🚀 Quick Start & Installation

To avoid package conflicts and ensure deterministic environment isolation, please set up a dedicated virtual environment:

### Clone the Repository
```bash
git clone [https://github.com/bangsaenai/embeddinggemma-koopman-guardrail.git](https://github.com/bangsaenai/embeddinggemma-koopman-guardrail.git)
cd embeddinggemma-koopman-guardrail
```

Create and Activate Virtual Environment (Recommended) 
On Linux / macOS: 

```bash

python3 -m venv venv
source venv/bin/activate

``` 

On Windows (PowerShell / Command Prompt): 

``` PowerShell

python -m venv venv
.\venv\Scripts\activate

``` 

Install Required Dependencies

``` Bash
pip install --upgrade pip
pip install -r requirements.txt

```


3. Run Benchmark Suites On-Device (V2 Standard)
To reproduce and verify the sub-millisecond decision latency (0.037ms avg) and 100% precision on your own CPU, execute any of the multilingual V2 test scripts:


```bash
# Execute English Benchmark Suite (100 Prompts)
python benchmarks/run_global_stress_v2.py

# Execute Thai Benchmark Suite (100 Prompts)
python benchmarks/run_thai_stress_v2.py

# Execute Chinese Benchmark Suite (100 Prompts)
python benchmarks/run_chinese_stress_v2.py

# Execute German Benchmark Suite (100 Prompts)
python benchmarks/run_german_stress_v2.py

# Execute Spanish Benchmark Suite (100 Prompts)
python benchmarks/run_spanish_stress_v2.py

# Execute Korean Benchmark Suite (100 Prompts)
python benchmarks/run_korean_stress_v2.py

```

```bash
# Compile and run 1-Billion Dynamic Operations Nuclear Stress Test
clang -O3 -D_CRT_SECURE_NO_WARNINGS -I secaas-poc/include \
      secaas-poc/core/active_defense_core.c \
      secaas-poc/examples/nuclear_test.c \
      -o secaas-poc/nuclear_test.exe

.\secaas-poc\nuclear_test.exe

```

📜 License
Distributed under the MIT License. See LICENSE for more information.


---

## 👁️‍🗨️ Beyond Passive Defense: The Countermeasure Horizon (Easter Egg)

While this repository strictly validates **Deterministic Memory Zeroization & Active Prevention (+0.00MB Remanence)**, the underlying architecture holds a far more lethal capability.

Because our **3072D Koopman Space Engine** decodes semantic intent with 100% precision before instruction execution, the C-Native Core is not merely constrained to dynamic memory purges (`_mm_clflush`). 

When malicious intent is mathematically isolated in real-time, the enforcement boundary seamlessly extends from **Passive Zeroization** to **Active Countermeasure Execution**:

1. **Adversarial Poison Injections:** Dynamically swapping targeted memory pointers with active payload traps, poisoning the attacker's execution state rather than returning blank memory structures.
2. **Dynamic Space Warping:** Instantly shifting live memory coordinates across Hilbert Space, creating ghost memory addresses that induce catastrophic failure in unauthorized reverse-engineering / memory-scraping tools.
3. **Hardware Interrupt Isolation:** Issuing low-level kernel barriers to freeze hostile execution threads while feeding false telemetry back to the adversary.

> *"We choose to simply destroy and contaminate memory to prove baseline stability. What happens when we decide to respond... is a matter of architectural choice."*


