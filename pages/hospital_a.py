import streamlit as st
import pydicom
import numpy as np
import io
import pandas as pd
import pyvista as pv
from PIL import Image
from encryption import encrypt_dna
from steganography import embed_message
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os
import tempfile

# Function to save a DICOM report as a CSV file
def save_dicom_report(dicom_data):
    report_data = {
        "Patient Name": [dicom_data.PatientName.family_name if hasattr(dicom_data, 'PatientName') else "N/A"],
        "Patient ID": [dicom_data.PatientID if hasattr(dicom_data, 'PatientID') else "N/A"],
        "Age": [dicom_data.PatientAge if hasattr(dicom_data, 'PatientAge') else "N/A"],
        "Study Date": [dicom_data.StudyDate if hasattr(dicom_data, 'StudyDate') else "N/A"],
        "Modality": [dicom_data.Modality if hasattr(dicom_data, 'Modality') else "N/A"],
    }
    df = pd.DataFrame(report_data)
    return df

def visualize_3d_volume(dicom_array):
    if len(dicom_array.shape) == 2:
        dicom_array = np.stack([dicom_array] * 3, axis=-1)
    
    grid = pv.ImageData()
    grid.dimensions = dicom_array.shape
    grid.origin = (0, 0, 0)
    grid.spacing = (1, 1, 1)
    grid.point_data["values"] = dicom_array.flatten(order="F")

    plotter = pv.Plotter()
    plotter.add_volume(grid, scalars="values", opacity="linear", cmap="gray")
    plotter.show()

def normalize_pixels(pixel_array):
    min_val = np.min(pixel_array)
    max_val = np.max(pixel_array)
    normalized_pixels = 255 * (pixel_array - min_val) / (max_val - min_val)
    return normalized_pixels.astype(np.uint8)

def animate_slices(dicom_data):
    pixel_array = dicom_data.pixel_array
    if pixel_array.ndim == 2:
        pixel_array = pixel_array[np.newaxis, :, :]
    elif pixel_array.ndim != 3:
        st.error("The DICOM file does not contain valid 2D or 3D pixel data.")
        return

    pixel_array = normalize_pixels(pixel_array)
    fig, ax = plt.subplots()
    img = ax.imshow(pixel_array[0, :, :], cmap='gray')
    ax.axis('off')

    def update(frame):
        img.set_array(pixel_array[frame, :, :])
        return [img]

    ani = animation.FuncAnimation(
        fig, update, frames=range(pixel_array.shape[0]), interval=100, blit=True
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as temp_file:
        ani.save(temp_file.name, fps=10, writer='imagemagick', savefig_kwargs={'bbox_inches': 'tight'})
        temp_file.seek(0)
        temp_filename = temp_file.name

    with open(temp_filename, 'rb') as f:
        gif_buffer = io.BytesIO(f.read())

    st.image(gif_buffer, caption="DICOM Slices Animation", use_column_width=True)

def main():
    # Login check
    if not st.session_state.get("logged_in", False):
        st.error("You need to log in to access this page.")
        st.stop()

    st.title("🏥 Hospital A Interface")
    st.write("""
    This interface allows you to securely encrypt and embed patient data into an image using DNA encryption and steganography. 
    The encoded image can then be securely transmitted to Hospital B for decryption.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.header("Step 1: Enter Patient Details")
        patient_data = st.text_area(
            "📝 Enter Patient Details to Encrypt",
            "Patient Name: John Doe; Age: 30; Diagnosis: Healthy;",
            help="Enter the sensitive patient information that you want to encrypt and hide within the image."
        )

    with col2:
        st.header("Step 2: Upload an Image")
        image_file = st.file_uploader(
            "🖼️ Choose an Image to Embed Encrypted Data",
            type=["png", "jpg", "jpeg"],
            help="Upload an image where the encrypted data will be hidden using steganography."
        )
        if image_file:
            st.image(image_file, caption="Uploaded Image Preview", use_column_width=True)

    dicom_file = st.file_uploader("📥 Upload DICOM File", type=["dcm"])

    if dicom_file:
        dicom_data = pydicom.dcmread(dicom_file)
        st.subheader("DICOM Metadata")
        st.write({
            "Patient Name": dicom_data.PatientName if hasattr(dicom_data, 'PatientName') else "N/A",
            "Patient ID": dicom_data.PatientID if hasattr(dicom_data, 'PatientID') else "N/A",
            "Age": dicom_data.PatientAge if hasattr(dicom_data, 'PatientAge') else "N/A",
            "Study Date": dicom_data.StudyDate if hasattr(dicom_data, 'StudyDate') else "N/A",
            "Modality": dicom_data.Modality if hasattr(dicom_data, 'Modality') else "N/A",
        })

        if hasattr(dicom_data, 'pixel_array'):
            pixel_array = dicom_data.pixel_array
            if pixel_array.ndim == 2:
                st.image(pixel_array, caption="DICOM Image Preview", use_column_width=True)
            elif pixel_array.ndim == 3:
                st.image(pixel_array[0], caption="First Slice of DICOM Image Volume", use_column_width=True)

                if st.button("🔍 Visualize in 3D"):
                    visualize_3d_volume(pixel_array)

            if st.button("Generate DICOM Report"):
                report_df = save_dicom_report(dicom_data)
                csv_buffer = io.StringIO()
                report_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                st.download_button(
                    label="📥 Download DICOM Report",
                    data=csv_buffer.getvalue(),
                    file_name="dicom_report.csv",
                    mime="text/csv",
                    help="Click to download the DICOM report as a CSV file."
                )
                st.success("Report generated successfully!")

            if st.button("🎥 Animate Slices"):
                animate_slices(dicom_data)

    dna_key = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    if st.button("🔒 Encrypt and Embed Data"):
        if patient_data and image_file:
            with st.spinner("Encrypting and Embedding Data... Please wait."):
                encrypted_data = encrypt_dna(patient_data, dna_key)
                st.subheader("Encrypted Data (DNA Format)")
                st.write(encrypted_data)

                input_image = Image.open(image_file)
                encoded_image = embed_message(input_image, encrypted_data)

                st.subheader("Encoded Image with Encrypted Data")
                st.image(encoded_image, caption="Encoded Image Preview", use_column_width=True)

                buf = io.BytesIO()
                encoded_image.save(buf, format='PNG')
                buf.seek(0)

                file_size = len(buf.getvalue()) / 1024
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

if __name__ == "__main__":
    main()
