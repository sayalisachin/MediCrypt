import streamlit as st
from decryption import decrypt_dna
from steganography import extract_message

def main():
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

if __name__ == "__main__":
    main()
