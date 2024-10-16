from PIL import Image
import numpy as np

def binary_to_message(binary):
    """Convert a binary string to a human-readable message, handling potential errors."""
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        try:
            chars.append(chr(int(byte, 2)))
        except ValueError:
            print(f"Invalid byte encountered during conversion: {byte}. Skipping.")
            continue
    return ''.join(chars)

def extract_message(stego_image_path):
    """Extract a hidden message from an image using LSB steganography."""
    img = Image.open(stego_image_path)
    data = np.array(img)

    # Flatten the image data to access the LSBs
    flat_data = data.flatten()

    binary_message = ""
    for i in range(len(flat_data)):
        # Extract the LSB of each byte
        binary_message += str(flat_data[i] & 1)

        # Check for delimiter to know when the message ends
        if binary_message[-16:] == '1111111111111110':
            break

    # Remove the delimiter
    binary_message = binary_message[:-16]

    # Validate the extracted binary message
    if not binary_message:
        raise ValueError("Extracted message is empty. Ensure the image contains a hidden message.")

    # Convert binary data to text
    message = binary_to_message(binary_message)
    return message
