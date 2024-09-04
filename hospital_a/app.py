import streamlit as st
from encryption import encrypt_dna
from steganography import embed_message
from PIL import Image
import io

def main():
    st.title("Hospital A Interface")

    # Step 1: User inputs patient details (data to be encrypted)
    patient_data = st.text_area("Enter Patient Details to Encrypt", "Patient Name: John Doe; Age: 30; Diagnosis: Healthy;")

    # Step 2: User selects an image to use for steganography
    image_file = st.file_uploader("Choose an Image to Embed Encrypted Data", type=["png", "jpg", "jpeg"])

    # Encryption key (This should be securely exchanged between hospitals)
    dna_key = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    if st.button("Encrypt and Embed Data"):
        if patient_data and image_file:
            # Step 3: Encrypt the patient data using DNA encryption
            encrypted_data = encrypt_dna(patient_data, dna_key)
            st.write("Encrypted Data (DNA):", encrypted_data)  # For debugging purposes

            # Step 4: Embed the encrypted data into the selected image using LSB steganography
            input_image = Image.open(image_file)
            encoded_image = embed_message(input_image, encrypted_data)
            
            # Display the stego image
            st.image(encoded_image, caption="Encoded Image with Encrypted Data", use_column_width=True)

            # Step 5: Provide an option to download the encoded image
            buf = io.BytesIO()
            encoded_image.save(buf, format='PNG')
            buf.seek(0)
            st.download_button(
                label="Download Encoded Image",
                data=buf,
                file_name="encoded_image.png",
                mime="image/png"
            )
            st.success("Encoded image created and ready for download.")
        else:
            st.error("Please provide both patient details and an image to proceed.")

if __name__ == "__main__":
    main()
