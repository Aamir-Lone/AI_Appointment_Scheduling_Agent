# tools/file_tools.py
import pandas as pd
import os
from datetime import datetime

def export_to_excel(appointment_details: dict):
    """
    Exports confirmed appointment details to a log file (appointment_log.xlsx).
    Appends to the file if it exists, otherwise creates a new one.
    """
    log_file = "data/appointment_log.xlsx"
    print(f"📄 Exporting to Excel log: {appointment_details}")

    # Add a timestamp to the record
    appointment_details['booking_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    new_log_df = pd.DataFrame([appointment_details])

    try:
        # If the log file already exists, append the new record
        if os.path.exists(log_file):
            existing_log_df = pd.read_excel(log_file)
            updated_log_df = pd.concat([existing_log_df, new_log_df], ignore_index=True)
        # Otherwise, this is the first record
        else:
            updated_log_df = new_log_df

        # Save the updated log back to the file
        updated_log_df.to_excel(log_file, index=False)
        
        print(f"✅ Successfully logged appointment to {log_file}")
        return "Appointment details have been logged for administrative review."

    except Exception as e:
        print(f"❌ Error exporting to Excel: {e}")
        return "Failed to log appointment details."

# You will also need to update the tool definition in agent/graph.py
# to expect a dictionary as input for this function.