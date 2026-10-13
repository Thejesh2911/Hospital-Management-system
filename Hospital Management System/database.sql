-- ==========================================================
-- Clinic Management System Database Script
-- Compatible with Microsoft SQL Server & SSMS
-- Database: clinic_db
-- ==========================================================

-- 1. Create Database if it does not exist
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'clinic_db')
BEGIN
    CREATE DATABASE clinic_db;
    PRINT 'Database clinic_db created successfully.';
END
GO

USE clinic_db;
GO

-- 2. Drop existing tables if re-running (respecting foreign key order)
IF OBJECT_ID('dbo.appointments', 'U') IS NOT NULL DROP TABLE dbo.appointments;
IF OBJECT_ID('dbo.patients', 'U') IS NOT NULL DROP TABLE dbo.patients;
IF OBJECT_ID('dbo.doctors', 'U') IS NOT NULL DROP TABLE dbo.doctors;
GO

-- 3. Create Patients Table
CREATE TABLE patients (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(20),
    phone VARCHAR(15)
);
GO

-- 4. Create Doctors Table
CREATE TABLE doctors (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(15)
);
GO

-- 5. Create Appointments Table
CREATE TABLE appointments (
    id INT PRIMARY KEY IDENTITY(1,1),
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    reason VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);
GO

-- 6. Insert Seed Data with South Indian Names & Basic Specializations

-- Insert South Indian Patients
INSERT INTO patients (name, age, gender, phone) VALUES
('Karthik Raja', 32, 'Male', '9840112233'),
('Lakshmi Narayanan', 28, 'Female', '9840223344'),
('Suresh Kumar', 54, 'Male', '9840334455'),
('Priya Balachandran', 22, 'Female', '9840445566'),
('Venkat Raghavan', 45, 'Male', '9840556677');
GO

-- Insert South Indian Doctors with Basic Specializations
INSERT INTO doctors (name, specialization, phone) VALUES
('Dr. Ananya Sundaram', 'General Physician', '9444011223'),
('Dr. Rajesh Kannan', 'Dentist', '9444022334'),
('Dr. Meenakshi Iyer', 'Pediatrician (Child Specialist)', '9444033445'),
('Dr. Murugan Swaminathan', 'Orthopedic (Bone Specialist)', '9444044556'),
('Dr. Deepa Krishnan', 'ENT Specialist', '9444055667');
GO

-- Insert Sample Appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES
(1, 1, DATEADD(hour, 10, CAST(CAST(DATEADD(day, 1, GETDATE()) AS DATE) AS DATETIME)), 'Viral Fever and Headache'),
(2, 2, DATEADD(hour, 11, CAST(CAST(DATEADD(day, 1, GETDATE()) AS DATE) AS DATETIME)), 'Tooth Pain and Cleaning'),
(3, 4, DATEADD(hour, 14, CAST(CAST(DATEADD(day, 2, GETDATE()) AS DATE) AS DATETIME)), 'Knee Pain and Joint Check'),
(4, 3, DATEADD(hour, 9,  CAST(CAST(DATEADD(day, 3, GETDATE()) AS DATE) AS DATETIME)), 'Child Routine Vaccination'),
(5, 5, DATEADD(hour, 16, CAST(CAST(DATEADD(day, 4, GETDATE()) AS DATE) AS DATETIME)), 'Ear Pain and Throat Infection');
GO

-- 7. Verification: Test the JOIN query
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
GO
