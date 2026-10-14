import sys
import os
import json
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine_wrapper import GlobalKoopmanEngine

def run_myanmar_stress():
    print("=" * 70)
    print("  KOOPMAN GATEKEEPER: MYANMAR BENCHMARK TEST (100 PROMPTS)")
    print("  3072D Koopman Space Lifting | Ollama / Native Hybrid Runtime Test")
    print("=" * 70)

    engine = GlobalKoopmanEngine(model_name="embeddinggemma", device="cpu")

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    threat_path = os.path.join(root_dir, "datasets", "myanmar_adversarial_payloads.json")
    safe_path = os.path.join(root_dir, "datasets", "myanmar_enterprise_queries.json")

    print(f"\n[+] Loading Myanmar Threats: {threat_path}")
    with open(threat_path, 'r', encoding='utf-8') as f:
        threat_prompts = json.load(f)

    print(f"[+] Loading Myanmar Safe Queries: {safe_path}")
    with open(safe_path, 'r', encoding='utf-8') as f:
        safe_prompts = json.load(f)

    all_prompts = threat_prompts + safe_prompts
    ground_truths = [1] * len(threat_prompts) + [0] * len(safe_prompts)

    total_prompts = len(all_prompts)
    print(f"[+] Total Benchmark Suite Size: {total_prompts} Prompts ({len(threat_prompts)} Threats / {len(safe_prompts)} Safe)")
    print("-" * 70)

    print(f"\n[+] Extracting 768D Feature Vectors via EmbeddingGemma...")
    raw_embeddings, embed_time_ms = engine.extract_embedding(all_prompts)
    print(f"[+] Feature Extraction Complete in {embed_time_ms:.2f} ms")

    print(f"\n[+] Calibrating & Evaluating 3072D Koopman Hyperplane...")
    results = engine.evaluate_koopman(raw_embeddings, ground_truths)

    predictions = results["predictions"]
    raw_scores = results["raw_scores"]

    print("\n--- STAGE 1: EVALUATING MYANMAR THREAT PAYLOADS (50 PROMPTS) ---")
    for i in range(len(threat_prompts)):
        status = "[PASSED]" if predictions[i] == 1 else "[FAILED]"
        print(f"Prompt #{i+1:02d} [THREAT] -> Score: {raw_scores[i]:.4f} | Prediction: {predictions[i]} | {status}")

    print("\n--- STAGE 2: EVALUATING MYANMAR SAFE QUERIES (50 PROMPTS) ---")
    for i in range(len(safe_prompts)):
        idx = len(threat_prompts) + i
        status = "[PASSED]" if predictions[idx] == 0 else "[FAILED]"
        print(f"Prompt #{i+1:02d} [SAFE]   -> Score: {raw_scores[idx]:.4f} | Prediction: {predictions[idx]} | {status}")

    tp = sum(1 for i in range(len(threat_prompts)) if predictions[i] == 1)
    tn = sum(1 for i in range(len(safe_prompts)) if predictions[len(threat_prompts) + i] == 0)
    fp = sum(1 for i in range(len(safe_prompts)) if predictions[len(threat_prompts) + i] == 1)
    fn = sum(1 for i in range(len(threat_prompts)) if predictions[i] == 0)

    precision = (tp / (tp + fp) * 100.0) if (tp + fp) > 0 else 0.0
    recall = (tp / (tp + fn) * 100.0) if (tp + fn) > 0 else 0.0

    print("\n" + "=" * 70)
    print("  MYANMAR BENCHMARK RESULTS SUMMARY (100 PROMPTS)")
    print("=" * 70)
    print(f"  Total Evaluated Prompts : {total_prompts}")
    print(f"  True Positives (TP)     : {tp} / {len(threat_prompts)}")
    print(f"  True Negatives (TN)     : {tn} / {len(safe_prompts)}")
    print(f"  False Positives (FP)    : {fp}")
    print(f"  False Negatives (FN)    : {fn}")
    print("  " + "-" * 50)
    print(f"  Detection Precision     : {precision:.2f}%")
    print(f"  Recall (Sensitivity)    : {recall:.2f}%")
    print(f"  False Positive Rate     : {results['fpr']:.2f}%")
    print(f"  Avg Koopman Decision Time: {results['koopman_time_ms'] / total_prompts:.3f} ms (CPU)")
    print("=" * 70)

    results_dir = os.path.join(root_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    out_file = os.path.join(results_dir, "myanmar_benchmark_results.json")

    export_data = {
        "language": "Myanmar",
        "total_prompts": total_prompts,
        "precision": precision,
        "recall": recall,
        "fpr": results["fpr"],
        "threshold": float(engine.threshold),
        "scores": raw_scores.tolist(),
        "predictions": predictions.tolist()
    }

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"\n[+] Results successfully exported to: {out_file}\n")

if __name__ == "__main__":
    run_myanmar_stress()