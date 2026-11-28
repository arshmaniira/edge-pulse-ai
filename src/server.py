import socket
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from src.engine import OfflineAIEngine

app = FastAPI(title="EdgePulse AI v2.0 — Offline Hotspot Node")
engine = OfflineAIEngine(model_name="qwen2.5:0.5b")

class QueryRequest(BaseModel):
    prompt: str

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.43.1"

@app.get("/", response_class=HTMLResponse)
def mobile_friendly_ui():
    local_ip = get_local_ip()
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EdgePulse v2.0 Offline AI</title>
        <style>
            body {{ font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; max-width: 680px; margin: 0 auto; padding: 18px; }}
            .badge {{ display: inline-block; background: #16a34a; color: white; padding: 5px 12px; border-radius: 99px; font-size: 12px; font-weight: bold; }}
            .ip-box {{ background: #1e293b; border: 1px dashed #38bdf8; color: #38bdf8; padding: 10px 14px; border-radius: 8px; font-family: monospace; font-size: 14px; margin-top: 12px; }}
            textarea {{ width: 100%; height: 95px; background: #1e293b; color: white; border: 1px solid #334155; border-radius: 10px; padding: 12px; font-size: 16px; margin-top: 14px; box-sizing: border-box; }}
            button {{ width: 100%; background: #3b82f6; color: white; border: none; padding: 14px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px; }}
            button:active {{ background: #2563eb; }}
            .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 16px; margin-top: 18px; white-space: pre-wrap; line-height: 1.6; font-size: 16px; }}
            .metrics {{ color: #38bdf8; font-family: monospace; font-size: 13px; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <span class="badge">● EDGEPULSE v2.0 — ZERO INTERNET HOTSPOT NODE</span>
        <h2 style="margin-bottom:6px;">EdgePulse AI Infrastructure</h2>
        <div class="ip-box">📱 Connect phone on same hotspot: <b>http://{local_ip}:8000</b></div>
        <textarea id="prompt" placeholder="Ask anything offline from laptop or phone..."></textarea>
        <button onclick="streamAI()">Stream Offline Response ⚡</button>
        <div id="output" class="card" style="display:none;"></div>
        <div id="metrics" class="metrics"></div>

        <script>
            async function streamAI() {{
                const prompt = document.getElementById("prompt").value;
                if (!prompt.trim()) return;
                const out = document.getElementById("output");
                const met = document.getElementById("metrics");
                out.style.display = "block";
                out.innerText = "";
                met.innerText = "Streaming tokens from local CPU...";

                const res = await fetch("/v2/stream", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ prompt }})
                }});

                const reader = res.body.getReader();
                const decoder = new TextDecoder();

                while (true) {{
                    const {{ value, done }} = await reader.read();
                    if (done) break;
                    const lines = decoder.decode(value).split("\\n\\n");
                    for (const line of lines) {{
                        if (line.startsWith("data: ")) {{
                            const data = JSON.parse(line.slice(6));
                            if (data.token) out.innerText += data.token;
                            if (data.done) {{
                                met.innerText = `Speed: ${{data.tokens_per_second}} tokens/sec | Latency: ${{data.latency_seconds}}s | Mode: 100% Offline Hotspot`;
                            }}
                        }}
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.post("/v1/generate")
def generate_offline(request: QueryRequest):
    return engine.generate(request.prompt)

@app.post("/v2/stream")
def stream_offline(request: QueryRequest):
    return StreamingResponse(engine.generate_stream(request.prompt), media_type="text/event-stream")

