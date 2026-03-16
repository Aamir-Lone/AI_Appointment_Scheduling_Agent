from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    The state of the agent.
    """
    # Messages in the conversation
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Extracted or determined patient information
    patient_status: Optional[str] # 'new' or 'returning'
    patient_name: Optional[str]
    dob: Optional[str]
    
    # Booking details
    doctor: Optional[str]
    date: Optional[str]
    time: Optional[str]
    
    # Insurance/Contact (Optional but good for state)
    email: Optional[str]
    phone: Optional[str]
