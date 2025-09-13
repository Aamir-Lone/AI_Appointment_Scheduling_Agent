



# agent/graph.py

import os
from dotenv import load_dotenv
from typing import Literal
import pandas as pd

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import your agent state and tools
from .state import AgentState
from tools.db_tools import patient_lookup
from tools.calendar_tools import check_availability, book_appointment
from tools.calendar_tools import check_availability, book_appointment, get_available_dates
from tools.calendar_tools import get_60min_slots
from tools.communication_tools import send_confirmation_email, send_confirmation_sms
from tools.general_tools import get_doctor_list

# Import the Google Gemini model
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 1. Initialize Your LLM and Tools ---

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please make sure it is set in your .env file.")

# Set up the Google Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=google_api_key)

tools = [
    patient_lookup,
    check_availability,
    book_appointment,
    send_confirmation_email,
    send_confirmation_sms,
    get_doctor_list,
    get_available_dates,
    get_60min_slots
]

# Use the standard .bind_tools() method for Gemini
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

# --- 2. Define the Agent's Nodes ---

def call_model(state: AgentState):
    """Invokes the LLM with the conversation history."""
    import logging
    logging.info("---CALLING MODEL: gemini-1.5-flash-latest---")
    messages = state['messages']
    logging.info(f"Model input messages: {messages}")
    response = llm_with_tools.invoke(messages)
    logging.info(f"Model response: {response}")
    return {"messages": [response]}

# --- 3. Define the Graph's Router (Conditional Edge) ---

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Acts as a router, deciding the next step based on the LLM's response."""
    import logging
    logging.info("---ROUTING---")
    last_message = state['messages'][-1]
    tool_calls = getattr(last_message, 'tool_calls', None)
    if tool_calls and len(tool_calls) > 0:
        logging.info("---DECISION: CALL TOOLS---")
        return "tools"
    logging.info("---DECISION: END---")
    return "end"

# --- 4. Assemble the Graph ---

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", "end": END}
)
workflow.add_edge("tools", "agent")
app = workflow.compile()