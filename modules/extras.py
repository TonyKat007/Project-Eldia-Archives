import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
import time

# --- UNPREDICTABLE EXPEDITION EVENTS (25 Scenarios) ---
EXPEDITION_EVENTS = [
    {"name": "The Female Titan Sighting", "desc": "A highly intelligent, athletic Titan has breached the right flank. It is ignoring standard combat doctrine.", "lethality": 25},
    {"name": "Sudden Torrential Rain", "desc": "Visibility drops to zero. Signal flares are rendered useless and ODM maneuverability is compromised. (No Regrets anomaly)", "lethality": 15},
    {"name": "Abnormal Ambush", "desc": "An Abnormal Titan completely ignored the vanguard and leaped directly into the supply wagons.", "lethality": 10},
    {"name": "Beast's Pitch", "desc": "Massive boulders are raining down from an unknown location beyond the tree line.", "lethality": 30},
    {"name": "Crawler Variant", "desc": "A quadrupedal Abnormal is rapidly closing in on the rearguard, outpacing the horses.", "lethality": 12},
    {"name": "Colossal Steam Eruption", "desc": "A sudden burst of localized extreme heat melts ODM wires in the center formation.", "lethality": 20},
    {"name": "Jaw Titan Hit-and-Run", "desc": "A small, incredibly fast Titan decimated a squad and vanished into the brush.", "lethality": 18},
    {"name": "Nightfall Awakening", "desc": "These Titans are ignoring the lack of sunlight. They are continuing their pursuit into the night.", "lethality": 22},
    {"name": "Giant Tree Forest Dead End", "desc": "The formation is funneled into a massive root system, restricting horse mobility.", "lethality": 8},
    {"name": "Defective ODM Gas", "desc": "A bad batch of gas from the Trost armory is causing mid-air pressure failures.", "lethality": 10},
    {"name": "Cart Titan Artillery", "desc": "The enemy is utilizing quadrupedal Titans mounted with heavy armaments.", "lethality": 25},
    {"name": "Buried Titans", "desc": "Titans covered in dirt are erupting from the ground directly beneath the center formation.", "lethality": 15},
    {"name": "Faulty Blade Steel", "desc": "Ultra-hard steel blades are snapping upon impact with Titan napes due to poor forging.", "lethality": 8},
    {"name": "Pure Titan Stampede", "desc": "A massive horde of mindless Titans is stampeding directly through the vanguard.", "lethality": 20},
    {"name": "Signal Flare Misfire", "desc": "A red flare was fired accidentally by a panicked recruit, drawing Titans to the command squad.", "lethality": 12},
    {"name": "Mutinous Panic", "desc": "A squad on the left flank broke formation and fled, opening a massive gap in our defenses.", "lethality": 14},
    {"name": "Talking Titan Encounter", "desc": "A deviant Titan is attempting to speak. The psychological shock has paralyzed a vanguard squad.", "lethality": 5},
    {"name": "Raining Titans", "desc": "Titans are falling from the sky. This defies all tactical logic.", "lethality": 28},
    {"name": "Thick Fog Bank", "desc": "Dense fog rolls in. Squads are navigating blindly using only acoustic signals.", "lethality": 10},
    {"name": "Supply Wagon Axle Break", "desc": "A critical supply wagon carrying backup gas has broken down in Titan territory.", "lethality": 12},
    {"name": "Deviant Jumper", "desc": "An Abnormal Titan just cleared a 30-meter tree in a single leap, taking out aerial scouts.", "lethality": 15},
    {"name": "Trapped in Ruins", "desc": "The regiment is bottlenecked in the ruins of an abandoned Eldian town.", "lethality": 10},
    {"name": "Titan Co-ordination", "desc": "The Titans are demonstrating pack-hunting behavior, cornering the left flank.", "lethality": 18},
    {"name": "Thunderstorm Lightning Strike", "desc": "Lightning struck a giant tree, causing it to collapse onto a squad.", "lethality": 8},
    {"name": "The Smiling Titan", "desc": "A particularly unsettling Titan is ignoring all diversions, walking straight toward the command center.", "lethality": 10}
]

def draw_tactical_map(sx, sy, tx, ty, formation):
    """Renders the current frame of the battlefield."""
    fig = go.Figure()
    
    # Active Titans
    if len(tx) > 0:
        fig.add_trace(go.Scatter(
            x=tx, y=ty, mode='markers', name='Detected Titans',
            marker=dict(color='#ff4b4b', size=12, symbol='x')
        ))

    # Surviving Scouts
    if len(sx) > 0:
        fig.add_trace(go.Scatter(
            x=sx, y=sy, mode='markers', name='Scout Squads',
            marker=dict(color='#00ffcc', size=10, symbol='triangle-up', line=dict(color='#ffffff', width=1))
        ))

    fig.update_layout(
        plot_bgcolor='rgba(20, 19, 17, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(visible=False, range=[-150, 150]),
        yaxis=dict(visible=False, range=[-50, 200]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#d8c3a5')),
        height=450
    )
    return fig

def render_war_room_tab():
    st.header("🗺️ Erwin's War Room")
    st.markdown("Command the next exterior scouting mission. Allocate resources and initiate the combat simulation.")
    
    col1, col2 = st.columns([1.2, 1.5])
    
    with col1:
        st.subheader("Expedition Parameters")
        
        personnel = st.slider("Scout Vanguard Deployment", 10, 300, 100, 10)
        gas_reserves = st.slider("Average Gas Reserves (%)", 0, 100, 85, 5)
        blade_sets = st.slider("Ultra-Hard Steel Blades (Per Soldier)", 1, 8, 4)
        
        # Expanded 16 Formations
        formation = st.selectbox(
            "Primary Tactical Formation",
            [
                "Long-Distance Enemy Scouting", "Wedge Vanguard", "Defensive Box", 
                "Center Ambush", "Flank Guard", "Retreat Phalanx", 
                "Pincer Maneuver", "Spearhead Assault", "Evasive Dispersal", 
                "Column March", "Rearguard Delay", "Staggered Line", 
                "Decoy Vanguard", "Encirclement Ring", "Chokepoint Funnel", 
                "Night Cover Operations"
            ]
        )
        
        with st.expander("⚙️ Advanced Logistics & Environment"):
            # Expanded 11 Terrains
            terrain = st.selectbox("Terrain Type", [
                "Open Plains", "Giant Tree Forest", "Ruined City", 
                "Mountain Pass", "Dense Woodland", "Shiganshina Outskirts", 
                "Barren Badlands", "Flooded Riverlands", "Utgard Castle Ruins", 
                "Snowy Tundra", "Coastal Shallows"
            ])
            veteran_ratio = st.slider("Veteran Soldier Ratio (%)", 0, 100, 20)
            titan_density = st.slider("Expected Titan Density", 1, 100, 35)
            flare_supply = st.slider("Signal Flare Inventory", 10, 200, 50)
            thunder_spears = st.slider("Thunder Spear Availability", 0, 100, 0)
            scout_spacing = st.slider("Formation Spacing (Meters)", 10, 150, 80)
            
        base_viability = (personnel * 0.1) + (gas_reserves * 0.6) + ((blade_sets / 8) * 20) + (veteran_ratio * 0.2)
        if formation in ["Long-Distance Enemy Scouting", "Evasive Dispersal"] and terrain in ["Open Plains", "Barren Badlands"]:
            base_viability *= 1.2
            
        st.divider()
        initiate_btn = st.button("⚔️ INITIATE EXPEDITION", use_container_width=True)

    
    with col2:
        mobility = gas_reserves
        lethality = min(100, ((blade_sets / 8) * 60) + (thunder_spears * 0.4) + (veteran_ratio * 0.4))
        detection = min(100, (flare_supply * 0.6))
        supplies = min(100, gas_reserves + (blade_sets * 5))
        morale = min(100, (personnel * 0.5) + (veteran_ratio * 0.5))

        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[mobility, lethality, detection, supplies, morale],
            theta=['Mobility', 'Lethality', 'Detection', 'Supply Chain', 'Regiment Morale'],
            fill='toself', fillcolor='rgba(139, 0, 0, 0.5)',
            line=dict(color='#ff4b4b', width=2), marker=dict(color='#c9a063', size=8)
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

    st.divider()
    st.subheader("Live Tactical Feeds")
    
    status_bar = st.empty()
    alert_box = st.empty()
    map_container = st.empty()
    report_container = st.empty()

    if initiate_btn:
        num_scouts = personnel
        num_titans = int(titan_density * 1.5)
        
        # Map visual geometries to the new formations
        if formation in ["Long-Distance Enemy Scouting", "Evasive Dispersal", "Staggered Line", "Decoy Vanguard"]:
            # Wide arc
            angles = np.linspace(np.pi/4, 3*np.pi/4, num_scouts)
            sx = np.cos(angles) * scout_spacing
            sy = np.sin(angles) * (scout_spacing / 2)
        elif formation in ["Wedge Vanguard", "Spearhead Assault", "Pincer Maneuver"]:
            # V-Shape
            sx = np.random.uniform(-scout_spacing/2, scout_spacing/2, num_scouts)
            sy = 40 - np.abs(sx) * 0.8
        elif formation in ["Column March", "Rearguard Delay", "Chokepoint Funnel"]:
            # Narrow vertical line
            sx = np.random.uniform(-15, 15, num_scouts)
            sy = np.random.uniform(-20, 60, num_scouts)
        elif formation in ["Center Ambush", "Encirclement Ring", "Flank Guard"]:
            # Circular perimeter
            angles = np.random.uniform(0, 2*np.pi, num_scouts)
            radii = np.random.uniform(scout_spacing/2, scout_spacing, num_scouts)
            sx = np.cos(angles) * radii
            sy = np.sin(angles) * radii + 20
        else:
            # Standard Box/Grid
            sx = np.random.uniform(-scout_spacing/2, scout_spacing/2, num_scouts)
            sy = np.random.uniform(0, 30, num_scouts)
        
        tx = np.random.uniform(-120, 120, num_titans)
        ty = np.random.uniform(80, 180, num_titans)
        
        current_viability = base_viability
        simulation_ticks = 15
        occurred_anomalies = []
        
        # Animation Loop
        for tick in range(simulation_ticks):
            # 1. Spatial Movement
            sy += np.random.uniform(2, 8, len(sy))
            
            if len(sx) > 0 and len(tx) > 0:
                mean_sx, mean_sy = np.mean(sx), np.mean(sy)
                tx += (mean_sx - tx) * np.random.uniform(0.05, 0.2, len(tx))
                ty -= np.random.uniform(2, 10, len(ty))
            
            # 2. Collision & Combat Resolution
            surviving_sx, surviving_sy = [], []
            surviving_tx, surviving_ty = [], []
            
            for i in range(len(sx)):
                distances = np.sqrt((tx - sx[i])**2 + (ty - sy[i])**2)
                if len(distances) > 0 and np.min(distances) < 15:
                    if random.randint(0, 100) > current_viability:
                        continue 
                surviving_sx.append(sx[i])
                surviving_sy.append(sy[i])
                
            for i in range(len(tx)):
                distances = np.sqrt((np.array(surviving_sx) - tx[i])**2 + (np.array(surviving_sy) - ty[i])**2)
                if len(distances) > 0 and np.min(distances) < 15:
                    if random.randint(0, 100) < (lethality * 0.8):
                        continue 
                surviving_tx.append(tx[i])
                surviving_ty.append(ty[i])
                
            sx, sy = np.array(surviving_sx), np.array(surviving_sy)
            tx, ty = np.array(surviving_tx), np.array(surviving_ty)
            
            # 3. Unpredictable Events (15% chance per tick)
            if random.random() < 0.15:
                event = random.choice(EXPEDITION_EVENTS)
                current_viability -= event["lethality"]
                alert_text = f"⚠️ **CRITICAL ANOMALY:** {event['name']} - {event['desc']} (Regiment Viability -{event['lethality']}%)"
                alert_box.error(alert_text)
                
                occurred_anomalies.append({"tick": tick + 1, "data": event})
                
                if event["lethality"] >= 20:
                    tx = np.append(tx, np.random.uniform(-50, 50, 5))
                    ty = np.append(ty, np.random.uniform(np.mean(sy), np.mean(sy)+20, 5))
            else:
                alert_box.empty()
                
            # 4. Render Updates
            survival_rate = (len(sx) / personnel) * 100 if personnel > 0 else 0
            status_bar.markdown(f"**Tick {tick+1}/{simulation_ticks}** | Active Scouts: {len(sx)} | Active Titans: {len(tx)} | Current Survival Rate: **{survival_rate:.1f}%**")
            
            fig_map = draw_tactical_map(sx, sy, tx, ty, formation)
            map_container.plotly_chart(fig_map, use_container_width=True)
            
            time.sleep(0.6)
            
        # End of Simulation Summary
        alert_box.success(f"⚔️ **EXPEDITION CONCLUDED.** {len(sx)} out of {personnel} scouts returned alive. Operation Survival Rate: {(len(sx) / personnel) * 100:.1f}%.")
        
        # Render the final anomaly report directly into the reserved container
        with report_container.container():
            st.divider()
            st.subheader("📜 Post-Expedition Anomaly Report")
            if occurred_anomalies:
                for anomaly in occurred_anomalies:
                    event = anomaly["data"]
                    st.warning(f"**[Anomaly Code {anomaly['tick']}] {event['name']}**: {event['desc']} *(Impact: -{event['lethality']}% Viability)*")
            else:
                st.info("No critical anomalies were encountered during this expedition.")
            
    else:
        status_bar.info("Awaiting Commander's orders. Set parameters and initiate the expedition to begin live tracking.")
        fig_map = draw_tactical_map([], [], [], [], formation)
        map_container.plotly_chart(fig_map, use_container_width=True)
        



def render_physics_lab_tab():
    st.header("⚙️ ODM Physics & Aerodynamics Lab")
    st.markdown("Simulate 3D spatial maneuvers. Calculate kinetic forces, dual-anchor structural tension, aerodynamic drag, and human physiological limits during a Titan nape-strike slingshot.")
    
    # --- UI LAYOUT ---
    col1, col2 = st.columns([1.2, 2])
    
    with col1:
        st.subheader("Maneuver Telemetry")
        
        scout_mass = st.slider("Operator + Gear Mass (kg)", 50.0, 120.0, 75.0, 1.0)
        gas_thrust = st.slider("Continuous Propellant Thrust (N)", 0.0, 5000.0, 2500.0, 100.0)
        cable_length = st.slider("Primary Anchor Cable Length (m)", 10.0, 100.0, 50.0, 1.0)
        
        with st.expander("🌪️ Aerodynamics & Environment"):
            cd_area = st.slider("Drag Area (Cd * A)", 0.1, 1.5, 0.6, 0.1, help="Accounts for cape flutter and body posture.")
            air_density = st.number_input("Air Density (kg/m³)", value=1.225)
            entry_velocity = st.slider("Initial Velocity (m/s)", 0.0, 50.0, 15.0, 1.0)

        # --- PHYSICS ENGINE ---
        g = 9.81
        time_steps = np.linspace(0, 3, 100) # 3-second maneuver
        
        # 3D Parametric Trajectory (Slingshot around a target)
        x = cable_length * np.sin(time_steps * 1.5)
        y = cable_length * np.cos(time_steps * 1.5) - cable_length
        z = 15 * np.sin(time_steps * np.pi) # Vertical evasion curve
        
        # Velocity Profile (Simplified Integration of Thrust vs Drag)
        velocities = []
        v_current = entry_velocity
        for _ in time_steps:
            drag = 0.5 * air_density * (v_current**2) * cd_area
            net_force = gas_thrust - drag + (scout_mass * g * 0.5) # Assisted by gravity
            accel = net_force / scout_mass
            v_current += accel * (3.0 / 100)
            velocities.append(v_current)
            
        velocities = np.array(velocities)
        max_v = np.max(velocities)
        
        # Centripetal Tension & G-Force
        radius_of_curvature = cable_length * 0.8
        centripetal_forces = (scout_mass * (velocities**2)) / radius_of_curvature
        tensions = centripetal_forces + (scout_mass * g)
        g_forces = tensions / (scout_mass * g)
        max_g = np.max(g_forces)
        max_t = np.max(tensions)
        
        st.divider()
        st.markdown("### Peak Forces Readout")
        
        m1, m2 = st.columns(2)
        m1.metric("Max Velocity", f"{max_v:.1f} m/s", f"{max_v * 3.6:.0f} km/h")
        
        g_color = "normal" if max_g <= 9 else "inverse"
        m2.metric("Peak G-Load", f"{max_g:.1f} G", delta="FATAL RISK" if max_g > 10 else "NOMINAL", delta_color=g_color)
        
        st.metric("Max Cable Tension", f"{max_t:.0f} N", "Wire Snap Threshold: 15000 N" if max_t > 15000 else "Structural Integrity Holding", delta_color="inverse" if max_t > 15000 else "normal")

    with col2:
        # --- 3D SPATIAL VISUALIZATION ---
        st.subheader("Spatial Trajectory Map")
        fig3d = go.Figure()
        
        # Flight Path
        fig3d.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color=velocities, colorscale='Reds', width=6, colorbar=dict(title="Velocity (m/s)", x=-0.1)),
            name='Scout Trajectory'
        ))
        
        # Target Titan Nape
        fig3d.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[10],
            mode='markers',
            marker=dict(size=10, color='#00ffcc', symbol='cross'),
            name='Titan Nape Target'
        ))
        
        # Anchor Points
        fig3d.add_trace(go.Scatter3d(
            x=[-cable_length*0.5, cable_length*0.5], y=[-cable_length*0.8, -cable_length*0.8], z=[15, 15],
            mode='markers',
            marker=dict(size=6, color='#c9a063'),
            name='Grapple Anchors'
        ))

        fig3d.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            scene=dict(
                xaxis=dict(showbackground=False, gridcolor='#3a2e24', title='X (m)', tickfont=dict(color='#8b6f47')),
                yaxis=dict(showbackground=False, gridcolor='#3a2e24', title='Y (m)', tickfont=dict(color='#8b6f47')),
                zaxis=dict(showbackground=False, gridcolor='#3a2e24', title='Altitude (m)', tickfont=dict(color='#8b6f47')),
                bgcolor='rgba(20, 19, 17, 0.8)'
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=450,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#d8c3a5'))
        )
        st.plotly_chart(fig3d, use_container_width=True)
        
        # --- TIME SERIES TELEMETRY ---
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=time_steps, y=g_forces, mode='lines', line=dict(color='#ffaa00', width=2), name='G-Force'))
        fig_line.add_trace(go.Scatter(x=time_steps, y=velocities/10, mode='lines', line=dict(color='#00ffcc', width=2), name='Velocity (scaled)'))
        
        # Lethal G-Limit Line
        fig_line.add_hline(y=10, line_dash="dash", line_color="#ff4b4b", annotation_text="Lethal G-Limit (10G)", annotation_font_color="#ff4b4b")
        
        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(20, 19, 17, 0.8)',
            xaxis=dict(title='Time (s)', gridcolor='#3a2e24', tickfont=dict(color='#8b6f47')),
            yaxis=dict(title='Magnitude', gridcolor='#3a2e24', tickfont=dict(color='#8b6f47')),
            margin=dict(l=0, r=0, t=10, b=0), height=200,
            legend=dict(font=dict(color='#d8c3a5'))
        )
        st.plotly_chart(fig_line, use_container_width=True)
def render_titan_forge_tab():
    st.header("⚡ Titan Shifter Forge")
    st.info("Awaiting structural integration...")
