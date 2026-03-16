import pandas as pd
from datetime import datetime, timedelta
from langchain_core.tools import tool
import os

# Helper to find consecutive slots for new patients
def _find_consecutive_slots(times, count=2):
    def time_to_minutes(t):
        h, m = map(int, t.split(':'))
        return h * 60 + m
    
    sorted_times = sorted(times)
    valid_starts = []
    for i in range(len(sorted_times) - count + 1):
        is_consecutive = True
        for j in range(count - 1):
            if time_to_minutes(sorted_times[i+j+1]) - time_to_minutes(sorted_times[i+j]) != 30:
                is_consecutive = False
                break
        if is_consecutive:
            valid_starts.append(sorted_times[i])
    return valid_starts

@tool
def get_doctor_list() -> list:
    """Returns a list of all unique doctor names available in the schedule."""
    try:
        df = pd.read_excel("data/doctor_schedules.xlsx")
        return df['doctor'].unique().tolist()
    except Exception as e:
        return [f"Error: {str(e)}"]

@tool
def check_availability(doctor: str, date: str, patient_status: str) -> list:
    """
    Checks for available time slots for a doctor on a specific date.
    patient_status: 'new' (needs 60 mins) or 'returning' (needs 30 mins).
    date format: 'YYYY-MM-DD'.
    """
    try:
        df = pd.read_excel("data/doctor_schedules.xlsx")
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # Filter for doctor, date, and availability
        available_df = df[
            (df['doctor'].str.lower() == doctor.lower()) & 
            (df['date'] == date) & 
            (df['is_available'] == True)
        ]
        
        times = available_df['time'].tolist()
        
        if patient_status.lower() == 'new':
            # New patients need 60 mins = 2 consecutive 30-min slots
            valid_starts = _find_consecutive_slots(times, count=2)
            if not valid_starts:
                return ["No 60-minute slots available for new patients on this date."]
            return [f"{t} (60 min)" for t in valid_starts]
        else:
            # Returning patients need 30 mins = 1 slot
            if not times:
                return [f"No availability for Dr. {doctor} on {date}."]
            return times
            
    except Exception as e:
        return [f"Error checking availability: {str(e)}"]

@tool
def book_appointment(patient_name: str, doctor: str, date: str, time: str, patient_status: str) -> str:
    """
    Books an appointment. 
    New patients (60 mins) occupy two slots. Returning patients (30 mins) occupy one.
    """
    try:
        df = pd.read_excel("data/doctor_schedules.xlsx")
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        doctor_lower = doctor.lower()
        
        if patient_status.lower() == 'new':
            # Find the two slots
            start_dt = datetime.strptime(time, "%H:%M")
            second_slot_time = (start_dt + timedelta(minutes=30)).strftime("%H:%M")
            
            mask1 = (df['doctor'].str.lower() == doctor_lower) & (df['date'] == date) & (df['time'] == time) & (df['is_available'] == True)
            mask2 = (df['doctor'].str.lower() == doctor_lower) & (df['date'] == date) & (df['time'] == second_slot_time) & (df['is_available'] == True)
            
            if df[mask1].empty or df[mask2].empty:
                return "Error: One or both of the required slots are no longer available."
            
            df.loc[mask1, 'is_available'] = False
            df.loc[mask1, 'patient_name'] = patient_name
            df.loc[mask2, 'is_available'] = False
            df.loc[mask2, 'patient_name'] = patient_name
            booking_display = f"{time} - {(start_dt + timedelta(minutes=60)).strftime('%H:%M')}"
        else:
            mask = (df['doctor'].str.lower() == doctor_lower) & (df['date'] == date) & (df['time'] == time) & (df['is_available'] == True)
            if df[mask].empty:
                return "Error: This slot is no longer available."
            
            df.loc[mask, 'is_available'] = False
            df.loc[mask, 'patient_name'] = patient_name
            booking_display = time

        df.to_excel("data/doctor_schedules.xlsx", index=False)
        
        # Log to appointment_log too
        from tools.file_tools import export_to_excel
        export_to_excel({
            "patient_name": patient_name,
            "doctor": doctor,
            "date": date,
            "time": booking_display,
            "status": patient_status
        })

        return f"Successfully booked {patient_status} appointment for {patient_name} with Dr. {doctor} on {date} at {booking_display}."
        
    except Exception as e:
        return f"Error booking appointment: {str(e)}"
