
# tools/general_tools.py
import pandas as pd

def get_doctor_list() -> list[str]:
    """
    Returns a list of all unique doctor names from the schedule.
    Call this tool when the user asks which doctors are available.
    """
    print("--- Reading doctor list from schedule ---")
    try:
        df = pd.read_excel("data/doctor_schedules.xlsx")
        unique_doctors = df['doctor'].unique().tolist()
        return unique_doctors
    except Exception as e:
        return [f"Error reading doctor list: {e}"]