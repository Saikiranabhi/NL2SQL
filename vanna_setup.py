import os
from dotenv import load_dotenv

from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory

# LLMs
from vanna.integrations.google import GeminiLlmService
from vanna.integrations.openai import OpenAILlmService

# Tools
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool,
)

load_dotenv()


# ✅ LLM with fallback
def get_llm():
    if os.getenv("GOOGLE_API_KEY"):
        print("✅ Using Gemini LLM")
        return GeminiLlmService(api_key=os.getenv("GOOGLE_API_KEY"))

    elif os.getenv("GROQ_API_KEY"):
        print("⚠️ Using Groq fallback LLM")
        return OpenAILlmService(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )

    else:
        raise ValueError("❌ No LLM API key found (Gemini or Groq required)")


# ✅ Create Agent
def create_agent():
    llm = get_llm()

    # Database connection
    sql_runner = SqliteRunner("sqlite:///clinic.db")

    # Initialize Tool Registry
    tool_registry = ToolRegistry()

    # Inject tools (your version doesn't support register/add_tool)
    # tool_registry._tools = {
    #     "run_sql": RunSqlTool(sql_runner),
    #     "visualize_data": VisualizeDataTool(),
    #     "save_question_tool": SaveQuestionToolArgsTool(),
    #     "search_memory_tool": SearchSavedCorrectToolUsesTool(),
    # }

    tool_registry._tools = {
    "run_sql": RunSqlTool(sql_runner),
    "visualize_data": VisualizeDataTool(),
    "save_question_tool": SaveQuestionToolArgsTool(),  # 👈 same name
    "search_memory_tool": SearchSavedCorrectToolUsesTool(),
    }

    # Memory
    agent_memory = DemoAgentMemory()

    # User Resolver
    class SimpleUserResolver(UserResolver):
        def resolve_user(self, request):
            return User(user_id="default_user")

    # Create Agent (version-compatible)
    agent = Agent(
        llm_service=llm,
        tool_registry=tool_registry,
        user_resolver=SimpleUserResolver(),
        agent_memory=agent_memory,
        config=AgentConfig(),
    )

    return agent