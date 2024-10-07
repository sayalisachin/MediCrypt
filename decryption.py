def dna_to_binary(dna):
    """Convert a DNA sequence to a binary string, handling unexpected characters."""
    binary_map = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}
    binary_string = ''

    for base in dna:
        if base in binary_map:
            binary_string += binary_map[base]
        else:
            print(f"Unexpected DNA base found during decryption: {base}. Skipping.")
            continue

    return binary_string

def binary_to_text(binary):
    """Convert a binary string to human-readable text, handling invalid bytes."""
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        try:
            chars.append(chr(int(byte, 2)))
        except ValueError:
            print(f"Invalid byte encountered: {byte}. Skipping.")
            continue
    return ''.join(chars)

def decrypt_dna(encrypted_dna, key):
    """Decrypt the DNA sequence using the provided key, ensuring the sequence is valid."""
    # Reverse the encryption key
    reverse_key = {v: k for k, v in key.items()}

    # Perform reverse substitution to decrypt the DNA sequence
    decrypted_dna = ''.join(reverse_key.get(base, '') for base in encrypted_dna)

    # Validate decrypted DNA before converting to binary
    if not decrypted_dna:
        raise ValueError("Decryption resulted in an empty DNA sequence. Ensure the key is correct and data is extracted properly.")

    # Convert decrypted DNA sequence to binary
    binary_data = dna_to_binary(decrypted_dna)

    # Convert binary data to text
    text = binary_to_text(binary_data)

    # Ensure that decryption resulted in valid text
    if not text:
        raise ValueError("Decryption resulted in an empty message after converting binary to text.")

    return text
