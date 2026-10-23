import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import random
from modules.quiz import render_quiz_tab
from modules.personality import render_personality_tab
from modules.roleplay import render_roleplay_tab
from modules.extras import render_war_room_tab, render_physics_lab_tab, render_public_info_tab, render_titan_forge_tab


# --- PAGE CONFIG ---
st.set_page_config(
    page_title="The Coordinate | AoT Hub",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM AOT MILITARY THEME CSS ---
st.markdown("""
<style>
    /* Import Cinematic Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Lora:ital,wght@0,400;0,700;1,400&display=swap');

    /* Global Gritty Background */
    .stApp {
        background-color: #0a0a0a;
        background-image: linear-gradient(rgba(10, 10, 10, 0.85), rgba(10, 10, 10, 0.95)), 
                          url('https://www.transparenttextures.com/patterns/cracked-earth.png');
        color: #d8c3a5;
        font-family: 'Lora', serif;
    }

    /* Broken Stone Title Effect */
    /* Metallic Stone Title Effect */
    .stone-title {
        font-family: 'Cinzel', serif;
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        letter-spacing: 4px;
        line-height: 1.1;
        margin-bottom: 0px;
        padding-bottom: 10px;
        /* Replaced external image with a reliable linear gradient */
        background: linear-gradient(to bottom, #f0e6d2, #8b6f47, #3a2e24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(3px 5px 5px rgba(0,0,0,0.9));
    }    
    .subtitle {
        text-align: center;
        color: #8b6f47;
        font-size: 1.2rem;
        font-style: italic;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }

    /* Military Brass Headers */
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: #c9a063 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
    }

    /* Lore Cards & Containers */
    .lore-card {
        background: linear-gradient(135deg, #1c1a17, #11100e);
        border: 2px solid #5c4033;
        border-radius: 2px;
        padding: 30px;
        text-align: center;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.8), 0 5px 15px rgba(0,0,0,0.6);
        position: relative;
    }
    .lore-card::before {
        content: '';
        position: absolute;
        top: 2px; left: 2px; right: 2px; bottom: 2px;
        border: 1px solid rgba(201, 160, 99, 0.2);
        pointer-events: none;
    }

    /* Heavy Duty Tabs */
    /* Grand Military Tabs - Blood Splatter Edition */
    /* Force Streamlit containers to allow overflowing elements */
    .stTabs [data-baseweb="tab-list"],
    .stTabs [data-baseweb="tab-list"] > div {
        overflow: visible !important;
    }

    /* Style the active tab text and remove its physical box */
    .stTabs [aria-selected="true"] {
        position: relative !important;
        background-color: transparent !important;
        border: none !important;
        color: #ffffff !important;
        text-shadow: 2px 2px 5px #000000, 0px 0px 10px #ff0000 !important;
        box-shadow: none !important;
    }

    /* Create the unbound bleeding splatter */
    .stTabs [aria-selected="true"]::before {
        content: '';
        position: absolute;
        /* Pull the image boundaries far outside the tab */
        top: -40px;    
        left: -40px;   
        right: -40px;  
        bottom: -20px; 
        background-image: url('https://github.com/TonyKat007/Project-Eldia-Archives/blob/main/image_f3b05e.png?raw=true');
        background-size: 350% !important; 
        background-position: center center !important;
        background-repeat: no-repeat !important;
        /* Drops the black background of your image, keeping only the red */
        mix-blend-mode: screen; 
        z-index: -1;
        /* Prevents the invisible expanded box from blocking clicks on other tabs */
        pointer-events: none; 
    }

    /* Aggressively hide the default red bottom highlight */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
        background-color: transparent !important;
    }
    
    
    /* Scout Regiment Buttons */
    .stButton > button {
        background: linear-gradient(to right, #4a1515, #7a2222);
        color: #e2dcd5;
        border: 1px solid #8b6f47;
        border-radius: 2px;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        letter-spacing: 1px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background: linear-gradient(to right, #7a2222, #9a2b2b);
        border-color: #c9a063;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(92, 24, 24, 0.5);
        color: white;
    }

    /* Chat Messages Restyling */
    .stChatMessage {
        background-color: rgba(20, 19, 17, 0.8) !important;
        border-left: 3px solid #5c1818;
        border-radius: 2px;
        padding: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Scout Regiment</h2>", unsafe_allow_html=True)
    st.caption("Dedicated to those who gave their hearts.")
    st.divider()
    
    st.markdown("### 🔑 Command Override")
    default_key = st.secrets.get("GROQ_API_KEY", "")
    api_key = st.text_input("Groq Clearance Code:", value=default_key, type="password")
    
    st.divider()
    st.markdown("**Regiment Status:** `<span style='color:#00ffcc;'>ACTIVE</span>`", unsafe_allow_html=True)
    st.markdown("**Wall Integrity:** `<span style='color:#ff4b4b;'>WALL MARIA BREACHED</span>`", unsafe_allow_html=True)

# --- MAIN HEADER ---
st.markdown("<div class='stone-title'>THE COORDINATE</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Archives of Eldia • Restricted Access Server</div>", unsafe_allow_html=True)
st.write("")
st.write("")

# --- 7 TABS ---
tabs = st.tabs([
    "Lore Quiz",
    "Psyche Matrix",
    "Roleplay Arena",
    "Erwin's War Room",
    "Physics Lab",
    "Public Info",
    "Titan Forge"
])
# ==========================================
# TAB 1: MULTI-TIER POP QUIZ
# ==========================================
with tabs[0]:
    render_quiz_tab()
# ==========================================
# TAB 2: PERSONALITY & RADAR MATRIX
# ==========================================
with tabs[1]:
    render_personality_tab()
# ==========================================
# TAB 3: IMMERSIVE AI ROLEPLAY ARENA
# ==========================================
with tabs[2]:
    # 2. Call the function and pass the API key from the sidebar
    render_roleplay_tab(api_key)
# ==========================================
# TAB 4: ERWIN'S WAR ROOM (TACTICAL SIM)
# ==========================================
with tabs[3]:
    render_war_room_tab()
with tabs[4]:
    render_physics_lab_tab()
with tabs[5]:
    render_public_info_tab()
with tabs[6]:
    render_titan_forge_tab()
