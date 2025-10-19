# stenography_tool/text_steg.py

# A dictionary mapping binary pairs to zero-width characters
ZWC = {"00": u'\u200C', "01": u'\u202C', "11": u'\u202D', "10": u'\u200E'}
# The reverse dictionary for decoding
ZWC_REVERSE = {u'\u200C': "00", u'\u202C': "01", u'\u202D': "11", u'\u200E': "10"}

def _binary_to_decimal(binary):
    """Converts a binary string to an integer."""
    return int(binary, 2)

def _secret_to_binary(text):
    """Converts the secret message into a custom binary string."""
    add = ''
    for char in text:
        t = ord(char)
        if 32 <= t <= 64:
            t1 = t + 48
            t2 = t1 ^ 170  # 170: 10101010
            res = bin(t2)[2:].zfill(8)
            add += "0011" + res
        else:
            t1 = t - 48
            t2 = t1 ^ 170
            res = bin(t2)[2:].zfill(8)
            add += "0110" + res
    
    # Add delimiter
    res1 = add + "111111111111"
    print(f"Binary after conversion: {res1}")
    return res1

def _binary_to_secret(binary_string):
    """Decodes the custom binary string back into the secret message."""
    final = ''
    i = 0
    while i < len(binary_string):
        t3 = binary_string[i:i+4]
        t4 = binary_string[i+4:i+12]
        if not t4 or len(t4) < 8:
            break # Stop if we are at the end

        if t3 == '0110':
            decimal_data = _binary_to_decimal(t4)
            final += chr((decimal_data ^ 170) + 48)
        elif t3 == '0011':
            decimal_data = _binary_to_decimal(t4)
            final += chr((decimal_data ^ 170) - 48)
        i += 12
    return final

# --- Core Logic for GUI ---

def encode_message_in_text(cover_text, secret_message):
    """Hides a secret message in a cover text using zero-width characters."""
    binary_secret = _secret_to_binary(secret_message)
    words = cover_text.split()
    
    if len(binary_secret) // 12 > len(words):
        raise ValueError("Error: The cover text is too short for this secret message.")

    stego_words = []
    i = 0
    while i < len(binary_secret):
        if (i // 12) >= len(words):
            # This should not be hit if the check above is correct, but as a safeguard
            raise ValueError("Error: Ran out of words in cover text during encoding.")
            
        s = words[int(i/12)]
        j = 0
        zwc_chars = ""
        while j < 12:
            x = binary_secret[j+i] + binary_secret[i+j+1]
            zwc_chars += ZWC[x]
            j += 2
        
        stego_words.append(s + zwc_chars)
        i += 12
    
    # Add the rest of the words from the cover text
    stego_words.extend(words[int(len(binary_secret)/12):])
    
    return " ".join(stego_words)

def decode_message_from_text(stego_text):
    """Extracts a secret message from a stego text file."""
    temp = ''
    for line in stego_text.splitlines():
        for word in line.split():
            binary_extract = ""
            for letter in word:
                if letter in ZWC_REVERSE:
                    binary_extract += ZWC_REVERSE[letter]
            
            if binary_extract == "111111111111": # Check for delimiter
                return _binary_to_secret(temp)
            else:
                temp += binary_extract
    
    return None # No delimiter found

# --- Functions for Command-Line Interface ---

def _txt_encode_cli():
    """Handles encoding via CLI."""
    try:
        # Note: This still uses a hardcoded path for the CLI.
        with open("Sample_cover_files/cover_text.txt", "r+") as file1:
            cover_text = file1.read()
    except FileNotFoundError:
        print("Error: 'Sample_cover_files/cover_text.txt' not found.")
        return

    text1 = input("\nEnter data to be encoded: ")
    
    try:
        stego_text = encode_message_in_text(cover_text, text1)
        
        nameoffile = input("\nEnter the name of the Stego file after Encoding (with .txt): ")
        with open(nameoffile, "w+", encoding="utf-8") as file3:
            file3.write(stego_text)
        
        print(f"\nStego file '{nameoffile}' has been successfully generated.")
    except ValueError as e:
        print(e)

def _decode_txt_data_cli():
    """Handles decoding via CLI."""
    stego_file = input("\nPlease enter the stego file name (with extension) to decode: ")
    try:
        with open(stego_file, "r", encoding="utf-8") as file4:
            stego_text = file4.read()
            
        final_message = decode_message_from_text(stego_text)
        
        if final_message:
            print(f"\nMessage after decoding from the stego file: {final_message}")
        else:
            print("\nCould not find a hidden message.")
            
    except FileNotFoundError:
        print(f"Error: File '{stego_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def txt_steg():
    """Main menu for Text Steganography (CLI)."""
    while True:
        print("\n\t\tTEXT STEGANOGRAPHY OPERATIONS")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Back to Main Menu")
        choice = input("Enter the Choice: ")
        
        if choice == '1':
            _txt_encode_cli()
        elif choice == '2':
            _decode_txt_data_cli()
        elif choice == '3':
            break
        else:
            print("Incorrect Choice")