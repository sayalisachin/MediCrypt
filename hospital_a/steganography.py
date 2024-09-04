from PIL import Image
import numpy as np

def message_to_binary(message):
    """Convert a string message to a binary string."""
    return ''.join(format(ord(char), '08b') for char in message)

def embed_message(image, message):
    """Embed a binary message into an image using LSB steganography."""
    data = np.array(image)

    # Check if the image can hold the message
    max_bytes = data.size // 8
    if len(message) > max_bytes:
        raise ValueError("Message is too large to hide in the selected image.")

    binary_message = message_to_binary(message) + '1111111111111110'  # Add a delimiter to mark the end of the message

    # Flatten the image data
    flat_data = data.flatten()

    # Embed the message
    for i in range(len(binary_message)):
        flat_data[i] = (flat_data[i] & ~1) | int(binary_message[i])  # Set the LSB to the current bit of the message
    
    # Reshape the flattened data back to the original image shape
    new_data = flat_data.reshape(data.shape)
    new_img = Image.fromarray(new_data.astype('uint8'))

    return new_img  # Return the PIL Image object
