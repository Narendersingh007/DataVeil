# steganography_tool/video_steg.py
import cv2
import numpy as np
import tempfile
import os
# Use a relative import to get the updated crypto functions
from . import crypto_utils

def msgtobinary(msg):
    """Converts a message to its binary representation."""
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        return [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8:
        return format(msg, "08b")
    else:
        raise TypeError("Input type not supported")

# --- Core Logic for GUI ---

def _embed_data_in_frame(frame, secret_message, key):
    """Embeds encrypted data into a single video frame."""
    data = crypto_utils.encryption(secret_message, key)
    print(f"The encrypted data is: {data}")

    if len(data) == 0:
        raise ValueError('Data is empty')

    data += '*^*^*'
    binary_data = msgtobinary(data)

    # Check for space
    max_bytes = (frame.shape[0] * frame.shape[1] * 3) // 8
    if len(data) > max_bytes:
        raise ValueError("Error: Message is too large for a single video frame.")

    data_index = 0
    frame_copy = frame.copy()

    for row in frame_copy:
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
    return frame_copy

def _extract_data_from_frame(frame, key):
    """Extracts and decrypts data from a single video frame."""
    data_binary = ""
    decoded_data = ""
    delimiter = "*^*^*"

    for row in frame:
        for pixel in row:
            r, g, b = msgtobinary(pixel)
            for bit in [r[-1], g[-1], b[-1]]:
                data_binary += bit
                if len(data_binary) == 8:
                    try:
                        decoded_char = chr(int(data_binary, 2))
                        decoded_data += decoded_char
                    except ValueError:
                        pass # Ignore non-ASCII bytes
                    data_binary = ""

                    if decoded_data.endswith(delimiter):
                        final_msg = crypto_utils.decryption(decoded_data[:-len(delimiter)], key)
                        return final_msg
    return None

def encode_message_in_video(video_bytes, secret_message, frame_number, key):
    """Hides data in a specific frame of a video using a lossless codec. Returns new video as bytes."""

    # Create a temporary file for the input video
    # Use .tmp extension to avoid potential conflicts if input is also .avi
    with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as temp_in:
        temp_in.write(video_bytes)
        temp_in_path = temp_in.name

    # Create a temporary file for the output video (always .avi for FFV1)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.avi') as temp_out:
        temp_out_path = temp_out.name

    vidcap = None
    out = None
    try:
        vidcap = cv2.VideoCapture(temp_in_path)
        if not vidcap.isOpened():
            raise IOError("Could not open input video file for reading.")

        # Get video properties
        # **** USE LOSSLESS FFV1 CODEC ****
        fourcc = cv2.VideoWriter_fourcc(*'FFV1')

        fps = vidcap.get(cv2.CAP_PROP_FPS)
        # Use round instead of int for potentially non-integer fps values
        fps = round(fps) if fps else 30 # Default to 30 if fps is 0 or invalid
        frame_width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (frame_width, frame_height)

        if frame_width == 0 or frame_height == 0:
             raise ValueError("Could not read video dimensions.")

        out = cv2.VideoWriter(temp_out_path, fourcc, fps, size)
        if not out.isOpened():
            raise IOError("Could not open video writer for the output file.")

        current_frame = 0
        while True: # Use True loop and break on ret false
            ret, frame = vidcap.read()
            if not ret:
                break # End of video

            if current_frame == frame_number:
                print(f"Embedding data in frame {frame_number}")
                try:
                    frame = _embed_data_in_frame(frame, secret_message, key)
                except ValueError as e: # Catch potential size error early
                     raise e

            out.write(frame)
            current_frame += 1

        # Check frame number validity *after* processing
        if frame_number >= current_frame:
            raise ValueError(f"Error: Frame number {frame_number} is out of range. Video only has {current_frame} frames (0-{current_frame-1}).")

        # Release resources *before* reading output file
        vidcap.release()
        out.release()
        vidcap = None
        out = None


        # Read the bytes from the output temp file
        with open(temp_out_path, 'rb') as f:
            output_video_bytes = f.read()

        return output_video_bytes

    finally:
        # Ensure resources are released even if errors occurred
        if vidcap is not None and vidcap.isOpened():
            vidcap.release()
        if out is not None and out.isOpened():
            out.release()
        # Clean up temporary files
        if 'temp_in_path' in locals() and os.path.exists(temp_in_path):
            os.unlink(temp_in_path)
        if 'temp_out_path' in locals() and os.path.exists(temp_out_path):
            os.unlink(temp_out_path)


def decode_message_from_video(video_bytes, frame_number, key):
    """Extracts data from a specific frame of a video."""

    # Create a temporary file for the input video (can be .avi or original format)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as temp_in:
        temp_in.write(video_bytes)
        temp_in_path = temp_in.name

    vidcap = None
    try:
        vidcap = cv2.VideoCapture(temp_in_path)
        if not vidcap.isOpened():
            raise IOError("Could not open video file for decoding.")

        total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0 :
             # Try getting it again if the first read failed
             vidcap.set(cv2.CAP_PROP_POS_FRAMES, 0)
             total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
             if total_frames <= 0:
                  raise ValueError("Could not determine video frame count.")


        if frame_number >= total_frames:
            raise ValueError(f"Error: Frame number {frame_number} is out of range. Video only has {total_frames} frames (0-{total_frames-1}).")

        # Set the video to the specific frame
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = vidcap.read()

        if not ret:
            raise IOError(f"Could not read frame {frame_number}.")

        # Release before returning
        vidcap.release()
        vidcap = None

        # Extract data
        return _extract_data_from_frame(frame, key)

    finally:
        # Ensure release and cleanup
        if vidcap is not None and vidcap.isOpened():
            vidcap.release()
        # Clean up temp file
        if os.path.exists(temp_in_path):
            os.unlink(temp_in_path)

# --- Functions for Command-Line Interface (CLI) ---

def vid_steg():
    """Main menu for Video Steganography (CLI)."""
    print("\n\t\tVIDEO STEGANOGRAPHY OPERATIONS")
    print("CLI for Video Steganography is not fully implemented in this refactor.")
    print("Please use the Streamlit GUI.")