import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Set up the Streamlit application
st.title('Image Captioning and Tagging')

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

# API Key input
API_KEY = st.text_input(
    "Enter your API Key: Get your Google Studio API key from [here](https://makersuite.google.com/app/apikey)",
    type="password",
)

if uploaded_file is not None:
    if st.button('Upload'):
        if API_KEY.strip() == '':
            st.error('Enter a valid API key')
        else:
            # Save the uploaded file to a temporary directory
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            img = Image.open(file_path)
            
            try:
                # Configure the Google Generative AI API
                genai.configure(api_key=API_KEY)
                
                # Use the updated model
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Generate caption
                caption_response = model.generate_content([
                    "Write a caption for the image in English", img
                ])
                
                # Generate tags
                tags_response = model.generate_content([
                    "Generate 5 hashtags for the image in English", img
                ])
                
                # Display the image and results
                st.image(img, caption=f"Caption: {caption_response.text}")
                st.write(f"Tags: {tags_response.text}")
            
            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg:
                    st.error("Invalid API Key. Please enter a valid API Key.")
                elif "404" in error_msg:
                    st.error("The specified model is not available. Ensure you are using the correct model identifier.")
                else:
                    st.error(f"An error occurred: {error_msg}")

# Footer styling
footer = """
<style>
    a:link, a:visited {
        color: blue;
        text-decoration: dotted;
    }

    a:hover, a:active {
        color: skyblue;
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 10%;
        font-size: 15px;
        color: white;
        text-align: center;
        padding: 10px 0;
        background-color: #333;
    }

    .footer p {
        font-size: 20px;
    }
</style>

<div class="footer">
    <p>Developed with ❤ by <a href="https://www.linkedin.com/in/sgvkamalakar" target="_blank">sgvkamalakar</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
