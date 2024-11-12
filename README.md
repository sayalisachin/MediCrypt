# MediCrypt - Advanced Image Steganography Tool

This is a Hospital Communication System Using DNA Encryption and Image Steganography
This project enables secure communication between two hospitals, Clinic A and Clinic B, by encrypting and hiding sensitive patient data within images using DNA encryption and Least Significant Bit (LSB) steganography techniques. 
The encoded image is then sent over a network, and the recipient (Hospital B) can decrypt the data to retrieve the original information.

## Key Features

- **Secure Communication Between Hospitals**: Uses encryption and steganography to establish a secure channel for exchanging sensitive patient data.

- **DNA Encryption**: Encrypts patient data using a DNA-based encryption algorithm, providing an additional layer of security.

- **Image Upload and Download Functionality**: Allows users to upload an image, embed encrypted data, and download the stego image for transmission.
  
- **User-Friendly Interface**: Built using Streamlit, providing a simple, intuitive interface for both hospitals to encrypt, embed, decrypt, and extract data.

- **Websocket (Socket.IO)**:  effortless transmission of Images without the need for local storage/download.

-  **DIACOM**: Integrates DIACOM and Slice generation to generate slices of 3D-Model based the DIACOM image.

-  **MatPlotLib**: Generate Analytics, Search reports of patients stored in SQL Database using MatPlotLib.


## Theoritical Background

- **User-Friendly Interface**:
  DNA encryption is inspired by the biological structure of DNA, which is made up of four nucleotide bases: Adenine (A), Thymine (T), Cytosine (C), and Guanine (G). DNA sequences can be used to represent binary data (e.g., A = 00, T = 01, C = 10, G = 11).

  In this project, a simple DNA-based substitution cipher is used for encryption. A symmetric key is shared between Hospital A and Hospital B, where each nucleotide is mapped to another (e.g., A ↔ T, C ↔ G). The steps for encryption are:

  1) Convert patient data to binary.
  2) Use a predefined DNA key to map binary sequences to DNA bases.
  3) Generate an encrypted DNA sequence.
  4) AES RES is used for encryption decryption

- **User-Friendly Interface**:
  Image steganography hides data within an image file by altering the least significant bits of each pixel’s color values. Because the LSB has the least impact on the color's appearance, the modifications remain imperceptible to the human eye. The steps involved in LSB steganography are:
  
  1) Convert the encrypted data into a binary format.
  2) Embed the binary data into the LSBs of the pixel values of the image.
  3) Add a delimiter to signify the end of the embedded data.
  4) Websocket Server for effortless transmission using Socket.IO
  5) Chatbot powered by OpenAI through text and voice input.
  6) DIACOM: Integrates DIACOM and Slice generation to generate slices of 3D-Model based the DIACOM image.
  7) Generate Analytics, Search reports using MatPlotLib.

## **Secure Communication Flow**:
1) Clinic A:

  - Accepts patient details and an image file.
  - Encrypts the patient details using the DNA encryption algorithm.
  - Embeds the encrypted data within the image using LSB steganography.
  - Provides an option to download the stego image for transmission.

2) Clinic B:

  - Receives the stego image from Hospital A.
  - Extracts the hidden data from the image using the reverse LSB steganography.
  - Decrypts the extracted DNA sequence back to the original patient data using the DNA key.

## Conclusion

This project demonstrates a secure and innovative approach to encrypting and transmitting sensitive patient information between hospitals using DNA encryption and image steganography. 
It ensures data privacy, integrity, and confidentiality while providing a user-friendly interface for healthcare professionals.

## Project Images
<details>
  <summary>Click to view images</summary>
  
  ![st1](https://github.com/user-attachments/assets/add84c66-ce86-44a9-b216-220e0ef93ae7)
  
  ![st2](https://github.com/user-attachments/assets/7694461b-670a-447f-b6a8-7db2d75d234c)
  
  ![st3](https://github.com/user-attachments/assets/3a1ee746-f1cc-4ebd-8e27-bce2a240b42b)
  
  ![st4](https://github.com/user-attachments/assets/50daa0ce-d8ae-4702-aeca-fc40f122539a)
  
  ![st5](https://github.com/user-attachments/assets/a7a1de09-259d-4a4c-a9a9-69ddc89b631e)
  
  ![st6](https://github.com/user-attachments/assets/78136391-253d-40c5-bc51-8ec57dadc92a)
  
  ![st7](https://github.com/user-attachments/assets/e9c4a56b-d146-49e3-9190-1eb51e60a5cd)
  
  ![st8](https://github.com/user-attachments/assets/245bae9c-7e0d-4b57-89e5-c407a14f0282)
  
  ![st9](https://github.com/user-attachments/assets/288fea56-7640-40b4-8052-55b12e6b8225)
  
  ![st10](https://github.com/user-attachments/assets/80ea7998-e8c8-4e5d-a062-acd73c77d8b2)
  
</details>








