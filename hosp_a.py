import streamlit as st
import io
from PIL import Image
from encryption import encrypt_dna
from steganography import embed_message
import os

# Function to send data to Hospital B
def send_to_hospital_b(encoded_image_bytes, key):
    # Define file paths (ensure these paths are shared between both applications)
    image_path = "shared_directory/encoded_image.png"
    key_path = "shared_directory/decryption_key.txt"
    
    # Ensure the shared directory exists
    os.makedirs("shared_directory", exist_ok=True)

    # Save the image and key to files in the shared directory
    with open(image_path, "wb") as img_file:
        img_file.write(encoded_image_bytes)

    with open(key_path, "w") as key_file:
        key_file.write(str(key))

    st.success(f"✅ Data sent to Hospital B! Files saved at {image_path} and {key_path}.")

st.title("🏥 Hospital A - Send Encrypted Data to Hospital B")

# Input for patient data and image upload
patient_data = st.text_area("Enter Patient Data", "Patient Name: John Doe; Age: 30; Diagnosis: Healthy;")
image_file = st.file_uploader("Choose an Image to Embed Encrypted Data", type=["png", "jpg", "jpeg"])

# Encrypt and send button
if st.button("Encrypt and Send"):
    if image_file and patient_data:
        with st.spinner("Encrypting and sending data..."):
            # Encrypt patient data
            dna_key = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
            encrypted_data = encrypt_dna(patient_data, dna_key)

            # Embed encrypted data in the image
            input_image = Image.open(image_file)
            encoded_image = embed_message(input_image, encrypted_data)

            # Convert image to byte buffer
            buf = io.BytesIO()
            encoded_image.save(buf, format='PNG')
            buf.seek(0)

            # Send image data and key to Hospital B (save to file)
            send_to_hospital_b(buf.getvalue(), dna_key)
    else:
        st.error("⚠️ Please provide both patient data and an image.")
