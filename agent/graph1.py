



# # agent/graph.py

# import os
# from dotenv import load_dotenv
# from typing import Literal
# import pandas as pd # <-- ADD PANDAS IMPORT HERE

# from langgraph.graph import StateGraph, END
# from langgraph.prebuilt import ToolNode

# # Import your agent state and the REST of your tools
# from .state import AgentState
# from tools.db_tools import patient_lookup
# from tools.calendar_tools import check_availability, book_appointment
# from tools.communication_tools import send_confirmation_email
# from langchain_google_genai import ChatGoogleGenerativeAI

# # --- NEW: Define the problematic tool directly in this file for testing ---
# def get_doctor_list() -> list[str]:
#     """
#     Returns a list of all unique doctor names from the schedule.
#     Call this tool when the user asks which doctors are available.
#     """
#     print("--- Reading doctor list from schedule ---")
#     try:
#         df = pd.read_excel("data/doctor_schedules.xlsx")
#         unique_doctors = df['doctor'].unique().tolist()
#         return unique_doctors
#     except Exception as e:
#         return [f"Error reading doctor list: {e}"]
# # --------------------------------------------------------------------

# # --- 1. Initialize Your LLM and Tools ---

# load_dotenv()

# google_api_key = os.getenv("GOOGLE_API_KEY")
# if not google_api_key:
#     raise ValueError("GOOGLE_API_KEY not found. Please make sure it is set in your .env file.")

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash-latest",
#     google_api_key=google_api_key
# )

# # The tools list now uses the get_doctor_list function we just defined above
# tools = [
#     patient_lookup, 
#     check_availability, 
#     # book_appointment, 
#     #  send_confirmation_email,
#     get_doctor_list 
# ]

# llm_with_tools = llm.bind_tools(tools)
# tool_node = ToolNode(tools)


# # --- 2. Define the Agent's Nodes ---

# def call_model(state: AgentState):
#     """Invokes the LLM with the conversation history."""
#     print("---CALLING MODEL---")
#     messages = state['messages']
#     response = llm_with_tools.invoke(messages)
#     return {"messages": [response]}


# # --- 3. Define the Graph's Router (Conditional Edge) ---

# def should_continue(state: AgentState) -> Literal["tools", "end"]:
#     """Acts as a router, deciding the next step based on the LLM's response."""
#     print("---ROUTING---")
#     last_message = state['messages'][-1]
    
#     if last_message.tool_calls:
#         print("---DECISION: CALL TOOLS---")
#         return "tools"
    
#     print("---DECISION: END---")
#     return "end"


# # --- 4. Assemble the Graph ---

# workflow = StateGraph(AgentState)

# workflow.add_node("agent", call_model)
# workflow.add_node("tools", tool_node)

# workflow.set_entry_point("agent")

# workflow.add_conditional_edges(
#     "agent",
#     should_continue,
#     {
#         "tools": "tools",
#         "end": END
#     }
# )

# workflow.add_edge("tools", "agent")

# app = workflow.compile()