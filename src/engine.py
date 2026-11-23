import time
import ollama

class OfflineAIEngine:
    def __init__(self, model_name: str = "qwen2.5:0.5b"):
        self.model_name = model_name
        print(f"EdgePulse Engine initialized with local model: {self.model_name}")

    def generate(self, prompt: str) -> dict:
        start_time = time.time()

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are EdgePulse, a fast offline AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        elapsed = round(time.time() - start_time, 2)
        reply = response["message"]["content"]
        tokens_generated = response.get("eval_count", 0)
        tokens_per_sec = round(tokens_generated / elapsed, 2) if elapsed > 0 else 0

        return {
            "response": reply,
            "infrastructure_metrics": {
                "model": self.model_name,
                "mode": "100% Offline Local Inference",
                "latency_seconds": elapsed,
                "tokens_per_second": tokens_per_sec
            }
        }
