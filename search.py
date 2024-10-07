import streamlit as st
import pandas as pd
import sqlite3


# Function to create a fresh connection
def get_db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create table and insert sample data only once
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

# Patient search function
def search_patient(search_term):
    conn = get_db_connection()  # Get a new connection
    query = f"SELECT * FROM patients WHERE name LIKE '%{search_term}%' OR diagnosis LIKE '%{search_term}%'"
    results = pd.read_sql_query(query, conn)
    conn.close()  # Close connection after query
    return results

# Streamlit interface for searching patients
def patient_search_page():
    st.title("Patient Data Search")
    
    search_term = st.text_input("Enter patient name or diagnosis to search")
    
    if st.button("Search"):
        results = search_patient(search_term)
        if not results.empty:
            st.dataframe(results)
        else:
            st.write("No records found.")

if __name__ == "__main__":
    patient_search_page()
