
# tools/calendar_tools.py
import pandas as pd
from datetime import datetime, timedelta
from tools.file_tools import export_to_excel
from tools.communication_tools import send_confirmation_email, send_confirmation_sms

def check_availability(doctor: str, date: str) -> list[str]:
    """
    Checks the doctor's schedule for a specific date to find available time slots.
    The date MUST be in 'YYYY-MM-DD' format. For example, September 8th, 2025 is '2025-09-08'.
    """
    try:
        df = pd.read_excel("data/doctor_schedules.xlsx")
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # --- MODIFIED: More robust cleaning of doctor names ---
        doctor_name_in_file = df['doctor'].str.replace('.', '', regex=False).str.lower()
        doctor_to_find = doctor.replace('.', '', regex=False).lower()

        is_available_mask = df['is_available'].astype(str).str.lower() == 'true'

        available_slots = df[
            (doctor_name_in_file == doctor_to_find) &
            (df['date'] == date) & 
            (is_available_mask)
        ]
        
        if available_slots.empty:
            return [f"No available slots found for Dr. {doctor.title()} on this day."]
            
        return available_slots['time'].tolist()
    except Exception as e:
        return [f"An error occurred: {e}"]

def book_appointment(patient_name: str, doctor: str, date: str, time: str, patient_status: str, insurance_carrier: str, insurance_id: str) -> str:
    """
    Books a patient's appointment after all information, including insurance, has been collected.
    Handles "Smart Scheduling": 60 minutes for new patients and 30 minutes for returning patients.
    Upon success, it automatically logs the appointment and sends a confirmation email and SMS.
    You MUST collect the patient's status ('new' or 'returning') and insurance details before calling this tool.
    """
    try:
        df = pd.read_excel("data/doctor_schedules.xlsx")
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # --- MODIFIED: More robust cleaning of doctor names ---
        doctor_name_in_file = df['doctor'].str.replace('.', '', regex=False).str.lower()
        doctor_to_find = doctor.replace('.', '', regex=False).lower()
        is_available_mask = df['is_available'].astype(str).str.lower() == 'true'
        
        if patient_status.lower() == 'new':
            start_time_obj = datetime.strptime(time, '%H:%M')
            end_time_obj = start_time_obj + timedelta(minutes=30)
            second_slot_time = end_time_obj.strftime('%H:%M')
            
            slot1_mask = ((doctor_name_in_file == doctor_to_find) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
            slot2_mask = ((doctor_name_in_file == doctor_to_find) & (df['date'] == date) & (df['time'] == second_slot_time) & (is_available_mask))
            
            slot1_index, slot2_index = df[slot1_mask].index, df[slot2_mask].index

            if slot1_index.empty or slot2_index.empty:
                return f"Sorry, a 60-minute appointment starting at {time} is not available. Please try another time."

            df.loc[slot1_index, ['is_available', 'patient_name']] = [False, patient_name]
            df.loc[slot2_index, ['is_available', 'patient_name']] = [False, patient_name]
            final_booking_time = f"{time} - {end_time_obj.strftime('%H:%M')}"

        else: # Returning patients
            mask = ((doctor_name_in_file == doctor_to_find) & (df['date'] == date) & (df['time'] == time) & (is_available_mask))
            if df[mask].empty:
                return f"Sorry, the slot at {time} is no longer available. Please check the availability again."
            df.loc[mask, ['is_available', 'patient_name']] = [False, patient_name]
            final_booking_time = time

        df.to_excel("data/doctor_schedules.xlsx", index=False)
        
        appointment_details = {"patient_name": patient_name, "doctor": doctor, "date": date, "time": final_booking_time, "patient_status": patient_status, "insurance_carrier": insurance_carrier, "insurance_id": insurance_id}
        export_to_excel(appointment_details)
        
        patient_email = f"{patient_name.replace(' ', '.').lower()}@example.com"
        patient_phone = "555-123-4567"
        
        send_confirmation_email(patient_email=patient_email, details=str(appointment_details))
        send_confirmation_sms(patient_phone=patient_phone, details=str(appointment_details))
        
        return f"Success! The appointment for {patient_name} for {final_booking_time} is confirmed, logged, and a confirmation email and SMS have been sent."
    except Exception as e:
        return f"An unexpected error occurred while booking: {e}"