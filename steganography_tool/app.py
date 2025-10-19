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

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Steganography Suite",
    page_icon="🔏",  # Adds a nice emoji to the browser tab
    layout="wide"
)


# --- SIDEBAR ---
with st.sidebar:
    st.title("🔏 Steganography Suite")
    st.write("Hide your secret messages in digital media. This tool uses classic LSB steganography.")
    tool = st.sidebar.selectbox("Select a steganography method:",
                                ["Image Steganography", "Text Steganography", "Audio Steganography", "Video Steganography"])
    st.info("All files are processed in your browser. No data is saved on any server.")

# --- MAIN PAGE ---

# --- IMAGE STEGANOGRAPHY ---
if tool == "Image Steganography":
    st.header("🖼️ Image Steganography")
    st.write("Hides data within the least significant bits (LSB) of image pixels.")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Encode a Message")
        uploaded_file = st.file_uploader("Choose a cover image...", type=["png", "jpg", "jpeg"], key="img_enc_file")
        secret_message = st.text_area("Enter the secret message:", key="img_enc_msg")

        if st.button("Encode Message", key="img_enc_btn") and uploaded_file is not None and secret_message:
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
                    
                    with st.expander("✅ Success! Click to see results", expanded=True):
                        st.image(pil_stego_image, caption="Stego Image Preview")
                        st.download_button(
                            label="Download Stego Image",
                            data=byte_im,
                            file_name="stego_image.png",
                            mime="image/png"
                        )
                except ValueError as e:
                    st.error(e)

    with col2:
        st.subheader("Decode a Message")
        uploaded_file_dec = st.file_uploader("Choose a stego image to decode...", type=["png", "jpg", "jpeg"], key="img_dec_file")

        if st.button("Decode Message", key="img_dec_btn") and uploaded_file_dec is not None:
            with st.spinner('Decoding your message...'):
                pil_image = Image.open(uploaded_file_dec).convert('RGB')
                stego_image = np.array(pil_image)
                stego_image_bgr = cv2.cvtColor(stego_image, cv2.COLOR_RGB2BGR)
                decoded_message = image_steg.decode_message_from_image(stego_image_bgr)
                
                if decoded_message:
                    with st.expander("✅ Success! Click to see results", expanded=True):
                        st.text_area("Decoded Message", value=decoded_message, height=200, key="img_dec_msg")
                else:
                    st.warning("No hidden message was found in the image.")

# --- TEXT STEGANOGRAPHY ---
elif tool == "Text Steganography":
    st.header("📄 Text Steganography")
    st.write("Hides data using invisible zero-width characters in a cover text file.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Encode a Message")
        uploaded_file = st.file_uploader("Choose a cover text file (.txt)...", type=["txt"], key="txt_enc_file")
        secret_message = st.text_area("Enter the secret message:", key="txt_enc_msg")

        if st.button("Encode Message", key="txt_enc_btn") and uploaded_file is not None and secret_message:
            with st.spinner('Encoding your message...'):
                try:
                    cover_text = uploaded_file.getvalue().decode("utf-8")
                    stego_text = text_steg.encode_message_in_text(cover_text, secret_message)
                    
                    with st.expander("✅ Success! Click to see results", expanded=True):
                        st.text_area("Stego Text (copy this or download)", value=stego_text, height=300, key="txt_stego_text")
                        st.download_button(
                            label="Download Stego Text",
                            data=stego_text,
                            file_name="stego_text.txt",
                            mime="text/plain"
                        )
                except ValueError as e:
                    st.error(e)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    with col2:
        st.subheader("Decode a Message")
        uploaded_file_dec = st.file_uploader("Choose a stego text file to decode...", type=["txt"], key="txt_dec_file")

        if st.button("Decode Message", key="txt_dec_btn") and uploaded_file_dec is not None:
            with st.spinner('Decoding your message...'):
                try:
                    stego_text = uploaded_file_dec.getvalue().decode("utf-8")
                    decoded_message = text_steg.decode_message_from_text(stego_text)
                    
                    if decoded_message:
                        with st.expander("✅ Success! Click to see results", expanded=True):
                            st.text_area("Decoded Message", value=decoded_message, height=200, key="txt_dec_msg")
                    else:
                        st.warning("No hidden message was found in the text.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

# --- AUDIO STEGANOGRAPHY ---
elif tool == "Audio Steganography":
    st.header("🎧 Audio Steganography")
    st.write("Hides data in the LSB of a .wav audio file.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Encode a Message")
        uploaded_file = st.file_uploader("Choose a cover audio file (.wav)...", type=["wav"], key="aud_enc_file")
        secret_message = st.text_area("Enter the secret message:", key="aud_enc_msg")

        if st.button("Encode Message", key="aud_enc_btn") and uploaded_file is not None and secret_message:
            with st.spinner('Encoding your message... This may take a moment.'):
                try:
                    audio_bytes = uploaded_file.getvalue()
                    stego_audio_bytes = audio_steg.encode_message_in_audio(audio_bytes, secret_message)
                    
                    with st.expander("✅ Success! Click to see results", expanded=True):
                        st.write("Listen to the stego audio (it should sound identical):")
                        st.audio(stego_audio_bytes, format="audio/wav")
                        st.download_button(
                            label="Download Stego Audio",
                            data=stego_audio_bytes,
                            file_name="stego_audio.wav",
                            mime="audio/wav"
                        )
                except ValueError as e:
                    st.error(e)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    with col2:
        st.subheader("Decode a Message")
        uploaded_file_dec = st.file_uploader("Choose a stego audio file to decode...", type=["wav"], key="aud_dec_file")

        if st.button("Decode Message", key="aud_dec_btn") and uploaded_file_dec is not None:
            with st.spinner('Decoding your message...'):
                try:
                    audio_bytes = uploaded_file_dec.getvalue()
                    decoded_message = audio_steg.decode_message_from_audio(audio_bytes)
                    
                    if decoded_message:
                        with st.expander("✅ Success! Click to see results", expanded=True):
                            st.text_area("Decoded Message", value=decoded_message, height=200, key="aud_dec_msg")
                    else:
                        st.warning("No hidden message was found in the audio.")
                except ValueError as e:
                    st.error(e)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

# --- VIDEO STEGANOGRAPHY ---
elif tool == "Video Steganography":
    st.header("🎬 Video Steganography")
    st.write("Hides encrypted data in a single frame of a video file.")
    st.info("ℹ️ **How this works:** This tool uses a **lossless** codec (`FFV1`) to save the new video. This is required to prevent the hidden data from being destroyed, but the output file will be **very large**.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Encode a Message")
        uploaded_file = st.file_uploader("Choose a cover video file (.mp4, .avi)...", type=["mp4", "avi"], key="vid_enc_file")
        secret_message = st.text_area("Enter the secret message:", key="vid_enc_msg")
        frame_number = st.number_input("Enter Frame Number to hide data in:", min_value=0, step=1, key="vid_frame", help="The message will be hidden in this *single* frame. You must use the same number to decode.")
        encryption_key = st.text_input("Enter Encryption Key:", type="password", key="vid_enc_key", help="Your password. You *must* use the same key to decode.")

        if st.button("Encode Message", key="vid_enc_btn") and all([uploaded_file, secret_message, encryption_key]):
            with st.spinner('Encoding your message... This will take a long time.'):
                try:
                    video_bytes = uploaded_file.getvalue()
                    stego_video_bytes = video_steg.encode_message_in_video(video_bytes, secret_message, frame_number, encryption_key)
                    
                    with st.expander("✅ Success! Click to see results", expanded=True):
                        st.write("The new video file is ready for download:")
                        st.download_button(
                            label="Download Stego Video (.avi)",
                            data=stego_video_bytes,
                            file_name="stego_video.avi",
                            mime="video/x-msvideo"
                        )
                except ValueError as e:
                    st.error(e)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    with col2:
        st.subheader("Decode a Message")
        uploaded_file_dec = st.file_uploader("Choose a stego video file to decode...", type=["mp4", "avi"], key="vid_dec_file")
        frame_number_dec = st.number_input("Enter Frame Number to extract data from:", min_value=0, step=1, key="vid_dec_frame", help="The exact frame number where the data was hidden.")
        encryption_key_dec = st.text_input("Enter Encryption Key:", type="password", key="vid_dec_key", help="The password used during encoding.")

        if st.button("Decode Message", key="vid_dec_btn") and all([uploaded_file_dec, encryption_key_dec]):
            with st.spinner('Decoding your message...'):
                try:
                    video_bytes = uploaded_file_dec.getvalue()
                    decoded_message = video_steg.decode_message_from_video(video_bytes, frame_number_dec, encryption_key_dec)
                    
                    if decoded_message:
                        with st.expander("✅ Success! Click to see results", expanded=True):
                            st.text_area("Decoded Message", value=decoded_message, height=200, key="vid_dec_msg")
                    else:
                        st.warning("No hidden message was found in that frame. (Check your frame number and key).")
                except ValueError as e:
                    st.error(e)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")