import streamlit as st
import json
import os

def load_quiz_data():
    # Dynamically locate the data folder relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'quiz_bank.json')
    with open(file_path, 'r') as f:
        return json.load(f)

def render_quiz_tab():
    st.header("📜 The Cadet Corps Knowledge Assessment")
    col1, col2 = st.columns([1, 3])
    
    quiz_data = load_quiz_data()
    
    with col1:
        tier = st.radio("Select Difficulty Tier:", list(quiz_data.keys()))
    
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
