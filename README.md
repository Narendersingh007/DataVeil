#  Steganography Suite 🔏

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

A versatile steganography tool written in Python to hide secret messages within various digital media files, including images, text, audio, and video. This project provides both a command-line interface (CLI) and a user-friendly web-based GUI built with Streamlit.

## Features ✨

-   **🖼️ Image Steganography**: Hides data within the least significant bits (LSB) of image pixels (`.png`, `.jpg`).
-   **📄 Text Steganography**: Encodes messages using zero-width characters in a cover text file.
-   **🎧 Audio Steganography**: Embeds secret messages into the bytes of `.wav` audio files.
-   **🎬 Video Steganography**: Hides data within the pixels of a specific frame in a video file.
-   **🔐 Encryption**: Utilizes RC4 stream cipher to encrypt messages before embedding them in video files for an extra layer of security.

## Tech Stack 💻

-   **Python 3**
-   **Streamlit**: For the interactive graphical user interface.
-   **OpenCV-Python**: For image and video processing.
-   **NumPy**: For efficient numerical operations.

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

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use 🚀

You can run this tool in two ways:

1.  **Using the Graphical User Interface (Recommended):**
    ```bash
    streamlit run app.py
    ```
    This will open a user-friendly interface in your web browser.

2.  **Using the Command-Line Interface:**
    ```bash
    python3 main.py
    ```
    This will launch the classic text-based menu in your terminal.
