# hospital_a.py

import asyncio
import base64
import io
import json
import streamlit as st
from PIL import Image
import websockets
from encryption import encrypt_dna

# Define your DNA key mappings
dna_key = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
reverse_dna_key = {v: k for k, v in dna_key.items()}

async def send_image(image, patient_data):
    # Encrypt patient data
    encrypted_patient_data = encrypt_dna(patient_data, dna_key)

    # Encode image to base64 for transmission
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    message = {
        "image": img_base64,
        "patient_data": encrypted_patient_data
    }

    async with websockets.connect("ws://127.0.0.1:8765") as websocket:
        await websocket.send(json.dumps(message))
        st.success("Image and encrypted patient details sent to Hospital B.")

def main():
    st.title("🏥 Hospital A Interface")
    st.write("""
    This interface allows you to securely encrypt and embed patient data into an image using DNA encryption. 
    The encoded image can then be securely transmitted to Hospital B for decryption.
    """)

    patient_data = st.text_input("Enter Patient Details to Encrypt", "Patient Name: John Doe; Age: 30; Diagnosis: Healthy;")
    image_file = st.file_uploader("Choose an Image to Embed Encrypted Data", type=["png", "jpg", "jpeg"])

    if st.button("Send Data"):
        if image_file and patient_data:
            input_image = Image.open(image_file)
            asyncio.run(send_image(input_image, patient_data))
        else:
            st.error("Please provide both patient details and an image to proceed.")

if __name__ == "__main__":
    main()
