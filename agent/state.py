
# agent/state.py
from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    patient_status: Optional[str]
    patient_name: Optional[str]
    dob: Optional[str]
    doctor: Optional[str]
    date: Optional[str]
    time: Optional[str]
    insurance_carrier: Optional[str]
    insurance_id: Optional[str]

