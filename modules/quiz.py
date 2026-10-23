import streamlit as st
import json
import os

def load_quiz_data():
    # Dynamically locate the data folder relative to this module
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'quiz_bank.json')
    with open(file_path, 'r') as f:
        return json.load(f)

def render_quiz_tab():
    st.header("📜 The Cadet Corps Knowledge Assessment")
    st.markdown("Test your knowledge of the Attack on Titan universe. Select your difficulty tier below.")
    
    col1, col2 = st.columns([1, 2.5])
    
    try:
        quiz_data = load_quiz_data()
    except FileNotFoundError:
        st.error("Error: Could not find `quiz_bank.json`. Make sure it exists in the `data/` folder.")
        return
    
    with col1:
        st.markdown("### Select Tier")
        tier = st.radio("Difficulty Levels:", list(quiz_data.keys()), label_visibility="collapsed")
    
    with col2:
        st.subheader(f"Active Assessment: {tier}")
        st.divider()
        
        # Initialize session state to track the quiz submission status
        state_key = f"quiz_submitted_{tier}"
        if state_key not in st.session_state:
            st.session_state[state_key] = False

        score = 0
        questions = quiz_data[tier]
        user_answers = {}
        
        # Form to handle submission cleanly
        with st.form(key=f"quiz_form_{tier}"):
            for idx, item in enumerate(questions):
                st.markdown(f"**Q{idx+1}: {item['q']}**")
                choice = st.radio(
                    "Select an answer:", 
                    item['options'], 
                    key=f"{tier}_q_{idx}", 
                    label_visibility="collapsed"
                )
                user_answers[idx] = choice
                st.write("") # Spacing
                
            submit_button = st.form_submit_button("Submit Assessment")
            
            if submit_button:
                st.session_state[state_key] = True

        # Display results if submitted
        if st.session_state.get(state_key, False):
            st.divider()
            st.subheader("📊 Assessment Results")
            for idx, item in enumerate(questions):
                if user_answers[idx] == item['ans']:
                    score += 1
                    
            st.success(f"**Final Score: {score} / {len(questions)}**")
            
            # Grade feedback
            percentage = (score / len(questions)) * 100
            if percentage == 100:
                st.balloons()
                st.markdown("🎖️ **Verdict:** *Perfect Score! You are ready to lead the vanguard beyond the walls!*")
            elif percentage >= 75:
                st.info("⚔️ **Verdict:** *Excellent work, soldier. The Survey Corps would be lucky to have you.*")
            elif percentage >= 50:
                st.warning("🛡️ **Verdict:** *Average performance. You belong in the Garrison.*")
            else:
                st.error("🥔 **Verdict:** *Back to the 104th Training Corps drills! Potato duty for a week!*")
