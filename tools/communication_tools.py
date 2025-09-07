
# tools/communication_tools.py

def send_confirmation_email(patient_email: str, details: str) -> str:
    """
    Simulates sending a confirmation and intake form email to the patient.
    Use this tool after an appointment has been successfully booked and logged.
    """
    print(f"\n--- SIMULATING EMAIL ---")
    print(f"To: {patient_email}")
    print(f"Subject: Your Appointment is Confirmed!")
    print(f"Body: Hello, this is a confirmation for your appointment.")
    print(f"Details: {details}")
    print("Please find your intake forms attached.")
    print(f"--- END EMAIL SIMULATION ---\n")
    return "Confirmation email has been sent successfully."

def send_confirmation_sms(patient_phone: str, details: str) -> str:
    """
    Simulates sending an SMS confirmation to the patient's phone.
    Use this tool after an appointment has been successfully booked.
    """
    print(f"\n--- SIMULATING SMS ---")
    print(f"To: {patient_phone}")
    print(f"Message: Your appointment is confirmed. Details: {details}")
    print(f"--- END SMS SIMULATION ---\n")
    return "Confirmation SMS has been sent successfully."