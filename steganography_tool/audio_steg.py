
import wave

def _encode_aud_data():
    """Encodes a secret message into a .wav file."""
    try:
        nameoffile = input("Enter name of the audio file (with .wav extension): ")
        with wave.open(nameoffile, mode='rb') as song:
            nframes = song.getnframes()
            frames = song.readframes(nframes)
            frame_list = list(frames)
            frame_bytes = bytearray(frame_list)

            data = input("\nEnter the secret message: ")
            data += '*^*^*'  # Delimiter

            result = []
            for char in data:
                bits = bin(ord(char))[2:].zfill(8)
                result.extend([int(b) for b in bits])
            
            j = 0
            for i in range(len(result)):
                frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
                j += 1
            
            frame_modified = bytes(frame_bytes)
            
            stegofile = input("\nEnter name of the new stego audio file (with .wav extension): ")
            with wave.open(stegofile, 'wb') as fd:
                fd.setparams(song.getparams())
                fd.writeframes(frame_modified)
            print("\nData encoded successfully.")

    except FileNotFoundError:
        print("Audio file not found. Please check the file name.")
    except Exception as e:
        print(f"An error occurred: {e}")

def _decode_aud_data():
    """Decodes a secret message from a .wav file."""
    try:
        nameoffile = input("Enter name of the audio file to be decoded: ")
        with wave.open(nameoffile, mode='rb') as song:
            nframes = song.getnframes()
            frames = song.readframes(nframes)
            frame_bytes = bytearray(list(frames))

            extracted = ""
            for i in range(len(frame_bytes)):
                extracted += str(frame_bytes[i] & 1)

            all_bytes = [extracted[i: i+8] for i in range(0, len(extracted), 8)]
            
            decoded_data = ""
            for byte in all_bytes:
                if len(byte) == 8:
                    decoded_data += chr(int(byte, 2))
                    if decoded_data[-5:] == "*^*^*":
                        print("The hidden data was: ", decoded_data[:-5])
                        return
    except FileNotFoundError:
        print("Audio file not found. Please check the file name.")
    except Exception as e:
        print(f"An error occurred: {e}")

def aud_steg():
    """Main menu for Audio Steganography."""
    while True:
        print("\n\t\tAUDIO STEGANOGRAPHY OPERATIONS")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Back to Main Menu")
        choice = input("Enter the Choice: ")
        if choice == '1':
            _encode_aud_data()
        elif choice == '2':
            _decode_aud_data()
        elif choice == '3':
            break
        else:
            print("Incorrect Choice")