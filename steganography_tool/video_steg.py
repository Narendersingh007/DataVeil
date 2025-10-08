
import cv2
import numpy as np
from .crypto_utils import encryption, decryption

# Re-defining msgtobinary here or putting it in a shared utils.py is better.
# For simplicity in this example, it's duplicated from image_steg.
def msgtobinary(msg):
    if type(msg) == str: return ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == np.ndarray: return [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8: return format(msg, "08b")
    else: raise TypeError("Input type not supported")

def _embed(frame):
    """Embeds encrypted data into a single video frame."""
    data = input("\nEnter the data to be encoded in video: ")
    data = encryption(data)
    print(f"The encrypted data is: {data}")
    
    if len(data) == 0:
        raise ValueError('Data is empty')
    
    data += '*^*^*'
    binary_data = msgtobinary(data)
    
    data_index = 0
    for row in frame:
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
    return frame

def _extract(frame):
    """Extracts and decrypts data from a single video frame."""
    data_binary = ""
    for row in frame:
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
            final_msg = decryption(decoded_data[:-5])
            print(f"\n\nThe hidden data was: {final_msg}")
            return

def _encode_vid_data():
    """Main function to encode data into a video file."""
    cap = cv2.VideoCapture(input("Enter cover video file path: "))
    vidcap = cv2.VideoCapture(input("Re-enter cover video file path: "))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))
    size = (frame_width, frame_height)
    out = cv2.VideoWriter('stego_video.avi', fourcc, 25.0, size)
    
    max_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        max_frame += 1
    cap.release()
    print(f"Total number of frames in video: {max_frame}")
    
    n = int(input(f"Enter the frame number (1-{max_frame}) to embed data: "))
    frame_number = 0
    while vidcap.isOpened():
        ret, frame = vidcap.read()
        if not ret: break
        frame_number += 1
        if frame_number == n:
            frame = _embed(frame)
        out.write(frame)
        
    vidcap.release()
    out.release()
    print("\nData encoded successfully in the video 'stego_video.avi'")

def _decode_vid_data():
    """Main function to decode data from a video file."""
    cap = cv2.VideoCapture(input("Enter stego video file path: "))
    max_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        max_frame += 1
    cap.release()
    print(f"Total frames: {max_frame}")

    n = int(input("Enter the frame number to extract data from: "))
    vidcap = cv2.VideoCapture(input("Re-enter stego video file path: "))
    
    frame_number = 0
    while vidcap.isOpened():
        ret, frame = vidcap.read()
        if not ret: break
        frame_number += 1
        if frame_number == n:
            _extract(frame)
            break
    vidcap.release()

def vid_steg():
    """Main menu for Video Steganography."""
    while True:
        print("\n\t\tVIDEO STEGANOGRAPHY OPERATIONS")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Back to Main Menu")
        choice = input("Enter the Choice: ")
        if choice == '1':
            _encode_vid_data()
        elif choice == '2':
            _decode_vid_data()
        elif choice == '3':
            break
        else:
            print("Incorrect Choice")