import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from agent.graph import app
from langchain_core.messages import HumanMessage
import datetime

def test_agent_flow():
    print("🚀 Starting Agent Verification Test...")
    
    # 1. Test Patient Lookup
    print("\n--- Testing Patient Lookup ---")
    state_lookup = {"messages": [HumanMessage(content="Hi, I'm Jason Santiago, born 1955-09-05. Am I a returning patient?")]}
    output_lookup = app.invoke(state_lookup)
    print(f"Agent Response: {output_lookup['messages'][-1].content}")

    # 2. Test Availability Check
    print("\n--- Testing Availability Check ---")
    state_avail = {"messages": [
        HumanMessage(content="I'm a returning patient. Can you check Dr. Smith's availability for 2025-09-08?")
    ]}
    output_avail = app.invoke(state_avail)
    print(f"Agent Response: {output_avail['messages'][-1].content}")

    # 3. Test Booking
    print("\n--- Testing Booking (Simulation) ---")
    # We won't actually hit the .xlsx in a way that breaks things unless the file exist
    state_book = {"messages": [
        HumanMessage(content="I'm Jason Santiago (returning). Book Dr. Smith on 2025-09-08 at 09:00.")
    ]}
    try:
        output_book = app.invoke(state_book)
        print(f"Agent Response: {output_book['messages'][-1].content}")
    except Exception as e:
        print(f"Booking Error (Likely due to missing file context in script): {e}")

if __name__ == "__main__":
    test_agent_flow()
