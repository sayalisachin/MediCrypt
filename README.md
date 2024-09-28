# MediCrypt - Advanced Image Steganography Tool

This is a Hospital Communication System Using DNA Encryption and Image Steganography
This project enables secure communication between two hospitals, Hospital A and Hospital B, by encrypting and hiding sensitive patient data within images using DNA encryption and Least Significant Bit (LSB) steganography techniques. The encoded image is then sent over a network, and the recipient (Hospital B) can decrypt the data to retrieve the original information.
## Key Features

- **Secure Communication Between Hospitals**: Uses encryption and steganography to establish a secure channel for exchanging sensitive patient data.

- **DNA Encryption**: Encrypts patient data using a DNA-based encryption algorithm, providing an additional layer of security.

- **Image Upload and Download Functionality**: Allows users to upload an image, embed encrypted data, and download the stego image for transmission.
  
- **User-Friendly Interface**: Built using Streamlit, providing a simple, intuitive interface for both hospitals to encrypt, embed, decrypt, and extract data.


## Theoritical Background

- **User-Friendly Interface**:
  DNA encryption is inspired by the biological structure of DNA, which is made up of four nucleotide bases: Adenine (A), Thymine (T), Cytosine (C), and Guanine (G). DNA sequences can be used to represent binary data (e.g., A = 00, T = 01, C = 10, G = 11).

  In this project, a simple DNA-based substitution cipher is used for encryption. A symmetric key is shared between Hospital A and Hospital B, where each nucleotide is mapped to another (e.g., A ↔ T, C ↔ G). The steps for encryption are:

  1) Convert patient data to binary.
  2) Use a predefined DNA key to map binary sequences to DNA bases.
  3) Generate an encrypted DNA sequence.

- **User-Friendly Interface**:
  Image steganography hides data within an image file by altering the least significant bits of each pixel’s color values. Because the LSB has the least impact on the color's appearance, the modifications remain imperceptible to the human eye. The steps involved in LSB steganography are:
  
  1) Convert the encrypted data into a binary format.
  2) Embed the binary data into the LSBs of the pixel values of the image.
  3) Add a delimiter to signify the end of the embedded data.

- **Secure Communication Flow**:
1) Hospital A:

  - Accepts patient details and an image file.
  - Encrypts the patient details using the DNA encryption algorithm.
  - Embeds the encrypted data within the image using LSB steganography.
  - Provides an option to download the stego image for transmission.

2) Hospital B:

  - Receives the stego image from Hospital A.
  - Extracts the hidden data from the image using the reverse LSB steganography.
  - Decrypts the extracted DNA sequence back to the original patient data using the DNA key.

## Conclusion

This project demonstrates a secure and innovative approach to encrypting and transmitting sensitive patient information between hospitals using DNA encryption and image steganography. It ensures data privacy, integrity, and confidentiality while providing a user-friendly interface for healthcare professionals.


