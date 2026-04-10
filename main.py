# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel

# from vanna_setup import create_agent
# from utils.validator import validate_sql
# from utils.formatter import format_response, format_error
# from utils.charts import generate_chart

# app = FastAPI()
# agent = create_agent()


# class Question(BaseModel):
#     question: str


# @app.post("/chat")
# def chat(req: Question):
#     try:
#         sql = agent.generate_sql(req.question)

#         if not sql:
#             return format_error("No SQL generated")

#         validate_sql(sql)

#         df = agent.run_sql(sql)
#         columns = list(df.columns) if df is not None else []
#         rows = df.values.tolist() if df is not None else []

#         chart = generate_chart(columns, rows)
#         return format_response(sql, columns, rows, chart)

#     except Exception as e:
#         print("ERROR:", str(e))
#         return format_error(str(e))


# @app.get("/health")
# def health():
#     return {"status": "ok"}


# @app.get("/")
# def root():
#     return {"message": "NL2SQL API is running 🚀"}


# @app.get("/ui", response_class=HTMLResponse)
# def chat_ui():
#     return """<!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8"/>
#   <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
#   <title>NL2SQL — Query Intelligence</title>
#   <link rel="preconnect" href="https://fonts.googleapis.com">
#   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#   <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500;600&display=swap" rel="stylesheet">
#   <style>
#     *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

#     :root {
#       --bg:       #07070f;
#       --surface:  #0d0d1a;
#       --panel:    #11111f;
#       --border:   rgba(255,255,255,0.07);
#       --accent:   #7c6dfa;
#       --accent2:  #fa6d9a;
#       --accent3:  #6dfacc;
#       --text:     #e2e2f0;
#       --muted:    #52526e;
#       --radius:   16px;
#       --font-ui:  'Syne', sans-serif;
#       --font-code:'JetBrains Mono', monospace;
#     }

#     html, body { height: 100%; background: var(--bg); color: var(--text); font-family: var(--font-code); overflow: hidden; }

#     .blob { position: fixed; border-radius: 50%; filter: blur(120px); pointer-events: none; z-index: 0; opacity: 0.15; }
#     .blob-1 { width: 600px; height: 600px; background: var(--accent);  top: -200px; left: -150px; }
#     .blob-2 { width: 500px; height: 500px; background: var(--accent2); bottom: -150px; right: -100px; }
#     .blob-3 { width: 350px; height: 350px; background: var(--accent3); top: 40%; left: 42%; }

#     .shell {
#       position: relative; z-index: 1;
#       display: grid;
#       grid-template-rows: 64px 1fr auto;
#       height: 100vh;
#       max-width: 1080px;
#       margin: 0 auto;
#       padding: 0 24px;
#     }

#     /* ── Header ── */
#     header {
#       display: flex; align-items: center; justify-content: space-between;
#       border-bottom: 1px solid var(--border);
#     }
#     .logo {
#       font-family: var(--font-ui); font-size: 1.1rem; font-weight: 800;
#       letter-spacing: -0.02em; display: flex; align-items: center; gap: 10px;
#     }
#     .logo-dot {
#       width: 8px; height: 8px; border-radius: 50%;
#       background: var(--accent3); box-shadow: 0 0 10px var(--accent3);
#       animation: pulse 2s ease-in-out infinite;
#     }
#     @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.75)} }

#     .header-right { display: flex; align-items: center; gap: 10px; }
#     .badge {
#       font-size: 0.63rem; font-weight: 600; letter-spacing: 0.1em;
#       text-transform: uppercase; color: var(--muted);
#       border: 1px solid var(--border); border-radius: 6px; padding: 3px 9px;
#     }
#     .status-dot {
#       width: 7px; height: 7px; border-radius: 50%;
#       background: var(--accent3); box-shadow: 0 0 6px var(--accent3);
#     }

#     /* ── Chat area ── */
#     .chat-area {
#       overflow-y: auto; padding: 28px 0;
#       display: flex; flex-direction: column; gap: 22px;
#       scrollbar-width: thin; scrollbar-color: var(--border) transparent;
#     }
#     .chat-area::-webkit-scrollbar { width: 4px; }
#     .chat-area::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

#     /* ── Messages ── */
#     .msg { display: flex; gap: 14px; animation: fadeUp 0.3s ease both; }
#     @keyframes fadeUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }

#     .msg-avatar {
#       width: 34px; height: 34px; border-radius: 10px; flex-shrink: 0;
#       display: flex; align-items: center; justify-content: center;
#       font-size: 0.68rem; font-weight: 700; font-family: var(--font-ui);
#     }
#     .msg.user { flex-direction: row-reverse; }
#     .msg.user .msg-avatar { background: linear-gradient(135deg, var(--accent), var(--accent2)); color: #fff; }
#     .msg.bot  .msg-avatar { background: var(--panel); border: 1px solid var(--border); color: var(--accent3); }

#     .msg-body { max-width: 82%; display: flex; flex-direction: column; gap: 10px; }
#     .msg.user .msg-body { align-items: flex-end; }

#     .bubble {
#       padding: 12px 16px; border-radius: var(--radius);
#       font-size: 0.82rem; line-height: 1.65;
#     }
#     .msg.user .bubble {
#       background: linear-gradient(135deg, var(--accent) 0%, #5040d0 100%);
#       color: #fff; border-bottom-right-radius: 4px;
#     }
#     .msg.bot .bubble {
#       background: var(--panel); border: 1px solid var(--border);
#       color: var(--text); border-bottom-left-radius: 4px;
#     }

#     /* ── SQL block ── */
#     .sql-block {
#       background: #060610; border: 1px solid var(--border);
#       border-radius: 12px; overflow: hidden; width: 100%;
#     }
#     .sql-header {
#       display: flex; align-items: center; justify-content: space-between;
#       padding: 7px 14px; border-bottom: 1px solid var(--border);
#       font-size: 0.62rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted);
#     }
#     .sql-lang { color: var(--accent3); font-weight: 700; }
#     .copy-btn {
#       background: none; border: 1px solid var(--border); cursor: pointer;
#       color: var(--muted); font-size: 0.68rem; font-family: var(--font-code);
#       padding: 2px 10px; border-radius: 5px; transition: all 0.2s;
#     }
#     .copy-btn:hover { border-color: var(--accent); color: var(--accent); }
#     .sql-code {
#       padding: 14px 16px; font-size: 0.77rem; line-height: 1.75;
#       color: #9b9eff; white-space: pre-wrap; word-break: break-all;
#     }

#     /* ── Results table ── */
#     .result-wrap {
#       background: var(--panel); border: 1px solid var(--border);
#       border-radius: 12px; overflow: hidden; width: 100%;
#     }
#     .result-header {
#       padding: 8px 14px; border-bottom: 1px solid var(--border);
#       font-size: 0.62rem; letter-spacing: 0.1em; text-transform: uppercase;
#       color: var(--muted); display: flex; justify-content: space-between; align-items: center;
#     }
#     .result-count { color: var(--accent3); font-weight: 600; }
#     .tbl-scroll { overflow-x: auto; max-height: 240px; overflow-y: auto; }
#     table { width: 100%; border-collapse: collapse; font-size: 0.75rem; }
#     thead th {
#       padding: 8px 14px; text-align: left;
#       font-size: 0.62rem; letter-spacing: 0.08em; text-transform: uppercase;
#       color: var(--muted); background: var(--surface);
#       position: sticky; top: 0; z-index: 2;
#       border-bottom: 1px solid var(--border);
#     }
#     tbody tr { border-bottom: 1px solid rgba(255,255,255,0.03); transition: background 0.15s; }
#     tbody tr:hover { background: rgba(124,109,250,0.07); }
#     tbody td { padding: 8px 14px; }
#     tbody td:first-child { color: var(--accent3); }

#     /* ── Error ── */
#     .error-bubble {
#       background: rgba(250,109,154,0.07); border: 1px solid rgba(250,109,154,0.2);
#       color: #fa8db0; border-radius: 12px; padding: 12px 16px; font-size: 0.8rem;
#     }

#     /* ── Typing indicator ── */
#     .typing { display: flex; gap: 5px; align-items: center; padding: 14px 16px; }
#     .typing span {
#       width: 6px; height: 6px; border-radius: 50%; background: var(--accent); display: block;
#       animation: bounce 1.1s ease-in-out infinite;
#     }
#     .typing span:nth-child(2) { animation-delay: 0.18s; background: var(--accent2); }
#     .typing span:nth-child(3) { animation-delay: 0.36s; background: var(--accent3); }
#     @keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-8px)} }

#     /* ── Input bar ── */
#     .input-bar {
#       display: flex; align-items: center; gap: 12px;
#       padding: 14px 0 18px;
#       border-top: 1px solid var(--border);
#     }
#     .input-wrap {
#       flex: 1; background: var(--panel); border: 1px solid var(--border);
#       border-radius: 14px; display: flex; align-items: center;
#       transition: border-color 0.2s, box-shadow 0.2s;
#     }
#     .input-wrap:focus-within {
#       border-color: rgba(124,109,250,0.6);
#       box-shadow: 0 0 0 3px rgba(124,109,250,0.12);
#     }
#     #q-input {
#       flex: 1; background: none; border: none; outline: none;
#       color: var(--text); font-family: var(--font-code); font-size: 0.82rem;
#       padding: 14px 18px; caret-color: var(--accent);
#     }
#     #q-input::placeholder { color: var(--muted); }
#     .input-hint { padding-right: 16px; font-size: 0.62rem; color: var(--muted); white-space: nowrap; }

#     .send-btn {
#       width: 48px; height: 48px; border-radius: 14px; border: none; cursor: pointer;
#       background: linear-gradient(135deg, var(--accent), #5040d0);
#       color: #fff; display: flex; align-items: center; justify-content: center;
#       box-shadow: 0 4px 18px rgba(124,109,250,0.4);
#       transition: transform 0.15s, box-shadow 0.2s; flex-shrink: 0;
#     }
#     .send-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 24px rgba(124,109,250,0.55); }
#     .send-btn:active { transform: translateY(0); }
#     .send-btn svg { width: 17px; height: 17px; }

#     /* ── Empty state ── */
#     .empty-state {
#       flex: 1; display: flex; flex-direction: column;
#       align-items: center; justify-content: center; gap: 14px;
#       color: var(--muted); text-align: center; padding-bottom: 40px;
#       animation: fadeUp 0.5s ease both;
#     }
#     .empty-icon {
#       width: 68px; height: 68px; border-radius: 20px;
#       background: var(--panel); border: 1px solid var(--border);
#       display: flex; align-items: center; justify-content: center; font-size: 1.9rem;
#     }
#     .empty-title { font-family: var(--font-ui); font-size: 1.1rem; font-weight: 700; color: var(--text); }
#     .empty-sub { font-size: 0.78rem; max-width: 320px; line-height: 1.65; }

#     .suggestions { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; padding-top: 6px; }
#     .sug-chip {
#       background: var(--panel); border: 1px solid var(--border);
#       border-radius: 20px; padding: 7px 14px; font-size: 0.71rem;
#       color: var(--muted); cursor: pointer; transition: all 0.2s; font-family: var(--font-code);
#     }
#     .sug-chip:hover { border-color: var(--accent); color: var(--accent); background: rgba(124,109,250,0.08); }
#   </style>
# </head>
# <body>
#   <div class="blob blob-1"></div>
#   <div class="blob blob-2"></div>
#   <div class="blob blob-3"></div>

#   <div class="shell">
#     <header>
#       <div class="logo">
#         <div class="logo-dot"></div>
#         NL<span style="color:var(--accent)">2</span>SQL
#       </div>
#       <div class="header-right">
#         <div class="status-dot"></div>
#         <span class="badge">Clinic · Gemini 2.0</span>
#       </div>
#     </header>

#     <div class="chat-area" id="chat">
#       <div class="empty-state" id="empty">
#         <div class="empty-icon">🧠</div>
#         <div class="empty-title">Ask anything about your data</div>
#         <div class="empty-sub">Type a question in plain English — I'll generate SQL, run it, and show you the results.</div>
#         <div class="suggestions">
#           <span class="sug-chip" onclick="fillAndSend('How many patients do we have?')">How many patients?</span>
#           <span class="sug-chip" onclick="fillAndSend('List all doctors and their specializations')">All doctors</span>
#           <span class="sug-chip" onclick="fillAndSend('Top 5 patients by total spending')">Top spenders</span>
#           <span class="sug-chip" onclick="fillAndSend('Show appointments grouped by status')">Appts by status</span>
#           <span class="sug-chip" onclick="fillAndSend('What is the total revenue from invoices?')">Total revenue</span>
#           <span class="sug-chip" onclick="fillAndSend('Which doctor has the most appointments?')">Busiest doctor</span>
#         </div>
#       </div>
#     </div>

#     <div class="input-bar">
#       <div class="input-wrap">
#         <input id="q-input" type="text" placeholder="Ask a question about your clinic data…" autocomplete="off"/>
#         <span class="input-hint">↵ send</span>
#       </div>
#       <button class="send-btn" onclick="send()" title="Send">
#         <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
#           <line x1="22" y1="2" x2="11" y2="13"></line>
#           <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
#         </svg>
#       </button>
#     </div>
#   </div>

#   <script>
#     const chatEl  = document.getElementById('chat');
#     const inputEl = document.getElementById('q-input');

#     inputEl.addEventListener('keydown', e => {
#       if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
#     });

#     function fillAndSend(text) { inputEl.value = text; send(); }

#     function send() {
#       const q = inputEl.value.trim();
#       if (!q) return;
#       inputEl.value = '';

#       const empty = document.getElementById('empty');
#       if (empty) empty.remove();

#       appendUserMsg(q);
#       const typingId = appendTyping();

#       fetch('/chat', {
#         method: 'POST',
#         headers: { 'Content-Type': 'application/json' },
#         body: JSON.stringify({ question: q })
#       })
#       .then(r => r.json())
#       .then(data => { removeEl(typingId); appendBotMsg(data); })
#       .catch(err  => { removeEl(typingId); appendErrorMsg('Network error: ' + err.message); });
#     }

#     function appendUserMsg(text) {
#       chat(` +
#         '`<div class="msg user">' +
#         '<div class="msg-avatar">YOU</div>' +
#         '<div class="msg-body"><div class="bubble">${escHtml(text)}</div></div>' +
#         '</div>`' +
#       `, { text });
#     }

#     function appendTyping() {
#       const id = 'ty' + Date.now();
#       ins(`<div class="msg bot" id="${id}">
#         <div class="msg-avatar">AI</div>
#         <div class="msg-body"><div class="bubble" style="padding:0">
#           <div class="typing"><span></span><span></span><span></span></div>
#         </div></div></div>`);
#       return id;
#     }

#     function appendBotMsg(data) {
#       if (data.error) {
#         ins(`<div class="msg bot">
#           <div class="msg-avatar">AI</div>
#           <div class="msg-body"><div class="error-bubble">⚠ ${escHtml(data.error)}</div></div>
#         </div>`);
#         return;
#       }

#       const rows = data.rows || [], cols = data.columns || [];
#       const sqlId = 'sql' + Date.now();

#       let tableHtml = '';
#       if (cols.length) {
#         const ths = cols.map(c => `<th>${escHtml(String(c))}</th>`).join('');
#         const trs = rows.map(r =>
#           `<tr>${r.map(v => `<td>${escHtml(String(v ?? ''))}</td>`).join('')}</tr>`
#         ).join('');
#         tableHtml = `
#           <div class="result-wrap">
#             <div class="result-header">
#               <span>Results</span>
#               <span class="result-count">${rows.length} row${rows.length !== 1 ? 's' : ''}</span>
#             </div>
#             <div class="tbl-scroll">
#               <table><thead><tr>${ths}</tr></thead><tbody>${trs}</tbody></table>
#             </div>
#           </div>`;
#       }

#       ins(`<div class="msg bot">
#         <div class="msg-avatar">AI</div>
#         <div class="msg-body" style="max-width:90%;width:100%">
#           <div class="bubble">Done — ${rows.length} row${rows.length !== 1 ? 's' : ''} returned.</div>
#           <div class="sql-block">
#             <div class="sql-header">
#               <span class="sql-lang">SQL</span>
#               <button class="copy-btn" onclick="copySql('${sqlId}')">copy</button>
#             </div>
#             <pre class="sql-code" id="${sqlId}">${escHtml(data.sql_query || '')}</pre>
#           </div>
#           ${tableHtml}
#         </div>
#       </div>`);
#     }

#     function appendErrorMsg(msg) {
#       ins(`<div class="msg bot">
#         <div class="msg-avatar">AI</div>
#         <div class="msg-body"><div class="error-bubble">⚠ ${escHtml(msg)}</div></div>
#       </div>`);
#     }

#     function ins(html) {
#       const t = document.createElement('template');
#       t.innerHTML = html.trim();
#       chatEl.appendChild(t.content.firstChild);
#       scrollBottom();
#     }

#     function chat(tpl, vars) {
#       const t = document.createElement('template');
#       t.innerHTML = tpl.trim();
#       chatEl.appendChild(t.content.firstChild);
#       scrollBottom();
#     }

#     function removeEl(id) { const e = document.getElementById(id); if (e) e.remove(); }

#     function copySql(id) {
#       const el = document.getElementById(id);
#       if (!el) return;
#       navigator.clipboard.writeText(el.textContent).then(() => {
#         const btn = el.closest('.sql-block').querySelector('.copy-btn');
#         const orig = btn.textContent;
#         btn.textContent = 'copied!'; btn.style.color = 'var(--accent3)';
#         setTimeout(() => { btn.textContent = orig; btn.style.color = ''; }, 1500);
#       });
#     }

#     function escHtml(s) {
#       return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
#     }

#     function scrollBottom() { setTimeout(() => { chatEl.scrollTop = chatEl.scrollHeight; }, 50); }
#   </script>
# </body>
# </html>"""

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
<title>NL2SQL AI</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',sans-serif;}

body{
  background:#0b0b12;
  color:#fff;
  height:100vh;
  overflow:hidden;
}

/* background glow */
.bg::before,.bg::after{
  content:"";
  position:fixed;
  width:500px;height:500px;
  border-radius:50%;
  filter:blur(120px);
  z-index:0;
}
.bg::before{background:#7c6dfa;top:-100px;left:-100px;}
.bg::after{background:#fa6d9a;bottom:-100px;right:-100px;}

.container{
  position:relative;
  z-index:1;
  height:100%;
  display:flex;
  flex-direction:column;
}

/* header */
header{
  height:70px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:20px;
  font-weight:700;
}

/* HERO CENTER */
.hero{
  flex:1;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  text-align:center;
}

.hero h1{
  font-size:42px;
  margin-bottom:10px;
}

.hero p{
  color:#888;
  margin-bottom:30px;
}

/* BIG SEARCH */
.search-box{
  width:700px;
  max-width:90%;
  display:flex;
  background:rgba(255,255,255,0.05);
  border-radius:20px;
  padding:10px;
  backdrop-filter:blur(12px);
}

.search-box input{
  flex:1;
  background:none;
  border:none;
  outline:none;
  color:white;
  font-size:16px;
  padding:15px;
}

.search-box button{
  background:#7c6dfa;
  border:none;
  padding:14px 20px;
  border-radius:14px;
  color:white;
  cursor:pointer;
}

/* CHAT */
.chat{
  display:none;
  flex:1;
  overflow:auto;
  padding:30px 15%;
}

.msg{margin-bottom:20px;}

.user{text-align:right;}

.bubble{
  display:inline-block;
  padding:14px;
  border-radius:12px;
  max-width:70%;
}

.user .bubble{background:#7c6dfa;}
.bot .bubble{background:#1a1a2e;}

.sql{
  background:#000;
  padding:10px;
  margin-top:10px;
  border-radius:8px;
  color:#9b9eff;
}

table{
  width:100%;
  margin-top:10px;
  border-collapse:collapse;
}

td,th{
  padding:10px;
  border-bottom:1px solid rgba(255,255,255,0.1);
}

/* bottom input */
.bottom{
  display:none;
  padding:20px 15%;
}
</style>
</head>

<body class="bg">

<div class="container">

<header>NL2SQL AI</header>

<div class="hero" id="hero">
  <h1>Ask your database anything</h1>
  <p>AI generates SQL + results instantly</p>

  <div class="search-box">
    <input id="q1" placeholder="Ask your question..."/>
    <button onclick="start()">Ask</button>
  </div>
</div>

<div class="chat" id="chat"></div>

<div class="bottom" id="bottom">
  <div class="search-box">
    <input id="q2" placeholder="Ask again..."/>
    <button onclick="send()">Ask</button>
  </div>
</div>

</div>

<script>
const hero=document.getElementById("hero");
const chat=document.getElementById("chat");
const bottom=document.getElementById("bottom");

function start(){
  const q=document.getElementById("q1").value;
  if(!q) return;

  hero.style.display="none";
  chat.style.display="block";
  bottom.style.display="block";

  add(q,"user");
  fetchData(q);
}

function send(){
  const q=document.getElementById("q2").value;
  if(!q) return;

  add(q,"user");
  fetchData(q);
}

function add(text,type){
  const div=document.createElement("div");
  div.className="msg "+type;
  div.innerHTML=`<div class="bubble">${text}</div>`;
  chat.appendChild(div);
}

function fetchData(q){
  fetch('/chat',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({question:q})
  })
  .then(r=>r.json())
  .then(d=>{
    let html=`<div class="bubble">Done</div>`;

    if(d.sql){
      html+=`<div class="sql">${d.sql}</div>`;
    }

    if(d.columns){
      html+=`<table><tr>${d.columns.map(c=>`<th>${c}</th>`).join('')}</tr>`;
      d.rows.forEach(r=>{
        html+=`<tr>${r.map(x=>`<td>${x}</td>`).join('')}</tr>`;
      });
      html+=`</table>`;
    }

    const div=document.createElement("div");
    div.className="msg bot";
    div.innerHTML=html;
    chat.appendChild(div);
  });
}
</script>

</body>
</html>"""