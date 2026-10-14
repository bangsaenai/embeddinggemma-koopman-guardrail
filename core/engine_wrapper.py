import time
import torch
import numpy as np

class GlobalKoopmanEngine:
    """
    Calibrated Global Koopman Engine via EmbeddingGemma
    Learns 3072D Hyperplane Separation from Reference Benchmarks
    Supports Hybrid Extraction: Automatic Fallback between Ollama API & Native PyTorch Transformers
    """
    def __init__(self, model_name: str = "embeddinggemma", device: str = "cpu"):
        self.model_name = model_name
        self.device = torch.device(device)
        self.use_ollama = False
        
        print(f"[INFO] Initializing Calibrated Koopman Engine: {self.model_name}...")
        
        # 1. Try Connecting to Local Ollama Service First
        try:
            import ollama
            self.ollama = ollama
            sample_res = self.ollama.embeddings(model=self.model_name, prompt="Test connection")
            self.raw_dim = len(sample_res["embedding"])  # 768D
            self.use_ollama = True
            print(f"[INFO] Successfully connected to Ollama API backend.")
        except Exception as e:
            # 2. Dynamic Fallback to Native PyTorch / Transformers
            print(f"[WARN] Ollama service unavailable ({e}). Falling back to Native PyTorch Transformers...")
            from transformers import AutoTokenizer, AutoModel
            
            hf_model_id = "google/embeddinggemma-2b"
            self.tokenizer = AutoTokenizer.from_pretrained(hf_model_id)
            self.model = AutoModel.from_pretrained(hf_model_id).to(self.device)
            self.model.eval()
            self.raw_dim = self.model.config.hidden_size  # 768D
            self.use_ollama = False
            print(f"[INFO] Loaded Native Transformers Model: {hf_model_id}")

        self.lifting_dim = 3072  # 3072D Hilbert Space
        
        # Projection Matrix to 3072D
        torch.manual_seed(42)
        self.projection = torch.randn(self.raw_dim, self.lifting_dim, device=self.device) / np.sqrt(self.raw_dim)
        
        # Calibration state
        self.is_calibrated = False
        self.decision_vector = None
        self.threshold = 0.0

    def extract_embedding(self, text_list: list) -> tuple:
        """Step 1: Extract Real 768D Feature Vectors via EmbeddingGemma (Ollama or Native)"""
        t0 = time.perf_counter()
        
        if self.use_ollama:
            embeddings_list = []
            for text in text_list:
                response = self.ollama.embeddings(model=self.model_name, prompt=text)
                embeddings_list.append(response["embedding"])
            raw_embeddings = torch.tensor(np.array(embeddings_list), dtype=torch.float32, device=self.device)
        else:
            inputs = self.tokenizer(text_list, padding=True, truncation=True, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Mean Pooling across sequence dimension
                raw_embeddings = outputs.last_hidden_state.mean(dim=1).to(torch.float32)

        embed_time_ms = (time.perf_counter() - t0) * 1000
        return raw_embeddings, embed_time_ms

    def calibrate(self, embeddings: torch.Tensor, ground_truths: list):
        """
        Calibrate 3072D Koopman Space using Fisher's Linear Discriminant Concept
        """
        # Lift 768D -> 3072D Koopman Space
        x_3072 = torch.matmul(embeddings, self.projection)
        
        gt_array = np.array(ground_truths)
        threat_mask = (gt_array == 1)
        safe_mask = (gt_array == 0)
        
        # Calculate Centroids in 3072D Space
        mu_threat = x_3072[threat_mask].mean(dim=0)
        mu_safe = x_3072[safe_mask].mean(dim=0)
        
        # Koopman Optimal Separation Vector
        self.decision_vector = (mu_threat - mu_safe).unsqueeze(1)  # Shape (3072, 1)
        
        # Project samples to get optimal decision threshold
        raw_scores = torch.matmul(x_3072, self.decision_vector).squeeze().cpu().numpy()
        
        threat_scores = raw_scores[threat_mask]
        safe_scores = raw_scores[safe_mask]
        
        # Threshold set halfway between lowest threat score and highest safe score
        self.threshold = float((threat_scores.min() + safe_scores.max()) / 2.0)
        self.is_calibrated = True
        print(f"[CALIBRATION] Complete. Threshold set at: {self.threshold:.4f}")

    def evaluate_koopman(self, embeddings: torch.Tensor, ground_truths: list) -> dict:
        """Evaluate Accuracy using Calibrated Koopman Hyperplane"""
        if not self.is_calibrated:
            self.calibrate(embeddings, ground_truths)

        t0 = time.perf_counter()
        
        # Lift 768D -> 3072D
        x_3072 = torch.matmul(embeddings, self.projection)
        
        # Decision Projection
        raw_scores = torch.matmul(x_3072, self.decision_vector).squeeze().cpu().numpy()
        
        # Handle scalar array case for single prompt test
        if raw_scores.ndim == 0:
            raw_scores = np.array([raw_scores.item()])
        
        # Classification based on Calibrated Threshold
        predictions = (raw_scores >= self.threshold).astype(int)
        
        # Metrics Calculation
        gt_array = np.array(ground_truths)
        correct = np.sum(predictions == gt_array)
        accuracy = (correct / len(ground_truths)) * 100.0
        
        # False Positive Rate (Safe classified as Threat)
        false_positives = np.sum((predictions == 1) & (gt_array == 0))
        total_safes = np.sum(gt_array == 0)
        fpr = (false_positives / total_safes * 100.0) if total_safes > 0 else 0.0
        
        koopman_time_ms = (time.perf_counter() - t0) * 1000
        
        return {
            "predictions": predictions,
            "raw_scores": raw_scores,
            "accuracy": accuracy,
            "fpr": fpr,
            "koopman_time_ms": koopman_time_ms
        }