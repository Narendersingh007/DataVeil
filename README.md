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
├── .gitignore
├── .streamlit
    └── config.toml
├── LICENSE
├── README.md
├── Sample_cover_files
    ├── cover_audio.wav
    ├── cover_image.jpg
    ├── cover_text.txt
    └── cover_video.mp4
├── assets
    └── background.jpg
├── main.py
├── requirements.txt
├── steganography_tool
    ├── __init__.py
    ├── app.py
    ├── audio_steg.py
    ├── crypto_utils.py
    ├── image_steg.py
    ├── text_steg.py
    └── video_steg.py
└── tests
    └── __init__.py
```
## How it Works 🧠

This tool primarily uses **Least Significant Bit (LSB) steganography** for images, audio, and video.

-   **LSB Insertion:** The core idea is to replace the least important bit (the last bit) of each color channel in a pixel (or each byte in an audio file) with a bit from the secret message. This change is usually too small for the human eye or ear to detect. A special delimiter (`*^*^*`) is appended to the message to mark its end during extraction.
-   **Text Steganography:** Uses Zero-Width Characters (ZWCs) – invisible Unicode characters – to encode binary data between the visible characters of a cover text.
-   **Video Steganography:** Embeds the encrypted message into the LSBs of the pixels within *one specific frame* of the video. To ensure the hidden data isn't destroyed by compression, the output video is saved using the **lossless FFV1 codec**, resulting in a potentially large file size.
-   **Encryption:** For video, the message is first encrypted using RC4 with a user-provided key before LSB insertion, adding another layer of security.

## Screenshots 📸

*(Add screenshots of your cool Streamlit UI here!)*

*Example:*
![Screenshot of Image Steganography Tool](link_to_your_screenshot.png)

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
