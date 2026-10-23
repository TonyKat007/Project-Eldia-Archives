import streamlit as st
import google.generativeai as genai

def query_ai(system_prompt, chat_history, api_key):
    """Handles the API call to Gemini using the full conversation history."""
    if not api_key:
        return "⚠️ *[System Note: Please enter your Gemini API Key in the sidebar to awaken the Coordinate AI!]*"
    
    try:
        genai.configure(api_key=api_key)
        
        # Initialize the Pro model and attach the character persona via system_instruction
        model = genai.GenerativeModel(
            model_name='gemini-pro',
            system_instruction=system_prompt
        )
        
        # Convert the Streamlit chat history into Gemini's required format
        gemini_messages = []
        for msg in chat_history:
            if "System Note" not in msg["content"]:
                # Map standard roles to Gemini's expected roles
                role = "user" if msg["role"] == "user" else "model"
                gemini_messages.append({"role": role, "parts": [msg["content"]]})

        # Generate response passing the entire formatted history
        response = model.generate_content(
            gemini_messages,
            generation_config={"temperature": 0.75, "max_output_tokens": 600}
        )
        return response.text
        
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

def render_roleplay_tab(api_key):
    st.header("🎭 The Coordinate Roleplay Simulation")
    # --- TEMPORARY DEBUG CODE ---
    if api_key:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        st.warning("Available Gemini Models for this API Key:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name)
    # -----------------------------
    st.markdown("Engage in a canonical, timeline-accurate dialogue with the cast.")
    
    rp_col1, rp_col2 = st.columns([1, 2.5])
    
    with rp_col1:
        st.subheader("Simulation Parameters")
        rp_char = st.selectbox("Select Character:", [
            "Levi Ackerman",
            "Eren Yeager (Season 4 / Marley Arc)",
            "Erwin Smith",
            "Hange Zoë",
            "Zeke Yeager",
            "Armin Arlert",
            "Reiner Braun"
        ])
        
        rp_arc = st.selectbox("Select Timeline / Setting:", [
            "Year 850: Trost District Recovery",
            "Year 850: 57th Exterior Expedition (Forest of Giant Trees)",
            "Year 850: Return to Shiganshina",
            "Year 854: Raid on Liberio",
            "The Paths (Timeless Dimension)"
        ])
        
        st.divider()
        if st.button("Reset Conversation", use_container_width=True):
            st.session_state.rp_messages = []
            st.rerun()

    with rp_col2:
        # Initialize the chat history if it doesn't exist
        if "rp_messages" not in st.session_state or len(st.session_state.rp_messages) == 0:
            st.session_state.rp_messages = [
                {"role": "assistant", "content": f"*[Setting: {rp_arc}]*\n\n**{rp_char}** turns to look at you. What do you say?"}
            ]

        # Display all previous messages in the chat interface
        for msg in st.session_state.rp_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # The Chat Input widget (this pins to the bottom of the column)
        user_input = st.chat_input(f"Speak to {rp_char}...")
        
        if user_input:
            # 1. Display user message immediately
            st.session_state.rp_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # 2. Define the strict persona parameters
            sys_prompt = f"""You are roleplaying strictly as {rp_char} from Attack on Titan during the '{rp_arc}' timeline. 
            Rules:
            1. Stay 100% in character. Use their exact speech patterns, worldview, trauma, and specific knowledge limit for that exact timeline (NO SPOILERS for future events).
            2. Include brief atmospheric action descriptions in italics (e.g., *adjusts ODM gear*).
            3. Do not act like an AI assistant. You are the character.
            4. Keep responses conversational, engaging, and under 3 paragraphs."""
            
            # 3. Call the AI and display the response
            with st.chat_message("assistant"):
                with st.spinner(f"Waiting for {rp_char} to respond..."):
                    response = query_ai(sys_prompt, st.session_state.rp_messages, api_key)
                st.markdown(response)
                st.session_state.rp_messages.append({"role": "assistant", "content": response})
