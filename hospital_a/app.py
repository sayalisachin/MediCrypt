import streamlit as st
import pydicom
import numpy as np
import io
import pandas as pd
import pyvista as pv
from PIL import Image
from encryption import encrypt_dna
from steganography import embed_message


# Function to save a DICOM report as a CSV file
# Function to save a DICOM report as a CSV file
def save_dicom_report(dicom_data):
    # Ensure that all values are single values (or flatten arrays)
    report_data = {
        "Patient Name": [dicom_data.PatientName.family_name if hasattr(dicom_data, 'PatientName') else "N/A"],
        "Patient ID": [dicom_data.PatientID if hasattr(dicom_data, 'PatientID') else "N/A"],
        "Age": [dicom_data.PatientAge if hasattr(dicom_data, 'PatientAge') else "N/A"],
        "Study Date": [dicom_data.StudyDate if hasattr(dicom_data, 'StudyDate') else "N/A"],
        "Modality": [dicom_data.Modality if hasattr(dicom_data, 'Modality') else "N/A"],
    }
    
    # Ensure the lengths match and create a DataFrame with appropriate row length
    df = pd.DataFrame(report_data)
    
    return df


def visualize_3d_volume(dicom_array):
    # Ensure that dicom_array is 3D; if it's not, you may need to reshape or stack slices
    if len(dicom_array.shape) == 2:
        # In case it's only a single 2D slice, we stack it into a 3D volume (single layer)
        dicom_array = np.stack([dicom_array] * 3, axis=-1)
    
    # Create a PyVista ImageData object for visualization
    grid = pv.ImageData()
    
    # Set dimensions: (x, y, z), matching the shape of the DICOM array
    grid.dimensions = dicom_array.shape
    
    # Set the origin (where the data begins in space)
    grid.origin = (0, 0, 0)

    # Set the spacing between grid points
    grid.spacing = (1, 1, 1)  # You can adjust the spacing if needed based on the dataset

    # Add the DICOM pixel data as scalar values to the grid
    grid.point_data["values"] = dicom_array.flatten(order="F")

    # Create the plotter and visualize the 3D volume
    plotter = pv.Plotter()
    plotter.add_volume(grid, scalars="values", opacity="linear", cmap="gray")
    plotter.show()

# Function to display the Streamlit app UI
def main():
    st.title("🏥 Hospital A Interface")
    st.write("""
    This interface allows you to securely encrypt and embed patient data into an image using DNA encryption and steganography. 
    The encoded image can then be securely transmitted to Hospital B for decryption.
    """)
    
    # Layout: Two columns for input fields and image preview
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

    # DICOM file upload
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

        # DICOM image preview
        if hasattr(dicom_data, 'pixel_array'):
            pixel_array = dicom_data.pixel_array
            if pixel_array.ndim == 2:
                # 2D image (single slice)
                st.image(pixel_array, caption="DICOM Image Preview", use_column_width=True)
            elif pixel_array.ndim == 3:
                # 3D image volume (multiple slices)
                st.image(pixel_array[0], caption="First Slice of DICOM Image Volume", use_column_width=True)
                
                # 3D visualization button
                if st.button("🔍 Visualize in 3D"):
                    visualize_3d_volume(pixel_array)

            # Generate CSV report
            if st.button("Generate DICOM Report"):
                report_df = save_dicom_report(dicom_data)
                
                # Create a CSV buffer
                csv_buffer = io.StringIO()
                report_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)  # Move to the beginning of the buffer

                # Provide a download button for the CSV file
                st.download_button(
                    label="📥 Download DICOM Report",
                    data=csv_buffer.getvalue(),
                    file_name="dicom_report.csv",
                    mime="text/csv",
                    help="Click to download the DICOM report as a CSV file."
                )
                st.success("Report generated successfully!")
            

    # Encryption key (This should be securely exchanged between hospitals)
    dna_key = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    # Button to trigger encryption and embedding
    if st.button("🔒 Encrypt and Embed Data"):
        if patient_data and image_file:
            with st.spinner("Encrypting and Embedding Data... Please wait."):
                encrypted_data = encrypt_dna(patient_data, dna_key)
                st.subheader("Encrypted Data (DNA Format)")
                st.write(encrypted_data)  # Display encrypted data (optional)

                input_image = Image.open(image_file)
                encoded_image = embed_message(input_image, encrypted_data)
                
                # Display the encoded image in the UI
                st.subheader("Encoded Image with Encrypted Data")
                st.image(encoded_image, caption="Encoded Image Preview", use_column_width=True)

                # Provide an option to download the encoded image
                buf = io.BytesIO()
                encoded_image.save(buf, format='PNG')
                buf.seek(0)
                
                # Calculate file size
                file_size = len(buf.getvalue()) / 1024  # Size in KB

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

# Run the Streamlit app
if __name__ == "__main__":
    main()
