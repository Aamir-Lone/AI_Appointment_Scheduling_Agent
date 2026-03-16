import os
import sys
import streamlit as st
import nest_asyncio

# To handle async loops in Streamlit
nest_asyncio.apply()

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.graph import app
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="AI Appointment Scheduling Agent", page_icon="🩺")

st.title("🩺 AI Medical Appointment Scheduler")
st.write("Welcome! I can help you find doctors and book appointments.")

# --- 1. Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. Display Chat History ---
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# --- 3. Chat Input and Interaction ---
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to state and display
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Invoke the Agent Graph
    with st.spinner("Thinking..."):
        try:
            # Prepare input state
            initial_state = {"messages": st.session_state.messages}
            
            # Run the graph
            output = app.invoke(initial_state)
            
            # The last message is the response
            final_response = output["messages"][-1]
            
            # Display and store assistant response
            if isinstance(final_response, AIMessage):
                st.session_state.messages.append(final_response)
                with st.chat_message("assistant"):
                    st.markdown(final_response.content)
            else:
                st.error("Received unexpected response type from agent.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
