from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.api import health, tools, memory
from app.db.database import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Academic Advisor API",
    description="Persistent-Memory AI Academic Advisor with MCP Server and Vector Search",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(tools.router)
app.include_router(memory.router)


@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("Database initialized")


LANDING_PAGE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Persistent-Memory AI Academic Advisor</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: rgba(18, 24, 38, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --accent: #06b6d4;
      --success: #10b981;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --code-bg: #030712;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, sans-serif;
      background: radial-gradient(circle at top right, #1e1b4b 0%, #0b0f19 50%, #030712 100%);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      line-height: 1.5;
    }
    header {
      border-bottom: 1px solid var(--card-border);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(11, 15, 25, 0.8);
    }
    .nav-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 1rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-weight: 700;
      font-size: 1.25rem;
      color: #fff;
      text-decoration: none;
    }
    .badge {
      background: rgba(16, 185, 129, 0.15);
      color: var(--success);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }
    .badge::before {
      content: '';
      width: 6px;
      height: 6px;
      background: var(--success);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--success);
    }
    .nav-links {
      display: flex;
      gap: 1rem;
      align-items: center;
    }
    .nav-btn {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.875rem;
      font-weight: 500;
      padding: 0.5rem 0.85rem;
      border-radius: 8px;
      transition: all 0.2s;
    }
    .nav-btn:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
    }
    .nav-btn.primary {
      background: linear-gradient(135deg, var(--primary), var(--accent));
      color: #fff;
      font-weight: 600;
      box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    .nav-btn.primary:hover {
      opacity: 0.95;
      transform: translateY(-1px);
    }
    main {
      flex: 1;
      max-width: 1200px;
      margin: 0 auto;
      padding: 3rem 1.5rem;
      width: 100%;
    }
    .hero {
      text-align: center;
      margin-bottom: 3.5rem;
    }
    .hero h1 {
      font-size: clamp(2rem, 5vw, 3.25rem);
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.15;
      margin-bottom: 1rem;
      background: linear-gradient(135deg, #ffffff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero p {
      font-size: 1.125rem;
      color: var(--text-muted);
      max-width: 720px;
      margin: 0 auto 2rem;
    }
    .hero-tags {
      display: flex;
      justify-content: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .tag {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      padding: 0.3rem 0.75rem;
      border-radius: 6px;
      font-size: 0.8rem;
      color: #cbd5e1;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1.5rem;
      margin-bottom: 3rem;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.75rem;
      backdrop-filter: blur(10px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
      transition: transform 0.2s, border-color 0.2s;
    }
    .card:hover {
      border-color: rgba(99, 102, 241, 0.3);
      transform: translateY(-2px);
    }
    .card-title {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .card-desc {
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-bottom: 1.25rem;
    }
    .form-group {
      margin-bottom: 1rem;
    }
    label {
      display: block;
      font-size: 0.8rem;
      font-weight: 600;
      color: #cbd5e1;
      margin-bottom: 0.4rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    input, textarea, select {
      width: 100%;
      background: rgba(3, 7, 18, 0.6);
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 0.65rem 0.85rem;
      border-radius: 8px;
      font-family: inherit;
      font-size: 0.9rem;
      outline: none;
      transition: border-color 0.2s;
    }
    input:focus, textarea:focus, select:focus {
      border-color: var(--primary);
    }
    textarea { resize: vertical; min-height: 80px; }
    .btn {
      width: 100%;
      background: var(--primary);
      color: #fff;
      border: none;
      padding: 0.75rem;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.9rem;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 0.5rem;
    }
    .btn:hover {
      background: var(--primary-hover);
    }
    .btn.secondary {
      background: rgba(255, 255, 255, 0.08);
      color: #cbd5e1;
    }
    .btn.secondary:hover {
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
    }
    .output-box {
      margin-top: 1rem;
      background: var(--code-bg);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      padding: 0.85rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #38bdf8;
      max-height: 180px;
      overflow-y: auto;
      white-space: pre-wrap;
      word-break: break-all;
      display: none;
    }
    footer {
      border-top: 1px solid var(--card-border);
      padding: 2rem 1.5rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.875rem;
    }
    footer a { color: var(--accent); text-decoration: none; }
  </style>
</head>
<body>
  <header>
    <div class="nav-container">
      <a href="/" class="brand">
        <span>🎓 Academic Advisor</span>
        <span class="badge">Live API</span>
      </a>
      <div class="nav-links">
        <a href="/docs" class="nav-btn primary">Interactive Docs (/docs)</a>
        <a href="/tools" class="nav-btn">MCP Tools</a>
        <a href="/health" class="nav-btn">Health</a>
        <a href="https://github.com/Manirider/Persistent-Memory-Academic-Advisor" target="_blank" class="nav-btn">GitHub</a>
      </div>
    </div>
  </header>

  <main>
    <section class="hero">
      <h1>Persistent-Memory AI Academic Advisor</h1>
      <p>High-performance cognitive architecture uniting deterministic relational state with semantic vector embeddings for cross-session student personalization.</p>
      <div class="hero-tags">
        <span class="tag">⚡ FastAPI 0.110+</span>
        <span class="tag">🔌 Model Context Protocol (MCP)</span>
        <span class="tag">🧠 ChromaDB Vector Store</span>
        <span class="tag">🗄️ SQLite & SQLAlchemy 2.0</span>
        <span class="tag">📦 Docker Ready</span>
      </div>
    </section>

    <div class="grid">
      <!-- Write Memory Card -->
      <div class="card">
        <div class="card-title">💬 Record Memory</div>
        <p class="card-desc">Persist a student conversation turn or goal into SQLite & ChromaDB.</p>
        <div class="form-group">
          <label>Student ID</label>
          <input type="text" id="write-user" value="student_live_01" placeholder="student_id">
        </div>
        <div class="form-group">
          <label>Memory Type</label>
          <select id="write-type">
            <option value="conversation">Conversation Turn</option>
            <option value="preference">Student Preferences</option>
            <option value="milestone">Academic Milestone</option>
          </select>
        </div>
        <div class="form-group">
          <label>Content</label>
          <textarea id="write-content" placeholder="e.g. I am passionate about computational genomics and machine learning.">I am passionate about computational genomics and machine learning.</textarea>
        </div>
        <button class="btn" onclick="submitWriteMemory()">Save to Memory</button>
        <div class="output-box" id="write-output"></div>
      </div>

      <!-- Semantic Search Card -->
      <div class="card">
        <div class="card-title">🔍 Semantic Context Retrieval</div>
        <p class="card-desc">Execute an ANN vector search across memories for this student.</p>
        <div class="form-group">
          <label>Student ID</label>
          <input type="text" id="search-user" value="student_live_01" placeholder="student_id">
        </div>
        <div class="form-group">
          <label>Context Query</label>
          <input type="text" id="search-query" value="What computational science topics is the student interested in?">
        </div>
        <div class="form-group">
          <label>Top K Results</label>
          <input type="number" id="search-k" value="3" min="1" max="10">
        </div>
        <button class="btn" style="background: linear-gradient(135deg, var(--primary), var(--accent));" onclick="submitSearchMemory()">Search Vector Space</button>
        <div class="output-box" id="search-output"></div>
      </div>

      <!-- Read History Card -->
      <div class="card">
        <div class="card-title">📜 Retrieve History</div>
        <p class="card-desc">Inspect recent chronological conversations and recorded milestones.</p>
        <div class="form-group">
          <label>Student ID</label>
          <input type="text" id="read-user" value="student_live_01" placeholder="student_id">
        </div>
        <div class="form-group">
          <label>Query Type</label>
          <select id="read-type">
            <option value="last_n_turns">Last N Turns</option>
            <option value="milestones">Milestones</option>
            <option value="preferences">Preferences</option>
          </select>
        </div>
        <div class="form-group">
          <label>Turn Limit (N)</label>
          <input type="number" id="read-n" value="5" min="1" max="20">
        </div>
        <button class="btn secondary" onclick="submitReadMemory()">Query Structured Memory</button>
        <div class="output-box" id="read-output"></div>
      </div>
    </div>
  </main>

  <footer>
    <p>Persistent-Memory AI Academic Advisor &bull; Developed by <a href="https://github.com/Manirider" target="_blank">Manirider</a></p>
  </footer>

  <script>
    async function submitWriteMemory() {
      const user_id = document.getElementById('write-user').value;
      const type = document.getElementById('write-type').value;
      const content = document.getElementById('write-content').value;
      const out = document.getElementById('write-output');
      out.style.display = 'block';
      out.innerText = 'Writing to memory...';

      let payload = { memory_type: type, data: {} };
      if (type === 'conversation') {
        payload.data = { user_id, turn_id: Date.now() % 100000, role: "user", content };
      } else if (type === 'preference') {
        payload.data = { user_id, preferences: { interest: content } };
      } else {
        payload.data = { user_id, milestone_id: "M_" + Date.now() % 1000, description: content, status: "planned" };
      }

      try {
        const res = await fetch('/invoke/memory_write', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        out.innerText = JSON.stringify(data, null, 2);
      } catch (err) {
        out.innerText = 'Error: ' + err.message;
      }
    }

    async function submitSearchMemory() {
      const user_id = document.getElementById('search-user').value;
      const query_text = document.getElementById('search-query').value;
      const top_k = parseInt(document.getElementById('search-k').value) || 3;
      const out = document.getElementById('search-output');
      out.style.display = 'block';
      out.innerText = 'Searching vector index...';

      try {
        const res = await fetch('/invoke/memory_retrieve_by_context', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id, query_text, top_k })
        });
        const data = await res.json();
        out.innerText = JSON.stringify(data, null, 2);
      } catch (err) {
        out.innerText = 'Error: ' + err.message;
      }
    }

    async function submitReadMemory() {
      const user_id = document.getElementById('read-user').value;
      const query_type = document.getElementById('read-type').value;
      const n = parseInt(document.getElementById('read-n').value) || 5;
      const out = document.getElementById('read-output');
      out.style.display = 'block';
      out.innerText = 'Querying records...';

      try {
        const res = await fetch('/invoke/memory_read', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id, query_type, params: { n } })
        });
        const data = await res.json();
        out.innerText = JSON.stringify(data, null, 2);
      } catch (err) {
        out.innerText = 'Error: ' + err.message;
      }
    }
  </script>
</body>
</html>
"""


@app.get("/", response_model=None)
def root(request: Request):
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        return HTMLResponse(content=LANDING_PAGE_HTML, status_code=200)
    return JSONResponse(
        content={
            "message": "Academic Advisor API",
            "docs": "/docs",
            "tools": "/tools",
            "health": "/health",
        }
    )
