# agent/nodes.py
from langchain_core.messages import HumanMessage, AIMessage
from tools.db_tools import patient_lookup
from tools.calendar_tools import check_availability, book_appointment
from .state import AgentState

def call_model(state: AgentState):
    """A node that calls the LLM."""
    messages = state['messages']
    response = llm.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

def call_patient_lookup_tool(state: AgentState):
    """A node that calls the patient_lookup tool."""
    # The last message is the HumanMessage with the patient info
    last_message = state['messages'][-1]
    # --- To-Do: Parse name and DOB from last_message.content ---
    name = "John Doe"
    dob = "1990-01-01"
    
    status = patient_lookup(name=name, dob=dob)
    
    message = AIMessage(content=f"Patient status is: {status}")
    
    return {"patient_status": status, "messages": [message]}

# --- To-Do: Add more nodes for other tools like check_availability and book_appointment ---