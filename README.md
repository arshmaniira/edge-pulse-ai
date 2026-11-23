# ⚡ EdgePulse AI
**Zero-internet, ultra-low-cost AI inference infrastructure built for everyday CPUs and offline environments.**

EdgePulse AI brings compressed Large Language Models (LLMs) to low-resource devices without requiring cloud GPUs, expensive API credits, or active internet connectivity.

## 🚀 Key Features
- **100% Offline Inference:** Runs completely air-gapped (Airplane Mode) with zero external API calls.
- **CPU-Optimized:** Engineered to run smoothly on standard laptops (tested on Intel 8th Gen CPU, 0 dedicated GPU).
- **Live Infrastructure Telemetry:** Tracks real-time `tokens/sec` generation speed and end-to-end latency.
- **Zero-CDN Web UI:** Serves an embedded dark-mode interface locally with zero external dependencies.

## 🛠️ Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Pull the quantized local model via Ollama:
   ```bash
   ollama pull qwen2.5:0.5b
   ```
3. Launch the offline inference server:
   ```bash
   python -m uvicorn src.server:app --host 0.0.0.0 --port 8000
   ```
4. Open `http://localhost:8000` in your browser (even with Wi-Fi turned off).
