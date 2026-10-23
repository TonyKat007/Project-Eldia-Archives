import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_war_room_tab():
    st.header("🗺️ Erwin's War Room")
    st.markdown("Command the next exterior scouting mission. Allocate resources and analyze regiment viability before departing the walls.")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("<div class='lore-card'>", unsafe_allow_html=True)
        st.subheader("Expedition Parameters")
        
        personnel = st.slider("Scout Vanguard Deployment", min_value=10, max_value=300, value=100, step=10)
        gas_reserves = st.slider("Average Gas Reserves (%)", min_value=0, max_value=100, value=85, step=5)
        blade_sets = st.slider("Ultra-Hard Steel Blades (Per Soldier)", min_value=1, max_value=8, value=4)
        
        formation = st.selectbox(
            "Primary Tactical Formation",
            ["Long-Distance Enemy Scouting", "Wedge Vanguard", "Night Cover Operations"]
        )
        
        # Calculate dynamic survival rate based on inputs
        viability_score = (personnel * 0.1) + (gas_reserves * 0.6) + ((blade_sets / 8) * 30)
        if formation == "Long-Distance Enemy Scouting":
            viability_score *= 1.2
        elif formation == "Night Cover Operations":
            viability_score *= 0.8
            
        final_rate = min(99.9, max(5.0, viability_score))
        
        st.divider()
        if final_rate > 75:
            color = "#00ffcc"
        elif final_rate > 40:
            color = "#ffaa00"
        else:
            color = "#ff4b4b"
            
        st.markdown(f"### Projected Survival Rate: <span style='color:{color};'>{final_rate:.1f}%</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Calculate matrix attributes
        mobility = gas_reserves
        lethality = (blade_sets / 8) * 100
        detection = 95 if formation == "Long-Distance Enemy Scouting" else 40
        supplies = (gas_reserves + ((blade_sets/8)*100)) / 2
        morale = min(100, personnel * 0.8)

        categories = ['Mobility', 'Lethality', 'Detection', 'Supply Chain', 'Regiment Morale']
        
        fig = go.Figure(data=go.Scatterpolar(
            r=[mobility, lethality, detection, supplies, morale],
            theta=categories,
            fill='toself',
            fillcolor='rgba(139, 0, 0, 0.5)',
            line=dict(color='#ff4b4b', width=2),
            marker=dict(color='#c9a063', size=8)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 100],
                    gridcolor='#3a2e24',
                    tickfont=dict(color='#8b6f47')
                ),
                angularaxis=dict(
                    gridcolor='#3a2e24',
                    tickfont=dict(color='#c9a063', family='Cinzel', size=14)
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)


def render_physics_lab_tab():
    st.header("⚙️ ODM Physics Lab")
    st.info("Awaiting structural integration...")


def render_public_info_tab():
    st.header("📖 Public Info Generator")
    st.info("Awaiting structural integration...")


def render_titan_forge_tab():
    st.header("⚡ Titan Shifter Forge")
    st.info("Awaiting structural integration...")
