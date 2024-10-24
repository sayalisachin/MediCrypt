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
    """Connects to the WebSocket server to receive encrypted data and image from Hospital A."""
    try:
        async with websockets.connect("ws://127.0.0.1:8765", timeout=10) as websocket:
            st.info("Connected to Hospital A WebSocket server.")
            message = await websocket.recv()
            st.info("Data received from Hospital A.")
            return json.loads(message)
    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedError) as e:
        st.error(f"Connection error: {e}")
        return None

def main():
    st.title("🏥 Hospital B Interface")
    st.write("""
    This interface allows you to receive encrypted patient data and images from Hospital A. 
    First, enter the decryption key. Once the data is received, the decryption process will be initiated.
    """)

    # Ask for the decryption key before receiving data
    decryption_key = st.text_input("Enter the Decryption Key", type="password")

    if decryption_key:
        if st.button("Receive Data"):
            with st.spinner("Connecting to Hospital A..."):
                data = asyncio.run(receive_data())

            if data:
                # Display the received encrypted image
                try:
                    img_data = base64.b64decode(data["image"])
                    img = Image.open(BytesIO(img_data))
                    st.image(img, caption="Received Encrypted Image", use_column_width=True)
                except Exception as e:
                    st.error(f"Error decoding image: {e}")

                # Check if the decryption key matches
                if decryption_key == data["decryption_key"]:
                    # Decrypt patient data using the provided key
                    try:
                        decrypted_patient_data = decrypt_dna(data["patient_data"], reverse_dna_key)
                        st.success("Data decrypted successfully!")
                        st.write("Decrypted Patient Details:", decrypted_patient_data)
                    except Exception as e:
                        st.error(f"Error decrypting data: {e}")
                else:
                    st.error("Incorrect decryption key! Unable to decrypt patient details.")
            else:
                st.error("Failed to receive data from Hospital A. Please ensure the server is running and reachable.")
    else:
        st.info("Please enter the decryption key to proceed with receiving data.")

if __name__ == "__main__":
    main()