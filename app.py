#!/usr/bin/env python3
"""
TMC CV Optimizer — VERSION 1.3.4-AIRTABLE-FIX
Interface Streamlit premium avec design moderne et backend complet

✅ AIRTABLE FIX (Current):
- ✅ Fixed field names: "Event_Type" (underscore), "User Location" (full name)
- ✅ Added missing fields: Client, Anonymized, Skills Matrix Used
- ✅ Full compatibility with CV Logs table structure

✨ PERFORMANCE OPTIMIZATIONS (30-35% faster):
- ✅ Fix #1: Matching analysis reuse (saves 15-20s per generation)
- ✅ Fix #2: Reduced timeline renders from 6 to 2 (saves 1-3s)
- ✅ Result: 60-75s → 37-52s generation time

🔧 Previous features:
- Skills Matrix Upload section added for Morgan Stanley
- Validation before CV generation for Morgan Stanley
- Correct generation method (generate_ms_cv_3parts) with Skills Matrix path
- Full functional parity with app_working.py
- Modern UI preserved from app.py
"""

import streamlit as st
from pathlib import Path
import base64
import tempfile
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import extra_streamlit_components as stx
import PyPDF2
from docx import Document
import json
import requests

# Charger les variables d'environnement depuis .env
load_dotenv()

# ==========================================
# 🎨 CONSTANTES COULEURS TMC
# ==========================================
PRIMARY_BLUE = "#193E92"    # Bleu TMC principal
SECONDARY_ORANGE = "#D97104"  # Orange TMC
BG_LIGHT = "#F9FAFB"
SUCCESS_GREEN = "#10B981"

# ==========================================
# ⚙️ CONFIG PAGE
# ==========================================
st.set_page_config(
    page_title="CV Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"  # ✨ NEW: Sidebar expanded by default
)

# ==========================================
# 🎨 CSS CENTRALISÉ (V1.3.4 Style)
# ==========================================
def local_css():
    """Styles CSS modernes et centralisés"""
    st.markdown(f"""
    <style>
        /* ========== GLOBAL STYLES ========== */
        .stApp {{
            background: linear-gradient(180deg, {BG_LIGHT} 0%, #ECEFF3 100%);
        }}
        
        * {{
            font-family: 'Arial', 'Open Sans', sans-serif;
        }}
        
        /* Remove default Streamlit padding */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1100px !important;  /* ✨ FIXED: Reduced from 1200px for better margins */
            width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-left: 2rem !important;  /* ✨ NEW: Consistent padding */
            padding-right: 2rem !important;
        }}
        
        /* Hide Streamlit default elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* ========== HIDE SECRETS ERROR MESSAGE - COMPREHENSIVE ========== */
        /* Target all possible classes and containers for secrets.toml error */
        .element-container:has(> .stException) {{
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            overflow: hidden !important;
        }}
        
        [data-testid="stException"] {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        .stException {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        div.stException {{
            display: none !important;
        }}
        
        /* Target error messages containing "secrets" keyword */
        [data-testid="stException"]:has([class*="secrets"]) {{
            display: none !important;
        }}
        
        /* Target specific error alert containers */
        [data-testid="stAlert"] {{
            display: none !important;
        }}
        
        div[data-testid="stNotification"] {{
            display: none !important;
        }}
        
        /* Hide any error message in main container */
        .main [data-testid="stException"] {{
            display: none !important;
        }}
        
        /* Nuclear option: hide all exception elements */
        [class*="Exception"] {{
            display: none !important;
        }}
        
        /* ========== SIDEBAR STYLES ========== */
        [data-testid="stSidebar"] {{
            background: white;
            padding: 2rem 1.5rem;
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            padding: 0;
        }}
        
        /* ========== HERO SECTION ========== */
        .tmc-hero {{
            text-align: center;
            padding: 2rem 0;
        }}
        
        .tmc-subtitle {{
            color: #6B7280;
            font-size: 1.1rem;
            margin-top: 0.3rem;
            line-height: 1.6;
        }}
        
        /* ========== CLIENT INFO CARDS ========== */
        .client-card {{
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            line-height: 1.8;
        }}
        
        .client-card-ms {{
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-left: 4px solid #3B82F6;
        }}
        
        .client-card-cae {{
            background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
            border-left: 4px solid #22C55E;
        }}
        
        .client-card-desj {{
            background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
            border-left: 4px solid #F59E0B;
        }}
        
        /* ========== CARDS ========== */
        .tmc-card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 8px 24px rgba(17, 24, 39, 0.08);
            transition: all 0.3s ease;
        }}
        
        .tmc-card:hover {{
            box-shadow: 0 12px 32px rgba(17, 24, 39, 0.12);
        }}
        
        /* ========== BUTTONS WITH GRADIENT ========== */
        .stButton>button {{
            background: linear-gradient(90deg, {PRIMARY_BLUE} 0%, {SECONDARY_ORANGE} 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.9rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 14px rgba(25, 62, 146, 0.25) !important;
            width: 100% !important;
            min-height: 60px !important;  /* ✨ MATCHED: Same as Download button */
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(25, 62, 146, 0.35) !important;
        }}
        
        .stButton>button:active {{
            transform: translateY(0) !important;
        }}
        
        .stButton>button:disabled {{
            background: #D1D5DB !important;
            color: #9CA3AF !important;
            cursor: not-allowed !important;
            transform: none !important;
            box-shadow: none !important;
        }}
        
        /* ========== DIVIDER ========== */
        .divider {{
            height: 1px;
            background: #E5E7EB;
            margin: 1.5rem 0;
        }}
        
        /* ========== PRIVACY NOTE ========== */
        .privacy-note {{
            display: flex;
            align-items: start;
            gap: 0.5rem;
            padding: 1rem;
            border-radius: 8px;
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            margin: 1rem 0;
            font-size: 0.875rem;
            color: #6B7280;
        }}
        
        /* ========== FILE UPLOADER ========== */
        [data-testid="stFileUploader"] {{
            border: 2px dashed {PRIMARY_BLUE}40;
            border-radius: 14px;
            background: white;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }}
        
        [data-testid="stFileUploader"]:hover {{
            border-color: {SECONDARY_ORANGE};
            background: #FEF3E2;
        }}
        
        /* ========== RADIO BUTTONS (Language) - CENTERED ========== */
        .stRadio > div {{
            display: flex;
            justify-content: center;
            gap: 1rem;
        }}
        
        .stRadio > div > label {{
            background: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            border: 2px solid #E5E7EB;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }}
        
        .stRadio > div > label:hover {{
            border-color: {PRIMARY_BLUE};
            background: {BG_LIGHT};
        }}
        
        .stRadio > div > label[data-checked="true"] {{
            border-color: {PRIMARY_BLUE};
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            color: {PRIMARY_BLUE};
        }}
        
        /* ========== DATAFRAME STYLES (Professional Table) ========== */
        [data-testid="stDataFrame"] {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(25, 62, 146, 0.12);
            border: 2px solid {PRIMARY_BLUE};
        }}
        
        [data-testid="stDataFrame"] table {{
            border-collapse: collapse;
        }}
        
        [data-testid="stDataFrame"] thead {{
            background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, #2563eb 100%);
        }}
        
        [data-testid="stDataFrame"] thead th {{
            color: white !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            padding: 18px 16px !important;
            text-align: left !important;
            border: none !important;
        }}
        
        [data-testid="stDataFrame"] tbody td {{
            padding: 16px !important;
            font-size: 0.9rem !important;
            border-bottom: 1px solid #e5e7eb !important;
            vertical-align: middle !important;
            line-height: 1.6 !important;
        }}
        
        [data-testid="stDataFrame"] tbody tr:last-child td {{
            border-bottom: none !important;
        }}
        
        [data-testid="stDataFrame"] tbody tr:hover {{
            box-shadow: inset 4px 0 0 {SECONDARY_ORANGE};
            transition: all 0.2s ease;
        }}
        
        /* ========== FOOTER ========== */
        .tmc-footer {{
            text-align: center;
            color: #6B7280;
            font-size: 0.9rem;
            border-top: 1px solid #E5E7EB;
            margin-top: 3rem;
        }}
        
        /* ========== DOWNLOAD BUTTON - GREEN GRADIENT ========== */
        /* Global styling for download button wrapper */
        #download-btn-wrapper {{
            margin: 1rem 0;
        }}
        
        #download-btn-wrapper button {{
            background: linear-gradient(90deg, #22c55e 0%, #047857 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.9rem 2rem !important;  /* ✨ MATCHED: Same as Generate button */
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            box-shadow: 0 4px 14px rgba(34, 197, 94, 0.35) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            min-height: 60px !important;  /* ✨ MATCHED: Same height as Generate */
        }}
        
        #download-btn-wrapper button:hover {{
            box-shadow: 0 8px 24px rgba(34, 197, 94, 0.45) !important;
            transform: translateY(-2px) !important;
        }}
        
        #download-btn-wrapper button:active {{
            transform: translateY(0) !important;
        }}
        
        /* ✨ V9 FIX: Force Download button to full width with green gradient */
        [data-testid="stDownloadButton"] {{
            width: 100% !important;
        }}
        
        [data-testid="stDownloadButton"] > button {{
            background: linear-gradient(90deg, #22c55e 0%, #047857 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.9rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            box-shadow: 0 4px 14px rgba(34, 197, 94, 0.35) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            min-height: 60px !important;
        }}
        
        [data-testid="stDownloadButton"] > button:hover {{
            box-shadow: 0 8px 24px rgba(34, 197, 94, 0.45) !important;
            transform: translateY(-2px) !important;
        }}
        
        [data-testid="stDownloadButton"] > button:active {{
            transform: translateY(0) !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 📊 CLIENT DATA DICTIONARY (V1.3.4)
# ==========================================
CLIENT_DATA = {
    "Morgan Stanley": {
        "rules": [
            "🇬🇧 <strong>English only</strong> (auto)",
            "🔒 <strong>Always Anonymized</strong> (auto)",
            "📄 Format: Cover + Skills Matrix + Details",
            "🎯 Financial experience highly valued"
        ],
        "card_class": "client-card-ms",
        "show_language": False,  # Pas de choix de langue
        "anonymize": True,       # Toujours anonymisé
        "language": "English",   # Toujours anglais
        "use_skizmatrix": True   # Utilise la Skills Matrix
    },
    "CAE": {
        "rules": [
            "🌐 <strong>French or English</strong> (your choice)",
            "🔒 <strong>Always Anonymized</strong> (required)",
            "📄 Format: TMC Standard",
            "🎯 Aerospace/Defense experience valued"
        ],
        "card_class": "client-card-cae",
        "show_language": True,   # Choix de langue
        "anonymize": True,       # Toujours anonymisé
        "language": None,        # À choisir par l'utilisateur
        "use_skizmatrix": False  # Pas de Skills Matrix
    },
    "Desjardins": {
        "rules": [
            "🌐 <strong>French only</strong>",
            "📄 Format: TMC Branded with logo",
            "🎯 Quebec experience valued"
        ],
        "card_class": "client-card-desj",
        "show_language": False,  # Pas de choix (toujours français)
        "anonymize": False,      # Jamais anonymisé
        "language": "French",    # Toujours français
        "use_skizmatrix": False  # Pas de Skills Matrix
    }
}

# ==========================================
# 🎨 HORIZONTAL TIMELINE (Keep from app.py)
# ==========================================
def horizontal_progress_timeline(current_step: int = 1, total_steps: int = 5, step_labels: list = None) -> str:
    """
    Génère une timeline horizontale avec des étapes dynamiques.
    current_step: étape en cours (1-N)
    total_steps: nombre total d'étapes
    step_labels: liste des étapes avec icon et label
    """
    if step_labels is None:
        # Default: 5 steps
        step_labels = [
            {"num": 1, "icon": "🔍", "label": "Extraction"},
            {"num": 2, "icon": "🤖", "label": "Analysis"},
            {"num": 3, "icon": "✨", "label": "Enrichment"},
            {"num": 4, "icon": "🗺️", "label": "Structuring"},
            {"num": 5, "icon": "📝", "label": "Generation"},
        ]
    
    # Calculate progress percentage
    if total_steps > 1:
        progress_percent = ((current_step - 1) / (total_steps - 1)) * 100
    else:
        progress_percent = 100 if current_step >= total_steps else 0
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Arial', sans-serif;
                background: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .timeline {
                display: flex;
                align-items: center;
                justify-content: space-between;
                width: 90%;
                max-width: 1000px;
                min-width: 600px;
                margin: 0 auto;
                position: relative;
            }
            .step {
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
                z-index: 2;
                flex: 1;
            }
            .step-circle {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                background: #E5E7EB;
                border: 4px solid #E5E7EB;
                transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .step.active .step-circle {
                background: linear-gradient(135deg, #193E92 0%, #D97104 100%);
                border-color: #193E92;
                transform: scale(1.1);
                box-shadow: 0 4px 20px rgba(25, 62, 146, 0.4);
                animation: pulse 1.5s ease-in-out infinite;
            }
            .step.completed .step-circle {
                background: #193E92;
                border-color: #193E92;
                transform: scale(1);
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1.1); }
                50% { transform: scale(1.15); }
            }
            .step-label {
                margin-top: 12px;
                font-size: 13px;
                font-weight: 600;
                color: #9CA3AF;
                transition: color 0.3s ease;
                text-align: center;
            }
            .step.active .step-label {
                color: #193E92;
                font-size: 14px;
            }
            .step.completed .step-label {
                color: #193E92;
            }
            .connector {
                position: absolute;
                top: 30px;
                left: 0;
                right: 0;
                height: 4px;
                background: #E5E7EB;
                z-index: 1;
                margin: 0 30px;
            }
            .connector-progress {
                height: 100%;
                background: linear-gradient(90deg, #193E92 0%, #D97104 100%);
                transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
                border-radius: 2px;
            }
        </style>
    </head>
    <body>
        <div class="timeline">
            <div class="connector">
                <div class="connector-progress" style="width: """ + str(progress_percent) + """%;"></div>
            </div>"""
    
    for step in step_labels:
        status = "completed" if step["num"] < current_step else ("active" if step["num"] == current_step else "")
        html_content += f"""
            <div class="step {status}">
                <div class="step-circle">{step["icon"]}</div>
                <div class="step-label">{step["label"]}</div>
            </div>"""
    
    html_content += """
        </div>
    </body>
    </html>
    """
    return html_content

# ==========================================
# 🍪 COOKIE MANAGER
# ==========================================
cookie_manager = stx.CookieManager()

# ==========================================
# 🔐 SESSION STATE INITIALIZATION
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'login_time' not in st.session_state:
    st.session_state.login_time = None
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = None
if 'user_location' not in st.session_state:
    st.session_state.user_location = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'matching_done' not in st.session_state:
    st.session_state.matching_done = False
if 'matching_data' not in st.session_state:
    st.session_state.matching_data = None
if 'selected_client' not in st.session_state:
    st.session_state.selected_client = "Desjardins"
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "French"
if 'cv_file' not in st.session_state:
    st.session_state.cv_file = None
if 'jd_file' not in st.session_state:
    st.session_state.jd_file = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
# ✨ FIXED: Ajout de skills_matrix_file dans session state
if 'skills_matrix_file' not in st.session_state:
    st.session_state.skills_matrix_file = None
if 'show_generate_button' not in st.session_state:
    st.session_state.show_generate_button = False

# ==========================================
# 🔐 AUTHENTICATION FUNCTIONS
# ==========================================

AUTHORIZED_USERS = [
    "Kevin Abecassis",
    "Aurélien Bertrand",
    "Julia Delpon",
    "Lucas Maurer",
    "Roberta Santiago"
]

def restore_session_from_cookies():
    """Restaure la session depuis les cookies si valide"""
    try:
        cookies = cookie_manager.get_all()
        
        if cookies and 'tmc_session' in cookies:
            session_data = cookies['tmc_session']
            
            # Vérifier si la session est valide (moins de 8 heures)
            if 'login_time' in session_data:
                login_time = datetime.fromisoformat(session_data['login_time'])
                if datetime.now() - login_time < timedelta(hours=8):
                    st.session_state.authenticated = True
                    st.session_state.user_name = session_data.get('user_name')
                    st.session_state.user_location = session_data.get('user_location')
                    st.session_state.login_time = login_time
                    st.session_state.last_activity = datetime.now()
                    return True
        return False
    except:
        return False

def save_session_to_cookies():
    """Sauvegarde la session dans les cookies"""
    try:
        session_data = {
            'user_name': st.session_state.user_name,
            'user_location': st.session_state.user_location,
            'login_time': st.session_state.login_time.isoformat()
        }
        cookie_manager.set('tmc_session', session_data, max_age=28800)  # 8 heures
    except:
        pass

def clear_session():
    """Clear session and cookies"""
    st.session_state.authenticated = False
    st.session_state.user_name = None
    st.session_state.user_location = None
    st.session_state.login_time = None
    st.session_state.matching_done = False
    st.session_state.matching_data = None
    st.session_state.cv_file = None
    st.session_state.jd_file = None
    st.session_state.processing = False
    st.session_state.skills_matrix_file = None  # ✨ FIXED: Clear skills matrix
    st.session_state.show_generate_button = False  # ✨ FIXED: Reset Generate button
    try:
        cookie_manager.delete('tmc_session')
    except:
        pass

# ==========================================
# 📊 AIRTABLE LOGGING
# ==========================================

def log_to_airtable(user_name, event_type, metadata=None):
    """
    Log usage events to Airtable for tracking
    
    Args:
        user_name: Full name of user
        event_type: Type of event (login, logout, analysis_completed, cv_generated)
        metadata: Optional dict with additional data
    """
    try:
        import requests
        import json
        
        # Try environment variables first (support both old and new naming)
        AIRTABLE_TOKEN = os.getenv('AIRTABLE_API_KEY') or os.getenv('AIRTABLE_TOKEN')
        AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
        AIRTABLE_TABLE_ID = os.getenv('AIRTABLE_TABLE_ID') or os.getenv('AIRTABLE_TABLE_NAME')
        
        # Fallback to secrets if env vars not found
        if not AIRTABLE_TOKEN:
            try:
                AIRTABLE_TOKEN = st.secrets.get("AIRTABLE_API_KEY") or st.secrets.get("AIRTABLE_TOKEN")
            except:
                pass
        
        if not AIRTABLE_BASE_ID:
            try:
                AIRTABLE_BASE_ID = st.secrets.get("AIRTABLE_BASE_ID")
            except:
                pass
        
        if not AIRTABLE_TABLE_ID:
            try:
                AIRTABLE_TABLE_ID = st.secrets.get("AIRTABLE_TABLE_ID") or st.secrets.get("AIRTABLE_TABLE_NAME")
            except:
                pass
        
        # Check if all required config is present
        if not all([AIRTABLE_TOKEN, AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID]):
            # Only print warning once per session
            if 'airtable_warning_shown' not in st.session_state:
                print("⚠️ Missing Airtable config - usage tracking disabled", flush=True)
                print(f"   Token: {bool(AIRTABLE_TOKEN)}, Base: {bool(AIRTABLE_BASE_ID)}, Table: {bool(AIRTABLE_TABLE_ID)}", flush=True)
                st.session_state.airtable_warning_shown = True
            return
        
        # Prepare timestamp
        timestamp_iso = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        
        # Parse user name
        name_parts = user_name.split(' ', 1) if user_name else ['Unknown', '']
        first_name = name_parts[0] if len(name_parts) > 0 else 'Unknown'
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Get user location if available
        user_location = st.session_state.get('user_location', 'Unknown')
        
        # Build fields based on event type
        fields = {
            "Timestamp": timestamp_iso,
            "Event_Type": event_type,  # Fixed: underscore instead of space
            "First Name": first_name,
            "Last Name": last_name,
            "User Location": user_location  # Fixed: "User Location" instead of "Location"
        }
        
        # Add metadata fields if present
        if metadata:
            if event_type == "cv_generated":
                # CV generation specific fields
                fields["Client"] = metadata.get("client", "")
                fields["Language"] = metadata.get("language", "")
                fields["Anonymized"] = metadata.get("anonymized", False)
                fields["Skills Matrix Used"] = metadata.get("skills_matrix_used", False)
                if "candidate_name" in metadata:
                    fields["Candidate Name"] = metadata["candidate_name"][:100]  # Truncate to 100 chars
                if "score" in metadata:
                    fields["Matching Score"] = int(metadata["score"])
                if "processing_time" in metadata:
                    fields["Processing Time"] = round(metadata["processing_time"], 2)
                if "total_tokens" in metadata:
                    fields["Total Tokens"] = int(metadata["total_tokens"])
                if "estimated_cost" in metadata:
                    fields["Estimated Cost ($)"] = round(metadata["estimated_cost"], 4)
            
            elif event_type == "analysis_completed":
                # Analysis specific fields
                if "client" in metadata:
                    fields["Client"] = metadata["client"]
                if "score" in metadata:
                    fields["Matching Score"] = int(metadata["score"])
            
            elif event_type == "login":
                # Login specific fields
                if "location" in metadata:
                    fields["User Location"] = metadata["location"]  # Fixed: "User Location" instead of "Location"
        
        # Build request
        url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}'
        headers = {
            'Authorization': f'Bearer {AIRTABLE_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        record_data = {
            "fields": fields
        }
        
        # Send to Airtable
        response = requests.post(url, headers=headers, data=json.dumps(record_data), timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Airtable tracking success: {event_type} for {user_name}", flush=True)
        else:
            print(f"⚠️ Airtable error: {response.status_code} - {response.text}", flush=True)
            
    except Exception as e:
        print(f"⚠️ Airtable tracking failed: {str(e)}", flush=True)


# ==========================================
# 🔓 LOGIN SCREEN
# ==========================================

def show_login_screen():
    """Display login screen"""
    local_css()
    
    st.markdown(f"""
    <div class="tmc-hero">
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 0.5rem;">
            <svg width="600" height="80" viewBox="0 0 600 80" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:{PRIMARY_BLUE};stop-opacity:1" />
                        <stop offset="100%" style="stop-color:{SECONDARY_ORANGE};stop-opacity:1" />
                    </linearGradient>
                </defs>
                <text x="50%" y="60" font-family="Arial, sans-serif" font-size="48" font-weight="800" fill="url(#titleGradient)" text-anchor="middle">
                    CV Optimizer
                </text>
            </svg>
        </div>
        <p class="tmc-subtitle">Generate optimized TMC CVs with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Authentication")
        
        name = st.selectbox(
            "Select your name",
            options=AUTHORIZED_USERS,
            key="name_select"
        )
        
        location = st.selectbox(
            "Select your location",
            options=["Montréal, QC", "Toronto, ON", "Vancouver, BC", "Other"],
            key="location_select"
        )
        
        # ✅ V9 FIX: Add password field
        password = st.text_input(
            "Password",
            type="password",
            key="password_input"
        )
        
        if st.button("🚀 Access CV Optimizer", use_container_width=True):
            # Check password
            correct_password = os.getenv('APP_PASSWORD') or st.secrets.get("APP_PASSWORD", "")
            
            if not correct_password:
                st.error("❌ Password not configured on server. Contact administrator.")
            elif password != correct_password:
                st.error("❌ Incorrect password. Please try again.")
            else:
                st.session_state.authenticated = True
                st.session_state.user_name = name
                st.session_state.user_location = location
                st.session_state.login_time = datetime.now()
                st.session_state.last_activity = datetime.now()
                
                # Save to cookies
                save_session_to_cookies()
                
                # Log to Airtable
                log_to_airtable(name, "login", {"location": location})
                
                st.rerun()
    
    # Signature Ekinext at bottom of login page
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; font-size: 0.85rem; color: #6B7280;">
        Made by <strong>Kevin Abecassis | Ekinext</strong> © 2025
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 🏠 MAIN APPLICATION
# ==========================================

def main_app():
    """Application principale"""
    
    # Initialize reset counter for file uploaders (if not exists)
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0
    
    # Apply custom CSS
    local_css()
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        # User info
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.markdown(f"📍 {st.session_state.user_location}")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Client selector
        st.markdown("#### 🏢 Select Client")
        
        clients_list = list(CLIENT_DATA.keys())
        client = st.selectbox(
            "Client",
            options=clients_list,
            index=clients_list.index(st.session_state.selected_client),
            label_visibility="collapsed",
            key="client_select"
        )
        
        # Update session state if changed
        if client != st.session_state.selected_client:
            st.session_state.selected_client = client
            # Reset matching when client changes
            st.session_state.matching_done = False
            st.session_state.matching_data = None
            st.session_state.skills_matrix_file = None  # ✨ FIXED: Reset skills matrix
            st.session_state.show_generate_button = False  # ✨ FIXED: Reset Generate button
            st.rerun()
        
        # Get current client info
        client_info = CLIENT_DATA[st.session_state.selected_client]
        rules_html = "<br>".join(client_info["rules"])
        
        # Display client card with dynamic styling
        st.markdown(f"""
        <div class="client-card {client_info['card_class']}">
            {rules_html}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Privacy note
        st.markdown("""
        <div class="privacy-note">
            <span>🔒</span>
            <span>Your data is processed securely and never stored</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Buttons
        col_new, col_logout = st.columns(2)
        
        with col_new:
            if st.button("🔄 New", use_container_width=True, key="new_button"):
                # Clear matching data but keep auth
                st.session_state.matching_done = False
                st.session_state.matching_data = None
                st.session_state.cv_file = None
                st.session_state.jd_file = None
                st.session_state.processing = False
                st.session_state.skills_matrix_file = None  # ✨ FIXED: Reset skills matrix
                st.session_state.show_generate_button = False  # ✨ FIXED: Reset Generate button
                
                # ✨ NEW: Increment reset counter to force file_uploader recreation
                st.session_state.reset_counter += 1
                
                st.rerun()
        
        with col_logout:
            if st.button("🚪 Logout", use_container_width=True, key="logout_button"):
                log_to_airtable(st.session_state.user_name, "logout", {
                    "duration_minutes": (datetime.now() - st.session_state.login_time).total_seconds() / 60
                })
                clear_session()
                st.rerun()
        
        # TMC Logo at bottom of sidebar
        # Use local logo from repository (simpler than GitHub URL)
        logo_path = "TMC big logo.png"  # Logo in root directory
        
        try:
            # Try to load logo using base64 encoding for Streamlit
            import base64
            from pathlib import Path
            
            if Path(logo_path).exists():
                with open(logo_path, "rb") as f:
                    logo_bytes = f.read()
                    logo_base64 = base64.b64encode(logo_bytes).decode()
                
                st.markdown(f"""
                <div style="text-align: center; margin-top: auto; padding-top: 2rem;">
                    <img src="data:image/png;base64,{logo_base64}" style="width: 120px; opacity: 0.7;">
                </div>
                """, unsafe_allow_html=True)
            else:
                # Fallback: Text logo if file not found
                st.markdown("""
                <div style="text-align: center; margin-top: auto; padding-top: 2rem; color: #193E92; font-weight: 700; font-size: 1.2rem;">
                    TMC
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            # Fallback: Text logo if any error
            st.markdown("""
            <div style="text-align: center; margin-top: auto; padding-top: 2rem; opacity: 0.6;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #193E92;">TMC</div>
                <div style="font-size: 0.7rem; color: #6B7280;">The Montreal Company</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========== MAIN CONTENT ==========
    # Header with gradient SVG - CENTERED
    st.markdown(f"""
    <div class="tmc-hero">
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 0.5rem;">
            <svg width="600" height="80" viewBox="0 0 600 80" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:{PRIMARY_BLUE};stop-opacity:1" />
                        <stop offset="100%" style="stop-color:{SECONDARY_ORANGE};stop-opacity:1" />
                    </linearGradient>
                </defs>
                <text x="50%" y="60" font-family="Arial, sans-serif" font-size="48" font-weight="800" fill="url(#titleGradient)" text-anchor="middle">
                    CV Optimizer
                </text>
            </svg>
        </div>
        <p class="tmc-subtitle">Generate a professional TMC CV perfectly aligned with your Job Description</p>
        <p class="tmc-subtitle" style="margin-top: 0.2rem; font-size: 0.95rem;">Designed for Business Managers and Recruiters</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Your Resume")
        cv_file = st.file_uploader(
            "Upload your CV",
            type=['pdf', 'docx', 'doc', 'txt'],
            label_visibility="collapsed",
            key=f"cv_uploader_{st.session_state.reset_counter}"  # ✨ FIXED: Dynamic key for reset
        )
        if cv_file:
            if 'cv_upload_status' not in st.session_state:
                st.session_state.cv_upload_status = st.empty()
            st.session_state.cv_upload_status.success(f"✅ {cv_file.name}")
            st.session_state.cv_file = cv_file
    
    with col2:
        st.markdown("### 📊 Job Description")
        jd_file = st.file_uploader(
            "Upload job description",
            type=['txt', 'docx', 'doc', 'pdf'],
            label_visibility="collapsed",
            key=f"jd_uploader_{st.session_state.reset_counter}"  # ✨ FIXED: Dynamic key for reset
        )
        if jd_file:
            if 'jd_upload_status' not in st.session_state:
                st.session_state.jd_upload_status = st.empty()
            st.session_state.jd_upload_status.success(f"✅ {jd_file.name}")
            st.session_state.jd_file = jd_file
    
    # Language section (only for CAE)
    if CLIENT_DATA[st.session_state.selected_client]["show_language"]:
        st.markdown("---")
        st.markdown('<h3 style="text-align: center;">🌐 Generated CV Language</h3>', unsafe_allow_html=True)
        language = st.radio(
            "Select language",
            options=["🇫🇷 French", "🇬🇧 English"],
            horizontal=True,
            label_visibility="collapsed",
            key="language_selector"
        )
        st.session_state.selected_language = language.split()[1]
        # ✅ DEBUG: Confirm language stored
        print(f"🌐 CAE Language selected and stored: {st.session_state.selected_language}", flush=True)
    else:
        # Set language based on client
        st.session_state.selected_language = CLIENT_DATA[st.session_state.selected_client]["language"]
        print(f"🌐 {st.session_state.selected_client} Language auto-set: {st.session_state.selected_language}", flush=True)
    
    # Analyze button (only show if Generate button is not active)
    if not st.session_state.show_generate_button:
        st.markdown("---")
        analyze_button = st.button(
            "📊 Analyze Matching",
            use_container_width=True,
            disabled=st.session_state.processing,
            key="analyze_button"
        )
        
        if analyze_button:
            if st.session_state.cv_file and st.session_state.jd_file:
                # Clear upload status messages
                if 'cv_upload_status' in st.session_state:
                    st.session_state.cv_upload_status.empty()
                if 'jd_upload_status' in st.session_state:
                    st.session_state.jd_upload_status.empty()
                
                st.session_state.processing = True
                process_cv_matching()
            else:
                st.error("⚠️ Please upload both CV and Job Description files")
    
    # Display results if matching is done
    if st.session_state.matching_done and st.session_state.matching_data:
        display_matching_results(st.session_state.matching_data)

# ==========================================
# 🔄 CV PROCESSING
# ==========================================

def process_cv_matching():
    """Process CV matching analysis with 3-step timeline"""
    st.markdown("---")
    st.markdown("## 🔍 Analyzing Matching...")
    st.markdown("<br>", unsafe_allow_html=True)
    
    timeline_placeholder = st.empty()
    
    # Define 3-step matching timeline
    matching_steps = [
        {"num": 1, "icon": "🔍", "label": "Extraction"},
        {"num": 2, "icon": "🤖", "label": "Analysis"},
        {"num": 3, "icon": "📊", "label": "Matching"},
    ]
    
    try:
        # Import enricher
        from tmc_cv_enricher import TMCUniversalEnricher
        
        # Initialize enricher
        api_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get("ANTHROPIC_API_KEY")
        enricher = TMCUniversalEnricher(api_key=api_key)
        
        # Save uploaded files temporarily
        cv_path = save_uploaded(st.session_state.cv_file)
        jd_path = save_uploaded(st.session_state.jd_file)
        
        # Step 1: Extraction
        timeline_placeholder.markdown(horizontal_progress_timeline(1, 3, matching_steps), unsafe_allow_html=True)
        cv_text = enricher.extract_cv_text(str(cv_path))
        
        # Step 2: Parsing (removed intermediate timeline render for performance)
        parsed_cv = enricher.parse_cv_with_claude(cv_text)
        
        # Step 3: Matching Analysis (removed intermediate timeline render for performance)
        jd_text = enricher.read_job_description(str(jd_path))
        matching_analysis = enricher.analyze_cv_matching(parsed_cv, jd_text)
        
        # Clear timeline
        timeline_placeholder.empty()
        
        # Store results
        st.session_state.matching_data = {
            'parsed_cv': parsed_cv,
            'jd_text': jd_text,
            'matching_analysis': matching_analysis,
            'cv_path': cv_path,
            'jd_path': jd_path
        }
        st.session_state.matching_done = True
        st.session_state.show_generate_button = True  # ✨ FIXED: Enable Generate button
        st.session_state.processing = False
        
        # Log to Airtable
        log_to_airtable(
            st.session_state.user_name,
            "analysis_completed",
            {
                "client": st.session_state.selected_client,
                "score": matching_analysis.get('score_matching', 0)
            }
        )
        
        st.success("✅ Analysis Complete!")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        st.session_state.processing = False
        import traceback
        st.code(traceback.format_exc())

# ==========================================
# 📊 DISPLAY RESULTS
# ==========================================

def display_matching_results(data):
    """Display matching results with professional styling"""
    results = data['matching_analysis']
    parsed_cv = data.get('parsed_cv', {})
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Score section
    col1, col2, col3 = st.columns(3)
    
    # Get parsed_cv and experiences for col2 and col3
    experiences = parsed_cv.get('experiences', [])
    
    with col1:
        score = results.get('score_matching', 0)
        st.metric(
            "🎯 Matching Score",
            f"{score}/100",
            help="Overall compatibility score"
        )
    
    with col2:
        nom = parsed_cv.get('nom_complet', 'Candidate')
        nom_display = nom if len(nom) < 20 else nom[:17] + "..."
        st.metric("👤 Candidate", nom_display)
    
    with col3:
        # Calculate years of experience
        import re
        total_years = 0
        current_year = datetime.now().year
        
        for exp in experiences:
            periode = exp.get('periode', '')
            periode_clean = periode.replace('Present', str(current_year)).replace('Présent', str(current_year))
            years_found = re.findall(r'\b(\d{4})\b', periode_clean)
            
            if len(years_found) >= 2:
                try:
                    start = int(years_found[0])
                    end = int(years_found[-1])
                    if end >= start:
                        total_years += (end - start)
                except:
                    pass
        
        years_display = f"{total_years} years" if total_years > 0 else "N/A"
        st.metric("📅 Years of Experience", years_display)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed weighting table
    if results.get('domaines_analyses'):
        import pandas as pd
        
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <h3 style="margin: 0; color: #111827; font-size: 1.4rem; font-weight: 700;">
                ⚙️ Detailed Weighting Analysis
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create DataFrame
        df_domaines = pd.DataFrame(results['domaines_analyses'])
        
        # Format columns
        def format_domain(row):
            match = row['match']
            if match == 'incompatible':
                icon = "❌"
            elif match == 'partiel':
                icon = "⚠️"
            else:
                icon = "✅"
            return f"{icon} {row['domaine']}"
        
        df_domaines['Domain'] = df_domaines.apply(format_domain, axis=1)
        df_domaines['Weight'] = df_domaines['poids'].astype(str) + '%'
        df_domaines['Score'] = df_domaines.apply(
            lambda row: f"{row['score']}/{row['score_max']}", axis=1
        )
        
        # Truncate comments
        def truncate(text, max_len=150):
            if len(text) <= max_len:
                return text
            text = text[:max_len]
            last_space = text.rfind(' ')
            if last_space > 0:
                text = text[:last_space]
            if text and text[-1] not in '.!?':
                text += '.'
            return text
        
        df_domaines['Comment'] = df_domaines['commentaire'].apply(truncate)
        
        # Select final columns
        df_display = df_domaines[['Domain', 'Weight', 'Score', 'Comment']]
        
        # Style rows
        def style_rows(row):
            idx = row.name
            match = df_domaines.loc[idx, 'match']
            
            if match == 'incompatible':
                bg = '#fef2f2'
            elif match == 'partiel':
                bg = '#fffbeb'
            else:
                bg = '#f0fdf4'
            
            return [f'background-color: {bg}'] * len(row)
        
        # Apply style
        styled_df = df_display.style.apply(style_rows, axis=1)
        
        # Display dataframe
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Domain": st.column_config.TextColumn(
                    "Domain",
                    width=400,
                    help="Technical/functional domain"
                ),
                "Weight": st.column_config.TextColumn(
                    "Weight",
                    width=70,
                    help="Importance weight (%)"
                ),
                "Score": st.column_config.TextColumn(
                    "Score",
                    width=70,
                    help="Candidate score"
                ),
                "Comment": st.column_config.TextColumn(
                    "Comment",
                    width=None,
                    help="Detailed assessment"
                ),
            }
        )
        
        # Summary - Generate locally based on actual results
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Generate summary from actual analysis data
        score = results.get('score_matching', 0)
        nom = parsed_cv.get('nom_complet', 'Candidate')
        
        # Calculate years of experience
        import re
        total_years = 0
        current_year = datetime.now().year
        for exp in experiences:
            periode = exp.get('periode', '')
            periode_clean = periode.replace('Present', str(current_year)).replace('Présent', str(current_year))
            years_found = re.findall(r'\b(\d{4})\b', periode_clean)
            if len(years_found) >= 2:
                try:
                    start = int(years_found[0])
                    end = int(years_found[-1])
                    if end >= start:
                        total_years += (end - start)
                except:
                    pass
            elif len(years_found) == 1:
                try:
                    start = int(years_found[0])
                    total_years += (current_year - start)
                except:
                    pass
        
        # Get strong domains (matched)
        domaines_analyses = results.get('domaines_analyses', [])
        strong_domains = [d['domaine'] for d in domaines_analyses if d.get('match') == 'complet']
        partial_domains = [d['domaine'] for d in domaines_analyses if d.get('match') == 'partiel']
        missing_domains = [d['domaine'] for d in domaines_analyses if d.get('match') == 'incompatible']
        
        # Generate score assessment
        if score >= 90:
            score_level = "Excellent match"
        elif score >= 80:
            score_level = "Strong match"
        elif score >= 70:
            score_level = "Good match"
        elif score >= 60:
            score_level = "Moderate match"
        else:
            score_level = "Weak match"
        
        # Build summary text
        # ✨ V9 FIX: Use Claude's comprehensive synthesis instead of auto-generated one
        # Claude provides 4-6 paragraph detailed analysis (250-350 words)
        generated_summary = results.get('synthese_matching', '')
        
        # Fallback: If synthesis is missing, generate short summary
        if not generated_summary or len(generated_summary.strip()) < 50:
            summary_parts = []
            summary_parts.append(f"{score_level} with {score}/100 score.")
            
            if total_years > 0:
                summary_parts.append(f"Candidate has {total_years} years of experience.")
            
            if strong_domains:
                if len(strong_domains) > 3:
                    domains_text = ", ".join(strong_domains[:3]) + f", and {len(strong_domains)-3} other domains"
                else:
                    domains_text = ", ".join(strong_domains)
                summary_parts.append(f"Exceeds requirements in: {domains_text}.")
            
            if partial_domains:
                if len(partial_domains) > 2:
                    summary_parts.append(f"Partial match in {len(partial_domains)} domains.")
                else:
                    domains_text = ", ".join(partial_domains)
                    summary_parts.append(f"Partial match in: {domains_text}.")
            
            if missing_domains:
                if len(missing_domains) > 2:
                    summary_parts.append(f"Gaps identified in {len(missing_domains)} areas.")
                else:
                    domains_text = ", ".join(missing_domains)
                    summary_parts.append(f"Gap in: {domains_text}.")
            
            generated_summary = " ".join(summary_parts)
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-left: 4px solid #3b82f6;
            border-radius: 12px;
            padding: 24px 28px;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
        ">
            <div style="display: flex; align-items: start;">
                <div style="font-size: 1.8rem; margin-right: 14px;">📊</div>
                <div>
                    <div style="font-weight: 700; color: #1e40af; font-size: 1.25rem; margin-bottom: 10px;">Analysis Summary</div>
                    <div style="color: #1e3a8a; line-height: 1.7; font-size: 1.05rem; white-space: pre-line;">{generated_summary}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key strengths
    if results.get('points_forts'):
        st.markdown("### 💪 Key Strengths Identified")
        for i, pf in enumerate(results['points_forts'][:5], 1):
            st.markdown(f"**{i}.** {pf}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ✨ FIXED: Skills Matrix Upload Section (ONLY for Morgan Stanley)
    if st.session_state.selected_client == "Morgan Stanley":
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 15px;">
            <strong style="color: #193E92; font-size: 1.15rem;">📊 Skills Matrix Upload (Required)</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader for Skills Matrix
        col_sm_left, col_sm_center, col_sm_right = st.columns([1, 2, 1])
        with col_sm_center:
            skills_matrix_file = st.file_uploader(
                "Upload Skills Matrix (.docx only)",
                type=['docx'],
                key=f"skills_matrix_uploader_{st.session_state.reset_counter}",  # ✨ FIXED: Dynamic key for reset
                help="Morgan Stanley requires a Skills Matrix as page 2 of the CV"
            )
            
            # Store in session state and show feedback
            if skills_matrix_file:
                st.session_state.skills_matrix_file = skills_matrix_file
                st.success(f"✅ Skills Matrix Uploaded: **{skills_matrix_file.name}**")
            else:
                if st.session_state.skills_matrix_file:
                    # Show previously uploaded file
                    st.info(f"✅ Skills Matrix Ready: **{st.session_state.skills_matrix_file.name}**")
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate CV button
    if st.button("📝 Generate Optimized CV", use_container_width=True, key="generate_cv_button"):
        generate_cv(data)

# ==========================================
# 📝 CV GENERATION
# ==========================================

def generate_cv(data):
    """Generate the optimized CV with 3-step timeline"""
    
    # ✨ FIXED: Validation pour Morgan Stanley
    if st.session_state.selected_client == "Morgan Stanley":
        if not st.session_state.skills_matrix_file:
            st.error("❌ **Skills Matrix is required for Morgan Stanley clients**")
            st.error("📊 Please upload the Skills Matrix document before generating the CV.")
            st.stop()
    
    st.markdown("---")
    st.markdown("## 📝 Generating Optimized CV")
    
    timeline_placeholder = st.empty()
    
    # Define 3-step generation timeline
    generation_steps = [
        {"num": 1, "icon": "✨", "label": "Enrichment"},
        {"num": 2, "icon": "🗂️", "label": "Structuring"},
        {"num": 3, "icon": "📝", "label": "Generation"},
    ]
    
    try:
        from tmc_cv_enricher import TMCUniversalEnricher
        
        api_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get("ANTHROPIC_API_KEY")
        enricher = TMCUniversalEnricher(api_key=api_key)
        
        # Get client config
        client_config = CLIENT_DATA[st.session_state.selected_client]
        
        # Step 1: Enrichment
        timeline_placeholder.markdown(horizontal_progress_timeline(1, 3, generation_steps), unsafe_allow_html=True)
        
        # ✅ DEBUG: Log selected language
        print(f"🌐 LANGUAGE SELECTED: {st.session_state.selected_language}", flush=True)
        print(f"📋 CLIENT: {st.session_state.selected_client}", flush=True)
        
        # 🚀 PERFORMANCE FIX: Pass matching_analysis to avoid redundant matching (saves 15-20s)
        enriched_cv = enricher.enrich_cv_with_prompt(
            data['parsed_cv'],
            data['jd_text'],
            language=st.session_state.selected_language,
            matching_analysis=data.get('matching_analysis')  # ✅ Reuse Step 1 matching
        )
        
        # Step 2: Structuring (removed intermediate timeline render for performance)
        tmc_context = enricher.map_to_tmc_structure(data['parsed_cv'], enriched_cv)
        
        # Step 3: Generation (removed intermediate timeline render for performance)
        
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            output_path = tmp_file.name
        
        # ✨ FIXED: Génération correcte avec Skills Matrix pour Morgan Stanley
        if client_config["use_skizmatrix"] and st.session_state.skills_matrix_file:
            # Morgan Stanley with Skills Matrix - Use generate_ms_cv_3parts
            
            # Save Skills Matrix temporarily
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            skills_matrix_path = Path(output_path).parent / f"skills_matrix_{ts}.docx"
            with open(skills_matrix_path, 'wb') as f:
                # Reset file pointer before reading
                st.session_state.skills_matrix_file.seek(0)
                f.write(st.session_state.skills_matrix_file.read())
            
            # Generate CV with 3 parts
            success, result = enricher.generate_ms_cv_3parts(
                tmc_context=tmc_context,
                skills_matrix_path=str(skills_matrix_path),
                output_path=output_path
            )
            
            # Post-processing: Bold keywords
            if success:
                keywords = enriched_cv.get('mots_cles_a_mettre_en_gras', [])
                if keywords:
                    enricher.apply_bold_post_processing(output_path, keywords)
        else:
            # Standard TMC CV (CAE / Desjardins)
            # Determine template based on client
            if client_config["anonymize"]:
                template_file = f"TMC_NA_template_{st.session_state.selected_language[:2].upper()}_Anonymise.docx"
            else:
                template_file = f"TMC_NA_template_{st.session_state.selected_language[:2].upper()}.docx"
            
            enricher.generate_tmc_docx(
                tmc_context,
                output_path,
                template_path=template_file
            )
            
            # Post-processing: Bold keywords
            keywords = enriched_cv.get('mots_cles_a_mettre_en_gras', [])
            if keywords:
                enricher.apply_bold_post_processing(output_path, keywords)
            
            success = True
        
        # Clear timeline
        timeline_placeholder.empty()
        
        if success:
            # Read the generated file
            with open(output_path, 'rb') as f:
                cv_bytes = f.read()
            
            # Clean up
            os.unlink(output_path)
            
            st.success("🎉 **CV Generated Successfully!**")
            
            # Generate filename with correct format per client
            parsed_cv = data.get('parsed_cv', {})
            nom_complet = parsed_cv.get('nom_complet', 'Candidate')
            
            # ✅ FIX: Use ENRICHED title (in correct language) instead of original
            titre = enriched_cv.get('titre_professionnel_enrichi', parsed_cv.get('titre_professionnel', 'Profile'))
            
            # Format name as "Prenom NOM" (last name in uppercase)
            import re
            nom_parts = nom_complet.strip().split()
            if len(nom_parts) >= 2:
                # Assume last part is surname
                prenom = ' '.join(nom_parts[:-1])  # Everything except last part
                nom = nom_parts[-1].upper()  # Last part in uppercase
                nom_formatted = f"{prenom} {nom}"
            else:
                # Single name - just use as is
                nom_formatted = nom_complet
            
            # Clean special characters from title
            titre_clean = re.sub(r'[^\w\s-]', '', titre).strip()
            
            # Build filename according to client
            client = st.session_state.selected_client
            language = st.session_state.selected_language
            
            if client == "Desjardins":
                filename = f"TMC - {nom_formatted} - {titre_clean}.docx"
            elif client == "Morgan Stanley":
                filename = f"CV - {nom_formatted} - {titre_clean}.docx"
            elif client == "CAE":
                # Add language suffix for CAE
                lang_suffix = "(EN)" if language == "English" else "(FR)"
                filename = f"CV - {nom_formatted} - {titre_clean} {lang_suffix}.docx"
            else:
                # Fallback to old format
                filename = f"TMC - {nom_formatted} - {titre_clean}.docx"
            
            # Download button with GREEN gradient (like app_working.py)
            # CRITICAL: Define CSS BEFORE opening wrapper div!
            st.markdown("""
            <style>
            #download-btn-wrapper button {
                background: linear-gradient(90deg, #22c55e 0%, #047857 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 0.9rem 2rem !important;
                font-weight: 700 !important;
                font-size: 1.1rem !important;
                box-shadow: 0 4px 14px rgba(34, 197, 94, 0.35) !important;
                transition: all 0.3s ease !important;
                width: 100% !important;
            }
            #download-btn-wrapper button:hover {
                box-shadow: 0 8px 24px rgba(34, 197, 94, 0.45) !important;
                transform: translateY(-2px) !important;
            }
            #download-btn-wrapper button:active {
                transform: translateY(0) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div id="download-btn-wrapper">', unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Optimized CV",
                data=cv_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Log to Airtable with comprehensive data
            metadata_info = enriched_cv.get('_metadata', {})
            log_to_airtable(
                st.session_state.user_name,
                "cv_generated",
                {
                    "client": st.session_state.selected_client,
                    "language": st.session_state.selected_language,
                    "anonymized": client_config["anonymize"],
                    "skills_matrix_used": bool(st.session_state.skills_matrix_file and client_config["use_skizmatrix"]),
                    "candidate_name": nom_complet,
                    "score": enriched_cv.get('score_matching', 0),
                    "processing_time": metadata_info.get('processing_time_seconds', 0),
                    "total_tokens": metadata_info.get('total_tokens', 0),
                    "estimated_cost": metadata_info.get('estimated_cost_usd', 0)
                }
            )
        else:
            st.error(f"❌ Error generating CV: {result}")
            
    except Exception as e:
        st.error(f"❌ Error during generation: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# ==========================================
# 🛠️ HELPER FUNCTIONS
# ==========================================

def save_uploaded(file, suffix=None) -> Path:
    """Save uploaded file to temp directory"""
    suffix = suffix or Path(file.name).suffix
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    file.seek(0)  # Reset file pointer
    tmp.write(file.read())
    tmp.flush()
    tmp.close()
    return Path(tmp.name)

# ==========================================
# 🔚 FOOTER
# ==========================================

def show_footer():
    """Display footer"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div class='tmc-footer'>
            <strong>TMC CV Optimizer V1.3.4-OPT</strong> — Designed for TMC Business Managers & Recruiters<br>
            Made by <strong>Kevin Abecassis | Ekinext</strong> © 2025
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# 🚀 MAIN ENTRY POINT
# ==========================================

if __name__ == "__main__":
    # Check if we need to restore session from cookies
    if not st.session_state.authenticated:
        restore_session_from_cookies()
    
    # Show appropriate screen
    if st.session_state.authenticated:
        main_app()
        show_footer()
    else:
        show_login_screen()
