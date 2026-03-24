from utils import resize_image

from claude_client import call_analyzer

import streamlit as st

from PIL import Image

import requests

from utils import resize_image, complete_schematic, call_build

from io import BytesIO

def call_starter(username):
    """username can be your hard-coded Minecraft name, or you could add a text input to capture this"""
    url = "http://localhost:5000/spawn_bot"  # This will have to change once deployed

    params = {"username": username}
    try:
        response = requests.get(url, params=params)  # Make the GET request
        if response.status_code == 200:
            data = response.json()
            st.session_state["api_data"] = data  # Store the result in session state. This state will last while the tab is open
            st.success("API call successful!")
        else:
            st.error(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

def main():
    st.title("Minecraft Image Builder")

    # 1. INITIALIZE SESSION STATE
    if "build_data" not in st.session_state:
        st.session_state.build_data = None

    # 2. DEFINE INPUTS FIRST (So 'username' exists)
    username = st.text_input("Minecraft Username", value="Bot")
    uploaded_img = st.file_uploader("Choose an image")

    # 3. ACTIONS (Now 'username' is safe to use)
    if st.button("Start Bot & Analyze"):
        call_starter(username)

    # 4. PROCESSING LOGIC (Fixed Indentation)
    if uploaded_img is not None:
        img_bytes = BytesIO(uploaded_img.read())
        img = Image.open(img_bytes)
        img = resize_image(img)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        resized_bytes = BytesIO()
        img.save(resized_bytes, format="WEBP")
        resized_bytes.seek(0)

        # Get raw string from Claude
        json_str = call_analyzer(uploaded_img, resized_bytes)
        
        # REPAIR & SAVE TO SESSION STATE
        st.session_state.build_data = complete_schematic(json_str)

    # 5. THE BUILD BUTTON BLOCK
    if st.session_state.build_data is not None:
        st.divider() 
        st.subheader("Final Schematic")
        st.code(st.session_state.build_data, language="json")

        if st.button("BUILD IN MINECRAFT"):
            call_build()
    


if __name__  == "__main__":

    main()
