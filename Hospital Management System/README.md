# Hospital / Clinic Management System 🏥

A clean, beginner-friendly fullstack Clinic Management System demo built with **Python (Flask)**, **Microsoft SQL Server / SSMS (pyodbc)**, and **HTML5 / CSS3 / Vanilla JavaScript**.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+
- Microsoft SQL Server / SQL Server Express (or LocalDB)
- ODBC Driver 18 or 17 for SQL Server
- SQL Server Management Studio (SSMS) (optional for inspecting the database)

### 2. Install Dependencies
Open your terminal in `e:\P1` and install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the Flask server:

```bash
python app.py
```

Open your browser and navigate to:
👉 **[http://localhost:5000](http://localhost:5000)** (or [http://localhost:5000/dashboard.html](http://localhost:5000/dashboard.html))

> **Note:** The application includes an automatic database initializer in `db.py`. On startup, it checks if `clinic_db` and the tables exist on your local SQL Server instance (`localhost\SQLEXPRESS`). If not, it creates them and populates demo seed data automatically!

---

## 🗄️ Database Setup in SSMS

If you prefer to inspect or run the SQL script manually in **SSMS (SQL Server Management Studio)**:
1. Open **SSMS** and connect to your SQL Server instance (e.g. `localhost\SQLEXPRESS`).
2. Open the file `database.sql`.
3. Click **Execute** (or press `F5`).

### Database Schema:
```
clinic_db
├── patients (id, name, age, gender, phone)
├── doctors (id, name, specialization, phone)
└── appointments (id, patient_id, doctor_id, appointment_date, reason)
```

### The Requested JOIN Query:
```sql
SELECT
    appointments.id,
    patients.name AS patient,
    doctors.name AS doctor,
    doctors.specialization,
    appointments.appointment_date,
    appointments.reason
FROM appointments
JOIN patients
    ON appointments.patient_id = patients.id
JOIN doctors
    ON appointments.doctor_id = doctors.id;
```

---

## 📁 Project Structure

```
e:\P1/
├── app.py                        # Flask Web API endpoints & static file hosting
├── db.py                         # pyodbc connection factory & automatic DB table initializer
├── config.py                     # Database connection string & server configuration
├── requirements.txt              # Python dependencies (Flask, pyodbc)
├── database.sql                  # SSMS-ready SQL script with tables and seed data
└── wwwroot/                      # Frontend HTML / CSS / JS
    ├── css/
    │   └── style.css             # Modern clinic healthcare stylesheet
    ├── js/
    │   └── api.js                # Reusable fetch client, date formatters & toast alerts
    ├── dashboard.html            # Metrics overview, quick actions & recent appointments
    ├── patients.html             # Patient list with search & delete
    ├── add_patient.html          # Form to register a new patient
    ├── edit_patient.html         # Form to update existing patient
    ├── doctors.html              # Doctor list with specialization badges
    ├── add_doctor.html           # Form to register a new doctor
    ├── edit_doctor.html          # Form to update existing doctor
    ├── appointments.html         # Appointments table showing JOIN results
    ├── add_appointment.html      # Form to book appointment with dynamic dropdowns
    └── edit_appointment.html     # Form to edit appointment details
```

---

## ✨ Features Included

| Module | Features |
| :--- | :--- |
| **Dashboard** | Real-time counts (Total Patients, Doctors, Appointments), quick booking buttons, upcoming visits preview |
| **Patients** | **Create** new patient, **Read** & search patients, **Update** details, **Delete** record with cascade |
| **Doctors** | **Create** new doctor, **Read** & search doctors, **Update** specialization/phone, **Delete** doctor |
| **Appointments** | **Create** appointment with patient & doctor dropdowns, **Read** with SQL `JOIN` query, **Update**, **Delete** |
| **UI / UX** | Responsive modern healthcare styling, floating toast feedback, confirmation dialogs, search filter bars |