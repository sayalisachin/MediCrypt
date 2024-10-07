import streamlit as st
from encryption import encrypt_dna
from steganography import embed_message
from PIL import Image
import io
import matplotlib.pyplot as plt
import numpy as np

# Function to display the Streamlit app UI
def main():
    if not st.session_state.get("logged_in", False):
        st.error("You need to log in to access this page.")
        st.stop()
    # App title and introduction
    st.title("🏥 Hospital A Interface")
    st.write("""
    This interface allows you to securely encrypt and embed patient data into an image using DNA encryption and steganography. 
    The encoded image can then be securely transmitted to Hospital B for decryption.
    """)
    
    # Layout: Two columns for input fields and image preview
    col1, col2 = st.columns(2)

    with col1:
        st.header("Step 1: Enter Patient Details")
        # Step 1: User inputs patient details (data to be encrypted)
        patient_data = st.text_area(
            "📝 Enter Patient Details to Encrypt",
            "Patient Name: John Doe; Age: 30; Diagnosis: Healthy;",
            help="Enter the sensitive patient information that you want to encrypt and hide within the image."
        )

    with col2:
        st.header("Step 2: Upload an Image")
        # Step 2: User selects an image to use for steganography
        image_file = st.file_uploader(
            "🖼️ Choose an Image to Embed Encrypted Data",
            type=["png", "jpg", "jpeg"],
            help="Upload an image where the encrypted data will be hidden using steganography."
        )
        if image_file:
            st.image(image_file, caption="Uploaded Image Preview", use_column_width=True)

    # Encryption key (This should be securely exchanged between hospitals)
    dna_key = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    # Button to trigger encryption and embedding
    if st.button("🔒 Encrypt and Embed Data"):
        if patient_data and image_file:
            with st.spinner("Encrypting and Embedding Data... Please wait."):
                # Step 3: Encrypt the patient data using DNA encryption
                encrypted_data = encrypt_dna(patient_data, dna_key)
                st.subheader("Encrypted Data (DNA Format)")
                st.write(encrypted_data)  # Display encrypted data (optional)

                # Step 4: Embed the encrypted data into the selected image using LSB steganography
                input_image = Image.open(image_file)
                encoded_image = embed_message(input_image, encrypted_data)
                
                # Display the encoded image in the UI
                st.subheader("Encoded Image with Encrypted Data")
                st.image(encoded_image, caption="Encoded Image Preview", use_column_width=True)

                # Step 5: Provide an option to download the encoded image
                buf = io.BytesIO()
                encoded_image.save(buf, format='PNG')
                buf.seek(0)
                
                # Calculate file size
                file_size = len(buf.getvalue()) / 1024  # Size in KB

                # Improved download button with a progress bar and confirmation message
                st.success(f"✅ Encoded image is ready for download! File size: {file_size:.2f} KB")
                st.download_button(
                    label="📥 Download Encoded Image",
                    data=buf,
                    file_name="encoded_image.png",
                    mime="image/png",
                    help="Click to download the encoded image with hidden patient data."
                )
        else:
            st.error("⚠️ Please provide both patient details and an image to proceed.")
        
        # Example plot - RGB histogram of the uploaded image
        if image_file:
            st.header("Color Distribution of Uploaded Image")
            input_image = Image.open(image_file)
            plot_color_histogram(input_image)



# Function to plot the RGB histogram of an image
def plot_color_histogram(image):
    # Convert image to numpy array
    img_array = np.array(image)

    # Plotting the histogram for each channel
    fig, ax = plt.subplots()
    ax.hist(img_array[:, :, 0].ravel(), bins=256, color='red', alpha=0.5, label='Red')
    ax.hist(img_array[:, :, 1].ravel(), bins=256, color='green', alpha=0.5, label='Green')
    ax.hist(img_array[:, :, 2].ravel(), bins=256, color='blue', alpha=0.5, label='Blue')

    # Adding labels and title
    ax.set_xlabel('Pixel Intensity')
    ax.set_ylabel('Frequency')
    ax.legend()
    st.pyplot(fig)


# Run the Streamlit app
if __name__ == "__main__":
    main()
