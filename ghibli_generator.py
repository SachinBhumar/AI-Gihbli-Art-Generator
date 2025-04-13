import streamlit as st
import stability_sdk.client
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import requests
from PIL import Image
import io
import os

# ===== GHIBLI-STYLE GENERATOR =====
def generate_ghibli_image(prompt):
    """Generate Studio Ghibli-style art using Stability AI"""
    stability_api = client.StabilityInference(
        key=os.getenv('STABILITY_KEY'),  # Get your free API key at stability.ai
        engine="stable-diffusion-xl-1024-v1-0",
    )
    
    responses = stability_api.generate(
        prompt=f"Studio Ghibli art style, {prompt}, magical forest, vibrant colors, anime style",
        width=512,
        height=512,
        samples=1,
        style_preset="fantasy-art",
        cfg_scale=12,
    )
    
    for resp in responses:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                raise ValueError("Content violation")
            if artifact.type == generation.ARTIFACT_IMAGE:
                return Image.open(io.BytesIO(artifact.binary))

# ===== STREAMLIT APP =====
st.set_page_config(page_title="Ghibli Magic Generator", page_icon="🎨")
st.title("🌟 Studio Ghibli Style Image Generator")

# API Key Input
api_key = st.text_input("Enter your Stability API Key:", type="password")
os.environ['STABILITY_KEY'] = api_key

# Prompt Input
prompt = st.text_area("Describe your scene:", 
                     "A young girl flying with a dragon over misty mountains")

if st.button("Create Ghibli Art"):
    if not api_key:
        st.error("Please enter your Stability API key")
        st.markdown("[Get free API key](https://platform.stability.ai/)")
    else:
        with st.spinner("Painting your Ghibli masterpiece..."):
            try:
                image = generate_ghibli_image(prompt)
                st.image(image, caption="Your Ghibli-style Art", use_column_width=True)
                st.success("✨ Magic created! Right-click to save")
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
                st.markdown("""
                **Common fixes:**
                1. Check your API key
                2. Avoid violent/adult content
                3. Try a simpler prompt
                """)

st.markdown("---")
st.info("💡 Example prompts:\n- A cat bus riding through starry skies\n- A floating castle in sunset clouds\n- A spirit animal in a glowing forest")