# steganography_tool/audio_steg.py
import wave
import io

# --- Core Logic for GUI ---

def encode_message_in_audio(audio_bytes, secret_message):
    """Hides a secret message in the LSB of audio bytes and returns new bytes."""
    data = secret_message + '*^*^*'  # Delimiter
    
    try:
        # Read the audio bytes from memory
        with wave.open(io.BytesIO(audio_bytes), mode='rb') as song:
            params = song.getparams()
            frames = song.readframes(song.getnframes())
            frame_list = list(frames)
            frame_bytes = bytearray(frame_list)

            # Convert secret data to bit array
            result = []
            for char in data:
                bits = bin(ord(char))[2:].zfill(8)
                result.extend([int(b) for b in bits])
            
            # Check if message will fit
            if len(result) > len(frame_bytes):
                raise ValueError("Error: Message is too large for this audio file.")

            # Embed bits into LSB of each frame byte
            j = 0
            for i in range(len(result)):
                frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
                j += 1
            
            frame_modified = bytes(frame_bytes)
            
            # Write the modified frames to an in-memory buffer
            with io.BytesIO() as out_buffer:
                with wave.open(out_buffer, 'wb') as fd:
                    fd.setparams(params)
                    fd.writeframes(frame_modified)
                
                return out_buffer.getvalue()

    except wave.Error as e:
        raise ValueError(f"Error processing audio file. Is it a valid .wav file? Error: {e}")
    except Exception as e:
        raise e

def decode_message_from_audio(audio_bytes):
    """Extracts a secret message from the LSB of audio bytes."""
    delimiter = "*^*^*"
    try:
        with wave.open(io.BytesIO(audio_bytes), mode='rb') as song:
            frames = song.readframes(song.getnframes())
            frame_bytes = bytearray(list(frames))

            extracted_bits = ""
            for i in range(len(frame_bytes)):
                extracted_bits += str(frame_bytes[i] & 1)

            all_bytes = [extracted_bits[i: i+8] for i in range(0, len(extracted_bits), 8)]
            
            decoded_data = ""
            for byte in all_bytes:
                if len(byte) == 8:
                    try:
                        decoded_data += chr(int(byte, 2))
                    except ValueError:
                        pass # Ignore non-ASCII bytes
                    
                    if decoded_data.endswith(delimiter):
                        return decoded_data[:-len(delimiter)]
        
        return None # No delimiter found

    except wave.Error as e:
        raise ValueError(f"Error processing audio file. Is it a valid .wav file? Error: {e}")
    except Exception as e:
        raise e


# --- Functions for Command-Line Interface ---

def _encode_aud_data_cli():
    """Handles encoding via CLI."""
    try:
        nameoffile = input("Enter name of the audio file (with .wav extension): ")
        with open(nameoffile, 'rb') as f:
            audio_bytes = f.read()
            
        data = input("\nEnter the secret message: ")
        stegofile = input("\nEnter name of the new stego audio file (with .wav extension): ")

        modified_bytes = encode_message_in_audio(audio_bytes, data)
        
        with open(stegofile, 'wb') as fd:
            fd.write(modified_bytes)
            
        print("\nData encoded successfully.")

    except FileNotFoundError:
        print("Audio file not found. Please check the file name.")
    except Exception as e:
        print(f"An error occurred: {e}")

def _decode_aud_data_cli():
    """Handles decoding via CLI."""
    try:
        nameoffile = input("Enter name of the audio file to be decoded: ")
        with open(nameoffile, 'rb') as f:
            audio_bytes = f.read()

        decoded_message = decode_message_from_audio(audio_bytes)
        
        if decoded_message:
            print("The hidden data was: ", decoded_message)
        else:
            print("No hidden message was found.")

    except FileNotFoundError:
        print("Audio file not found. Please check the file name.")
    except Exception as e:
        print(f"An error occurred: {e}")

def aud_steg():
    """Main menu for Audio Steganography (CLI)."""
    while True:
        print("\n\t\tAUDIO STEGANOGRAPHY OPERATIONS")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Back to Main Menu")
        choice = input("Enter the Choice: ")
        if choice == '1':
            _encode_aud_data_cli()
        elif choice == '2':
            _decode_aud_data_cli()
        elif choice == '3':
            break
        else:
            print("Incorrect Choice")