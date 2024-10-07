# main.py
import streamlit as st
import login  # Import the login page
import pages.hospital_a
import pages.hospital_b

# Main app logic
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.sidebar.write("Logged in as user")
        
        # Provide the option to log out
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page_reloaded = True 

        # Display page navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Select a Hospital:", ("Hospital A", "Hospital B"))
        st.title("MediCrypt")
        st.write("""
            Welcome to MediCrypt!
            
            ## Instructions
            - **Hospital A**: Enter patient data and upload an image to encrypt the data.
            - **Hospital B**: Upload the stego image to decrypt the patient data.
            
            ## Features
            - Secure communication between hospitals using DNA encryption and image steganography.
            - View history of encrypted and decrypted data.
            """)
        if page == "Analytics":
            import pages.statistics
        elif page == "Hospital A":
            import pages.hospital_a
        elif page == "Hospital B":
            import pages.hospital_b
    else:
        # Show login page if not logged in
        login.login()

if __name__ == "__main__":
    main()
