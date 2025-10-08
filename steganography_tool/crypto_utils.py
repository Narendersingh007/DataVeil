import numpy as np

def KSA(key):
    """Key Scheduling Algorithm (KSA) for RC4."""
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S, n):
    """Pseudo-Random Generation Algorithm (PRGA) for RC4."""
    i = 0
    j = 0
    key = []
    while n > 0:
        n = n - 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        key.append(K)
    return key

def _prepare_key_array(s):
    """Helper to convert string key to array of ASCII values."""
    return [ord(c) for c in s]

def encryption(plaintext):
    """Encrypts plaintext using RC4."""
    key = input("Enter the key for encryption: ")
    key = _prepare_key_array(key)
    
    S = KSA(key)
    keystream = np.array(PRGA(S, len(plaintext)))
    
    plaintext = np.array([ord(i) for i in plaintext])
    cipher = keystream ^ plaintext
    
    ctext = ''.join([chr(c) for c in cipher])
    return ctext

def decryption(ciphertext):
    """Decrypts ciphertext using RC4."""
    key = input("Enter the key for decryption: ")
    key = _prepare_key_array(key)
    
    S = KSA(key)
    keystream = np.array(PRGA(S, len(ciphertext)))
    
    ciphertext = np.array([ord(i) for i in ciphertext])
    decoded = keystream ^ ciphertext
    
    dtext = ''.join([chr(c) for c in decoded])
    return dtext