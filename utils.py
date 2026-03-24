from PIL import Image
import json
from pydantic import ValidationError
from bot.models import MinecraftBuild

def resize_image(img):
    w, h = img.size
    longer_edge = w if w > h else h
    if longer_edge > 1568:
        max_size = (1568, 1568)
        img.thumbnail(max_size, Image.LANCZOS)

    return img



def complete_schematic(data):
    # in case data is a string
    if not isinstance(data, dict):
        # Find the last completed object
        last_brace = data.rfind("}")
        if last_brace == -1:
            return None

        trimmed = data[: last_brace + 1] # get all the completed blocks
        # Close blocks array and top-level object if missing
        trimmed = trimmed.rstrip()

        if not trimmed.endswith("]}"):
            trimmed += "]}"

        return json.loads(trimmed)

    return data  # complete data

import requests
import streamlit as st

def call_build(button=True): # This button parameter will come in handy during a later week
    url = "http://localhost:5000/build"

    data = st.session_state.get("build_data")
    try:
        response = requests.post(url, json=data)  # Make the POST request
        if response.status_code == 200:
            data = response.json()
            st.session_state["api_data"] = data  # Store the result in session state
            num_blocks = data.get("blocks")
            if button:
                st.success(f"Build call successful! Blocks placed: {num_blocks}")
        else:
            st.error(f"Build call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")