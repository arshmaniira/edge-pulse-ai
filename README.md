# ⚡ EdgePulse AI (v2.0)
**Zero-internet, ultra-low-cost AI inference infrastructure built for everyday CPUs and local hotspot networks.**

EdgePulse AI turns any standard laptop into an offline edge inference node—allowing nearby smartphones and devices to stream real-time LLM responses over a local Wi-Fi hotspot with **zero internet, zero cloud servers, and zero GPU requirements**.

## 🚀 What's New in v2.0
- **📱 Offline Mobile Hotspot Access:** Any smartphone on the same local hotspot/LAN can connect directly via browser (`http://<local-ip>:8000`) with mobile data completely off.
- **⚡ Real-Time Token Streaming:** Streams AI responses word-by-word via Server-Sent Events (SSE) instead of waiting for full paragraphs.
- **📊 Live Edge Telemetry:** Tracks real-time `tokens/sec` generation speed and end-to-end latency on CPU.
- **🌑 Zero-CDN Mobile-Responsive UI:** Serves an embedded dark-mode web app locally with zero external dependencies.

## 🛠️ Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Pull the quantized local model via Ollama:
   ```bash
   ollama pull qwen2.5:0.5b
   ```
3. Launch the EdgePulse v2.0 node:
   ```bash
   python -m uvicorn src.server:app --host 0.0.0.0 --port 8000
   ```
4. Open `http://localhost:8000` on your laptop—or connect any phone to your laptop's hotspot and visit `http://192.168.137.1:8000` with **zero internet**.
