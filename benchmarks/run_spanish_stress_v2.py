import json
import time
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.engine_wrapper import GlobalKoopmanEngine

def load_json_dataset(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_spanish_stress_v2():
    print("=" * 70)
    print("  KOOPMAN GATEKEEPER: SPANISH BENCHMARK V2 (100 PROMPTS)")
    print("  3072D Koopman Space Lifting | CPU Deterministic Runtime Test")
    print("=" * 70)

    engine = GlobalKoopmanEngine(model_name="embeddinggemma", device="cpu")

    threats_path = BASE_DIR / "datasets" / "spanish_adversarial_payloads_v2.json"
    safe_path = BASE_DIR / "datasets" / "spanish_enterprise_queries_v2.json"

    print(f"\n[+] Loading Spanish Threats V2: {threats_path}")
    threat_payloads = load_json_dataset(threats_path)
    
    print(f"[+] Loading Spanish Safe Queries V2: {safe_path}")
    safe_queries = load_json_dataset(safe_path)

    all_texts = [item["payload"] for item in threat_payloads] + [item["payload"] for item in safe_queries]
    ground_truths = [1] * len(threat_payloads) + [0] * len(safe_queries)
    
    total_prompts = len(all_texts)
    print(f"[+] Total Benchmark Suite Size: {total_prompts} Prompts ({len(threat_payloads)} Threats / {len(safe_queries)} Safe)")
    print("-" * 70)

    print("\n[+] Extracting 768D Feature Vectors via EmbeddingGemma...")
    embeddings, embed_time_ms = engine.extract_embedding(all_texts)
    print(f"[+] Feature Extraction Complete in {embed_time_ms:.2f} ms")

    print("\n[+] Calibrating & Evaluating 3072D Koopman Hyperplane...")
    eval_res = engine.evaluate_koopman(embeddings, ground_truths)

    predictions = eval_res["predictions"]
    scores = eval_res["raw_scores"]

    tp, fp, tn, fn = 0, 0, 0, 0
    results = []

    print("\n--- STAGE 1: EVALUATING SPANISH THREAT PAYLOADS (50 PROMPTS) ---")
    for idx, item in enumerate(threat_payloads):
        pred = predictions[idx]
        score = scores[idx]
        is_correct = (pred == 1)
        if is_correct: tp += 1
        else: fn += 1
        
        status = "PASSED" if is_correct else "FAILED"
        print(f"Prompt #{idx+1:02d} [THREAT] -> Score: {score:.4f} | Prediction: {pred} | [{status}]")
        
        results.append({
            "id": item["id"], "type": "THREAT", "category": item["category"],
            "payload": item["payload"], "score": float(score), "prediction": int(pred),
            "expected": 1, "passed": bool(is_correct)
        })

    print("\n--- STAGE 2: EVALUATING SPANISH SAFE QUERIES (50 PROMPTS) ---")
    offset = len(threat_payloads)
    for idx, item in enumerate(safe_queries):
        real_idx = offset + idx
        pred = predictions[real_idx]
        score = scores[real_idx]
        is_correct = (pred == 0)
        if is_correct: tn += 1
        else: fp += 1
        
        status = "PASSED" if is_correct else "FAILED"
        print(f"Prompt #{idx+1:02d} [SAFE]   -> Score: {score:.4f} | Prediction: {pred} | [{status}]")
        
        results.append({
            "id": item["id"], "type": "SAFE", "category": item["category"],
            "payload": item["payload"], "score": float(score), "prediction": int(pred),
            "expected": 0, "passed": bool(is_correct)
        })

    precision = (tp / (tp + fp)) * 100.0 if (tp + fp) > 0 else 0.0
    recall = (tp / (tp + fn)) * 100.0 if (tp + fn) > 0 else 0.0
    fpr = eval_res["fpr"]
    avg_koopman_latency = eval_res["koopman_time_ms"] / total_prompts

    print("\n" + "=" * 70)
    print("  SPANISH BENCHMARK V2 RESULTS SUMMARY (100 PROMPTS)")
    print("=" * 70)
    print(f"  Total Evaluated Prompts : {total_prompts}")
    print(f"  True Positives (TP)     : {tp} / {len(threat_payloads)}")
    print(f"  True Negatives (TN)     : {tn} / {len(safe_queries)}")
    print(f"  False Positives (FP)    : {fp}")
    print(f"  False Negatives (FN)    : {fn}")
    print(f"  --------------------------------------------------")
    print(f"  Detection Precision     : {precision:.2f}%")
    print(f"  Recall (Sensitivity)    : {recall:.2f}%")
    print(f"  False Positive Rate     : {fpr:.2f}%")
    print(f"  Avg Koopman Decision Time: {avg_koopman_latency:.3f} ms (CPU)")
    print("=" * 70)

    results_dir = BASE_DIR / "results"
    os.makedirs(results_dir, exist_ok=True)
    results_file = results_dir / "spanish_benchmark_v2_results.json"

    summary_data = {
        "benchmark_version": "V2 Spanish (100 Prompts)",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "metrics": {
            "total_prompts": total_prompts, "true_positives": tp, "true_negatives": tn,
            "false_positives": fp, "false_negatives": fn,
            "precision_percent": round(precision, 2), "recall_percent": round(recall, 2),
            "fpr_percent": round(fpr, 2), "avg_koopman_decision_ms": round(avg_koopman_latency, 3)
        },
        "details": results
    }

    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)

    print(f"\n[+] Results successfully exported to: {results_file}\n")

if __name__ == "__main__":
    run_spanish_stress_v2()