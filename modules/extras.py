import json
import os
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




def render_public_info_tab():
    st.header("☢️ Colossal Detonation Simulator")
    st.markdown("Analyze the thermonuclear-equivalent yield, blast radius, and projected casualties of a God of Destruction transformation.")
    
    # --- CANONICAL SCENARIOS ---
    scenarios = {
        "Liberio Port (Armin Arlert, 854)": {
            "yield": 35.0, "alt": 0.0, "density": 18500, 
            "desc": "Ground-level harbor detonation. Maximum kinetic displacement and fleet vaporization."
        },
        "Shiganshina Retrieval (Bertholdt Hoover, 850)": {
            "yield": 20.0, "alt": 60.0, "density": 400, 
            "desc": "Mid-air airburst transformation over ruined Shiganshina. Focused thermal damage, maximized blast wave spread."
        },
        "Wall Maria Breach (Bertholdt Hoover, 845)": {
            "yield": 2.5, "alt": 0.0, "density": 6000, 
            "desc": "Suppressed transformation. Minimal explosive yield, energy directed into a focused kinetic kick."
        },
        "Custom Tactical Detonation": {
            "yield": 15.0, "alt": 20.0, "density": 5000, 
            "desc": "Manual parameter override authorized for theoretical combat modeling."
        }
    }

    col1, col2 = st.columns([1.2, 1.5])
    
    with col1:
        st.subheader("Detonation Parameters")
        
        selected_scenario = st.selectbox("Historical / Theoretical Scenario", list(scenarios.keys()))
        s_data = scenarios[selected_scenario]
        
        st.info(s_data["desc"])
        
        is_custom = selected_scenario == "Custom Tactical Detonation"
        
        energy_yield = st.slider("Explosive Yield (Kiloton Equivalent)", 1.0, 50.0, float(s_data["yield"]), 0.5, disabled=not is_custom)
        altitude = st.slider("Transformation Altitude (Meters)", 0.0, 100.0, float(s_data["alt"]), 5.0, disabled=not is_custom)
        pop_density = st.slider("Population Density (People per km²)", 0, 25000, int(s_data["density"]), 100, disabled=not is_custom)
        
        # --- DESTRUCTION CALCULATIONS ---
        # Radii in kilometers scaled to yield
        r_vaporization = 0.15 * (energy_yield ** 0.4)
        r_thermal = 0.6 * (energy_yield ** 0.38)
        r_blast = 1.1 * (energy_yield ** 0.33)
        
        # Altitude modifiers (Airbursts increase blast range but reduce point-blank vaporization)
        if altitude > 20:
            r_blast *= 1.2
            r_vaporization *= 0.7
            
        # Area calculations (km²)
        area_vaporized = np.pi * (r_vaporization ** 2)
        area_thermal = np.pi * (r_thermal ** 2) - area_vaporized
        area_blast = np.pi * (r_blast ** 2) - area_thermal - area_vaporized
        
        # Lethality Distribution
        fatality_vap = area_vaporized * pop_density * 1.0     # 100% lethality
        fatality_therm = area_thermal * pop_density * 0.85    # 85% lethality
        fatality_blast = area_blast * pop_density * 0.4       # 40% lethality
        
        total_casualties = int(fatality_vap + fatality_therm + fatality_blast)
        
        st.divider()
        st.markdown("### Casualty Assessment")
        st.metric("Estimated Immediate Fatalities", f"{total_casualties:,}", delta=f"{int(fatality_vap):,} instantly vaporized", delta_color="inverse")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Vaporization", f"{r_vaporization*1000:.0f} m")
        c2.metric("Thermal Range", f"{r_thermal*1000:.0f} m")
        c3.metric("Shockwave", f"{r_blast*1000:.0f} m")

    with col2:
        st.subheader("Blast Radius Topography")
        
        fig = go.Figure()
        
        # Base Grid / Debris Scatter (Simulating city structures)
        debris_x = np.random.uniform(-r_blast*1.2, r_blast*1.2, 300)
        debris_y = np.random.uniform(-r_blast*1.2, r_blast*1.2, 300)
        fig.add_trace(go.Scatter(
            x=debris_x, y=debris_y, mode='markers',
            marker=dict(size=2, color='rgba(216, 195, 165, 0.3)'),
            name="Urban Infrastructure", hoverinfo="skip"
        ))
        
        # Concentric Blast Zones
        # 3. Outer Blast Wave (Overpressure)
        fig.add_shape(type="circle", x0=-r_blast, y0=-r_blast, x1=r_blast, y1=r_blast,
                      fillcolor="rgba(139, 0, 0, 0.2)", line_color="#8b0000", line_width=2)
        fig.add_trace(go.Scatter(x=[0], y=[r_blast], mode="text", text=["20 PSI Overpressure"], textposition="top center", textfont=dict(color="#8b0000")))
        
        # 2. Thermal Radiation Zone
        fig.add_shape(type="circle", x0=-r_thermal, y0=-r_thermal, x1=r_thermal, y1=r_thermal,
                      fillcolor="rgba(255, 75, 75, 0.3)", line_color="#ff4b4b", line_width=2)
        fig.add_trace(go.Scatter(x=[0], y=[r_thermal], mode="text", text=["3rd Degree Burns"], textposition="top center", textfont=dict(color="#ff4b4b")))
        
        # 1. Vaporization Zone (Ground Zero)
        fig.add_shape(type="circle", x0=-r_vaporization, y0=-r_vaporization, x1=r_vaporization, y1=r_vaporization,
                      fillcolor="rgba(255, 255, 255, 0.6)", line_color="#ffffff", line_width=3)
        fig.add_trace(go.Scatter(x=[0], y=[r_vaporization], mode="text", text=["Absolute Vaporization"], textposition="top center", textfont=dict(color="#ffffff")))
        
        # Epicenter Marker
        fig.add_trace(go.Scatter(
            x=[0], y=[0], mode='markers',
            marker=dict(size=12, color='#ffffff', symbol='star'),
            name="Epicenter (Transformation)"
        ))

        max_range = r_blast * 1.3
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(10, 10, 10, 0.8)',
            xaxis=dict(range=[-max_range, max_range], showgrid=True, gridcolor='#3a2e24', zeroline=False, title="Distance (km)"),
            yaxis=dict(range=[-max_range, max_range], showgrid=True, gridcolor='#3a2e24', zeroline=False, title="Distance (km)"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)




import json
import os
import streamlit as st
import plotly.graph_objects as go

def render_titan_forge_tab():
    st.header("⚡ Titan Bio-Engineering Forge")
    st.markdown("Synthesize a custom Titan Shifter chassis. Select canonical bloodlines or engineer an anomalous progenitor using cross-dimensional conceptual powers.")
    
    # --- LOAD POWER DATABASE ---
    try:
        with open("titan_powers.json", "r") as f:
            powers_db = json.load(f)
    except Exception:
        powers_db = [{"name": "Data Corruption", "desc": "Database missing.", "genre": "Eldritch", "grade": "S"}]
        st.error("Missing titan_powers.json file. Generating fallback capabilities.")

    # Hidden Grade Multipliers for Threat Engine
    grade_scale = {
        "F": 10, "E": 20, "D": 30, "C": 40, "B": 50, "A": 65, 
        "S": 80, "R": 90, "SR": 100, "SS": 115, "SSR": 135, "SSRX": 160
    }

    col1, col2 = st.columns([1.2, 1.5])
    
    with col1:
        st.subheader("Genetic Architecture")
        
        origin = st.radio("Chassis Origin", ["The Nine Titans (Canon)", "Custom Progenitor (Anomalous)"], horizontal=True)
        
        st.divider()
        
        if origin == "The Nine Titans (Canon)":
            chassis = st.selectbox("Base Titan Chassis Template", [
                "Attack (Balanced/Offensive)", "Armored (Heavy Defense)", 
                "Colossal (Massive/Thermal)", "Female (Agile/Versatile)", 
                "Jaw (High Speed/Lethality)", "Beast (Variable/Projectile)", 
                "Cart (Endurance/Quadruped)", "War Hammer (Structural Synthesis)"
            ])
            
            with st.expander("🧬 Physiological Allocation", expanded=True):
                height = st.slider("Vertical Stature (Meters)", 4.0, 60.0, 15.0, 1.0)
                muscle = st.slider("Muscle Fiber Density (Kinetic Power)", 1, 100, 75)
                hardening = st.slider("Structural Hardening Capacity (%)", 0, 100, 50)
                mobility = st.slider("Agility & Neural Reflexes", 1, 100, 80)
                regen = st.slider("Cellular Regeneration Rate", 1, 100, 60)
                anomaly_output = st.slider("Thermal & Steam Output", 0, 100, 20)
                
            # Canon Threat Calculation
            base_threat = (muscle * 0.25) + (hardening * 0.2) + (mobility * 0.25) + (regen * 0.15) + (anomaly_output * 0.15)
            if height > 20 and "Colossal" not in chassis:
                base_threat *= 0.85 
            if "Colossal" in chassis:
                base_threat = max(base_threat, 85.0)
            threat_level = min(100.0, base_threat)
            power_desc = f"Standard Eldian physiology bound to the {chassis.split()[0]} Titan lineage."
            
        else:
            # Custom Progenitor Engine
            c1, c2 = st.columns(2)
            chassis_gender = c1.selectbox("Base Morphology", ["Androgynous", "Masculine", "Feminine", "Beast-like", "Skeletal"])
            chassis_trait = c2.selectbox("Cosmetic Anomaly", ["Eyeless", "Exposed Ribcage", "Elongated Limbs", "Bioluminescent", "Crown of Horns"])
            
            # Extract unique genres from JSON
            unique_genres = sorted(list(set([p.get("genre", "Unknown") for p in powers_db])))
            selected_genre = st.selectbox("Conceptual Domain (Genre)", unique_genres)
            
            # Filter powers by genre
            filtered_powers = [p for p in powers_db if p.get("genre") == selected_genre]
            power_names = [p["name"] for p in filtered_powers]
            selected_power_name = st.selectbox("Manifested Ability", power_names)
            
            # Retrieve active power data
            active_power = next((p for p in filtered_powers if p["name"] == selected_power_name), filtered_powers[0])
            hidden_grade = active_power.get("grade", "C")
            power_desc = active_power.get("desc", "Unknown capability.")
            
            st.info(f"**Ability Signature:** {power_desc}")
            
            with st.expander("🧬 Physiological Allocation", expanded=False):
                height = st.slider("Vertical Stature (Meters)", 3.0, 120.0, 15.0, 1.0)
                muscle = st.slider("Muscle Fiber Density (Kinetic Power)", 1, 100, 60)
                hardening = st.slider("Structural Hardening Capacity (%)", 0, 100, 40)
                mobility = st.slider("Agility & Neural Reflexes", 1, 100, 70)
                regen = st.slider("Cellular Regeneration Rate", 1, 100, 80)
            
            # Anomalous Threat Calculation
            anomaly_output = grade_scale.get(hidden_grade, 40)
            base_threat = (muscle * 0.15) + (hardening * 0.15) + (mobility * 0.15) + (regen * 0.15) + (anomaly_output * 0.5)
            # Penalize absurd heights lacking anomalous structural support unless they have high-tier powers
            if height > 30 and anomaly_output < 80:
                base_threat *= 0.7 
            
            threat_level = base_threat # Can exceed 100 for god-tier
            
        st.divider()
        
        # --- BIOMECHANICAL PHYSICS ---
        estimated_mass = (height ** 3) * (muscle * 0.1)
        footprint_area = (height * 0.15) ** 2
        ground_pressure = (estimated_mass * 9.81) / (footprint_area * 1000) if footprint_area > 0 else 0
        
        if threat_level > 140:
            classification, color = "EX-CLASS (GOD THREAT)", "#9400D3" # Deep Purple
        elif threat_level > 110:
            classification, color = "SS-CLASS (WORLD ENDER)", "#ff00ff" # Neon Magenta
        elif threat_level > 90:
            classification, color = "S-CLASS (APOCALYPTIC)", "#ff4b4b" # Crimson
        elif threat_level > 70:
            classification, color = "A-CLASS (EXTREME THREAT)", "#ffaa00" # Orange
        elif threat_level > 40:
            classification, color = "B-CLASS (HIGH THREAT)", "#00ffcc" # Cyan
        else:
            classification, color = "C-CLASS (MANAGEABLE)", "#d8c3a5" # Bone
            
        st.markdown("### Tactical Assessment")
        st.markdown(f"**Designation:** <span style='color:{color}; font-weight:900; font-size: 1.2rem; letter-spacing: 1px;'>{classification}</span>", unsafe_allow_html=True)
        
        m1, m2 = st.columns(2)
        m1.metric("Est. Mass", f"{estimated_mass/1000:.1f} Tons")
        m2.metric("Ground Pressure", f"{ground_pressure:.0f} kPa")

    with col2:
        st.subheader("Bio-Signature Analysis")
        
        # Max out radar chart values at 100 for clean visualization, even if anomalous output is 160
        r_kinetic = min(100, muscle)
        r_armor = min(100, hardening)
        r_mobility = min(100, mobility)
        r_regen = min(100, regen)
        r_anomaly = min(100, anomaly_output)
        
        fig = go.Figure()
        categories = ['Kinetic Power', 'Structural Armor', 'Mobility', 'Regeneration', 'Anomalous Output']
        fig.add_trace(go.Scatterpolar(
            r=[r_kinetic, r_armor, r_mobility, r_regen, r_anomaly],
            theta=categories,
            fill='toself',
            fillcolor='rgba(201, 160, 99, 0.3)',
            line=dict(color=color, width=2),
            marker=dict(color='#ffffff', size=6),
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#3a2e24', tickfont=dict(color='#8b6f47')),
                angularaxis=dict(gridcolor='#3a2e24', tickfont=dict(color='#c9a063', family='Cinzel', size=13)),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=40, b=40),
            height=320,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Dynamic Gauge Max Range
        gauge_max = 160 if threat_level > 100 else 100
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = threat_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Overall Threat Index", 'font': {'color': '#c9a063', 'family': 'Cinzel', 'size': 18}},
            gauge = {
                'axis': {'range': [None, gauge_max], 'tickwidth': 2, 'tickcolor': "#3a2e24"},
                'bar': {'color': color},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#3a2e24",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(216, 195, 165, 0.1)'},
                    {'range': [40, 70], 'color': 'rgba(0, 255, 204, 0.2)'},
                    {'range': [70, 90], 'color': 'rgba(255, 170, 0, 0.2)'},
                    {'range': [90, 110], 'color': 'rgba(255, 75, 75, 0.3)'},
                    {'range': [110, gauge_max], 'color': 'rgba(148, 0, 211, 0.4)'}
                ],
            },
            number = {'font': {'color': color}}
        ))
        fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.divider()
        if st.button("💾 LOCK CHASSIS & DEPLOY TO APEX ARENA", use_container_width=True):
            st.session_state['titan_deployment'] = {
                'threat_level': threat_level,
                'classification': classification,
                'power_desc': power_desc,
                'mass': estimated_mass,
                'color': color,
                'name': f"Custom {chassis.split()[0] if origin == 'The Nine Titans (Canon)' else selected_genre} Titan"
            }
            st.success("Titan registered to global session network. Proceed to the Apex Arena tab.")


def render_apex_arena_tab():
    st.header("🏟️ The Apex Arena")
    
    if 'titan_deployment' not in st.session_state:
        st.warning("⚠️ No Titan detected in orbit. Return to the **Titan Forge**, engineer a chassis, and lock its deployment state.")
        return
        
    titan = st.session_state['titan_deployment']
    
    st.markdown(f"**Deployed Asset:** {titan['name']} | **Classification:** <span style='color:{titan['color']}'>{titan['classification']}</span> | **Mass:** {titan['mass']/1000:.1f} Tons", unsafe_allow_html=True)
    
    try:
        with open("opponents.json", "r") as f:
            opponents = json.load(f)
    except Exception:
        st.error("opponents.json not found. Run the generation script.")
        return

    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("<div class='lore-card'>", unsafe_allow_html=True)
        st.subheader("Target Selection")
        
        opponent_names = [o["name"] for o in opponents]
        selected_opp = st.selectbox("Select Target Entity", opponent_names)
        
        enemy = next(o for o in opponents if o["name"] == selected_opp)
        
        st.markdown(f"**Origin:** {enemy['origin']}")
        st.info(f"**Profile:** {enemy['desc']}")
        
        environment = st.selectbox("Battleground", ["Shattered Earth (Tokyo Ruins)", "Dying Sun Orbit", "The Null Void", "Pre-Historic Pangea"])
        
        st.divider()
        initiate = st.button("🔥 INITIATE DEATHMATCH", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        log_box = st.empty()
        gauge_box = st.empty()
        
    if initiate:
        t_power = titan['threat_level']
        e_power = enemy['power']
        
        # Calculate win probability based on power gap and a massive random chaos factor
        power_diff = t_power - e_power
        chaos_roll = random.uniform(-40, 40)
        final_clash = power_diff + chaos_roll
        
        logs = [
            f"INITIALIZING MANIFESTATION... Transmitting {titan['name']} to {environment}.",
            f"TARGET ACQUIRED: {enemy['name']} has entered the airspace.",
            "ATMOSPHERIC IGNITION: The sheer presence of both entities is warping gravity.",
            f"The Titan lunges, utilizing: {titan['power_desc']}",
            f"COLLISION: {enemy['name']} retaliates! Shockwaves shatter the tectonic plates below!"
        ]
        
        if final_clash > 0:
            logs.append(f"CRITICAL STRIKE: The Titan overpowers {enemy['name']}, tearing through their conceptual defenses!")
            logs.append(f"VICTORY: {enemy['name']} is obliterated. The Titan stands alone amidst the ash.")
            earth_damage = min(100, 30 + (t_power * 0.4))
            result_color = "#00ffcc"
            winner = "TITAN"
        else:
            logs.append(f"CATASTROPHIC FAILURE: {enemy['name']} unleashes an apex counter-attack, ignoring the Titan's armor!")
            logs.append(f"DEFEAT: The Titan is completely atomized. {enemy['name']} remains untouched.")
            earth_damage = min(100, 50 + (e_power * 0.4))
            result_color = "#ff4b4b"
            winner = enemy['name'].upper()

        # Render Dramatic Animation
        log_text = ""
        for line in logs:
            log_text += f"\n\n> {line}"
            log_box.markdown(log_text)
            time.sleep(1.2)
            
        # Post-Fight Environmental Damage Report
        gauge_box.divider()
        gauge_box.subheader("🌍 Planetary Integrity Report")
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = earth_damage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Biosphere Destruction (%)", 'font': {'color': '#c9a063'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#3a2e24"},
                'bar': {'color': result_color},
                'bgcolor': "rgba(0,0,0,0)",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(216, 195, 165, 0.1)'},
                    {'range': [40, 70], 'color': 'rgba(255, 170, 0, 0.2)'},
                    {'range': [70, 100], 'color': 'rgba(255, 75, 75, 0.3)'}],
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
        
        gauge_box.plotly_chart(fig, use_container_width=True)
        gauge_box.error(f"**MATCH CONCLUDED.** The victor is **{winner}**. Estimated energy release: {earth_damage * 4.2:.1f} Petajoules.")
