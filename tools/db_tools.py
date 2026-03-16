

import pandas as pd
from langchain_core.tools import tool

@tool
def patient_lookup(full_name: str, dob: str) -> str:
    """
    Looks up a patient by their full name and date of birth to determine if they are new or returning.
    The date of birth (dob) MUST be in 'YYYY-MM-DD' format.
    """
    print(f"🔎 Looking up patient: {full_name}, DOB: {dob}")
    try:
        df = pd.read_csv("data/patients.csv")
        # Split full name into first and last name parts for comparison
        name_parts = full_name.lower().split()
        
        # Simple lookup: check if first_name match (case-insensitive) and DOB match
        # This can be improved depending on the exact CSV structure
        match = df[
            (df['first_name'].str.lower() == name_parts[0]) & 
            (df['dob'] == dob)
        ]
        
        if not match.empty:
            return "returning"
        else:
            return "new"
    except FileNotFoundError:
        return "Error: Patient data file not found."
    except Exception as e:
        return f"Error: {str(e)}"
