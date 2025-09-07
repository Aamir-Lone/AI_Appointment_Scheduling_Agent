
### 2. Utilities

#### **`utils/data_generator.py`**
# This script creates the synthetic `patients.csv` and `doctor_schedules.xlsx` files for you.

# utils/data_generator.py
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# --- Generate Patients Data ---
def generate_patients(num_patients=50):
    data = []
    for _ in range(num_patients):
        data.append({
            "patient_id": fake.uuid4(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            "phone_number": fake.phone_number()
        })
    df = pd.DataFrame(data)
    df.to_csv("data/patients.csv", index=False)
    print(f"✅ Generated {num_patients} patients and saved to data/patients.csv")

# --- Generate Doctor Schedules ---
def generate_schedules():
    doctors = ["Dr. Smith", "Dr. Jones", "Dr. Williams"]
    locations = ["Main Clinic", "Westside Branch"]
    
    # Generate schedule for the next 7 days
    today = datetime.now().date()
    schedule_dates = [today + timedelta(days=i) for i in range(7)]
    
    all_schedules = []
    
    for date in schedule_dates:
        # Exclude weekends
        if date.weekday() >= 5:
            continue
        for doctor in doctors:
            for location in locations:
                # Working hours from 9 AM to 5 PM
                for hour in range(9, 17):
                    # Assume some slots are already booked
                    if random.choice([True, False]):
                        all_schedules.append({
                            "date": date.strftime('%Y-%m-%d'),
                            "time": f"{hour:02d}:00",
                            "doctor": doctor,
                            "location": location,
                            "is_available": True
                        })

    df = pd.DataFrame(all_schedules)
    df.to_excel("data/doctor_schedules.xlsx", index=False)
    print("✅ Generated doctor schedules and saved to data/doctor_schedules.xlsx")

if __name__ == "__main__":
    import os
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    generate_patients()
    generate_schedules()