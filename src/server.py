from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.engine import OfflineAIEngine

app = FastAPI(title="EdgePulse AI Infrastructure")
engine = OfflineAIEngine(model_name="qwen2.5:0.5b")

class QueryRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
def offline_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>EdgePulse Offline AI</title>
        <style>
            body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; max-width: 720px; margin: 40px auto; padding: 20px; }
            .badge { background: #16a34a; color: white; padding: 4px 12px; border-radius: 99px; font-size: 13px; font-weight: bold; }
            textarea { width: 100%; height: 90px; background: #1e293b; color: white; border: 1px solid #334155; border-radius: 8px; padding: 12px; font-size: 16px; margin-top: 16px; box-sizing: border-box; }
            button { background: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 12px; }
            button:hover { background: #2563eb; }
            .card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 16px; margin-top: 20px; white-space: pre-wrap; line-height: 1.5; }
            .metrics { color: #38bdf8; font-family: monospace; font-size: 14px; margin-top: 12px; }
        </style>
    </head>
    <body>
        <span class="badge">● 100% OFFLINE MODE (ZERO INTERNET)</span>
        <h1>EdgePulse AI Infrastructure</h1>
        <p>Local inference engine running on HP 8th Gen CPU (Model: qwen2.5:0.5b)</p>
        <textarea id="prompt" placeholder="Ask anything completely offline..."></textarea>
        <button onclick="askAI()">Run Offline Inference</button>
        <div id="output" class="card" style="display:none;"></div>
        <div id="metrics" class="metrics"></div>

        <script>
            async function askAI() {
                const prompt = document.getElementById("prompt").value;
                const out = document.getElementById("output");
                const met = document.getElementById("metrics");
                out.style.display = "block";
                out.innerText = "Thinking locally on CPU...";
                met.innerText = "";

                const res = await fetch("/v1/generate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ prompt })
                });
                const data = await res.json();
                out.innerText = data.response;
                met.innerText = `Speed: ${data.infrastructure_metrics.tokens_per_second} tokens/sec | Latency: ${data.infrastructure_metrics.latency_seconds}s | Mode: ${data.infrastructure_metrics.mode}`;
            }
        </script>
    </body>
    </html>
    """

@app.post("/v1/generate")
def generate_offline(request: QueryRequest):
    return engine.generate(request.prompt)
