import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import random
from modules.quiz import render_quiz_tab
from modules.personality import render_personality_tab
from modules.roleplay import render_roleplay_tab

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
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px !important;
        background-color: transparent !important;
        padding-bottom: 10px !important;
        border-bottom: 2px solid #3a2e24 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(20, 19, 17, 0.9) !important;
        border: 1px solid #3a2e24 !important;
        border-radius: 4px !important;
        padding: 10px 24px !important;
        color: #8b6f47 !important;
        font-family: 'Cinzel', serif !important;
        font-size: 1.1rem !important;
        white-space: nowrap !important; /* Prevents text overlapping edges */
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(40, 32, 26, 0.9) !important;
        color: #c9a063 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #050505 !important;
        background-image: url('https://github.com/TonyKat007/Project-Eldia-Archives/blob/main/image_f3b05e.png?raw=true') !important;
        /* Drastically increase scale so the blood covers the box */
        background-size: 350% !important; 
        background-position: center center !important;
        background-repeat: no-repeat !important;
        /* Remove the curved outline boundary completely */
        border: none !important; 
        border-radius: 4px 4px 0 0 !important;
        color: #ffffff !important;
        text-shadow: 2px 2px 5px #000000, 0px 0px 10px #ff0000 !important;
        box-shadow: none !important; 
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
    st.header("🗺️ Erwin's War Room: Expedition Simulator")
    st.markdown("Plan your Long-Distance Enemy Scouting Formation and test your survival odds.")
    
    w1, w2, w3 = st.columns(3)
    with w1:
        formation = st.selectbox("Formation Type:", ["Standard Semi-Circle Scouting", "Tight Spearhead Vanguard", "Decoy Split-Flank"])
    with w2:
        gas_reserve = st.slider("Wagon Supply Carts vs Speed Balance:", 10, 100, 50, help="Higher = More gas resupply, but slower convoy movement.")
    with w3:
        flare_policy = st.selectbox("Upon Sighting Abnormal Titans:", ["Fire Black Flare & Reroute", "Engage Immediately with Levi Squad", "Hold Formation & Push Through"])

    if st.button("⚔️ Launch Expedition Beyond Wall Rose"):
        survival_rate = random.randint(35, 88)
        st.subheader(f"📈 Estimated Vanguard Survival Rate: {survival_rate}%")
        prompt = f"Write a tense, 150-word tactical after-action report written by Commander Erwin Smith evaluating a scouting expedition that used a '{formation}' formation, '{flare_policy}' protocol, and achieved a {survival_rate}% survival rate."
        st.markdown(query_ai("You are Commander Erwin Smith writing an official military report.", prompt, api_key))

# ==========================================
# TAB 5: ODM GEAR PHYSICS LAB
# ==========================================
with tabs[4]:
    st.header("⚙️ ODM Gear Ballistics & Kinetic Physics Lab")
    st.markdown("Calculate whether your custom Iceburst gas pressure and cable geometry generate enough kinetic impact to sever a Titan's nape.")
    
    p1, p2 = st.columns([1, 2])
    with p1:
        mass = st.slider("Scout Mass + Gear (kg):", 50, 100, 68)
        pressure = st.slider("Iceburst Gas Ejection Thrust (N):", 500, 3000, 1600)
        angle = st.slider("Grapple Anchor Angle (Degrees):", 15, 75, 40)
        distance = st.slider("Cable Reel Distance (m):", 10, 80, 35)
        
        accel = (pressure * np.cos(np.radians(angle))) / mass
        final_velocity = np.sqrt(2 * accel * distance)
        kinetic_energy = 0.5 * mass * (final_velocity ** 2) / 1000 # in kJ

        st.metric("Terminal Reel Velocity", f"{final_velocity:.1f} m/s")
        st.metric("Impact Kinetic Energy", f"{kinetic_energy:.1f} kJ")
        
        if final_velocity > 42:
            st.error("⚠️ DANGER: G-Force exceeds human tolerance! Cable snap or internal injury likely (Unless you're an Ackerman).")
        elif kinetic_energy > 22:
            st.success("✅ LETHAL SLICE: Deep nape severing achieved!")
        else:
            st.warning("❌ SHALLOW CUT: Blade bounced off Titan skin. Need higher gas pressure!")

    with p2:
        t = np.linspace(0, np.sqrt(2*distance/accel), 50)
        x = 0.5 * accel * (t**2)
        y = x * np.tan(np.radians(angle)) - 0.5 * 9.81 * (t**2)
        
        fig_odm = go.Figure()
        fig_odm.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Scout Trajectory', line=dict(color='#c9a063', width=3)))
        fig_odm.update_layout(title="3D Maneuver Grapple Trajectory", xaxis_title="Horizontal Distance (m)", yaxis_title="Altitude (m)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#1b1e23', font=dict(color='white'))
        st.plotly_chart(fig_odm, use_container_width=True)

# ==========================================
# TAB 6: PUBLICLY AVAILABLE INFO GENERATOR
# ==========================================
with tabs[5]:
    st.header("📖 'Information Available for Public Disclosure'")
    st.markdown("Turn any modern object or inside joke into a canonical Paradis Island mid-episode eyecatch card.")
    
    topic = st.text_input("Enter any modern item or concept:", placeholder="e.g., Wireless Earbuds, Coffee, GitHub Merge Conflicts")
    if st.button("Generate Mid-Episode Lore Card") and topic:
        sys_lore = "You write the iconic mid-episode 'Currently Publicly Available Information' lore cards from Attack on Titan. Write in an overly formal, slightly archaic military historian tone, explaining a modern object as if it were an ancient artifact or ration discovered within the Walls."
        lore_text = query_ai(sys_lore, f"Write a 90-word lore card about: {topic}", api_key)
        
        st.markdown(f"""
        <div class="lore-card">
            <h3>📜 Information Available for Public Disclosure</h3>
            <hr style="border-color: #8b6f47;">
            <h4>【 {topic.upper()} 】</h4>
            <p style="font-size: 17px; line-height: 1.6;">{lore_text}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 7: TITAN SHIFTER FORGE
# ==========================================
with tabs[6]:
    st.header("⚡ The Subject of Ymir Registry: Titan Forge")
    st.markdown("Allocate **35 Total Skill Points** to engineer a custom Titan Shifter variant.")
    
    s1, s2 = st.columns(2)
    with s1:
        t_name = st.text_input("Titan Designation:", "The Obsidian Titan")
        height = st.select_slider("Class Height (Meters):", options=[4, 8, 15, 22, 60, 120], value=15)
        hardening = st.slider("Structural Hardening:", 1, 10, 7)
        speed = st.slider("Agility & Burst Speed:", 1, 10, 7)
        regen = st.slider("Steam & Regeneration Rate:", 1, 10, 7)
        stamina = st.slider("Consecutive Shift Endurance:", 1, 10, 7)
        special = st.text_input("Unique Manifestation:", "Can superheat hardened knuckles into molten slag.")
        
        total_pts = hardening + speed + regen + stamina
        if total_pts > 35:
            st.error(f"⚠️ Over Budget! You used {total_pts}/35 points. Lower your stats!")
        else:
            st.success(f"Points Allocated: {total_pts}/35")

    with s2:
        if st.button("Generate Marleyan Tactical Dossier") and total_pts <= 35:
            prompt = f"Write a brief, excited research observation by Hange Zoë and a cold Marleyan military threat assessment for a newly discovered {height}m Titan Shifter called '{t_name}'. Stats: Hardening {hardening}/10, Speed {speed}/10, Regen {regen}/10, Stamina {stamina}/10. Special ability: {special}."
            st.markdown(query_ai("You write Attack on Titan military intelligence dossiers.", prompt, api_key))
