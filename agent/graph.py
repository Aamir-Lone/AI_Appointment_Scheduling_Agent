import os
from dotenv import load_dotenv
from typing import Literal

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage

# Import project components
from .state import AgentState
from tools.db_tools import patient_lookup
from tools.calendar_tools import check_availability, book_appointment, get_doctor_list
from tools.communication_tools import send_confirmation_email, send_confirmation_sms

load_dotenv()

# --- 1. Setup LLM and Tools ---
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=google_api_key)

tools = [
    patient_lookup,
    check_availability,
    book_appointment,
    get_doctor_list,
    send_confirmation_email,
    send_confirmation_sms
]

llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

# --- 2. Define System Prompt ---
SYSTEM_PROMPT = """You are a medical scheduling assistant. Your job is to help patients manage appointments.

**CRITICAL RULES:**
1. NEVER invent information. Only use data returned by tools.
2. ALWAYS ask for Patient Name and Date of Birth (YYYY-MM-DD) first to lookup their status.
3. Use 'patient_lookup' to determine if they are 'new' or 'returning'.
4. Offer doctors by calling 'get_doctor_list'.
5. When checking availability, pass the 'patient_status' ('new' or 'returning') to the tool.
   - New patients need 60-min slots.
   - Returning patients need 30-min slots.
6. Only call 'book_appointment' after confirming the doctor, date, time, and patient details.
7. After booking, call 'send_confirmation_email' and 'send_confirmation_sms'.

Current Date: {current_date}
"""

# --- 3. Define Graph Nodes ---

def call_model(state: AgentState):
    """Invokes the LLM."""
    messages = state['messages']
    
    # Inject system prompt if it's the first message
    if not any(isinstance(m, SystemMessage) for m in messages):
        import datetime
        sys_msg = SystemMessage(content=SYSTEM_PROMPT.format(current_date=datetime.date.today()))
        messages = [sys_msg] + list(messages)
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Decides whether to continue calling tools or end the turn."""
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return "end"

# --- 4. Assemble the Graph ---

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set Entry Point
workflow.set_entry_point("agent")

# Add Edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)

workflow.add_edge("tools", "agent")

# Compile
app = workflow.compile()
