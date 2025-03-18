import streamlit as st
import pickle
import numpy as np
import pandas as pd
import base64
import time

# Set Streamlit page config first
st.set_page_config(page_title="Exoplanet Analyzer", layout="wide")

# Load the trained model
model_path = "decision_tree_model.pkl"
with open(model_path, "rb") as model_file:
    model = pickle.load(model_file)

# Video Background using HTML5 video element
def get_video_base64(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode()

# Video path - make sure this path is correct for your deployment environment
video_path = "C:/Users/Admin/Desktop/IITR/image/space.mp4"

# Attempt to encode the video - handle failure gracefully
try:
    encoded_video = get_video_base64(video_path)
    video_html = f"""
    <style>
    .stApp {{
        background: rgba(0, 0, 0, 0.5);
    }}
    
    .video-background {{
        position: fixed;
        right: 0;
        bottom: 0;
        width: 100%;
        height: 100%;
        z-index: -1000;
        object-fit: cover;
    }}

    /* Keep other styling elements from previous code */
    .main-content {{
        background-color: rgba(0, 0, 0, 0.7);
        color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }}
    
    /* Styling for prediction card */
    .prediction-card {{
        background-color: rgba(0, 0, 0, 0.8);
        border-radius: 10px;
        padding: 20px;
        border: 2px solid #4CAF50;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 0 15px rgba(76, 175, 80, 0.5);
        backdrop-filter: blur(5px);
    }}
    
    /* Styling for prediction text */
    .prediction-text {{
        font-size: 28px;
        font-weight: bold;
        color: #4CAF50;
        padding: 10px;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 5px;
        display: inline-block;
        margin: 10px 0;
    }}
    
    /* Styling for interpretation section */
    .interpretation {{
        background-color: rgba(0, 0, 0, 0.8);
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        border-left: 4px solid #2196F3;
        backdrop-filter: blur(5px);
    }}
    
    /* Enhanced header styling */
    h1, h2, h3 {{
        text-shadow: 2px 2px 4px #000000;
    }}
    
    /* Futuristic header styling */
    .cyber-header {{
        font-family: 'Arial', sans-serif;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: white;  /* Changed to white for better visibility */
        text-shadow: 0 0 10px rgba(0, 0, 0, 0.7);  /* Adjusted shadow for contrast */
        margin-bottom: 20px;
    }}

    /* Futuristic loader */
    .loader-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }}
    
    .loader {{
        width: 150px;
        height: 150px;
        border: 5px solid rgba(0, 198, 255, 0.3);
        border-radius: 50%;
        border-top-color: #00c6ff;
        animation: spin 1s ease-in-out infinite;
        position: relative;
    }}
    
    .loader::before {{
        content: "";
        position: absolute;
        top: 5px;
        left: 5px;
        right: 5px;
        bottom: 5px;
        border: 5px solid transparent;
        border-top-color: #0072ff;
        border-radius: 50%;
        animation: spin 2s linear infinite;
    }}
    
    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}
    
    /* Parameter control panel styling */
    .parameter-panel {{
        background-color: rgba(0, 0, 0, 0.8);
        border: 1px solid #00c6ff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 0 10px rgba(0, 198, 255, 0.3);
        backdrop-filter: blur(5px);
    }}
    
    .parameter-label {{
        color: #00c6ff;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }}
    
    /* Parameter value indicator */
    .value-indicator {{
        height: 25px;
        background: linear-gradient(90deg, #001B3A, #0072ff);
        border-radius: 4px;
        position: relative;
        margin-bottom: 10px;
        box-shadow: 0 0 5px rgba(0, 198, 255, 0.5);
    }}
    
    /* Data visualization styling */
    .data-visual {{
        background-color: rgba(0, 0, 0, 0.8);
        border: 1px solid #00c6ff;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.3);
        backdrop-filter: blur(5px);
    }}
    
    /* Hide the default Streamlit slider label */
    div.row-widget.stSlider [data-testid="stMarkdownContainer"] {{
        display: none;
    }}
    
    /* Hide loader when prediction is complete */
    .hidden {{
        display: none !important;
    }}
    </style>
    <video autoplay muted loop playsinline class="video-background">
        <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
    </video>
    """
    st.markdown(video_html, unsafe_allow_html=True)
except Exception as e:
    # Fallback to previous animation if video loading fails
    st.error(f"Unable to load video background: {e}")
    video_background_css = """
        <style>
        .stApp {
            background: rgba(0, 0, 0, 0.5);
        }
        
        /* Space background with stars animation effect */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(45deg, #000000, #000022, #000033);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        /* Add stars to the background */
        .stApp::after {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 4px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 4px);
            background-size: 550px 550px, 350px 350px, 250px 250px;
            background-position: 0 0, 40px 60px, 130px 270px;
            animation: twinkle 10s ease infinite alternate;
        }
        
        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        @keyframes twinkle {
            0% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        
        /* Other styling elements remain the same */
        .main-content {
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        /* Styling for prediction card */
        .prediction-card {
            background-color: rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            padding: 20px;
            border: 2px solid #4CAF50;
            margin: 20px 0;
            text-align: center;
            box-shadow: 0 0 15px rgba(76, 175, 80, 0.5);
            backdrop-filter: blur(5px);
        }
        
        /* Styling for prediction text */
        .prediction-text {
            font-size: 28px;
            font-weight: bold;
            color: #4CAF50;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 5px;
            display: inline-block;
            margin: 10px 0;
        }
        
        /* Styling for interpretation section */
        .interpretation {
            background-color: rgba(0, 0, 0, 0.8);
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            border-left: 4px solid #2196F3;
            backdrop-filter: blur(5px);
        }
        
        /* Enhanced header styling */
        h1, h2, h3 {
            text-shadow: 2px 2px 4px #000000;
        }
        
        /* Futuristic header styling */
        .cyber-header {
            font-family: 'Arial', sans-serif;
            text-transform: uppercase;
            letter-spacing: 3px;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
            padding: 10px;
            border-bottom: 2px solid #00c6ff;
            margin-bottom: 20px;
        }
        
        /* Futuristic loader */
        .loader-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
        }
        
        .loader {
            width: 150px;
            height: 150px;
            border: 5px solid rgba(0, 198, 255, 0.3);
            border-radius: 50%;
            border-top-color: #00c6ff;
            animation: spin 1s ease-in-out infinite;
            position: relative;
        }
        
        .loader::before {
            content: "";
            position: absolute;
            top: 5px;
            left: 5px;
            right: 5px;
            bottom: 5px;
            border: 5px solid transparent;
            border-top-color: #0072ff;
            border-radius: 50%;
            animation: spin 2s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Parameter control panel styling */
        .parameter-panel {
            background-color: rgba(0, 0, 0, 0.8);
            border: 1px solid #00c6ff;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0 0 10px rgba(0, 198, 255, 0.3);
            backdrop-filter: blur(5px);
        }
        
        .parameter-label {
            color: #00c6ff;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 14px;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        
        /* Parameter value indicator */
        .value-indicator {
            height: 25px;
            background: linear-gradient(90deg, #001B3A, #0072ff);
            border-radius: 4px;
            position: relative;
            margin-bottom: 10px;
            box-shadow: 0 0 5px rgba(0, 198, 255, 0.5);
        }
        
        /* Data visualization styling */
        .data-visual {
            background-color: rgba(0, 0, 0, 0.8);
            border: 1px solid #00c6ff;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            box-shadow: 0 0 15px rgba(0, 198, 255, 0.3);
            backdrop-filter: blur(5px);
        }
        
        /* Hide the default Streamlit slider label */
        div.row-widget.stSlider [data-testid="stMarkdownContainer"] {
            display: none;
        }
        
        /* Hide loader when prediction is complete */
        .hidden {
            display: none !important;
        }
        </style>
    """
    
    # Inject CSS
    st.markdown(video_background_css, unsafe_allow_html=True)

# Add custom JS for loader handling
st.markdown("""
<script>
function hideLoader() {
    document.querySelector('.loader-container').classList.add('hidden');
}
</script>
""", unsafe_allow_html=True)

# Futuristic title and intro
st.markdown("""
    <div class="cyber-header">
        <h1 style="color: white;">🪐 EXOPLANET CLASSIFICATION MATRIX 🌌</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-content">
        <h2 style="color: white;">✧ COSMIC CARTOGRAPHER ✧</h2>
        
        Welcome to the frontier of interstellar exploration. This advanced neural interface allows you to analyze 
        distant worlds across the cosmos by manipulating planetary parameters within our quantum prediction matrix.
        
        Our hyperspace algorithm processes multidimensional data vectors including atmospheric composition, 
        gravitational constants, and thermal signatures to classify potential exoplanets for the Galactic Federation's 
        colonization initiative.
        
        Begin your mission by calibrating the planetary parameters below and initiate the quantum scan sequence.
    </div>
""", unsafe_allow_html=True)

# Feature names and updated min-max values
feature_ranges = {
    "Atmospheric Density": (-4.28, 9.32),
    "Surface Temperature": (-5.43, 5.64),
    "Gravity": (-5.55, 6.03),
    "Water Content": (-5.82, 6.29),
    "Mineral Abundance": (-5.08, 5.34),
    "Orbital Period": (-4.80, 5.11),
    "Proximity to Star": (-4.54, 4.73),
    "Magnetic Field Strength": (1.00, 20.00),
    "Radiation Levels": (1.00, 20.00),
    "Atmospheric Composition Index": (-4.01, 3.85)
}

# Improved parameter input section
st.markdown("""
    <div class="cyber-header" style="margin-top: 30px;">
        <h2 style="color: white;">⚛ PLANETARY PARAMETER CALIBRATION</h2>
    </div>
""", unsafe_allow_html=True)

# Create two columns for parameter panels
col1, col2 = st.columns(2)
input_values = []

# Function to create parameter panel with custom slider
def parameter_panel(feature, min_val, max_val, column):
    with column:
        st.markdown(f"""
            <div class="parameter-panel">
                <div class="parameter-label">{feature}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Use a unique key for each slider
        slider_key = f"slider_{feature.replace(' ', '_').lower()}"
        
        # Use streamlit slider with a unique key and hidden label
        value = st.slider(
            "###", 
            min_value=float(min_val), 
            max_value=float(max_val), 
            value=float((min_val + max_val) / 2),
            key=slider_key,
            label_visibility="collapsed"
        )
        
        # Calculate percentage for visual indicator
        percentage = ((value - min_val) / (max_val - min_val)) * 100
        
        # Display current value with futuristic styling
        # st.markdown(f"""
        #     <div style="display: flex; justify-content: space-between; margin-top: -15px;">
        #         <span style="color: #00c6ff; font-size: 12px;">{min_val:.2f}</span>
        #         <span style="color: #00c6ff; font-size: 14px; font-weight: bold;">{value:.2f}</span>
        #         <span style="color: #00c6ff; font-size: 12px;">{max_val:.2f}</span>
        #     </div>
        #     <div class="value-indicator" style="width: {percentage}%;"></div>
        # """, unsafe_allow_html=True)
        
        return value

# Create parameter panels in alternating columns
features = list(feature_ranges.keys())
for i, (feature, (min_val, max_val)) in enumerate(feature_ranges.items()):
    value = parameter_panel(feature, min_val, max_val, col1 if i % 2 == 0 else col2)
    input_values.append(value)

# Convert input values to Pandas DataFrame with correct feature names
input_df = pd.DataFrame([input_values], columns=feature_ranges.keys())

# Function to get interpretation text based on planet type
def get_planet_description(prediction_code):
    descriptions = {
        1: "This celestial body exhibits prime habitability markers with Earth-comparable atmospheric composition, liquid water, and stable temperature ranges. Potential for immediate colonization without environmental adaptation technologies.",
        2: "Analysis indicates this world possesses fundamental planetary characteristics conducive to geo-engineering. With appropriate atmospheric modification and biosphere seeding, habitability index could reach 78.3% within 2.7 centuries.",
        3: "Scans detect exceptional concentrations of rare minerals and elemental deposits including quantum-stabilized metals, antimatter catalysts, and chronoton-rich isotopes. Prime candidate for automated mining operations.",
        4: "This anomalous world presents unique physical properties that defy standard classification parameters. Further scientific observation recommended to document previously unknown cosmic phenomena.",
        5: "Massive gaseous body with hyper-pressurized core. Atmospheric layers contain exotic compounds ideal for cloud-city habitation modules and gas harvesting operations at upper atmospheric strata.",
        6: "Xerothermic conditions dominate this planet with minimal hydrosphere presence. Surface exhibits extreme temperature fluctuations between day-night cycles with periodic silicate storms.",
        7: "Cryogenic world with multiple ice compositions. Deep scans indicate potential for sub-surface liquid oceans with chemical signatures suggesting primitive extremophile evolution.",
        8: "Atmospheric toxicity index exceeds safety parameters by 874%. Contains corrosive compounds and neurological agents hazardous to most known biological entities. Specialized containment protocols required for exploration.",
        9: "Dangerous radiation flux emanates from unstable planetary core and/or proximity to stellar radiation sources. Extended exposure would compromise biological tissue and electronic systems without quantum shielding.",
        10: "Complete absence of biosphere indicators. Planetary conditions hostile to all known forms of organic development with no terraformation potential. Classification: null-spectrum exoworld."
    }
    return descriptions.get(prediction_code, "Unknown planetary classification")

# Function to get exploration protocol based on planet type
def get_exploration_protocol(prediction_code):
    protocols = {
        1: "Deploy standard colonization modules with minimal terraforming required. Initiate biosphere compatibility scans for native ecosystem integration.",
        2: "Begin atmospheric processors deployment at polar regions. Recommended timeline: 27.6 cycles for initial habitability zones.",
        3: "Deploy automated mineral extraction drones with quantum refinement capabilities. Establish orbital processing station at L4 Lagrange point.",
        4: "Launch scientific observation satellites and minimal-impact probe network. Maintain planetary preservation protocols to avoid contamination of anomalous properties.",
        5: "Station orbital gas harvesting platform with cloud-city capability. High-altitude exploration recommended with pressure-resistant vehicles.",
        6: "Heat-resistant exploration equipment required. Water conservation systems at maximum efficiency. Deploy subsurface moisture extraction apparatus.",
        7: "Deploy thermal drilling units for subsurface ocean access. Specialized cryogenic research modules required for surface operations.",
        8: "Atmospheric isolation protocols mandatory. Deploy remote-operated exploration units with enhanced corrosion resistance. No biological exploration permitted.",
        9: "Establish orbital observation only. If surface exploration is critical, quantum-shielded vehicles with limited exposure duration recommended.",
        10: "Automated probe deployment permitted for geological sampling. No long-term presence recommended due to null-spectrum classification."
    }
    return protocols.get(prediction_code, "Standard exploration protocol with caution advised due to unknown classification.")

# Dictionary for planet type to color mapping
planet_colors = {
    1: "#4CAF50",  # Habitable - Green
    2: "#8BC34A",  # Terraformable - Light Green
    3: "#FFC107",  # Resource Rich - Amber
    4: "#2196F3",  # Scientific - Blue
    5: "#9C27B0",  # Gas Giant - Purple
    6: "#FF9800",  # Desert Planet - Orange
    7: "#00BCD4",  # Ice World - Cyan
    8: "#F44336",  # Toxic Atmosphere - Red
    9: "#FF5722",  # High Radiation - Deep Orange
    10: "#9E9E9E"  # Dead World - Grey
}

# Dictionary for planet type to label mapping
planet_labels = {
    1: "BEWOHNBAR: HABITABLE WORLD",
    2: "TERRAFORMIERBAR: TERRAFORMATION CANDIDATE",
    3: "ROHSTOFFREICH: RESOURCE-ABUNDANT SPHERE",
    4: "WISSENSCHAFTLICH: ANOMALOUS RESEARCH WORLD",
    5: "GASRIESE: JOVIAN GAS GIANT",
    6: "WÜSTENPLANET: DESERT XEROSPHERE",
    7: "EISWELT: CRYOGENIC ICE PLANET",
    8: "TOXISCHETMOSÄRE: LETHAL ATMOSPHERE DETECTED",
    9: "HOHESTRAHLUNG: RADIATION-SATURATED WORLD",
    10: "TOTERAHSWELT: NULL-SPECTRUM DEAD WORLD"
}

# Predict button with futuristic styling
st.markdown("""
    <div style="margin-top: 30px;">
        <h2 class="cyber-header">⚡ INITIATE QUANTUM ANALYSIS</h2>
    </div>
""", unsafe_allow_html=True)

# Place to put the loader
loader_container = st.empty()

predict_btn = st.button("SCAN PLANETARY PARAMETERS", key="predict_button", use_container_width=True)

# Only show prediction once
if predict_btn:
    # Show the loader
    loader_container.markdown("""
        <div class="loader-container">
            <div class="loader"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Simulate processing for effect
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        # Update progress bar
        progress_bar.progress(i + 1)
        
        # Update status text based on progress
        if i < 25:
            status_text.markdown('<div style="text-align: center; color: #00c6ff;">Analyzing atmospheric composition...</div>', unsafe_allow_html=True)
        elif i < 50:
            status_text.markdown('<div style="text-align: center; color: #00c6ff;">Calculating habitability parameters...</div>', unsafe_allow_html=True)
        elif i < 75:
            status_text.markdown('<div style="text-align: center; color: #00c6ff;">Processing planetary metrics...</div>', unsafe_allow_html=True)
        else:
            status_text.markdown('<div style="text-align: center; color: #00c6ff;">Finalizing classification matrix...</div>', unsafe_allow_html=True)
        
        # Simulate processing time
        time.sleep(0.02)
    
    # Hide the loader when processing is complete
    loader_container.empty()
    
    # Remove progress indicators
    progress_bar.empty()
    status_text.empty()
    
    # Get prediction
    prediction = model.predict(input_df)[0]
    
    # Get color and label based on prediction
    color = planet_colors.get(prediction, "#9E9E9E")
    label = planet_labels.get(prediction, "UNCLASSIFIED ANOMALY")
    description = get_planet_description(prediction)
    
    # Custom CSS for this specific prediction color
    st.markdown(f"""
        <style>
        .prediction-text-{prediction} {{
            color: {color};
            border: 2px solid {color};
            text-shadow: 0 0 10px {color};
        }}
        .prediction-card-{prediction} {{
            border-color: {color};
            box-shadow: 0 0 20px {color}80;
        }}
        </style>
        
        <div class="prediction-card prediction-card-{prediction}">
            <h2 style="color: {color}; text-shadow: 0 0 10px {color}60;">⚠ CLASSIFICATION COMPLETE ⚠</h2>
            <div class="prediction-text prediction-text-{prediction}">
                {label}
            </div>
        </div>
        
        <div class="interpretation" style="border-color: {color};">
            <h3 style="color: {color};">🔍 PLANETARY ANALYSIS</h3>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Data Visualization
    st.markdown("""
        <div class="cyber-header" style="margin-top: 30px;">
            <h2>🔮 PARAMETER MATRIX VISUALIZATION</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Create a column chart of input values with enhanced styling
    st.markdown("""
        <div class="data-visual">
            <div style="color: #00c6ff; font-weight: bold; margin-bottom: 10px;">
                PLANETARY PARAMETER SPECTRUM ANALYSIS
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Prepare data for visualization
    chart_data = pd.DataFrame({
        'Parameter': list(feature_ranges.keys()),
        'Value': input_values,
        'Min': [min_val for min_val, _ in feature_ranges.values()],
        'Max': [max_val for _, max_val in feature_ranges.values()]
    })
    
    # Normalize values for better visualization
    chart_data['Normalized'] = chart_data.apply(
        lambda row: (row['Value'] - row['Min']) / (row['Max'] - row['Min']), 
        axis=1
    )
    
    # Create columns for visualization
    viz_col1, viz_col2 = st.columns([2, 1])
    
    with viz_col1:
        # Use Streamlit's native plotting with custom styling
        radar_data = pd.DataFrame({
            'Parameter': chart_data['Parameter'],
            'Value': chart_data['Normalized'] * 100  # Scale to percentage
        })
        
        # Use a horizontal bar chart for a more futuristic look
        st.markdown("""
            <div style="background-color: rgba(0, 0, 0, 0.7); padding: 10px; border-radius: 5px;">
                <p style="color: #00c6ff; text-align: center;">PARAMETER INTENSITY SPECTRUM</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.bar_chart(radar_data.set_index('Parameter'), use_container_width=True)
    
    with viz_col2:
        # Show key metrics in futuristic display
        st.markdown(f"""
            <div style="background-color: rgba(0, 0, 0, 0.8); padding: 15px; border-radius: 10px; border: 1px solid {color};">
                <div style="color: {color}; font-weight: bold; text-align: center; margin-bottom: 10px;">
                    DOMINANT PARAMETERS
                </div>
                <div style="font-family: monospace; font-size: 14px;">
        """, unsafe_allow_html=True)
        
        # Find top 3 most extreme values
        normalized_values = chart_data['Normalized'].values
        top_indices = np.argsort(np.abs(normalized_values - 0.5))[-3:]
        
        for idx in top_indices:
            param = chart_data.iloc[idx]['Parameter']
            value = chart_data.iloc[idx]['Value']
            percentage = int(chart_data.iloc[idx]['Normalized'] * 100)
            
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>{param}</span>
                    <span style="color: {color};">{value:.2f}</span>
                </div>
                <div style="background-color: #001B3A; height: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <div style="background-color: {color}; width: {percentage}%; height: 10px; border-radius: 5px;"></div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Add recommendation section
    st.markdown(f"""
        <div class="interpretation" style="border-color: {color}; margin-top: 20px;">
            <h3 style="color: {color};">🚀 EXPLORATION PROTOCOL</h3>
            <p>Based on the planetary classification, the following mission parameters are recommended:</p>
            <ul style="list-style-type: none; padding-left: 10px;">
                <li>• {get_exploration_protocol(prediction)}</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)



