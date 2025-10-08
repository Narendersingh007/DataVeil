import cv2
import numpy as np

def msgtobinary(msg):
    """Converts a message to its binary representation."""
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        return [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8:
        return format(msg, "08b")
    else:
        raise TypeError("Input type is not supported in this function")

# --- Core Logic for GUI ---

def encode_message_in_image(image_data, secret_message):
    """Encodes a message into an image and returns the modified image data."""
    max_bytes = (image_data.shape[0] * image_data.shape[1] * 3) // 8
    print(f"Maximum bytes to encode: {max_bytes}")
    
    if len(secret_message) > max_bytes:
        raise ValueError("Error: Message is too long to be encoded in this image.")

    data_with_delimiter = secret_message + '*^*^*'
    binary_data = msgtobinary(data_with_delimiter)
    
    data_index = 0
    img_data_copy = image_data.copy()

    for row in img_data_copy:
        for pixel in row:
            r, g, b = msgtobinary(pixel)
            if data_index < len(binary_data):
                pixel[0] = int(r[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < len(binary_data):
                pixel[1] = int(g[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < len(binary_data):
                pixel[2] = int(b[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index >= len(binary_data):
                break
        if data_index >= len(binary_data):
            break
            
    return img_data_copy

def decode_message_from_image(image_data):
    """Decodes a message from an image and returns the string."""
    data_binary = ""
    for row in image_data:
        for pixel in row:
            r, g, b = msgtobinary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
            
    total_bytes = [data_binary[i: i+8] for i in range(0, len(data_binary), 8)]
    
    decoded_data = ""
    for byte in total_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "*^*^*":
            return decoded_data[:-5]
    
    return None # Return None if no delimiter is found

# --- Functions for Command-Line Interface ---

def _encode_img_data_cli():
    """Handles encoding via CLI."""
    img_path = input("Enter the cover image file path: ")
    image = cv2.imread(img_path)
    if image is None:
        print("Image not found. Please check the path.")
        return
    
    data = input("\nEnter the data to be encoded in the image: ")
    if len(data) == 0:
        print("Data is empty.")
        return
    
    stego_image_name = input("\nEnter the name for the new stego image (e.g., stego.png): ")
    
    try:
        stego_image = encode_message_in_image(image, data)
        cv2.imwrite(stego_image_name, stego_image)
        print(f"\nData encoded successfully. Stego image saved as {stego_image_name}")
    except ValueError as e:
        print(e)

def _decode_img_data_cli():
    """Handles decoding via CLI."""
    img_path = input("Enter the stego image file path to decode: ")
    image = cv2.imread(img_path)
    if image is None:
        print("Image not found. Please check the path.")
        return

    message = decode_message_from_image(image)
    if message:
        print("\n\nThe hidden data was: ", message)
    else:
        print("\nNo hidden message found.")

def img_steg():
    """Main menu for Image Steganography (CLI)."""
    while True:
        print("\n\t\tIMAGE STEGANOGRAPHY OPERATIONS")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Back to Main Menu")
        choice = input("Enter the Choice: ")

        if choice == '1':
            _encode_img_data_cli()
        elif choice == '2':
            _decode_img_data_cli()
        elif choice == '3':
            break
        else:
            print("Incorrect Choice.")