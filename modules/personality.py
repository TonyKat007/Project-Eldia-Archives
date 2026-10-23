import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import json
import os

def load_character_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'character_stats.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Convert lists back to numpy arrays for calculation
    for char in data:
        data[char]["vec"] = np.array(data[char]["vec"])
    return data

def render_personality_tab():
    st.header("🧬 Paths Psychological & Tactical Evaluation")
    st.markdown("Answer the ideological prompts below to map your 6-axis combat & philosophy matrix against the characters.")
    
    c1, c2 = st.columns(2)
    with c1:
        q_freedom = st.slider("1. How much are you willing to sacrifice for absolute personal freedom?", 1, 10, 5)
        q_logic = st.slider("2. In a crisis, do you rely on cold statistical sacrifice (10) or saving the comrade in front of you (1)?", 1, 10, 5)
        q_loyalty = st.slider("3. How strictly do you follow the chain of command (10) vs acting as a lone wolf (1)?", 1, 10, 5)
    with c2:
        q_curiosity = st.slider("4. When facing an unknown threat, how strong is your urge to study it rather than destroy it?", 1, 10, 5)
        q_empathy = st.slider("5. Can you forgive an enemy if you learn they were brainwashed as a child?", 1, 10, 5)
        q_combat = st.slider("6. Do you prefer frontline aggressive assault (10) or long-range strategic orchestration (1)?", 1, 10, 5)

    user_vector = np.array([q_freedom, q_logic, q_loyalty, q_curiosity, q_empathy, q_combat])
    categories = ['Drive for Freedom', 'Cold Calculation', 'Order & Loyalty', 'Scientific Curiosity', 'Empathy/Guilt', 'Frontline Aggression']

    characters = load_character_data()

    # Calculate Compatibility using Euclidean Closeness
    matches = {}
    for name, data in characters.items():
        dist = np.linalg.norm(user_vector - data["vec"])
        # Scale to a 0-100% format for easier reading
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
        # Show top 5 matches in the dataframe
        df_matches = pd.DataFrame(sorted_matches[:8], columns=["Character", "Compatibility (%)"])
        st.dataframe(df_matches, use_container_width=True, hide_index=True)

    with res_col2:
        # Plotly Radar Chart
        fig = go.Figure()
        
        # User Trace
        fig.add_trace(go.Scatterpolar(
            r=np.append(user_vector, user_vector[0]),
            theta=categories + [categories[0]],
            fill='toself',
            name='Your Psyche',
            line_color='#00ffcc'
        ))
        
        # Top Match Trace
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
