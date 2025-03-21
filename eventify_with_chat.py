import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ Updated model

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.title("🔍 Multimodal AI: Event Designer Assistant")
st.write("Upload an image for event analysis and engage in a continuous Q&A with the AI!")

# Image Upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display image
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
        "Your response should be direct, impactful, and persuasive, as if closing a deal with the client." \
        "Answer in points ans simpler human style like a professional- dont overwhelm the client with large paragraphs"
    )

    response = model.generate_content([prompt, image])
    
    # Display AI response
    st.subheader("📝 AI Event Insights:")
    st.write(response.text)

# Continuous Chat System
st.subheader("💬 Chat with the AI")
user_input = st.chat_input("Ask anything about your event...")

if user_input:
    # Append previous chat history
    chat_history = "\n".join(st.session_state.chat_history)
    
    chat_prompt = (
        f"You are an expert event consultant. Respond conversationally and contextually based on previous discussions.\n"
        f"Previous Conversations:\n{chat_history}\n\n"
        f"Client: {user_input}\n"
        f"AI:"
    )

    # Generate response
    chat_response = model.generate_content(chat_prompt)

    # Store history
    st.session_state.chat_history.append(f"Client: {user_input}")
    st.session_state.chat_history.append(f"AI: {chat_response.text}")

    # Display response
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(chat_response.text)
