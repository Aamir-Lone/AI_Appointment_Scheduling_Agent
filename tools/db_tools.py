





# tools/db_tools.py
import pandas as pd

def patient_lookup(name: str, dob: str) -> str:
    """
    Looks up a patient by their full name and date of birth to determine if they are new or returning.
    The date of birth (dob) MUST be in 'YYYY-MM-DD' format.
    """
    print(f"🔎 Looking up patient: {name}, DOB: {dob}")
    try:
        df = pd.read_csv("data/patients.csv")
        # This is a simplified name check. A real system would be more robust.
        patient = df[
            (df['first_name'].str.contains(name.split()[0], case=False)) & 
            (df['dob'] == dob)
        ]
        if not patient.empty:
            return "returning"
        else:
            return "new"
    except FileNotFoundError:
        return "Error: Patient data file not found."