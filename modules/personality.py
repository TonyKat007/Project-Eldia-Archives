import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import json
import os

def load_json(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', filename)
    with open(file_path, 'r') as f:
        return json.load(f)

def render_personality_tab():
    st.header("🧬 Paths Psychological & Tactical Evaluation")
    st.markdown("Complete this 40-question psychological profile. Your choices will mathematically map your ideology onto the 6-axis Eldian military matrix.")
    
    # Load data
    quiz_data = load_json('personality_quiz.json')
    characters = load_json('character_stats.json')
    
    # Convert character vectors to numpy arrays
    for char in characters:
        characters[char]["vec"] = np.array(characters[char]["vec"])

    # Axis mapping dictionary
    axis_map = {
        "F": 0, # Drive for Freedom
        "L": 1, # Cold Calculation
        "O": 2, # Order & Loyalty
        "C": 3, # Scientific Curiosity
        "E": 4, # Empathy/Guilt
        "A": 5  # Frontline Aggression
    }
    categories = ['Drive for Freedom', 'Cold Calculation', 'Order & Loyalty', 'Scientific Curiosity', 'Empathy/Guilt', 'Frontline Aggression']

    # Wrap the 40 questions in a form so it doesn't refresh on every click
    with st.form("personality_quiz_form"):
        st.subheader("Section 1: Tactical & Moral Scenarios")
        
        # Split into 2 columns to make 40 questions scrollable and clean
        col1, col2 = st.columns(2)
        
        user_selections = []
        for idx, item in enumerate(quiz_data):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                options = list(item["opts"].keys())
                choice = st.radio(f"**{idx+1}. {item['q']}**", options, index=None, key=f"psyche_q_{idx}")
                user_selections.append({"q_idx": idx, "choice": choice})
                st.write("") # spacing
                
        submitted = st.form_submit_button("Submit Evaluation to the Coordinate", use_container_width=True)

    if submitted:
        # Validate that all questions were answered
        if any(sel["choice"] is None for sel in user_selections):
            st.error("⚠️ Command requires you to answer all scenarios before processing your profile.")
            return

        # Base Vector: Everyone starts at neutral 5 for all axes
        user_vector = np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0])

        # Apply Modifiers based on answers
        for sel in user_selections:
            q_idx = sel["q_idx"]
            choice = sel["choice"]
            modifiers = quiz_data[q_idx]["opts"][choice]
            
            for axis_key, value in modifiers.items():
                if axis_key in axis_map:
                    vec_index = axis_map[axis_key]
                    user_vector[vec_index] += value

        # Clip values strictly between 1 and 10 to match the radar chart scale
        user_vector = np.clip(user_vector, 1.0, 10.0)

        # Calculate Compatibility using Euclidean Closeness
        matches = {}
        for name, data in characters.items():
            dist = np.linalg.norm(user_vector - data["vec"])
            # Scale to a 0-100% format
            similarity = max(0, 100 - (dist * 5.5))
            matches[name] = round(similarity, 1)

        sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
        top_char, top_score = sorted_matches[0]

        st.divider()
        st.success("✅ Paths Evaluation Complete. Generating Profile...")
        
        res_col1, res_col2 = st.columns([1.2, 1])

        with res_col1:
            st.subheader(f"🏆 Primary Match: {top_char} ({top_score}% Sync)")
            st.markdown(f"**Title:** *{characters[top_char]['role']}*")
            st.info(f"💬 \"{characters[top_char]['quote']}\"")
            
            st.markdown("#### 📊 Roster Compatibility Breakdown")
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
                name='Your Profile',
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
