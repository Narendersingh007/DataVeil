# DataVeil 🔏

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A versatile steganography suite written in Python to hide secret messages within various digital media files, including images, text, audio, and video. This project provides both a command-line interface (CLI) and a user-friendly web-based GUI built with Streamlit.

## Features ✨

-   **🖼️ Image Steganography**: Hides data within the least significant bits (LSB) of image pixels (`.png`, `.jpg`).
-   **📄 Text Steganography**: Encodes messages using invisible zero-width characters (ZWC) in a cover text file.
-   **🎧 Audio Steganography**: Embeds secret messages into the least significant bits (LSB) of `.wav` audio file bytes.
-   **🎬 Video Steganography**: Hides data within the pixels of a *single, specific frame* in a video file, using a lossless codec (`FFV1`) to preserve data integrity.
-   **🔐 Encryption**: Utilizes RC4 stream cipher (Note: RC4 is outdated, consider upgrading to AES) to encrypt messages before embedding them in video files for an extra layer of security.
-   **🌐 Web Interface**: A clean, easy-to-use GUI built with Streamlit.

## Tech Stack 💻

-   **Python 3.9+**
-   **Streamlit**: For the interactive graphical user interface.
-   **OpenCV-Python**: For image and video processing.
-   **NumPy**: For efficient numerical operations.
-   **Pillow**: For image handling.

## File Structure 🌳
```
├── .gitignore                  # Tells Git which files/folders to ignore (like temp files, virtual envs)
├── .streamlit/                 # Folder for Streamlit-specific configuration
│   └── config.toml             # Streamlit config (e.g., set max file upload size)
├── LICENSE                     # Contains the project's open-source license details (MIT)
├── README.md                   # The main documentation file you see on GitHub, explaining the project
├── Sample_cover_files/         # Directory containing example media files for testing the tools
│   ├── cover_audio.wav         # Sample WAV audio file to hide data in
│   ├── cover_image.jpg         # Sample JPG image file to hide data in
│   ├── cover_text.txt          # Sample TXT text file to hide data in
│   └── cover_video.mp4         # Sample MP4 video file to hide data in
├── assets/                     # Folder for static assets used by the app (like UI images)
│   └── background.jpg          # Background image used in the Streamlit UI (if using image background)
├── main.py                     # The script to run the Command-Line Interface (CLI) version of the tool
├── requirements.txt            # Lists the necessary Python packages (like streamlit, opencv-python) to install
├── steganography_tool/         # The main Python package containing all the core logic and the GUI app
│   ├── __init__.py             # An empty file that tells Python this directory is a package
│   ├── app.py                  # The script to run the Streamlit Web Interface (GUI)
│   ├── audio_steg.py           # Contains the Python functions for audio steganography
│   ├── crypto_utils.py         # Contains the encryption/decryption helper functions (currently RC4)
│   ├── image_steg.py           # Contains the Python functions for image steganography
│   ├── text_steg.py            # Contains the Python functions for text steganography (using Zero-Width Chars)
│   └── video_steg.py           # Contains the Python functions for video steganography
└── tests/                      # Folder intended for automated tests (currently basic)
    └── __init__.py             # Makes the tests directory a Python package
```
## How it Works 🧠

This tool primarily uses **Least Significant Bit (LSB) steganography** for images, audio, and video.

-   **LSB Insertion:** The core idea is to replace the least important bit (the last bit) of each color channel in a pixel (or each byte in an audio file) with a bit from the secret message. This change is usually too small for the human eye or ear to detect. A special delimiter (`*^*^*`) is appended to the message to mark its end during extraction.
-   **Text Steganography:** Uses Zero-Width Characters (ZWCs) – invisible Unicode characters – to encode binary data between the visible characters of a cover text.
-   **Video Steganography:** Embeds the encrypted message into the LSBs of the pixels within *one specific frame* of the video. To ensure the hidden data isn't destroyed by compression, the output video is saved using the **lossless FFV1 codec**, resulting in a potentially large file size.
-   **Encryption:** For video, the message is first encrypted using RC4 with a user-provided key before LSB insertion, adding another layer of security.

## Screenshots 📸
<img width="1708" height="888" alt="Screenshot 2025-10-20 at 9 59 41 AM" src="https://github.com/user-attachments/assets/d5cce600-a64e-491a-8f88-9d7ea2379f33" />
<img width="1710" height="885" alt="Screenshot 2025-10-20 at 9 59 59 AM" src="https://github.com/user-attachments/assets/39a2a112-769d-4b3f-ac46-d7a48122ae39" />
<img width="1710" height="886" alt="Screenshot 2025-10-20 at 10 00 16 AM" src="https://github.com/user-attachments/assets/01085c06-d48d-4a39-a36f-6220a91d6a25" />
<img width="1709" height="884" alt="Screenshot 2025-10-20 at 10 00 36 AM" src="https://github.com/user-attachments/assets/3c2ed555-890b-4394-8291-6ff2c884b089" />





## Setup and Installation 🚀

To get this project running on your local machine, follow these steps.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Narendersingh007/stenography-tool.git](https://github.com/Narendersingh007/stenography-tool.git)
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd stenography-tool
    ```

3.  **(Optional but Recommended) Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use 🚀

You can run this tool in two ways:

1.  **Using the Graphical User Interface (Recommended):**
    Make sure you are in the main `stenography-tool` directory.
    ```bash
    streamlit run app.py
    ```
    This will open a user-friendly interface in your web browser. *(Note: Ensure you have created the `.streamlit/config.toml` file to handle large video uploads if needed).*

2.  **Using the Command-Line Interface:**
    ```bash
    python3 main.py
    ```
    This will launch the classic text-based menu in your terminal. Follow the prompts.

## Future Improvements 💡

-   Upgrade video encryption from RC4 to a more secure standard like AES.
-   Add support for more file types (e.g., `.bmp`, `.tiff` images; `.flac` audio).
-   Implement steganalysis features to detect potential hidden messages.
-   Centralize the `msgtobinary` function into a `utils.py` file.
-   Add more robust error handling and input validation.
-   Write unit tests for core encoding/decoding functions.

## Contributing 🤝

Contributions are welcome! If you find a bug or have an idea for an improvement, please open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
