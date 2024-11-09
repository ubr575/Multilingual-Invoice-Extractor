from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini API
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to process the uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")

# Initialize Streamlit app with custom configuration
st.set_page_config(page_title="Multilingual Invoice Extractor", page_icon="💼")

# Title and header
st.title("💼 Multilingual Invoice Extractor")
st.subheader("Extract details from invoices in multiple languages")

# Custom CSS styling
st.markdown("""
    <style>
        .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px; font-size: 18px;}
        .stTextInput>div {font-size: 18px;}
        .stImage {border: 2px solid #ddd; border-radius: 10px;}
        .stFileUploader {font-size: 16px; color: #4CAF50;}
    </style>
""", unsafe_allow_html=True)

# Multi-column layout
col1, col2 = st.columns([2, 1])

with col1:
    # Input field for the user to provide a prompt
    input_prompt = st.text_input("Enter a specific question about the invoice:", key="input", placeholder="E.g., What is the total amount?")

with col2:
    # File uploader for the invoice image
    uploaded_file = st.file_uploader("Upload Invoice Image", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_column_width=True)

# Language selection dropdown (for multilingual support)
language = st.selectbox("Choose the response language:", ["English", "Spanish", "French", "German", "Chinese"])

# Button to trigger the extraction
submit = st.button("Extract Invoice Details")

# Default input prompt for Gemini API
base_prompt = """
You are an expert in understanding invoices. We will upload an image of an invoice, and you will answer any questions based on the uploaded image in the selected language.
"""

# Handle button click and generate response
if submit:
    if uploaded_file:
        try:
            image_data = input_image_setup(uploaded_file)
            # Combine base prompt with user input
            prompt = base_prompt + "\n" + f"Language: {language}\n" + input_prompt
            response = get_gemini_response(prompt, image_data, input_prompt)
            st.subheader("Invoice Extraction Results")
            st.write(response)
        except Exception as e:
            st.error(f"Error processing the invoice: {e}")
    else:
        st.warning("Please upload an invoice image to proceed.")
