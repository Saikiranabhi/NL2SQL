from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.responses import HTMLResponse

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
        result = agent.send_message(message=req.question)

        print("RAW RESULT:", result)  # 👈 debug

        # Handle different formats safely
        if isinstance(result, dict):
            sql = result.get("sql")
            columns = result.get("columns", [])
            rows = result.get("rows", [])
        else:
            return format_error(f"Unexpected response: {result}")

        if not sql:
            return format_error("No SQL generated")

        validate_sql(sql)

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
def chat_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NL2SQL Chat</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            #chat { max-width: 600px; margin: auto; }
            .msg { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user { background: #d1e7dd; }
            .bot { background: #f8d7da; }
        </style>
    </head>
    <body>
        <div id="chat">
            <h2>💬 NL2SQL Chat</h2>
            <div id="messages"></div>
            <input id="input" type="text" placeholder="Ask something..." style="width:80%">
            <button onclick="send()">Send</button>
        </div>

        <script>
            async function send() {
                const input = document.getElementById("input");
                const text = input.value;

                addMessage("You: " + text, "user");

                const res = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: text })
                });

                const data = await res.json();

                addMessage("Bot: " + data.message, "bot");
                addMessage("SQL: " + data.sql_query, "bot");

                input.value = "";
            }

            function addMessage(text, cls) {
                const div = document.createElement("div");
                div.className = "msg " + cls;
                div.innerText = text;
                document.getElementById("messages").appendChild(div);
            }
        </script>
    </body>
    </html>
    """