import os
import pyodbc

# Server Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')

# Database Configuration (Microsoft SQL Server)
DB_SERVER = os.getenv('DB_SERVER', r'localhost\SQLEXPRESS')
DB_NAME = os.getenv('DB_NAME', 'clinic_db')

def get_best_odbc_driver():
    """Automatically pick the best available SQL Server ODBC driver on the machine."""
    installed_drivers = pyodbc.drivers()
    preferred_drivers = [
        'ODBC Driver 18 for SQL Server',
        'ODBC Driver 17 for SQL Server',
        'SQL Server'
    ]
    for d in preferred_drivers:
        if d in installed_drivers:
            return d
    return 'ODBC Driver 18 for SQL Server'

ODBC_DRIVER = os.getenv('DB_DRIVER', get_best_odbc_driver())

def get_connection_string(database=None):
    """Build ODBC connection string for the target database (or master)."""
    target_db = database if database is not None else DB_NAME
    extra_params = ['Trusted_Connection=yes']
    if '18' in ODBC_DRIVER or '17' in ODBC_DRIVER:
        extra_params.append('TrustServerCertificate=yes')
    extra_str = ';' + ';'.join(extra_params) if extra_params else ''
    return f"DRIVER={{{ODBC_DRIVER}}};SERVER={DB_SERVER};DATABASE={target_db}{extra_str};"