import streamlit as st
import sqlite3
import pandas as pd

# Step 1: Define get_db_connection function
def get_db_connection():
    conn = sqlite3.connect(':memory:')  # Create a new SQLite in-memory database
    cursor = conn.cursor()
    
    # Create table and insert sample data if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients 
                      (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, diagnosis TEXT, visit_date TEXT)''')
    patients = [
        (1, 'John Doe', 45, 'Hypertension', '2024-01-15'),
        (2, 'Jane Smith', 38, 'Diabetes', '2024-02-10'),
        (3, 'Alice Brown', 29, 'Asthma', '2024-03-12')
    ]
    cursor.executemany('INSERT INTO patients VALUES (?, ?, ?, ?, ?)', patients)
    conn.commit()
    return conn

# Step 2: Report generation function
def generate_report():
    st.title("Generate Patient Reports")
    
    # Get patient data from SQLite
    conn = get_db_connection()  # Get a new connection
    query = "SELECT * FROM patients"
    results = pd.read_sql_query(query, conn)
    conn.close()  # Close connection after query

    if st.button("Generate CSV Report"):
        results.to_csv('patient_report.csv', index=False)
        st.write("Report generated successfully!")
        st.download_button(
            label="Download CSV",
            data=results.to_csv(index=False).encode('utf-8'),
            file_name='patient_report.csv',
            mime='text/csv'
        )

# Step 3: Add main function to run the report page
if __name__ == "__main__":
    generate_report()
