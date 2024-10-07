import streamlit as st
from decryption import decrypt_dna
from dsteganography import extract_message
import matplotlib.pyplot as plt

def main():
    if not st.session_state.get("logged_in", False):
        st.error("You need to log in to access this page.")
        st.stop()
    
    st.title("Hospital B Interface")
    
    # Upload Stego Image
    stego_image = st.file_uploader("Upload Stego Image", type=["png", "jpg", "jpeg"])
    
    if st.button("Extract and Decrypt Data"):
        if stego_image:
            # Extract Encrypted Data
            extracted_data = extract_message(stego_image)
            
            # Example key (ensure this matches the key used in encryption)
            dna_key = {'T': 'A', 'A': 'T', 'G': 'C', 'C': 'G'}
            
            try:
                # Decrypt Data
                decrypted_message = decrypt_dna(extracted_data, dna_key)
                st.write("Decrypted Data:", decrypted_message)
                st.success("Data extracted and decrypted successfully!")
            except ValueError as e:
                st.error(f"Decryption error: {e}")
    # Example plot
    st.header("Data Visualization")
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    st.pyplot(fig)

if __name__ == "__main__":
    main()
