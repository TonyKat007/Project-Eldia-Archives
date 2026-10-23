import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random

def generate_battlefield_map(formation, titan_density, spacing):
    """Calculates 2D coordinates for the tactical map overlay."""
    fig = go.Figure()
    
    # Generate Titan Coordinates (Randomly distributed outer ring/clusters)
    num_titans = int(titan_density * 1.5)
    tx = np.random.uniform(-100, 100, num_titans)
    ty = np.random.uniform(20, 100, num_titans)
    
    fig.add_trace(go.Scatter(
        x=tx, y=ty, mode='markers', name='Detected Titans',
        marker=dict(color='#ff4b4b', size=10, symbol='x')
    ))

    # Generate Scout Coordinates based on formation geometry
    sx, sy = [], []
    if formation == "Long-Distance Enemy Scouting":
        # Wide semi-circle
        angles = np.linspace(np.pi/4, 3*np.pi/4, 20)
        sx = np.cos(angles) * spacing
        sy = np.sin(angles) * spacing - 20
    elif formation == "Wedge Vanguard":
        # V-shape pushing forward
        sy = np.linspace(-20, 40, 10)
        sx_right = np.linspace(0, spacing/2, 10)
        sx_left = np.linspace(0, -spacing/2, 10)
        sx = np.concatenate([sx_left, sx_right])
        sy = np.concatenate([sy, sy])
    elif formation == "Defensive Box":
        # Grid array
        grid_x, grid_y = np.meshgrid(np.linspace(-spacing/3, spacing/3, 4), np.linspace(-20, 20, 4))
        sx, sy = grid_x.flatten(), grid_y.flatten()
    else:
        # Default clustered
        sx = np.random.uniform(-spacing/4, spacing/4, 15)
        sy = np.random.uniform(-10, 10, 15)

    fig.add_trace(go.Scatter(
        x=sx, y=sy, mode='markers', name='Scout Squads',
        marker=dict(color='#00ffcc', size=12, symbol='triangle-up', line=dict(color='#ffffff', width=1))
    ))

    # Map Styling
    fig.update_layout(
        plot_bgcolor='rgba(20, 19, 17, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(visible=False, range=[-100, 100]),
        yaxis=dict(visible=False, range=[-40, 120]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#d8c3a5')),
        height=400
    )
    return fig


def render_war_room_tab():
    st.header("🗺️ Erwin's War Room")
    st.markdown("Command the next exterior scouting mission. Allocate resources and analyze regiment viability before departing the walls.")
    
    # --- TOP METRICS ROW ---
    col1, col2 = st.columns([1.2, 1.5])
    
    with col1:
        st.subheader("Expedition Parameters")
        
        # Primary Parameters
        personnel = st.slider("Scout Vanguard Deployment", 10, 300, 100, 10)
        gas_reserves = st.slider("Average Gas Reserves (%)", 0, 100, 85, 5)
        blade_sets = st.slider("Ultra-Hard Steel Blades (Per Soldier)", 1, 8, 4)
        
        formation = st.selectbox(
            "Primary Tactical Formation",
            ["Long-Distance Enemy Scouting", "Wedge Vanguard", "Defensive Box", "Night Cover Operations", "Center Ambush", "Flank Guard", "Retreat Phalanx"]
        )
        
        # Advanced Logistics (The 10 New Parameters)
        with st.expander("⚙️ Advanced Logistics & Environment"):
            terrain = st.selectbox("Terrain Type", ["Open Plains", "Giant Tree Forest", "Ruined City", "Mountain Pass"])
            weather = st.selectbox("Weather Conditions", ["Clear", "Heavy Rain", "Dense Fog", "Snowstorm"])
            time_of_day = st.selectbox("Time of Day", ["Dawn", "High Noon", "Dusk", "Midnight"])
            veteran_ratio = st.slider("Veteran Soldier Ratio (%)", 0, 100, 20)
            titan_density = st.slider("Expected Titan Density", 1, 100, 35)
            flare_supply = st.slider("Signal Flare Inventory", 10, 200, 50)
            horse_stamina = st.slider("Average Mount Stamina (%)", 10, 100, 90)
            supply_wagons = st.slider("Supply Wagon Count", 0, 20, 5)
            thunder_spears = st.slider("Thunder Spear Availability", 0, 100, 0)
            medical_kits = st.slider("Medical Supplies (%)", 0, 100, 75)
            scout_spacing = st.slider("Formation Spacing (Meters)", 10, 150, 80)
            
        # Calculation Engine
        viability_score = (personnel * 0.1) + (gas_reserves * 0.6) + ((blade_sets / 8) * 20) + (veteran_ratio * 0.2) + (medical_kits * 0.1)
        
        if formation == "Long-Distance Enemy Scouting" and terrain == "Open Plains":
            viability_score *= 1.2
        if weather in ["Heavy Rain", "Dense Fog"]:
            viability_score -= (titan_density * 0.4)
            
        final_rate = min(99.9, max(1.0, viability_score - (titan_density * 0.2)))
        
        st.divider()
        color = "#00ffcc" if final_rate > 75 else "#ffaa00" if final_rate > 40 else "#ff4b4b"
        st.markdown(f"### Projected Survival Rate: <span style='color:{color};'>{final_rate:.1f}%</span>", unsafe_allow_html=True)

    # --- RADAR CHART ---
    with col2:
        mobility = (gas_reserves + horse_stamina) / 2
        lethality = min(100, ((blade_sets / 8) * 60) + (thunder_spears * 0.4) + (veteran_ratio * 0.4))
        detection = min(100, (flare_supply * 0.5) + (80 if weather == "Clear" else 20))
        supplies = (supply_wagons * 5) + medical_kits
        morale = min(100, (personnel * 0.5) + (veteran_ratio * 0.5))

        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[mobility, lethality, detection, supplies, morale],
            theta=['Mobility', 'Lethality', 'Detection', 'Supply Chain', 'Regiment Morale'],
            fill='toself',
            fillcolor='rgba(139, 0, 0, 0.5)',
            line=dict(color='#ff4b4b', width=2),
            marker=dict(color='#c9a063', size=8)
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#3a2e24', tickfont=dict(color='#8b6f47')),
                angularaxis=dict(gridcolor='#3a2e24', tickfont=dict(color='#c9a063', family='Cinzel', size=14)),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- LIVE BATTLEFIELD MAP ---
    st.divider()
    st.subheader("Live Tactical Feeds")
    st.markdown(f"*Simulating spatial coordinates for {formation} across {terrain}...*")
    
    fig_map = generate_battlefield_map(formation, titan_density, scout_spacing)
    st.plotly_chart(fig_map, use_container_width=True)

def render_physics_lab_tab():
    st.header("⚙️ ODM Physics Lab")
    st.info("Awaiting structural integration...")


def render_public_info_tab():
    st.header("📖 Public Info Generator")
    st.info("Awaiting structural integration...")


def render_titan_forge_tab():
    st.header("⚡ Titan Shifter Forge")
    st.info("Awaiting structural integration...")
