

def _binary_to_decimal(binary):
    return int(binary, 2)

def _txt_encode(text):
    """Encodes a string into a custom binary format and then into zero-width characters."""
    l = len(text)
    i = 0
    add = ''
    while i < l:
        t = ord(text[i])
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
        i += 1
    
    res1 = add + "111111111111"
    print(f"The string after binary conversion applying all the transformation: {res1}")
    print(f"Length of binary after conversion: {len(res1)}")

    # Hide in cover text
    ZWC = {"00": u'\u200C', "01": u'\u202C', "11": u'\u202D', "10": u'\u200E'}
    
    with open("cover_text.txt", "r+") as file1, open("stego_text.txt", "w+", encoding="utf-8") as file3:
        words = file1.read().split()
        i = 0
        while i < len(res1):
            s = words[int(i/12)]
            j = 0
            HM_SK = ""
            while j < 12:
                x = res1[j+i] + res1[i+j+1]
                HM_SK += ZWC[x]
                j += 2
            s1 = s + HM_SK
            file3.write(s1 + " ")
            i += 12
        
        t = int(len(res1) / 12)
        while t < len(words):
            file3.write(words[t] + " ")
            t += 1

    print("\nStego file 'stego_text.txt' has been successfully generated.")

def _decode_txt_data():
    """Decodes a message from a text stego file."""
    ZWC_reverse = {u'\u200C': "00", u'\u202C': "01", u'\u202D': "11", u'\u200E': "10"}
    stego_file = input("\nEnter the stego file name to decode (e.g., stego_text.txt): ")
    
    with open(stego_file, "r", encoding="utf-8") as file4:
        temp = ''
        for line in file4:
            for word in line.split():
                binary_extract = ""
                for letter in word:
                    if letter in ZWC_reverse:
                        binary_extract += ZWC_reverse[letter]
                
                if binary_extract == "111111111111":
                    break
                else:
                    temp += binary_extract
            else:
                continue
            break
            
    print(f"\nEncrypted message presented in code bits: {temp}")
    print(f"Length of encoded bits: {len(temp)}")

    # Decode the binary string
    final = ''
    i = 0
    while i < len(temp):
        t3 = temp[i:i+4]
        t4 = temp[i+4:i+12]
        if t3 == '0110':
            decimal_data = _binary_to_decimal(t4)
            final += chr((decimal_data ^ 170) + 48)
        elif t3 == '0011':
            decimal_data = _binary_to_decimal(t4)
            final += chr((decimal_data ^ 170) - 48)
        i += 12
        
    print(f"\nMessage after decoding from the stego file: {final}")

def txt_steg():
    """Main menu for Text Steganography."""
    while True:
        print("\n\t\tTEXT STEGANOGRAPHY OPERATIONS")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Back to Main Menu")
        choice = input("Enter the Choice: ")
        
        if choice == '1':
            text1 = input("\nEnter data to be encoded: ")
            _txt_encode(text1)
        elif choice == '2':
            _decode_txt_data()
        elif choice == '3':
            break
        else:
            print("Incorrect Choice")