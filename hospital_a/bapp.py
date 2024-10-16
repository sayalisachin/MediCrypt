# hospital_b.py

import asyncio
import base64
import json
import streamlit as st
import websockets
from PIL import Image
from io import BytesIO
from encryption import decrypt_dna, reverse_dna_key

async def receive_data():
    async with websockets.connect("ws://127.0.0.1:8765") as websocket:
        while True:
            message = await websocket.recv()
            return json.loads(message)

def main():
    st.title("🏥 Hospital B Interface")
    st.write("""
    This interface allows you to receive encrypted patient data and images from Hospital A. 
    The received data will be decrypted and displayed.
    """)

    data = asyncio.run(receive_data())
    
    # Decode the image
    img_data = base64.b64decode(data["image"])
    img = Image.open(BytesIO(img_data))
    
    # Decrypt patient details
    decrypted_patient_data = decrypt_dna(data["patient_data"], reverse_dna_key)

    # Display received image and decrypted data
    st.image(img, caption="Received Image", use_column_width=True)
    st.write("Decrypted Patient Details:", decrypted_patient_data)

if __name__ == "__main__":
    main()
