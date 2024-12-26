import os
import streamlit as st
from typing import Dict, Optional
from groq import Groq

# Streamlit page configuration
st.set_page_config(layout="wide", page_title="AI Storytime Creator", initial_sidebar_state="expanded")

# Supported models
SUPPORTED_MODELS: Dict[str, str] = {
    "Llama 3.2 1B (Preview)": "llama-3.2-1b-preview",
    "Llama 3 70B": "llama3-70b-8192",
    "Llama 3 8B": "llama3-8b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 2 9B": "gemma2-9b-it",
    "Llama 3.2 11B Vision (Preview)": "llama-3.2-11b-vision-preview",
    "Llama 3.2 11B Text (Preview)": "llama-3.2-11b-text-preview",
    "Llama 3.1 8B Instant (Text-Only Workloads)": "llama-3.1-8b-instant",
    "Llama 3.2 90B Vision (Preview)": "llama-3.2-90b-vision-preview",
}

MAX_TOKENS: int = 1500

# Initialize Groq client with API key
@st.cache_resource
def get_groq_client() -> Optional[Groq]:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("GROQ_API_KEY not found in environment variables. Please set it and restart the app.")
        return None
    return Groq(api_key=groq_api_key)

client = get_groq_client()

# Sidebar - Model Configuration
st.sidebar.image("icon.png", width=300)
st.sidebar.title("Model Configuration")
selected_model = st.sidebar.selectbox("Choose an AI Model", list(SUPPORTED_MODELS.keys()))

# Sidebar - Temperature Slider
st.sidebar.subheader("Temperature")
temperature = st.sidebar.slider("Set temperature for story variability:", min_value=0.0, max_value=1.0, value=0.7)

# Sidebar - Story Structure
st.sidebar.subheader("Story Structure")
story_structure = st.sidebar.radio(
    "Select the narrative structure:",
    ["Three-Act Structure", "Hero's Journey", "Five Key Phases", "Freytag's Pyramid"],
)

# Sidebar - Emotional Arc
st.sidebar.subheader("Emotional Arc")
emotional_arcs = st.sidebar.multiselect(
    "Choose emotional tones:", ["Mad", "Sad", "Glad", "Scared"], default=["Mad", "Glad"]
)

# Main Content
st.title("AI Storytime Creator")
st.markdown("Generate engaging narratives for games, stories, or educational content.")

# User Input - Episode Description
episode_description = st.text_area(
    "Describe the episode or theme:", placeholder="A team of heroes embarks on a dangerous quest to retrieve a magical artifact."
)

# Generate Story Button
if st.button("Generate Story"):
    if not episode_description:
        st.warning("Please provide a description for the episode.")
    elif client:
        st.spinner("Generating your story...")
        prompt = f"""
        Create a story using the {story_structure} structure. Integrate the following emotional arcs: {', '.join(emotional_arcs)}.
        Episode Theme: {episode_description}
        """
        try:
            response = client.chat.completions.create(
                model=SUPPORTED_MODELS[selected_model],
                messages=[
                    {"role": "system", "content": "You are an AI that generates engaging narratives."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=MAX_TOKENS,
            )
            story_output = response.choices[0].message.content.strip()
            st.subheader("Generated Story")
            st.text_area("Story Output:", story_output, height=400)
            st.download_button(
                label="Download Story",
                data=story_output,
                file_name="generated_story.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Error generating story: {e}")
    else:
        st.error("Groq client not initialized.")

st.info("build by dw - Designed for writers, game developers, and educators to craft compelling narratives.")