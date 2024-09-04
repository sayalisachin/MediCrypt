def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_dna(binary):
    dna_map = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
    return ''.join(dna_map[binary[i:i+2]] for i in range(0, len(binary), 2))

def encrypt_dna(text, key):
    binary_data = text_to_binary(text)
    dna_data = binary_to_dna(binary_data)
    # Apply encryption key (DNA substitution/permutation)
    encrypted_dna = ''.join(key[base] for base in dna_data)
    return encrypted_dna
