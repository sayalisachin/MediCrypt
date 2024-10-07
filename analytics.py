import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# Function to generate analytics
def analytics_dashboard():
    st.title("Patient Data Analytics Dashboard")

    # Sample Data
    data = pd.DataFrame({
        "Diagnosis": ["Hypertension", "Diabetes", "Asthma"],
        "Patient Count": [45, 30, 25],
        "Average Wait Time": [20, 30, 25]
    })

    # Bar chart of diagnoses
    st.subheader("Diagnosis Distribution")
    fig, ax = plt.subplots()
    ax.bar(data['Diagnosis'], data['Patient Count'])
    ax.set_ylabel('Number of Patients')
    st.pyplot(fig)

    # Line chart of average wait time
    st.subheader("Average Wait Time by Diagnosis")
    fig, ax = plt.subplots()
    ax.plot(data['Diagnosis'], data['Average Wait Time'], marker='o')
    ax.set_ylabel('Average Wait Time (minutes)')
    st.pyplot(fig)

# Call the analytics dashboard in the main app
if __name__ == "__main__":
    analytics_dashboard()
