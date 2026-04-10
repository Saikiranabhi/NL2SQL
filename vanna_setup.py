import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class DirectNL2SQL:
    """Lightweight NL2SQL using Google Gemini directly — no vanna internals needed."""

    def __init__(self, api_key: str, db_path: str):
        import google.genai as genai
        self.client = genai.Client(api_key=api_key)
        self.db_path = db_path
        self.schema = self._load_schema()
        print("✅ Schema loaded")

    def _load_schema(self) -> str:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        ddl_parts = []
        for (table,) in tables:
            cursor.execute("SELECT sql FROM sqlite_master WHERE name=?", (table,))
            row = cursor.fetchone()
            if row and row[0]:
                ddl_parts.append(row[0])
        conn.close()
        return "\n\n".join(ddl_parts)

    def generate_sql(self, question: str) -> str:
        prompt = f"""You are an expert SQL generator for SQLite databases.

Database schema:
{self.schema}

Convert this question to a valid SQLite SELECT query.
Return ONLY the raw SQL query — no markdown, no backticks, no explanation, nothing else.

Question: {question}

SQL:"""
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        sql = response.text.strip()
        # Strip markdown fences if model adds them
        if "```" in sql:
            parts = sql.split("```")
            sql = parts[1] if len(parts) > 1 else parts[0]
            if sql.lower().startswith("sql"):
                sql = sql[3:]
        return sql.strip()

    def run_sql(self, sql: str) -> pd.DataFrame:
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df


class GroqNL2SQL(DirectNL2SQL):
    """Groq fallback using OpenAI-compatible API."""

    def __init__(self, api_key: str, db_path: str):
        self.db_path = db_path
        self.api_key = api_key
        self.schema = self._load_schema()
        print("✅ Schema loaded (Groq)")

    def generate_sql(self, question: str) -> str:
        from openai import OpenAI
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        prompt = f"""You are an expert SQL generator for SQLite databases.

Database schema:
{self.schema}

Convert this question to a valid SQLite SELECT query.
Return ONLY the raw SQL — no markdown, no backticks, no explanation.

Question: {question}"""

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        sql = response.choices[0].message.content.strip()
        if "```" in sql:
            parts = sql.split("```")
            sql = parts[1] if len(parts) > 1 else parts[0]
            if sql.lower().startswith("sql"):
                sql = sql[3:]
        return sql.strip()


def create_agent():
    google_key = os.getenv("GOOGLE_API_KEY")
    groq_key   = os.getenv("GROQ_API_KEY")

    if google_key:
        print("✅ Using Gemini LLM")
        return DirectNL2SQL(api_key=google_key, db_path="clinic.db")

    elif groq_key:
        print("⚠️ Using Groq fallback LLM")
        return GroqNL2SQL(api_key=groq_key, db_path="clinic.db")

    else:
        raise ValueError("❌ No API key found. Set GOOGLE_API_KEY or GROQ_API_KEY in .env")