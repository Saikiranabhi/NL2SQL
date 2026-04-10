from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from vanna_setup import create_agent
from utils.validator import validate_sql
from utils.formatter import format_response, format_error
from utils.charts import generate_chart

app = FastAPI()
agent = create_agent()


class Question(BaseModel):
    question: str


@app.post("/chat")
def chat(req: Question):
    try:
        sql = agent.generate_sql(req.question)

        if not sql:
            return format_error("No SQL generated")

        validate_sql(sql)

        df = agent.run_sql(sql)
        columns = list(df.columns) if df is not None else []
        rows = df.values.tolist() if df is not None else []

        chart = generate_chart(columns, rows)
        return format_response(sql, columns, rows, chart)

    except Exception as e:
        print("ERROR:", str(e))
        return format_error(str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "NL2SQL API is running 🚀"}


@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NL2SQL — Clinic Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --ink:       #0d0d14;
  --ink2:      #1a1a28;
  --ink3:      #252538;
  --glass:     rgba(255,255,255,0.04);
  --glass2:    rgba(255,255,255,0.07);
  --rim:       rgba(255,255,255,0.09);
  --rim2:      rgba(255,255,255,0.15);
  --gold:      #c9a96e;
  --gold2:     #e8c88a;
  --rose:      #d4607a;
  --teal:      #4ecdc4;
  --muted:     rgba(255,255,255,0.35);
  --text:      rgba(255,255,255,0.88);
  --radius:    14px;
  --serif:     'DM Serif Display', Georgia, serif;
  --mono:      'DM Mono', monospace;
  --sans:      'DM Sans', sans-serif;
}

html, body {
  height: 100%;
  background: var(--ink);
  color: var(--text);
  font-family: var(--sans);
  overflow: hidden;
}

/* ── Animated mesh background ── */
.bg-mesh {
  position: fixed; inset: 0; z-index: 0; overflow: hidden;
}

.bg-mesh::before {
  content: '';
  position: absolute; inset: -50%;
  background:
    radial-gradient(ellipse 800px 600px at 20% 30%, rgba(201,169,110,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 600px 800px at 80% 70%, rgba(212,96,122,0.10) 0%, transparent 60%),
    radial-gradient(ellipse 700px 500px at 50% 90%, rgba(78,205,196,0.07) 0%, transparent 60%);
  animation: meshDrift 18s ease-in-out infinite alternate;
}

@keyframes meshDrift {
  0%   { transform: translate(0,0) rotate(0deg) scale(1); }
  33%  { transform: translate(30px,-20px) rotate(1deg) scale(1.02); }
  66%  { transform: translate(-20px,30px) rotate(-1deg) scale(0.98); }
  100% { transform: translate(10px,10px) rotate(0.5deg) scale(1.01); }
}

/* Grid overlay */
.bg-grid {
  position: fixed; inset: 0; z-index: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 48px 48px;
}

/* Vignette */
.bg-vignette {
  position: fixed; inset: 0; z-index: 0;
  background: radial-gradient(ellipse 120% 100% at 50% 0%, transparent 40%, rgba(13,13,20,0.7) 100%);
}

/* ── Layout shell ── */
.shell {
  position: relative; z-index: 1;
  height: 100vh;
  display: grid;
  grid-template-rows: 68px 1fr auto;
  max-width: 960px;
  margin: 0 auto;
  padding: 0 28px;
}

/* ── Header ── */
header {
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid var(--rim);
}

.logo {
  font-family: var(--serif);
  font-size: 1.35rem;
  letter-spacing: -0.01em;
  display: flex; align-items: center; gap: 12px;
}

.logo-icon {
  width: 32px; height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--gold) 0%, var(--rose) 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem;
  box-shadow: 0 4px 16px rgba(201,169,110,0.3);
}

.logo em {
  font-style: italic;
  color: var(--gold);
}

.hdr-pills {
  display: flex; gap: 8px; align-items: center;
}

.pill {
  font-family: var(--mono);
  font-size: 0.62rem;
  letter-spacing: 0.06em;
  padding: 4px 10px;
  border-radius: 20px;
  border: 1px solid var(--rim);
  color: var(--muted);
  background: var(--glass);
}

.pill.live {
  border-color: rgba(78,205,196,0.3);
  color: var(--teal);
  background: rgba(78,205,196,0.06);
}

.pulse-dot {
  display: inline-block;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--teal);
  margin-right: 5px;
  animation: pulse 2.4s ease-in-out infinite;
  box-shadow: 0 0 6px var(--teal);
}

@keyframes pulse {
  0%,100% { opacity:1; transform:scale(1); }
  50%      { opacity:0.4; transform:scale(0.7); }
}

/* ── Chat area ── */
.chat {
  overflow-y: auto;
  padding: 32px 0 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  scrollbar-width: thin;
  scrollbar-color: var(--rim) transparent;
}

.chat::-webkit-scrollbar { width: 3px; }
.chat::-webkit-scrollbar-thumb { background: var(--rim); border-radius: 3px; }

/* ── Hero / empty state ── */
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  text-align: center;
  gap: 20px;
  padding-bottom: 40px;
  animation: fadeUp 0.6s ease both;
}

@keyframes fadeUp {
  from { opacity:0; transform:translateY(16px); }
  to   { opacity:1; transform:translateY(0); }
}

.hero-badge {
  font-family: var(--mono);
  font-size: 0.65rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gold);
  border: 1px solid rgba(201,169,110,0.3);
  background: rgba(201,169,110,0.06);
  padding: 5px 14px;
  border-radius: 20px;
}

.hero h1 {
  font-family: var(--serif);
  font-size: clamp(2rem, 5vw, 3rem);
  line-height: 1.15;
  letter-spacing: -0.02em;
  max-width: 560px;
}

.hero h1 em {
  font-style: italic;
  background: linear-gradient(90deg, var(--gold), var(--rose));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero p {
  font-size: 0.88rem;
  color: var(--muted);
  max-width: 380px;
  line-height: 1.7;
}

/* Suggestion chips */
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  padding-top: 4px;
}

.chip {
  font-family: var(--mono);
  font-size: 0.71rem;
  padding: 8px 14px;
  border-radius: 24px;
  border: 1px solid var(--rim);
  background: var(--glass);
  color: var(--muted);
  cursor: pointer;
  transition: all 0.2s;
}

.chip:hover {
  border-color: rgba(201,169,110,0.4);
  color: var(--gold2);
  background: rgba(201,169,110,0.06);
  transform: translateY(-1px);
}

/* ── Messages ── */
.msg {
  display: flex;
  gap: 14px;
  animation: fadeUp 0.3s ease both;
}

.msg.user { flex-direction: row-reverse; }

.avatar {
  width: 34px; height: 34px;
  border-radius: 10px;
  flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--mono);
  font-size: 0.6rem;
  font-weight: 500;
  letter-spacing: 0.05em;
}

.msg.user .avatar {
  background: linear-gradient(135deg, var(--gold) 0%, var(--rose) 100%);
  color: #fff;
}

.msg.bot .avatar {
  background: var(--glass2);
  border: 1px solid var(--rim);
  color: var(--teal);
}

.msg-body {
  max-width: 84%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.msg.user .msg-body { align-items: flex-end; }

/* Bubble */
.bubble {
  padding: 12px 18px;
  border-radius: var(--radius);
  font-size: 0.84rem;
  line-height: 1.65;
}

.msg.user .bubble {
  background: linear-gradient(135deg, rgba(201,169,110,0.2), rgba(212,96,122,0.15));
  border: 1px solid rgba(201,169,110,0.2);
  border-bottom-right-radius: 4px;
}

.msg.bot .bubble {
  background: var(--glass);
  border: 1px solid var(--rim);
  border-bottom-left-radius: 4px;
}

/* SQL card */
.sql-card {
  background: #080810;
  border: 1px solid var(--rim);
  border-radius: var(--radius);
  overflow: hidden;
  width: 100%;
}

.sql-card-hdr {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 16px;
  border-bottom: 1px solid var(--rim);
}

.sql-lang-tag {
  font-family: var(--mono);
  font-size: 0.6rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--teal);
  display: flex; align-items: center; gap: 6px;
}

.sql-lang-tag::before {
  content: '';
  display: inline-block;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--teal);
}

.copy-btn {
  font-family: var(--mono);
  font-size: 0.65rem;
  padding: 3px 10px;
  border-radius: 6px;
  border: 1px solid var(--rim);
  background: var(--glass);
  color: var(--muted);
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn:hover { border-color: var(--gold); color: var(--gold); }

.sql-code {
  padding: 16px 18px;
  font-family: var(--mono);
  font-size: 0.78rem;
  line-height: 1.8;
  color: #9fa8ff;
  white-space: pre-wrap;
  word-break: break-all;
}

/* Results table */
.results-card {
  background: var(--glass);
  border: 1px solid var(--rim);
  border-radius: var(--radius);
  overflow: hidden;
  width: 100%;
}

.results-hdr {
  display: flex; align-items: center; justify-content: space-between;
  padding: 9px 16px;
  border-bottom: 1px solid var(--rim);
  font-family: var(--mono);
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
}

.row-count {
  color: var(--gold);
  font-weight: 500;
}

.tbl-wrap {
  overflow-x: auto;
  max-height: 260px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--rim) transparent;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.76rem;
}

thead th {
  padding: 9px 16px;
  text-align: left;
  font-family: var(--mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  background: var(--ink2);
  position: sticky; top: 0; z-index: 2;
  border-bottom: 1px solid var(--rim);
}

tbody tr {
  border-bottom: 1px solid rgba(255,255,255,0.03);
  transition: background 0.15s;
}

tbody tr:hover { background: rgba(201,169,110,0.04); }

tbody td { padding: 9px 16px; }
tbody td:first-child { color: var(--gold2); font-family: var(--mono); }

/* Error */
.error-card {
  background: rgba(212,96,122,0.07);
  border: 1px solid rgba(212,96,122,0.2);
  border-radius: var(--radius);
  padding: 12px 18px;
  font-size: 0.82rem;
  color: #f09ab0;
}

/* Typing indicator */
.typing-wrap { display: flex; gap: 5px; align-items: center; padding: 14px 18px; }
.typing-wrap span {
  width: 6px; height: 6px;
  border-radius: 50%;
  display: block;
  animation: bounce 1.1s ease-in-out infinite;
}
.typing-wrap span:nth-child(1) { background: var(--gold); }
.typing-wrap span:nth-child(2) { background: var(--rose); animation-delay: 0.18s; }
.typing-wrap span:nth-child(3) { background: var(--teal); animation-delay: 0.36s; }

@keyframes bounce {
  0%,60%,100% { transform: translateY(0); }
  30%          { transform: translateY(-8px); }
}

/* ── Input bar ── */
.input-bar {
  display: flex;
  gap: 12px;
  padding: 14px 0 20px;
  border-top: 1px solid var(--rim);
}

.input-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  background: var(--glass);
  border: 1px solid var(--rim);
  border-radius: var(--radius);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-wrap:focus-within {
  border-color: rgba(201,169,110,0.4);
  box-shadow: 0 0 0 3px rgba(201,169,110,0.08);
}

.input-wrap input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  color: var(--text);
  font-family: var(--sans);
  font-size: 0.84rem;
  padding: 15px 18px;
  caret-color: var(--gold);
}

.input-wrap input::placeholder { color: var(--muted); }

.input-hint {
  padding-right: 16px;
  font-family: var(--mono);
  font-size: 0.6rem;
  color: rgba(255,255,255,0.2);
  white-space: nowrap;
}

.send-btn {
  width: 50px; height: 50px;
  border-radius: var(--radius);
  border: none;
  cursor: pointer;
  background: linear-gradient(135deg, var(--gold) 0%, var(--rose) 100%);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 20px rgba(201,169,110,0.3);
  transition: transform 0.15s, box-shadow 0.2s;
  flex-shrink: 0;
}

.send-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(201,169,110,0.45);
}

.send-btn:active { transform: translateY(0); }

.send-btn svg { width: 18px; height: 18px; }
</style>
</head>

<body>
  <div class="bg-mesh"></div>
  <div class="bg-grid"></div>
  <div class="bg-vignette"></div>

  <div class="shell">
    <header>
      <div class="logo">
        <div class="logo-icon">⚡</div>
        NL<em>2</em>SQL
      </div>
      <div class="hdr-pills">
        <span class="pill live"><span class="pulse-dot"></span>Live</span>
        <span class="pill">Clinic DB</span>
        <span class="pill">Gemini 2.0</span>
      </div>
    </header>

    <div class="chat" id="chat">
      <div class="hero" id="hero">
        <div class="hero-badge">Clinic Intelligence System</div>
        <h1>Ask your database <em>anything</em></h1>
        <p>Type a question in plain English — the AI generates SQL, runs it, and returns structured results instantly.</p>
        <div class="chips">
          <span class="chip" onclick="fillAndSend('How many patients do we have?')">How many patients?</span>
          <span class="chip" onclick="fillAndSend('List all doctors and their specializations')">All doctors</span>
          <span class="chip" onclick="fillAndSend('Top 5 patients by total spending')">Top spenders</span>
          <span class="chip" onclick="fillAndSend('Show appointments grouped by status')">Appts by status</span>
          <span class="chip" onclick="fillAndSend('What is the total revenue from invoices?')">Total revenue</span>
          <span class="chip" onclick="fillAndSend('Which doctor has the most appointments?')">Busiest doctor</span>
        </div>
      </div>
    </div>

    <div class="input-bar">
      <div class="input-wrap">
        <input id="q-input" type="text" placeholder="Ask a question about your clinic data…" autocomplete="off"/>
        <span class="input-hint">↵ send</span>
      </div>
      <button class="send-btn" onclick="send()" title="Send">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
  </div>

  <script>
    const chatEl  = document.getElementById('chat');
    const inputEl = document.getElementById('q-input');

    inputEl.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
    });

    function fillAndSend(text) { inputEl.value = text; send(); }

    function esc(s) {
      return String(s)
        .replace(/&/g,'&amp;')
        .replace(/</g,'&lt;')
        .replace(/>/g,'&gt;')
        .replace(/"/g,'&quot;');
    }

    function ins(html) {
      const t = document.createElement('template');
      t.innerHTML = html.trim();
      chatEl.appendChild(t.content.firstChild);
      scrollBottom();
    }

    function removeEl(id) { const e = document.getElementById(id); if(e) e.remove(); }

    function scrollBottom() { setTimeout(() => { chatEl.scrollTop = chatEl.scrollHeight; }, 50); }

    function send() {
      const q = inputEl.value.trim();
      if (!q) return;
      inputEl.value = '';

      const hero = document.getElementById('hero');
      if (hero) hero.remove();

      // User bubble
      ins(`<div class="msg user">
        <div class="avatar">YOU</div>
        <div class="msg-body"><div class="bubble">${esc(q)}</div></div>
      </div>`);

      // Typing indicator
      const tid = 'ty' + Date.now();
      ins(`<div class="msg bot" id="${tid}">
        <div class="avatar">AI</div>
        <div class="msg-body">
          <div class="bubble" style="padding:0">
            <div class="typing-wrap"><span></span><span></span><span></span></div>
          </div>
        </div>
      </div>`);

      fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q })
      })
      .then(r => r.json())
      .then(data => { removeEl(tid); appendBot(data); })
      .catch(err  => { removeEl(tid); appendError('Network error: ' + err.message); });
    }

    function appendBot(data) {
      if (data.error) {
        ins(`<div class="msg bot">
          <div class="avatar">AI</div>
          <div class="msg-body"><div class="error-card">⚠ ${esc(data.error)}</div></div>
        </div>`);
        return;
      }

      const rows = data.rows    || [];
      const cols = data.columns || [];
      const sql  = data.sql_query || '';   // ✅ FIXED: was d.sql, now correctly d.sql_query
      const sqlId = 'sql' + Date.now();

      // Table HTML
      let tableHtml = '';
      if (cols.length) {
        const ths = cols.map(c => `<th>${esc(String(c))}</th>`).join('');
        const trs = rows.map(r =>
          `<tr>${r.map(v => `<td>${esc(String(v ?? '—'))}</td>`).join('')}</tr>`
        ).join('');
        tableHtml = `
          <div class="results-card">
            <div class="results-hdr">
              <span>Results</span>
              <span class="row-count">${rows.length} row${rows.length !== 1 ? 's' : ''}</span>
            </div>
            <div class="tbl-wrap">
              <table>
                <thead><tr>${ths}</tr></thead>
                <tbody>${trs}</tbody>
              </table>
            </div>
          </div>`;
      }

      ins(`<div class="msg bot">
        <div class="avatar">AI</div>
        <div class="msg-body" style="max-width:92%;width:100%">
          <div class="bubble">
            Returned <strong>${rows.length}</strong> row${rows.length !== 1 ? 's' : ''}.
          </div>
          <div class="sql-card">
            <div class="sql-card-hdr">
              <span class="sql-lang-tag">SQL</span>
              <button class="copy-btn" onclick="copySql('${sqlId}')">copy</button>
            </div>
            <pre class="sql-code" id="${sqlId}">${esc(sql)}</pre>
          </div>
          ${tableHtml}
        </div>
      </div>`);
    }

    function appendError(msg) {
      ins(`<div class="msg bot">
        <div class="avatar">AI</div>
        <div class="msg-body"><div class="error-card">⚠ ${esc(msg)}</div></div>
      </div>`);
    }

    function copySql(id) {
      const el = document.getElementById(id);
      if (!el) return;
      navigator.clipboard.writeText(el.textContent).then(() => {
        const btn = el.closest('.sql-card').querySelector('.copy-btn');
        const orig = btn.textContent;
        btn.textContent = 'copied!';
        btn.style.color = 'var(--teal)';
        setTimeout(() => { btn.textContent = orig; btn.style.color = ''; }, 1600);
      });
    }
  </script>
</body>
</html>"""