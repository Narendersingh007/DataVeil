import sys
import os
import streamlit as st
from PIL import Image
import numpy as np
import cv2
import io

# --- FORCE PARENT DIRECTORY ONTO PATH ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# -----------------------------------------

from steganography_tool import image_steg, text_steg, audio_steg, video_steg

st.set_page_config(page_title="Steganography Suite", layout="wide")

st.title("🔏 Steganography Suite")
st.write("Hide your secret messages in digital media.")

# Sidebar for navigation
st.sidebar.title("Choose Your Tool")
tool = st.sidebar.selectbox("Select a steganography method:",
                            ["Image Steganography", "Text Steganography", "Audio Steganography", "Video Steganography"])

# --- IMAGE STEGANOGRAPHY ---
if tool == "Image Steganography":
    st.header("Image Steganography")

    option = st.radio("What do you want to do?", ('Encode', 'Decode'), horizontal=True)

    if option == 'Encode':
        st.subheader("Encode a Message")
        uploaded_file = st.file_uploader("Choose a cover image...", type=["png", "jpg", "jpeg"])
        secret_message = st.text_area("Enter the secret message:")

        if st.button("Encode Message") and uploaded_file is not None and secret_message:
            with st.spinner('Encoding your message... Please wait.'):
                pil_image = Image.open(uploaded_file).convert('RGB')
                cover_image = np.array(pil_image)
                cover_image_bgr = cv2.cvtColor(cover_image, cv2.COLOR_RGB2BGR)

                try:
                    stego_image_data = image_steg.encode_message_in_image(cover_image_bgr, secret_message)
                    
                    stego_image_rgb = cv2.cvtColor(stego_image_data, cv2.COLOR_BGR2RGB)
                    
                    pil_stego_image = Image.fromarray(stego_image_rgb)
                    buf = io.BytesIO()
                    pil_stego_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()

                    st.success("Message encoded successfully!")
                    st.image(pil_stego_image, caption="Stego Image Preview")
                    st.download_button(
                        label="Download Stego Image",
                        data=byte_im,
                        file_name="stego_image.png",
                        mime="image/png"
                    )

                except ValueError as e:
                    st.error(e)

    elif option == 'Decode':
        st.subheader("Decode a Message")
        uploaded_file = st.file_uploader("Choose a stego image to decode...", type=["png", "jpg", "jpeg"])

        if st.button("Decode Message") and uploaded_file is not None:
            with st.spinner('Decoding your message...'):
                pil_image = Image.open(uploaded_file).convert('RGB')
                stego_image = np.array(pil_image)
                stego_image_bgr = cv2.cvtColor(stego_image, cv2.COLOR_RGB2BGR)

                decoded_message = image_steg.decode_message_from_image(stego_image_bgr)

                if decoded_message:
                    st.success("Found a hidden message!")
                    st.text_area("Decoded Message", value=decoded_message, height=200)
                else:
                    st.warning("No hidden message was found in the image.")

# Add placeholders for other tools
elif tool == "Text Steganography":
    st.header("Text Steganography")
    st.info("GUI for Text Steganography is under construction.")

elif tool == "Audio Steganography":
    st.header("Audio Steganography")
    st.info("GUI for Audio Steganography is under construction.")

elif tool == "Video Steganography":
    st.header("Video Steganography")
    st.info("GUI for Video Steganography is under construction.")