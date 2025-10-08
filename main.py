# main.py
from stenography_tool import image_steg, text_steg, audio_steg, video_steg

def main():
    print("\t\t STEGANOGRAPHY")
    while True:
        print("\n\t\t\tMAIN MENU\n")
        print("1. IMAGE STEGANOGRAPHY")
        print("2. TEXT STEGANOGRAPHY")
        print("3. AUDIO STEGANOGRAPHY")
        print("4. VIDEO STEGANOGRAPHY")
        print("5. Exit\n")
        choice = input("Enter the Choice: ")

        if choice == '1':
            image_steg.img_steg()
        elif choice == '2':
            text_steg.txt_steg()
        elif choice == '3':
            audio_steg.aud_steg()
        elif choice == '4':
            video_steg.vid_steg()
        elif choice == '5':
            break
        else:
            print("Incorrect Choice")

if __name__ == "__main__":
    main()