# agent/schemas.py
from pydantic import BaseModel, Field

class PatientInfo(BaseModel):
    """Information to identify a patient."""
    name: str = Field(description="The patient's full name.")
    dob: str = Field(description="The patient's date of birth in YYYY-MM-DD format.")

class ScheduleRequest(BaseModel):
    """Information required to check a doctor's schedule."""
    doctor: str = Field(description="The name of the doctor.")
    date: str = Field(description="The desired date for the appointment, in YYYY-MM-DD format.")