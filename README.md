

#   AI Appointment Scheduling Agent 

## Project Overview

The AI Appointment Scheduling Agent automates patient appointment management for clinics and healthcare providers.
It leverages an AI-driven agent to: Schedule/manage appointments 
Send automated notifications via email or SMS.(Not yet implemented) 
This project combines Python, Langchain, Streamlit, and modular agent design for a scalable appointment management system.

## Demo

Try the live demo here: [https://appointmentagent.streamlit.app/]

---

## Directory Structure

```
AI_Appointment_Scheduling_Agent/
    app/
        main.py                # Streamlit frontend

    agent/
        __init__.py
        state.py               # Agent state management
        graph.py               # Agent workflow (nodes & tools)
        schemas.py             # Data schemas

    tools/
        __init__.py
        db_tools.py            # CSV/Excel lookups
        communication_tools.py # Email/SMS functions
        calendar_tools.py      # scheduling functionality
        file_tools.py          # File utilities

    data/
        patients.csv           # Patient details
        appointment_log.xlsx   # Appointment logs

    .env                       # Environment variables (API keys, etc.)
    requirements.txt           # Python dependencies
    README.md                  # Project documentation
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Aamir-Lone/AI_Appointment_Scheduling_Agent

cd AI_Appointment_Scheduling_Agent
```

2. Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set the Google Gemini API key in `.env`:

```env
GOOGLE_API_KEY="YOUR_API_KEY"
```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app/main.py
```

Open the app in your browser:

* Local URL: `http://localhost:8501`

---

## Notes

* The **email/SMS notifications feature** is planned but not yet implemented.


---

## Contact

Project by **Aamir Lone**
Email: [aamirlone004@gmail.com]

---
