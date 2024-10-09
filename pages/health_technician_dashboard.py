import streamlit as st

# Sample data for demonstration
patients = {
    1: {'name': 'John Doe', 'history': 'Allergic to penicillin', 'prescriptions': []},
    2: {'name': 'Jane Smith', 'history': 'Diabetes Type 1', 'prescriptions': []},
}

appointments = {
    1: {'patient_id': 1, 'time': '2024-10-09 09:00', 'status': 'Scheduled'},
    2: {'patient_id': 2, 'time': '2024-10-09 10:00', 'status': 'Scheduled'},
}

test_requests = {
    1: {'patient_id': 1, 'test_type': 'Blood Test', 'status': 'Pending'},
    2: {'patient_id': 2, 'test_type': 'Urine Test', 'status': 'Pending'},
}

# Streamlit App Layout
st.title("Healthcare Management System")

# Step 1: Role Selection
role = st.selectbox("Select Your Role", ["Doctor", "Nurse", "Lab Technician"])

# Step 2: Role-based Functionality
if role == "Doctor":
    st.subheader("Doctor Dashboard")
    selected_patient = st.selectbox("Select Patient", list(patients.keys()), format_func=lambda x: patients[x]['name'])
    
    if st.button("View Patient History"):
        st.write("Patient Name:", patients[selected_patient]['name'])
        st.write("History:", patients[selected_patient]['history'])
        
    prescription = st.text_input("Add Prescription")
    if st.button("Submit Prescription"):
        if prescription:
            patients[selected_patient]['prescriptions'].append(prescription)
            st.success("Prescription added successfully!")
        else:
            st.warning("Please enter a prescription.")

    st.write("Current Prescriptions:", patients[selected_patient]['prescriptions'])

elif role == "Nurse":
    st.subheader("Nurse Dashboard")
    
    st.write("Manage Appointments:")
    for appointment_id, appointment in appointments.items():
        patient_name = patients[appointment['patient_id']]['name']
        st.write(f"Patient: {patient_name}, Time: {appointment['time']}, Status: {appointment['status']}")

    appointment_status = st.selectbox("Select Appointment Status", ["Scheduled", "Completed", "Cancelled"])
    if st.button("Update Appointment"):
        selected_appointment_id = st.selectbox("Select Appointment to Update", list(appointments.keys()))
        appointments[selected_appointment_id]['status'] = appointment_status
        st.success("Appointment status updated!")

elif role == "Lab Technician":
    st.subheader("Lab Technician Dashboard")
    
    st.write("Test Requests:")
    for test_id, test in test_requests.items():
        patient_name = patients[test['patient_id']]['name']
        st.write(f"Patient: {patient_name}, Test Type: {test['test_type']}, Status: {test['status']}")
        
    test_result = st.text_input("Enter Test Result")
    if st.button("Submit Test Result"):
        selected_test_id = st.selectbox("Select Test to Update", list(test_requests.keys()))
        test_requests[selected_test_id]['status'] = 'Completed'
        st.success("Test result updated!")
        st.write("Result:", test_result)

# Add some UI enhancements
st.write("This system facilitates role-based access to patient management, improving workflow and communication between healthcare professionals.")
