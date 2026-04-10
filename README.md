# 🧠 AI-Powered Natural Language to SQL (NL2SQL) System

## 📌 Overview

This project is an AI-powered backend system that converts natural language queries into SQL, executes them on a database, and returns structured results along with visualizations.

Users can interact with the system using plain English instead of writing SQL queries.

---

## 🚀 Key Features

- Natural Language → SQL conversion
- FastAPI-based REST API
- SQLite database (clinic management system)
- Secure SQL validation (SELECT-only execution)
- Plotly-based chart generation
- Agent memory for improved accuracy
- LLM fallback support (Gemini → Groq)

---

## 🏗️ Architecture

```
Client (Postman/UI)
│
▼
FastAPI Backend (main.py)
│
▼
Vanna 2.0 Agent (LLM + Tools + Memory)
│
▼
SQL Validation Layer
│
▼
SQLite Database (clinic.db)
│
▼
Result Formatter + Chart Generator
│
▼
JSON Response (data + visualization)
```

### 🔄 Flow

1. User sends a question
2. Vanna Agent converts it to SQL
3. SQL is validated for safety
4. Query is executed on SQLite
5. Results are formatted and visualized
6. Response is returned to the user

---

## 🧰 Tech Stack

| Layer             | Technology                        |
|-------------------|-----------------------------------|
| Backend API       | FastAPI                           |
| AI/Agent Layer    | Vanna 2.0                         |
| LLM Providers     | Gemini (Primary), Groq (Fallback) |
| Database          | SQLite                            |
| Visualization     | Plotly                            |
| Language          | Python 3.10+                      |
| Containerization  | Docker                            |

---

## 📁 Project Structure

```
project/
│
├── main.py               # FastAPI application
├── vanna_setup.py        # Vanna agent configuration
├── setup_database.py     # DB schema + dummy data
├── seed_memory.py        # Seed agent memory
│
├── utils/
│   ├── validator.py      # SQL validation
│   ├── formatter.py      # Response formatting
│   ├── charts.py         # Chart generation
│   └── __init__.py
│
├── clinic.db             # Generated database
├── requirements.txt
├── README.md
├── RESULTS.md
├── .env
├── Dockerfile
└── .dockerignore
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <https://github.com/Saikiranabhi/NL2SQL.git>
cd project
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

### 4️⃣ Create Database

```bash
python setup_database.py
```

### 5️⃣ Seed Agent Memory

```bash
python seed_memory.py
```

### 6️⃣ Run Server

```bash
uvicorn main:app --reload --port 8000
```

---

## 🐳 Docker Setup

### Build Image

```bash
docker build -t nl2sql-app .
```

### Run Container

```bash
docker run -p 8000:8000 nl2sql-app
```

---

## 📡 API Endpoints

### 🔹 POST `/chat`

**Request**

```json
{
  "question": "Top 5 patients by spending"
}
```

**Response**

```json
{
  "message": "Query executed successfully",
  "sql_query": "...",
  "columns": ["..."],
  "rows": ["..."],
  "row_count": 5,
  "chart": {},
  "chart_type": "bar"
}
```

### 🔹 GET `/health`

```json
{
  "status": "ok"
}
```

---

## 🛡️ Security Features

- Only `SELECT` queries allowed
- Blocks dangerous SQL keywords (`DROP`, `DELETE`, etc.)
- Prevents access to system tables

---

## 📊 Testing & Evaluation

System tested with 20 predefined queries covering:

- Aggregations
- Joins
- Time-based queries
- Filtering and grouping

👉 See [RESULTS.md](./RESULTS.md) for detailed results.

---

## ⚡ LLM Strategy

- **Primary Model:** Google Gemini
- **Fallback Model:** Groq (OpenAI-compatible API)

This ensures reliability in case of API failures.

---

## 🔮 Future Improvements

- Query caching
- Rate limiting
- Better prompt engineering
- Frontend dashboard
- Multi-database support

---

## 👨‍💻 Author

**Kiran**

---

## 📌 Note

This project was developed as part of an **AI/ML Developer Internship** technical assignment to demonstrate skills in:

- AI integration
- Backend development
- System design
- Problem solving
