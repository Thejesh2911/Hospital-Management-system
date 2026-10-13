import os
import datetime
from flask import Flask, request, jsonify, send_from_directory, abort
import config
import db

app = Flask(__name__, static_folder='wwwroot', static_url_path='')

# -------------------------------------------------------------
# CORS & OPTIONS HANDLER
# -------------------------------------------------------------
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/api/<path:dummy>', methods=['OPTIONS'])
def options_handler(dummy):
    return ('', 204)

# -------------------------------------------------------------
# STATIC FILE HOSTING (Matching ASP.NET DefaultFiles & StaticFiles)
# -------------------------------------------------------------
@app.route('/')
def root():
    return send_from_directory('wwwroot', 'dashboard.html')

@app.route('/<path:filename>')
def serve_static(filename):
    file_path = os.path.join(app.root_path, 'wwwroot', filename)
    if os.path.isfile(file_path):
        return send_from_directory('wwwroot', filename)
    abort(404)

# -------------------------------------------------------------
# PATIENT APIS (CRUD)
# -------------------------------------------------------------
@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = db.query_all("SELECT id, name, age, gender, phone FROM patients ORDER BY id DESC;")
    return jsonify(patients), 200

@app.route('/api/patients/<int:id>', methods=['GET'])
def get_patient(id):
    patient = db.query_one("SELECT id, name, age, gender, phone FROM patients WHERE id = ?;", (id,))
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    return jsonify(patient), 200

@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'message': 'Patient name is required'}), 400

    age = data.get('age')
    gender = data.get('gender')
    phone = data.get('phone')

    sql = """
        INSERT INTO patients (name, age, gender, phone)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?);
    """
    new_id = db.execute_scalar(sql, (name, age, gender, phone))
    created = {
        'id': new_id,
        'name': name,
        'age': age,
        'gender': gender,
        'phone': phone
    }
    return jsonify(created), 201

@app.route('/api/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'message': 'Patient name is required'}), 400

    age = data.get('age')
    gender = data.get('gender')
    phone = data.get('phone')

    sql = """
        UPDATE patients
        SET name = ?, age = ?, gender = ?, phone = ?
        WHERE id = ?;
    """
    affected = db.execute_non_query(sql, (name, age, gender, phone, id))
    if affected == 0:
        return jsonify({'message': 'Patient not found'}), 404

    updated = {
        'id': id,
        'name': name,
        'age': age,
        'gender': gender,
        'phone': phone
    }
    return jsonify(updated), 200

@app.route('/api/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    sql = "DELETE FROM patients WHERE id = ?;"
    affected = db.execute_non_query(sql, (id,))
    if affected == 0:
        return jsonify({'message': 'Patient not found'}), 404
    return jsonify({'message': 'Patient deleted successfully'}), 200


# -------------------------------------------------------------
# DOCTOR APIS (CRUD)
# -------------------------------------------------------------
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    doctors = db.query_all("SELECT id, name, specialization, phone FROM doctors ORDER BY id DESC;")
    return jsonify(doctors), 200

@app.route('/api/doctors/<int:id>', methods=['GET'])
def get_doctor(id):
    doctor = db.query_one("SELECT id, name, specialization, phone FROM doctors WHERE id = ?;", (id,))
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    return jsonify(doctor), 200

@app.route('/api/doctors', methods=['POST'])
def create_doctor():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'message': 'Doctor name is required'}), 400

    specialization = data.get('specialization')
    phone = data.get('phone')

    sql = """
        INSERT INTO doctors (name, specialization, phone)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?);
    """
    new_id = db.execute_scalar(sql, (name, specialization, phone))
    created = {
        'id': new_id,
        'name': name,
        'specialization': specialization,
        'phone': phone
    }
    return jsonify(created), 201

@app.route('/api/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'message': 'Doctor name is required'}), 400

    specialization = data.get('specialization')
    phone = data.get('phone')

    sql = """
        UPDATE doctors
        SET name = ?, specialization = ?, phone = ?
        WHERE id = ?;
    """
    affected = db.execute_non_query(sql, (name, specialization, phone, id))
    if affected == 0:
        return jsonify({'message': 'Doctor not found'}), 404

    updated = {
        'id': id,
        'name': name,
        'specialization': specialization,
        'phone': phone
    }
    return jsonify(updated), 200

@app.route('/api/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    sql = "DELETE FROM doctors WHERE id = ?;"
    affected = db.execute_non_query(sql, (id,))
    if affected == 0:
        return jsonify({'message': 'Doctor not found'}), 404
    return jsonify({'message': 'Doctor deleted successfully'}), 200


# -------------------------------------------------------------
# APPOINTMENT APIS (CRUD + JOIN)
# -------------------------------------------------------------
APPOINTMENT_SELECT_SQL = """
    SELECT
        appointments.id,
        appointments.patient_id AS patientId,
        patients.name AS patient,
        appointments.doctor_id AS doctorId,
        doctors.name AS doctor,
        doctors.specialization AS specialization,
        appointments.appointment_date AS appointmentDate,
        appointments.reason AS reason
    FROM appointments
    JOIN patients
        ON appointments.patient_id = patients.id
    JOIN doctors
        ON appointments.doctor_id = doctors.id
"""

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    sql = f"{APPOINTMENT_SELECT_SQL} ORDER BY appointments.appointment_date ASC;"
    appointments = db.query_all(sql)
    return jsonify(appointments), 200

@app.route('/api/appointments/<int:id>', methods=['GET'])
def get_appointment(id):
    sql = f"{APPOINTMENT_SELECT_SQL} WHERE appointments.id = ?;"
    appointment = db.query_one(sql, (id,))
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    return jsonify(appointment), 200

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json(silent=True) or {}
    patient_id = data.get('patientId') or data.get('patient_id')
    doctor_id = data.get('doctorId') or data.get('doctor_id')
    appointment_date = data.get('appointmentDate') or data.get('appointment_date')
    reason = data.get('reason')

    try:
        patient_id = int(patient_id) if patient_id is not None else 0
        doctor_id = int(doctor_id) if doctor_id is not None else 0
    except (ValueError, TypeError):
        patient_id = 0
        doctor_id = 0

    if patient_id <= 0 or doctor_id <= 0 or not appointment_date:
        return jsonify({'message': 'Patient and Doctor must be selected'}), 400

    # Parse appointment_date if it ends with Z or has ISO format
    clean_date_str = str(appointment_date).replace('Z', '')

    sql = """
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?);
    """
    new_id = db.execute_scalar(sql, (patient_id, doctor_id, clean_date_str, reason))
    created = {
        'id': new_id,
        'patientId': patient_id,
        'doctorId': doctor_id,
        'appointmentDate': appointment_date,
        'reason': reason
    }
    return jsonify(created), 201

@app.route('/api/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    data = request.get_json(silent=True) or {}
    patient_id = data.get('patientId') or data.get('patient_id')
    doctor_id = data.get('doctorId') or data.get('doctor_id')
    appointment_date = data.get('appointmentDate') or data.get('appointment_date')
    reason = data.get('reason')

    try:
        patient_id = int(patient_id) if patient_id is not None else 0
        doctor_id = int(doctor_id) if doctor_id is not None else 0
    except (ValueError, TypeError):
        patient_id = 0
        doctor_id = 0

    if patient_id <= 0 or doctor_id <= 0 or not appointment_date:
        return jsonify({'message': 'Patient and Doctor must be selected'}), 400

    clean_date_str = str(appointment_date).replace('Z', '')

    sql = """
        UPDATE appointments
        SET patient_id = ?, doctor_id = ?, appointment_date = ?, reason = ?
        WHERE id = ?;
    """
    affected = db.execute_non_query(sql, (patient_id, doctor_id, clean_date_str, reason, id))
    if affected == 0:
        return jsonify({'message': 'Appointment not found'}), 404

    updated = {
        'id': id,
        'patientId': patient_id,
        'doctorId': doctor_id,
        'appointmentDate': appointment_date,
        'reason': reason
    }
    return jsonify(updated), 200

@app.route('/api/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    sql = "DELETE FROM appointments WHERE id = ?;"
    affected = db.execute_non_query(sql, (id,))
    if affected == 0:
        return jsonify({'message': 'Appointment not found'}), 404
    return jsonify({'message': 'Appointment deleted successfully'}), 200


# -------------------------------------------------------------
# DASHBOARD STATS API
# -------------------------------------------------------------
@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    total_patients = db.execute_scalar("SELECT COUNT(*) FROM patients;") or 0
    total_doctors = db.execute_scalar("SELECT COUNT(*) FROM doctors;") or 0
    total_appointments = db.execute_scalar("SELECT COUNT(*) FROM appointments;") or 0

    recent_sql = f"""
        SELECT TOP 5
            appointments.id,
            appointments.patient_id AS patientId,
            patients.name AS patient,
            appointments.doctor_id AS doctorId,
            doctors.name AS doctor,
            doctors.specialization AS specialization,
            appointments.appointment_date AS appointmentDate,
            appointments.reason AS reason
        FROM appointments
        JOIN patients
            ON appointments.patient_id = patients.id
        JOIN doctors
            ON appointments.doctor_id = doctors.id
        ORDER BY appointments.appointment_date ASC;
    """
    recent_appointments = db.query_all(recent_sql)

    return jsonify({
        'totalPatients': total_patients,
        'totalDoctors': total_doctors,
        'totalAppointments': total_appointments,
        'recentAppointments': recent_appointments
    }), 200


# -------------------------------------------------------------
# APPLICATION ENTRYPOINT
# -------------------------------------------------------------
if __name__ == '__main__':
    # Initialize DB and tables if needed on startup
    db.initialize_database()
    print(f"Server starting on http://{config.HOST}:{config.PORT} (or http://localhost:{config.PORT})")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)