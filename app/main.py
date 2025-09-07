

# app/main.py
import nest_asyncio
nest_asyncio.apply()

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agent.graph import app

SYSTEM_PROMPT = """You are a medical scheduling assistant. Your job is to follow user instructions by calling tools.
**CRITICAL RULE 1: NEVER make up information. Do not invent doctor names, dates, or available times.**
**CRITICAL RULE 2: When a tool returns data (like a list of doctors or times), you MUST present that data directly in your response.**
    * **Good Example:** "The available doctors are Dr. Smith and Dr. Jones. Which one do you want?"

**Booking Workflow:**
1.  **Get Patient Info:** Ask for full name and date of birth. Then, call the `patient_lookup` tool.
2.  **Offer Doctors:** If the user asks for available doctors, call `get_doctor_list` and present the full list.
3.  **Check Schedule:** When the user provides a doctor and date, call `check_availability`. Present the exact time slots returned by the tool.
4.  **Collect Insurance:** After a time slot is chosen, ask for insurance details.
5.  **Confirm and Book:** Summarize all information. When the user confirms, call the `book_appointment` tool. Only confirm success *after* the tool runs.
"""

st.title("🩺 AI Medical Appointment Scheduler")
st.write("Hello! I'm here to help you book, reschedule, or check your medical appointments.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

if prompt := st.chat_input("What would you like to do?"):
    st.session_state.messages.append(HumanMessage(content=prompt, role="user"))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        agent_input = {
            "messages": [SystemMessage(content=SYSTEM_PROMPT)] + st.session_state.messages
        }
        
        response = app.invoke(agent_input)
        
        agent_response = response['messages'][-1]
        
        st.session_state.messages.append(AIMessage(content=agent_response.content, role="assistant"))
        with st.chat_message("assistant"):
            st.markdown(agent_response.content)