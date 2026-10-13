import pyodbc
import datetime
from contextlib import contextmanager
import config

def get_connection(database=None):
    """Create and return a new pyodbc connection."""
    conn_str = config.get_connection_string(database)
    return pyodbc.connect(conn_str)

@contextmanager
def get_db_cursor(commit=False):
    """Context manager for obtaining database connection and cursor."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        if commit:
            conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def row_to_dict(cursor, row):
    """Convert a pyodbc Row object into a python dictionary with formatted types."""
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    result = {}
    for col_name, val in zip(columns, row):
        # Format datetime objects to ISO format string (compatible with JS Date parsing)
        if isinstance(val, (datetime.datetime, datetime.date)):
            val = val.isoformat()
        result[col_name] = val
    return result

def query_all(sql, params=None):
    """Execute a SELECT query and return all rows as list of dicts."""
    with get_db_cursor() as cursor:
        cursor.execute(sql, params or ())
        rows = cursor.fetchall()
        return [row_to_dict(cursor, r) for r in rows]

def query_one(sql, params=None):
    """Execute a SELECT query and return the first row as dict or None."""
    with get_db_cursor() as cursor:
        cursor.execute(sql, params or ())
        row = cursor.fetchone()
        return row_to_dict(cursor, row)

def execute_scalar(sql, params=None):
    """Execute a query and return a single scalar value."""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(sql, params or ())
        row = cursor.fetchone()
        return row[0] if row else None

def execute_non_query(sql, params=None):
    """Execute INSERT, UPDATE, DELETE query and return affected row count."""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(sql, params or ())
        return cursor.rowcount

def initialize_database():
    """Ensure database clinic_db and required tables exist with initial seed data."""
    try:
        # Step 1: Ensure database exists on master
        master_conn = pyodbc.connect(config.get_connection_string('master'), autocommit=True)
        master_cursor = master_conn.cursor()
        master_cursor.execute("SELECT COUNT(*) FROM sys.databases WHERE name = 'clinic_db'")
        db_exists = master_cursor.fetchone()[0]
        if db_exists == 0:
            master_cursor.execute("CREATE DATABASE clinic_db;")
            print("Database clinic_db created successfully.")
        master_cursor.close()
        master_conn.close()

        # Step 2: Ensure tables exist
        conn = get_connection()
        cursor = conn.cursor()

        # Patients Table
        cursor.execute("""
            IF OBJECT_ID('dbo.patients', 'U') IS NULL
            BEGIN
                CREATE TABLE patients (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    name VARCHAR(100) NOT NULL,
                    age INT,
                    gender VARCHAR(20),
                    phone VARCHAR(15)
                );

                INSERT INTO patients (name, age, gender, phone) VALUES
                ('Karthik Raja', 32, 'Male', '9840112233'),
                ('Lakshmi Narayanan', 28, 'Female', '9840223344'),
                ('Suresh Kumar', 54, 'Male', '9840334455'),
                ('Priya Balachandran', 22, 'Female', '9840445566'),
                ('Venkat Raghavan', 45, 'Male', '9840556677');
            END
        """)

        # Doctors Table
        cursor.execute("""
            IF OBJECT_ID('dbo.doctors', 'U') IS NULL
            BEGIN
                CREATE TABLE doctors (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    name VARCHAR(100) NOT NULL,
                    specialization VARCHAR(100),
                    phone VARCHAR(15)
                );

                INSERT INTO doctors (name, specialization, phone) VALUES
                ('Dr. Ananya Sundaram', 'General Physician', '9444011223'),
                ('Dr. Rajesh Kannan', 'Dentist', '9444022334'),
                ('Dr. Meenakshi Iyer', 'Pediatrician (Child Specialist)', '9444033445'),
                ('Dr. Murugan Swaminathan', 'Orthopedic (Bone Specialist)', '9444044556'),
                ('Dr. Deepa Krishnan', 'ENT Specialist', '9444055667');
            END
        """)

        # Appointments Table
        cursor.execute("""
            IF OBJECT_ID('dbo.appointments', 'U') IS NULL
            BEGIN
                CREATE TABLE appointments (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    patient_id INT NOT NULL,
                    doctor_id INT NOT NULL,
                    appointment_date DATETIME NOT NULL,
                    reason VARCHAR(255),
                    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
                );

                INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES
                (1, 1, DATEADD(hour, 10, CAST(CAST(DATEADD(day, 1, GETDATE()) AS DATE) AS DATETIME)), 'Viral Fever and Headache'),
                (2, 2, DATEADD(hour, 11, CAST(CAST(DATEADD(day, 1, GETDATE()) AS DATE) AS DATETIME)), 'Tooth Pain and Cleaning'),
                (3, 4, DATEADD(hour, 14, CAST(CAST(DATEADD(day, 2, GETDATE()) AS DATE) AS DATETIME)), 'Knee Pain and Joint Check'),
                (4, 3, DATEADD(hour, 9,  CAST(CAST(DATEADD(day, 3, GETDATE()) AS DATE) AS DATETIME)), 'Child Routine Vaccination'),
                (5, 5, DATEADD(hour, 16, CAST(CAST(DATEADD(day, 4, GETDATE()) AS DATE) AS DATETIME)), 'Ear Pain and Throat Infection');
            END
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Database tables initialized successfully.")
    except Exception as ex:
        print(f"Database initialization notice: {ex}")