# encryption.py

# DNA key mappings
dna_key = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
reverse_dna_key = {v: k for k, v in dna_key.items()}

def encrypt_dna(data, key):
    """
    Encrypts the given data using DNA-based encryption.
    """
    encrypted_data = ''.join(key.get(base, base) for base in data)
    return encrypted_data

def decrypt_dna(encrypted_data, reverse_key):
    """
    Decrypts the encrypted data using the reverse DNA mapping.
    """
    decrypted_data = ''.join(reverse_key.get(base, base) for base in encrypted_data)
    return decrypted_data
