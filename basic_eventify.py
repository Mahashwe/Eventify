import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Check if API key is loaded
if not API_KEY:
    st.error("API Key is missing! Please check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ Updated model

# Streamlit UI
st.title("AI: Event Designer Assistant")

# Image Upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

# Process only when user clicks the button
if st.button("Analyze Image"):
    if uploaded_file:  
        # Open and display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Send image to Gemini API with prompt
        st.write("⏳ Analyzing image...")

        prompt = (
            "You are a professional event designer and strategist. Act as if you are pitching to a high-value client. "
            "Analyze the given image and provide a sharp, business-focused response:\n\n"
            "1. **Client’s Vision**: Summarize the event theme and style based on the image.\n"
            "2. **Expert Insights**: Provide a refined, strategic recommendation to elevate the design, ambiance, and experience.\n"
            "3. **Color & Aesthetic Strategy**: Identify the dominant color palette and suggest enhancements that align with branding, mood, and elegance.\n\n"
            "Your response should be direct, impactful, and persuasive, as if closing a deal with the client. "
            "Answer in points and simpler human style like a professional—don't overwhelm the client with large paragraphs."
        )

        # Generate response from AI
        response = model.generate_content([prompt, image])

        if response and hasattr(response, "text"):
            st.write(response.text)
        else:
            st.error("⚠️ Failed to generate a response. Please try again.")
    else:
        st.warning("⚠️ Please upload an image before analyzing.")  # Warning only appears when the button is clicked.
