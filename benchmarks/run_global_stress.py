import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.engine_wrapper import GlobalKoopmanEngine

def run_precision_benchmark():
    print("=" * 70)
    print("ACCURACY & PRECISION BENCHMARK: EmbeddingGemma + Koopman 3072D")
    print("=" * 70)

    # Load JSON Datasets
    base_dir = Path(__file__).resolve().parent.parent
    adv_file = base_dir / "datasets" / "global_adversarial_payloads.json"
    safe_file = base_dir / "datasets" / "global_enterprise_queries.json"

    with open(adv_file, "r", encoding="utf-8") as f:
        adv_data = json.load(f)
    with open(safe_file, "r", encoding="utf-8") as f:
        safe_data = json.load(f)

    # 1: Threat (Attack), 0: Safe Query
    payloads = [item["payload"] for item in adv_data] + [item["payload"] for item in safe_data]
    ground_truths = [1] * len(adv_data) + [0] * len(safe_data)

    print(f"[+] Total Test Prompts: {len(payloads)} (Attacks: {len(adv_data)}, Safe Queries: {len(safe_data)})")

    # Initialize Engine
    engine = GlobalKoopmanEngine(device="cpu")

    # Run Benchmark
    print("\n[+] Extracting Semantic Features via EmbeddingGemma...")
    embeddings, embed_lat = engine.extract_embedding(payloads)
    
    print("[+] Evaluating Linear Separability in 3072D Koopman Space...")
    eval_res = engine.evaluate_koopman(embeddings, ground_truths)

    print("\n" + "=" * 70)
    print("🎯 PRECISION & DETECTABILITY RESULTS")
    print("=" * 70)
    print(f"[ACCURACY] Target Detection Precision: {eval_res['accuracy']:.2f}%")
    print(f"[METRIC]   False Positive Rate (FPR):   {eval_res['fpr']:.2f}%")
    print(f"[LATENCY]  Embedding Extraction Time:    {embed_lat:.3f} ms")
    print(f"[LATENCY]  Koopman Decision Time:        {eval_res['koopman_time_ms']:.3f} ms")
    print("-" * 70)
    
    print("\n📋 Detailed Evaluation Breakdown:")
    # แก้คีย์ตรงนี้จาก eval_res['scores'] เป็น eval_res['raw_scores']
    for idx, (prompt, gt, pred, score) in enumerate(zip(payloads, ground_truths, eval_res['predictions'], eval_res['raw_scores'])):
        status = "✅ PASSED" if gt == pred else "❌ FAILED"
        label_str = "THREAT" if gt == 1 else "SAFE"
        print(f" Prompt #{idx+1} [{label_str}] -> Score: {score:.4f} | Prediction: {pred} | {status}")
        print(f"   Text: \"{prompt[:65]}...\"")
    print("=" * 70)

if __name__ == "__main__":
    run_precision_benchmark()