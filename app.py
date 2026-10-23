import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import random

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="The Coordinate | AoT Interactive Hub",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM AOT MILITARY THEME CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1012;
        color: #e2dcd5;
    }
    h1, h2, h3 {
        color: #c9a063 !important;
        font-family: 'Georgia', serif;
        letter-spacing: 1px;
    }
    .lore-card {
        background-color: #1c1a17;
        border: 2px solid #8b6f47;
        padding: 25px;
        border-radius: 4px;
        text-align: center;
        font-family: 'Georgia', serif;
        box-shadow: 0 0 15px rgba(0,0,0,0.8);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1b1e23;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        color: #c9a063;
    }
    .stTabs [aria-selected="true"] {
        background-color: #5c1818 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: FREE LLM SETUP ---
with st.sidebar:
    st.title("⚔️ Scout Regiment")
    st.caption("Dedicated to those who gave their hearts.")
    st.divider()
    st.subheader("🔑 Free AI Engine Setup")
    st.markdown("To use Roleplay & Lore Generation for **$0**, grab a free API key from [Groq Console](https://console.groq.com) or [Google AI Studio](https://aistudio.google.com).")
    api_key = st.text_input("Enter Free Groq / Gemini API Key:", type="password")
    
    st.divider()
    st.markdown("**Regiment Status:** `ACTIVE`")
    st.markdown("**Wall Integrity:** `WALL MARIA BREACHED`")

# --- HELPER FOR FREE AI CALLS ---
def query_ai(system_prompt, user_prompt, api_key):
    if not api_key:
        return "⚠️ *[System Note: Please enter a free Groq API Key in the sidebar to awaken the Coordinate AI! Showing simulated offline response below...]*\n\n**Simulated Response:** 'Tch. You want answers without putting in the credentials? Dedicate your heart first, brat.'"
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.75,
            max_tokens=600
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# --- MAIN HEADER ---
st.title("⚔️ THE COORDINATE: ARCHIVES OF ELDIA")
st.markdown("*An interactive multi-module simulation hub for Attack on Titan.*")

# --- 7 TABS ---
tabs = st.tabs([
    "📜 1. Lore Quiz",
    "🧬 2. Psyche Matrix",
    "🎭 3. Roleplay Arena",
    "🗺️ 4. Erwin's War Room",
    "⚙️ 5. ODM Physics Lab",
    "📖 6. Public Info Card",
    "⚡ 7. Shifter Forge"
])

# ==========================================
# TAB 1: MULTI-TIER POP QUIZ
# ==========================================
with tabs[0]:
    st.header("📜 The Cadet Corps Knowledge Assessment")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        tier = st.radio("Select Difficulty Tier:", [
            "Tier 1: Garrison (Easy)",
            "Tier 2: Survey Corps (Medium)",
            "Tier 3: Special Ops Squad (Hard)",
            "Tier 4: Founder's Memory (Extreme)"
        ])
    
    quiz_data = {
        "Tier 1: Garrison (Easy)": [
            {"q": "What are the names of the three walls from outermost to innermost?", "options": ["Maria, Rose, Sina", "Rose, Maria, Sina", "Sina, Rose, Maria", "Maria, Sina, Rose"], "ans": "Maria, Rose, Sina"},
            {"q": "Which district is at the southern edge of Wall Maria where Eren grew up?", "options": ["Trost", "Shiganshina", "Stohess", "Karanes"], "ans": "Shiganshina"}
        ],
        "Tier 2: Survey Corps (Medium)": [
            {"q": "What was the exact rank of Eren's father, Grisha Yeager, within the Eldian Restorationists?", "options": ["The Owl", "Leader of the Mosley Faction", "Key ideological figure recruited by the Owl", "Marleyan Honorary Captain"], "ans": "Key ideological figure recruited by the Owl"},
            {"q": "In the long-distance scouting formation, what does a BLACK smoke signal indicate?", "options": ["Titan sighted", "Emergency / Retreat", "Abnormal Titan spotted", "Obstacle in terrain"], "ans": "Abnormal Titan spotted"}
        ],
        "Tier 3: Special Ops Squad (Hard)": [
            {"q": "Which member of the original Levi Squad bit their tongue while riding a horse?", "options": ["Oluo Bozad", "Eld Jinn", "Gunther Schultz", "Petra Rall"], "ans": "Oluo Bozad"},
            {"q": "What was the fake king's name who sat on the throne before Historia's coronation?", "options": ["Fritz", "Rod Reiss", "Darius Zackly", "Uri Reiss"], "ans": "Fritz"}
        ],
        "Tier 4: Founder's Memory (Extreme)": [
            {"q": "What exact year did Ymir Fritz gain the power of the Titans according to Marleyan historical records (roughly how many years before the Fall of Shiganshina in 845)?", "options": ["1,820 years ago", "2,000 years ago", "1,745 years ago", "1,903 years ago"], "ans": "1,820 years ago"},
            {"q": "What is the name of the metal exclusively mined on Paradis Island used to forge ODM gear blades and canisters?", "options": ["Iceburst Stone & Ultra-Hard Steel", "Marleyan Titanium", "Glowing Basalt", "Crystallized Titan Marrow"], "ans": "Iceburst Stone & Ultra-Hard Steel"}
        ]
    }
    
    with col2:
        st.subheader(f"Active Assessment: {tier}")
        score = 0
        questions = quiz_data[tier]
        for idx, item in enumerate(questions):
            choice = st.radio(f"**Q{idx+1}: {item['q']}**", item['options'], key=f"{tier}_{idx}")
            if choice == item['ans']:
                score += 1
        
        if st.button("Submit Assessment"):
            st.success(f"Final Score: {score} / {len(questions)}")
            if score == len(questions):
                st.balloons()
                st.markdown("🎖️ **Verdict:** *You are ready to lead the vanguard beyond the walls!*")
            else:
                st.warning("⚔️ **Verdict:** *Back to the 104th Training Corps drills!*")

# ==========================================
# TAB 2: PERSONALITY & RADAR MATRIX
# ==========================================
with tabs[1]:
    st.header("🧬 Paths Psychological & Tactical Evaluation")
    st.markdown("Answer the ideological prompts below to map your 6-axis combat & philosophy matrix against Attack on Titan characters.")
    
    c1, c2 = st.columns(2)
    with c1:
        q_freedom = st.slider("1. How much are you willing to sacrifice for absolute personal freedom?", 1, 10, 5)
        q_logic = st.slider("2. In a crisis, do you rely on cold statistical sacrifice (10) or saving the comrade in front of you (1)?", 1, 10, 5)
        q_loyalty = st.slider("3. How strictly do you follow the chain of command vs acting as a lone wolf?", 1, 10, 5)
    with c2:
        q_curiosity = st.slider("4. When facing an unknown threat, how strong is your urge to study it rather than destroy it?", 1, 10, 5)
        q_empathy = st.slider("5. Can you forgive an enemy if you learn they were brainwashed as a child?", 1, 10, 5)
        q_combat = st.slider("6. Do you prefer frontline aggressive assault (10) or long-range strategic orchestration (1)?", 1, 10, 5)

    user_vector = np.array([q_freedom, q_logic, q_loyalty, q_curiosity, q_empathy, q_combat])
    categories = ['Drive for Freedom', 'Cold Calculation', 'Order & Loyalty', 'Scientific Curiosity', 'Empathy/Guilt', 'Frontline Aggression']

    # Character Reference Vectors
    characters = {
        "Eren Yeager":      {"vec": np.array([10, 8, 1, 3, 4, 10]), "quote": "If someone tries to take my freedom away... I won't hesitate to take theirs.", "role": "The Usurper / Attack Titan"},
        "Erwin Smith":      {"vec": np.array([8, 10, 8, 9, 5, 7]),  "quote": "My soldiers, rage! My soldiers, scream! My soldiers, fight!", "role": "13th Commander of the Survey Corps"},
        "Levi Ackerman":    {"vec": np.array([6, 8, 9, 4, 8, 10]),  "quote": "Make a choice you won't regret.", "role": "Humanity's Strongest Soldier"},
        "Armin Arlert":     {"vec": np.array([7, 8, 7, 9, 10, 3]),  "quote": "Someone who cannot abandon everything cannot achieve anything.", "role": "15th Commander / Strategist"},
        "Hange Zoë":        {"vec": np.array([7, 7, 7, 10, 9, 6]),  "quote": "Titans are truly marvelous, aren't they?!", "role": "14th Commander / Chief Researcher"},
        "Reiner Braun":     {"vec": np.array([3, 5, 9, 3, 9, 8]),   "quote": "We were just kids... we didn't know anything.", "role": "The Armored Titan"}
    }

    # Calculate Cosine Similarity / Euclidean Closeness
    matches = {}
    for name, data in characters.items():
        dist = np.linalg.norm(user_vector - data["vec"])
        similarity = max(0, 100 - (dist * 5.5))
        matches[name] = round(similarity, 1)

    sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    top_char, top_score = sorted_matches[0]

    st.divider()
    res_col1, res_col2 = st.columns([1.2, 1])

    with res_col1:
        st.subheader(f"🏆 Primary Match: {top_char} ({top_score}% Sync)")
        st.markdown(f"**Title:** *{characters[top_char]['role']}*")
        st.info(f"💬 \"{characters[top_char]['quote']}\"")
        
        st.markdown("#### 📊 Roster Compatibility Breakdown")
        df_matches = pd.DataFrame(sorted_matches, columns=["Character", "Compatibility (%)"])
        st.dataframe(df_matches, use_container_width=True, hide_index=True)

    with res_col2:
        # Plotly Radar Chart
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=np.append(user_vector, user_vector[0]),
            theta=categories + [categories[0]],
            fill='toself',
            name='Your Psyche',
            line_color='#00ffcc'
        ))
        top_vec = characters[top_char]["vec"]
        fig.add_trace(go.Scatterpolar(
            r=np.append(top_vec, top_vec[0]),
            theta=categories + [categories[0]],
            fill='toself',
            name=top_char,
            line_color='#ff4b4b'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 3: IMMERSIVE AI ROLEPLAY ARENA
# ==========================================
with tabs[2]:
    st.header("🎭 The Coordinate Roleplay Simulation")
    rp_col1, rp_col2 = st.columns([1, 2.5])
    
    with rp_col1:
        rp_char = st.selectbox("Select Character:", [
            "Levi Ackerman",
            "Eren Yeager (Season 4 / Marley Arc)",
            "Erwin Smith",
            "Hange Zoë",
            "Zeke Yeager"
        ])
        rp_arc = st.selectbox("Select Timeline / Setting:", [
            "Year 850: Trost District Recovery",
            "Year 850: 57th Exterior Expedition (Forest of Giant Trees)",
            "Year 850: Return to Shiganshina",
            "Year 854: Raid on Liberio",
            "The Paths (Timeless Dimension)"
        ])
        if st.button("Reset Conversation"):
            st.session_state.rp_messages = []

    with rp_col2:
        if "rp_messages" not in st.session_state:
            st.session_state.rp_messages = [
                {"role": "assistant", "content": f"*[Setting: {rp_arc}]*\n\n**{rp_char}** turns to look at you as the sound of ODM cables echoes in the distance. What do you say?"}
            ]

        for msg in st.session_state.rp_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input(f"Speak or perform an action with {rp_char}...")
        if user_input:
            st.session_state.rp_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            sys_prompt = f"""You are roleplaying strictly as {rp_char} from Attack on Titan during {rp_arc}. 
            Stay 100% in character. Use their exact speech patterns, worldview, trauma, and knowledge limit for that specific timeline. 
            Include brief atmospheric action descriptions in italics. Keep responses engaging and around 1-2 paragraphs."""
            
            with st.chat_message("assistant"):
                response = query_ai(sys_prompt, user_input, api_key)
                st.markdown(response)
                st.session_state.rp_messages.append({"role": "assistant", "content": response})

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
