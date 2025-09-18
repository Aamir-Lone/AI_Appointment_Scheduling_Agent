
AI Appointment Scheduling Agent


Project Overview

The AI Appointment Scheduling Agent automates patient appointment management for clinics and healthcare providers. It leverages an AI-driven agent to:


Schedule/manage appointments 

Send automated notifications via email or SMS.(Not yet implemented)


This project combines Python, Streamlit, and modular agent design for a scalable appointment management system.

Demo
https://appointmentagent.streamlit.app/


Directory Structure
AI_Appointment_Scheduling_Agent/
│
├── app/
│   └── main.py               # Streamlit frontend
│
├── agent/
│   ├── __init__.py
│   ├── state.py              # Agent state management
│   ├── graph.py              # Agent workflow (nodes & tools)
│   └── schemas.py            # Data schemas
│
├── tools/
│   ├── __init__.py
│   ├── db_tools.py           # CSV/Excel lookups
│   ├── communication_tools.py# Email/SMS functions
│   ├── calendar_tools.py     # Optional calendar scheduling
│   └── file_tools.py         # File utilities
│
├── data/
│   ├── patients.csv          # Patient details
│   └── appointment_log.xlsx  # Appointment logs
|── .env
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation


Installation
# Clone the repository
git clone https://github.com/Aamir-Lone/AI_Appointment_Scheduling_Agent
cd AI_Appointment_Scheduling_Agent

# Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt


# set google gemini api key in AI_Appointment_Scheduling_Agent/.env
GOOGLE_API_KEY="YOUR API KEY"

Usage

Run the Streamlit app:

streamlit run app/main.py


Access the app:

Local URL: http://localhost:8501





# project by Aamir lone
# email:aamirlone004@gmail.com

