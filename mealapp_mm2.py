import streamlit as st
import openai
import base64
from PIL import Image
import io
import json
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import hashlib
from datetime import datetime
import os
import time
import pandas as pd

# Enhanced mobile-first Streamlit page configuration
st.set_page_config(
    page_title="AI Meal Identifier", 
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsed by default for mobile
)

# MOBILE-FIRST RESPONSIVE STYLING
def apply_mobile_friendly_styling():
    st.markdown("""
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global mobile-first styling */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: #ffffff;
        background-attachment: fixed;
    }

    /* Mobile-optimized main header */
    .modern-main-header {
        text-align: center;
        background: linear-gradient(135deg, rgba(99, 179, 237, 0.8), rgba(155, 81, 224, 0.8));




        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 2rem 1rem;
        color: #1e293b;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2), 
                    0 4px 16px rgba(0, 0, 0, 0.1), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.6);
        position: relative;
        overflow: hidden;
        animation: slideInDown 1s ease-out;
    }

    .modern-main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        border-radius: 20px 20px 0 0;
    }

    .modern-main-header h1 {
        margin: 0;
        font-size: clamp(1.8rem, 4vw, 3.2rem);
        font-weight: 800;
        color: #1e293b !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        letter-spacing: -1px;
        line-height: 1.2;
    }

    .modern-main-header p {
        margin: 1rem 0 0 0;
        font-size: clamp(0.9rem, 2.5vw, 1.2rem);
        color: #64748b !important;
        font-weight: 500;
    }

    /* Mobile-optimized floating cards */
    .floating-card {
        background: linear-gradient(135deg, rgba(244, 114, 182, 0.8), rgba(236, 72, 153, 0.8));

        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        border: 1px solid transparent !important;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        position: relative;
        overflow: hidden;
        margin-bottom: 1rem;
    }


    /* Mobile-optimized metric cards */
    .modern-metric-card {
        background: rgba(248, 250, 252, 0.9) !important;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(203, 213, 225, 0.8) !important;
        border-radius: 15px;
        padding: 1.5rem 1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: bounceIn 0.8s ease-out;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        margin-bottom: 1rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }



    .metric-value-modern {
        font-size: clamp(1.8rem, 5vw, 2.8rem);
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        color: #1e293b !important;
        line-height: 1;
        animation: countUp 1.5s ease-out;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .metric-label-modern {
        font-size: clamp(0.7rem, 2vw, 0.85rem);
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin: 0;
    }

    /* Mobile-optimized section headers */
    .modern-section-header {
        font-size: clamp(1.3rem, 4vw, 1.8rem);
        font-weight: 700;
        color: #1e293b !important;
        margin-bottom: 1.5rem;
        padding: 1rem 1.5rem;
        position: relative;
        text-align: center;
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.5), rgba(59, 130, 246, 0.8));  ###colors additoin for headers    
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(203, 213, 225, 0.6);
        border-radius: 15px;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    /* Mobile-optimized buttons */
    .stButton > button {
        margin-top: 1rem !important;  
        background: linear-gradient(135deg, rgba(251, 140, 150, 0.6), rgba(251, 146, 60, 0.7));


        backdrop-filter: blur(20px) !important;
        color: #1e293b !important;
        border: 1px solid rgba(203, 213, 225, 0.8) !important;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 700 !important;
        font-size: clamp(0.9rem, 2.5vw, 1rem);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            0 4px 16px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100%;
        min-height: 56px;
        touch-action: manipulation;
    }

    .stButton > button:hover, .stButton > button:active {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 12px 48px rgba(102, 126, 234, 0.4),
            0 6px 24px rgba(0, 0, 0, 0.15) !important;
        background: #e6a98a !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        color: #ffffff !important;
    }

    /* Mobile-optimized input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background: rgba(248, 250, 252, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(203, 213, 225, 0.6) !important;
        border-radius: 12px !important;
        color: #1e293b !important;
        font-weight: 500 !important;
        font-size: 16px !important; /* Prevents zoom on iOS */
        min-height: 48px !important; /* Touch-friendly height */
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 
            0 6px 24px rgba(102, 126, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        background: rgba(255, 255, 255, 0.2) !important;
    }

    /* Mobile-optimized file uploader */
    .stFileUploader > div {
        background: rgba(248, 250, 252, 0.8) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 2px dashed rgba(255, 255, 255, 0.4) !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
        min-height: 120px !important;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }

    .stFileUploader > div:hover {
        border-color: rgba(102, 126, 234, 0.6) !important;
        background: rgba(255, 255, 255, 0.18) !important;
        box-shadow: 
            0 12px 48px rgba(102, 126, 234, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    }

    /* Mobile-optimized status badges */
    .modern-status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.6rem 1rem;
        border-radius: 15px;
        font-size: clamp(0.7rem, 2vw, 0.85rem);
        font-weight: 700;
        margin: 0.3rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(203, 213, 225, 0.8);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    .status-high-modern { 
        background: rgba(34, 197, 94, 0.2) !important; 
        color: #065f46 !important; 
        border-color: rgba(34, 197, 94, 0.4) !important;
    }
    .status-medium-modern { 
        background: rgba(251, 191, 36, 0.2) !important; 
        color: #92400e !important; 
        border-color: rgba(251, 191, 36, 0.4) !important;
    }
    .status-low-modern { 
        background: rgba(239, 68, 68, 0.2) !important; 
        color: #991b1b !important; 
        border-color: rgba(239, 68, 68, 0.4) !important;
    }

    /* Mobile-optimized confidence bars */
    .modern-confidence-bar {
        background: rgba(226, 232, 240, 0.15) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        height: 10px;
        border-radius: 10px;
        margin: 1rem 0;
        overflow: hidden;
        position: relative;
        box-shadow: 
            inset 0 2px 4px rgba(0, 0, 0, 0.1),
            0 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .modern-confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #ef4444, #f59e0b, #22c55e) !important;
        border-radius: 10px;
        transition: all 1.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }

    /* Mobile-specific responsive breakpoints */
    @media (max-width: 768px) {
        .stApp > .main .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .modern-main-header {
            padding: 1.5rem 1rem;
            border-radius: 15px;
        }

        .floating-card { 
            padding: 1.25rem; 
            border-radius: 15px;
            margin-bottom: 1rem;
        }

        .modern-metric-card { 
            padding: 1.25rem 0.75rem;
            min-height: 100px;
        }

        .modern-section-header {
            padding: 0.8rem 1rem;
            border-radius: 12px;
        }

        /* Stack columns vertically on mobile */
        .stColumn {
            width: 100% !important;
            flex: none !important;
        }

        /* Adjust spacing for mobile */
        .element-container {
            margin-bottom: 0.5rem !important;
        }
    }

    @media (max-width: 480px) {
        .stApp > .main .block-container {
            padding-top: 0.5rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }

        .modern-main-header {
            padding: 1rem 0.75rem;
            margin-bottom: 1rem;
        }

        .floating-card { 
            padding: 1rem; 
            border-radius: 12px;
        }

        .modern-metric-card { 
            padding: 1rem 0.5rem;
            min-height: 90px;
        }

        .modern-status-badge {
            padding: 0.5rem 0.8rem;
            margin: 0.2rem;
            font-size: 0.7rem;
        }
    }

    /* Touch-friendly interactions */
    @media (hover: none) and (pointer: coarse) {
        .floating-card:hover,
        .modern-metric-card:hover,
        .stButton > button:hover {
            transform: none !important;
        }

        .floating-card:active,
        .modern-metric-card:active {
            transform: scale(0.98) !important;
            transition: transform 0.1s ease !important;
        }
    }

    /* Enhanced loading container for mobile */
    .modern-loading-container {
        text-align: center;
        padding: 3rem 1.5rem;
        background: linear-gradient(135deg, rgba(219, 234, 254, 0.8), rgba(191, 219, 254, 0.8)) !important;

        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(203, 213, 225, 0.6);
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    .modern-loading-spinner {
        width: 50px;
        height: 50px;
        border: 6px solid rgba(102, 126, 234, 0.2);
        border-top: 6px solid rgba(102, 126, 234, 0.8);
        border-radius: 50%;
        animation: modernSpin 1s linear infinite;
        margin: 0 auto 1.5rem auto;
        filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.15));
    }

    /* Enhanced welcome message for mobile */
    .modern-welcome {
        text-align: center;
        padding: 3rem 1.5rem;
        background: rgba(248, 250, 252, 0.8) !important;
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(203, 213, 225, 0.6) !important;
        border-radius: 20px;
        margin: 1.5rem 0;
        animation: pulse 3s infinite;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    .modern-welcome h3 {
        color: #1e293b !important;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        font-size: clamp(1.2rem, 4vw, 1.5rem);
    }

    .modern-welcome p {
        color: #64748b !important;
        font-size: clamp(0.9rem, 2.5vw, 1rem);
        line-height: 1.5;
    }

    .modern-welcome-icon {
        font-size: clamp(3rem, 8vw, 5rem);
        margin-bottom: 1.5rem;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.15));
    }

    /* Mobile-optimized footer */
    .modern-footer {
        text-align: center;
        padding: 2rem 1.5rem;
        background: rgba(248, 250, 252, 0.8) !important;
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(203, 213, 225, 0.6) !important;
        border-radius: 20px;
        margin-top: 2rem;
        color: #1e293b !important;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    .modern-footer h3 {
        color: #1e293b !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        font-size: clamp(1.2rem, 4vw, 1.5rem);
    }

    .modern-footer p {
        color: #64748b !important;
        font-size: clamp(0.8rem, 2.5vw, 1rem);
    }

    /* Enhanced Streamlit expanders for mobile */
    .streamlit-expanderHeader {
        background: rgba(248, 250, 252, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(203, 213, 225, 0.6) !important;
        border-radius: 12px !important;
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: clamp(0.9rem, 2.5vw, 1rem) !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    .streamlit-expanderContent {
        background: rgba(248, 250, 252, 0.8) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(203, 213, 225, 0.6) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    /* Mobile-optimized sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
    }

    .sidebar-header {
        background: rgba(248, 250, 252, 0.9) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(203, 213, 225, 0.6) !important;
        border-radius: 15px;
        padding: 1.5rem 1rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    .sidebar-header h2 {
        font-size: clamp(1.1rem, 3vw, 1.5rem) !important;
    }

    .sidebar-header p {
        font-size: clamp(0.8rem, 2vw, 0.9rem) !important;
    }

    /* Enhanced animations remain the same */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3) translateY(-20px);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    @keyframes modernSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes countUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    /* Hide Streamlit default elements */
    /*#MainMenu {visibility: hidden;}*/                                           #streamlit icons hide
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Mobile-optimized custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.6);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.8);
    }

    /* Enhanced text contrast for mobile */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #1e293b !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    .stMarkdown strong {
        color: #1e293b !important;
        font-weight: 700 !important;
    }

    /* Mobile-friendly focus styles */
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stButton > button:focus {
        outline: 3px solid rgba(102, 126, 234, 0.3) !important;
        outline-offset: 2px !important;
    }

    /* Ensure all text has good contrast and mobile optimization */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        -webkit-tap-highlight-color: rgba(102, 126, 234, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Mobile-optimized header component
def render_mobile_header():
    st.markdown("""
    <div class="modern-main-header">
        <h1>🍽️ AI Meal Identifier</h1>
        <p>AI Powered Smart nutrition analysis from your meal photo</p>
    </div>
    """, unsafe_allow_html=True)

# Mobile-optimized metric display with responsive grid
def render_mobile_nutrition_metrics(total_nutrition):
    st.markdown('<div class="modern-section-header">📊 Nutritional Overview</div>', unsafe_allow_html=True)

    # Safely get values and ensure they're numeric
    def safe_float(value, default=0.0):
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    metrics = [
        ("Calories", safe_float(total_nutrition.get('total_calories', 0)), "kcal", "#FF6B6B"),
        ("Protein", safe_float(total_nutrition.get('total_protein_g', 0)), "g", "#4ECDC4"),
        ("Carbs", safe_float(total_nutrition.get('total_carbohydrates_g', 0)), "g", "#45B7D1"),
        ("Fat", safe_float(total_nutrition.get('total_fat_g', 0)), "g", "#FFA07A"),
        ("Fiber", safe_float(total_nutrition.get('total_fiber_g', 0)), "g", "#98D8C8")
    ]

    # Mobile-responsive metric grid
    # On mobile, display 2 columns, on tablet 3, on desktop 5
    if st.session_state.get('is_mobile', False):
        # Display in 2x3 grid for mobile
        for i in range(0, len(metrics), 2):
            col1, col2 = st.columns(2)
            columns = [col1, col2]

            for j, col in enumerate(columns):
                if i + j < len(metrics):
                    label, value, unit, color = metrics[i + j]
                    with col:
                        st.markdown(f"""
                        <div class="modern-metric-card" style="--accent-color: {color};">
                            <div class="metric-value-modern">{value:.1f}</div>
                            <div class="metric-label-modern">{label} ({unit})</div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        # Desktop layout with 5 columns
        col1, col2, col3, col4, col5 = st.columns(5)
        columns = [col1, col2, col3, col4, col5]

        for i, (col, (label, value, unit, color)) in enumerate(zip(columns, metrics)):
            with col:
                st.markdown(f"""
                <div class="modern-metric-card" style="--accent-color: {color};">
                    <div class="metric-value-modern">{value:.1f}</div>
                    <div class="metric-label-modern">{label} ({unit})</div>
                </div>
                """, unsafe_allow_html=True)

# Mobile-optimized food items display
def render_mobile_food_items(detected_foods, show_confidence=True):
    st.markdown('<div class="modern-section-header">🍽️ Detected Food Items</div>', unsafe_allow_html=True)

    for i, food in enumerate(detected_foods):
        food_name = food.get('food_name', 'Unknown Food')
        category = food.get('category', 'Unknown')
        confidence = food.get('identification_confidence', 
                           food.get('portion_estimate', {}).get('confidence_level', 0))

        # Safely convert confidence to float
        try:
            confidence = float(confidence) if confidence is not None else 0.0
        except (ValueError, TypeError):
            confidence = 0.0

        nutrition = food.get('nutrition', {})

        # Determine confidence level and styling
        if confidence >= 8:
            conf_level = "High"
            badge_class = "status-high-modern"
        elif confidence >= 5:
            conf_level = "Medium" 
            badge_class = "status-medium-modern"
        else:
            conf_level = "Low"
            badge_class = "status-low-modern"

        # Create mobile-friendly expandable food card
        with st.expander(f"🍴 {food_name}", expanded=(i == 0)):
            # Mobile-optimized badge layout
            badge_container = st.container()
            with badge_container:
                col1, col2 = st.columns(2) if show_confidence else st.columns([1])

                with col1:
                    st.markdown(f"""
                    <span class="modern-status-badge {badge_class}">
                        {category}
                    </span>
                    """, unsafe_allow_html=True)

                if show_confidence:
                    with col2:
                        st.markdown(f"""
                        <span class="modern-status-badge {badge_class}">
                            Confidence: {confidence:.1f}/10
                        </span>
                        """, unsafe_allow_html=True)

            # Food details section
            st.markdown("**🔍 Food Details:**")

            # Mobile-optimized details layout
            details_col1, details_col2 = st.columns(2)
            with details_col1:
                st.markdown(f"**Preparation:** {food.get('preparation_method', 'Unknown')}")
                st.markdown(f"**Position:** {food.get('position_in_image', 'Unknown')}")

            with details_col2:
                st.markdown(f"**Visibility:** {food.get('visibility', 'Full')}")
                portion = food.get('portion_estimate', {})
                if portion.get('serving_size'):
                    st.markdown(f"**Serving:** {portion.get('serving_size', 'Unknown')}")

            # Enhanced confidence bar visualization for mobile
            if show_confidence:
                conf_percentage = (confidence / 10) * 100
                st.markdown(f"""
                <div style="margin: 1rem 0;">
                    <p style="margin-bottom: 0.5rem; font-weight: 600; color: #334155; font-size: 0.9rem;">Confidence Level</p>
                    <div class="modern-confidence-bar">
                        <div class="modern-confidence-fill" style="width: {conf_percentage:.1f}%;"></div>
                    </div>
                    <p style="text-align: right; font-size: 0.8rem; margin-top: 0.25rem; color: #64748b; font-weight: 600;">
                        {conf_level} ({confidence:.1f}/10)
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # Mobile-optimized nutrition facts section
            st.markdown("**📊 Nutrition Facts**")

            # Safe function for nutrition values
            def safe_nutrition_value(value, default=0.0):
                if value is None:
                    return default
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default

            nutrition_data = [
                ("Calories", safe_nutrition_value(nutrition.get('calories', 0)), "kcal"),
                ("Protein", safe_nutrition_value(nutrition.get('protein_g', 0)), "g"),
                ("Carbs", safe_nutrition_value(nutrition.get('carbohydrates_g', 0)), "g"),
                ("Fat", safe_nutrition_value(nutrition.get('fat_g', 0)), "g"),
                ("Fiber", safe_nutrition_value(nutrition.get('fiber_g', 0)), "g"),
                ("Sodium", safe_nutrition_value(nutrition.get('sodium_mg', 0)), "mg")
            ]

            # Mobile-optimized nutrition display in 2-column grid
# 2-column flat display like food details
            nutrition_col1, nutrition_col2 = st.columns(2)

            for i, (label, value, unit) in enumerate(nutrition_data):
                if value > 0:
                    col = nutrition_col1 if i % 2 == 0 else nutrition_col2
                    with col:
                        st.markdown(f"**{label}:** {value:.1f} {unit}")


# Mobile-optimized analysis results display
def display_mobile_analysis_results(analysis_result, analysis_depth="Standard", show_confidence=True):
    if not analysis_result or "detected_foods" not in analysis_result:
        st.error("❌ No analysis data available")
        return

    # Overview section with mobile-optimized layout
    if "total_nutrition" in analysis_result:
        render_mobile_nutrition_metrics(analysis_result["total_nutrition"])

    # Analysis metadata summary with mobile-friendly cards
    if "analysis_metadata" in analysis_result:
        metadata = analysis_result["analysis_metadata"]
        st.markdown("---")

        # Mobile-responsive metadata grid (2x2 on mobile, 4x1 on desktop)
        if st.session_state.get('is_mobile', False):
            # 2x2 grid for mobile
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            columns = [col1, col2, col3, col4]
        else:
            # Single row for desktop
            col1, col2, col3, col4 = st.columns(4)
            columns = [col1, col2, col3, col4]

        metadata_items = [
            ("Items", metadata.get("total_items_detected", 0), "#8b5cf6"),
            ("Confidence", f"{float(metadata.get('overall_confidence', 0)):.1f}/10" if metadata.get('overall_confidence') else "0.0/10", "#06b6d4"),
            ("Quality", str(metadata.get('image_quality', 'Unknown')).title()[:4], "#f59e0b"),
            ("Analysis", str(metadata.get('analysis_thoroughness', 'Standard')).title()[:4], "#10b981")
        ]

        for i, (col, (label, value, color)) in enumerate(zip(columns, metadata_items)):
            with col:
                st.markdown(f"""
                <div class="modern-metric-card" style="--accent-color: {color};">
                    <div class="metric-value-modern">{value}</div>
                    <div class="metric-label-modern">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # Food items section with mobile-optimized display
    if analysis_result.get("detected_foods"):
        render_mobile_food_items(analysis_result["detected_foods"], show_confidence)
    else:
        st.markdown("""
        <div class="modern-welcome">
            <div class="modern-welcome-icon">🤔</div>
            <h3>No Food Items Detected</h3>
            <p>Try uploading a clearer image with visible food items</p>
        </div>
        """, unsafe_allow_html=True)

    # Advanced visualizations for detailed analysis
    if analysis_depth == "Advanced" and analysis_result.get("detected_foods"):
        st.markdown("---")
        st.markdown('<div class="modern-section-header">📈 Advanced Analytics</div>', unsafe_allow_html=True)

        # Create mobile-optimized charts
        create_mobile_nutrition_charts(analysis_result)

        # Mobile-optimized recommendations section
        if analysis_result.get("analysis_metadata", {}).get("recommendations"):
            st.markdown('<div class="modern-section-header">💡 AI Recommendations</div>', unsafe_allow_html=True)
            recommendations = analysis_result["analysis_metadata"]["recommendations"]

            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"""
                <div class="floating-card">
                    <div style="display: flex; align-items: flex-start; margin-bottom: 0.5rem;">
                        <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; font-weight: 600; margin-right: 1rem; font-size: 0.8rem; flex-shrink: 0; margin-top: 0.1rem;">{i}</span>
                        <div>
                            <strong style="color: #334155; font-size: 0.9rem;">AI Recommendation</strong>
                            <p style="margin: 0.5rem 0 0 0; color: #64748b; line-height: 1.4; font-size: 0.9rem;">{rec}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Mobile-optimized sidebar with collapsible sections
def render_mobile_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2>⚙️ Settings</h2>
            <p>Configure your analysis</p>
        </div>
        """, unsafe_allow_html=True)

        # Cultural context selection
        with st.expander("🌍 Cultural Context", expanded=True):
            cultural_context = st.selectbox(
                "Select cuisine type",
                ["None", "Asian Cuisine", "Indian", "Mexican", 
                 "Italian", "Middle Eastern", "African", "Latin American", "Other"],
                help="Helps identify culture-specific ingredients and dishes"
            )

            if cultural_context == "Other":
                cultural_context = st.text_input("Specify cuisine type:")

        # Analysis level selection
        with st.expander("📊 Analysis Level", expanded=True):
            analysis_depth = st.select_slider(
                "Choose detail level",
                options=["Quick", "Standard", "Advanced"],
                value="Standard",
                help="Quick: Basic info | Standard: Detailed analysis | Advanced: Complete with charts"
            )

        # Advanced options in a collapsible section
        # with st.expander("🔧 Advanced Options"):                                            #####HIDING ADVANCED OPTIONS
        #     show_confidence_scores = st.checkbox(
        #         "Show Confidence Scores",
        #         value=True,
        #         help="Display AI confidence levels for each food item"
        #     )

        #     min_confidence_threshold = st.slider(
        #         "Minimum Confidence Threshold",
        #         min_value=0.0,
        #         max_value=10.0,
        #         value=3.0,
        #         step=0.5,
        #         help="Filter out low-confidence detections"
        #     )
        show_confidence_scores = True
        min_confidence_threshold = 3.0
        # Mobile-optimized information card
        st.markdown("---")
        st.markdown("""
        <div class="floating-card">
            <h4 style="margin-top: 0; color: #1e293b; display: flex; align-items: center; font-size: 1rem;">
                <span style="margin-right: 0.5rem;">📸</span> Photo Tips
            </h4>
            <ul style="margin-bottom: 0; font-size: 0.85rem; color: #64748b; line-height: 1.5; padding-left: 1rem;">
                <li>Use good lighting</li>
                <li>Capture entire meal</li>
                <li>Avoid shadows and glare</li>
                <li>Take from slightly above</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        return cultural_context, analysis_depth, show_confidence_scores, min_confidence_threshold

# Mobile-optimized chart creation
def create_mobile_nutrition_charts(analysis_result):
    if "total_nutrition" not in analysis_result:
        return

    total_nutrition = analysis_result["total_nutrition"]

    # Safe function for chart values
    def safe_chart_value(value, default=0.0):
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    # Enhanced macronutrient pie chart optimized for mobile
    macros = {
        "Protein": safe_chart_value(total_nutrition.get("total_protein_g", 0)) * 4,
        "Carbohydrates": safe_chart_value(total_nutrition.get("total_carbohydrates_g", 0)) * 4,
        "Fat": safe_chart_value(total_nutrition.get("total_fat_g", 0)) * 9
    }

    if sum(macros.values()) > 0:
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(macros.keys()),
            values=list(macros.values()),
            hole=.3,
            textinfo='label+percent',
            textposition='inside',
            marker=dict(
                colors=['#667eea', '#764ba2', '#f093fb'],
                line=dict(color='#FFFFFF', width=3)
            ),
            textfont=dict(size=14, color='white', family='Inter', weight='bold')
        )])

        fig_pie.update_layout(
            title={
                'text': "🥧 Macronutrient Distribution",
                'x': 0.5,
                'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter', 'weight': 'bold'}
            },
            showlegend=True,
            height=350,  # Reduced height for mobile
            font=dict(size=12, family='Inter', color='#1e293b'),
            paper_bgcolor='rgba(255,255,255,0.98)',
            plot_bgcolor='rgba(255,255,255,0.98)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5,
                font=dict(color='#1e293b', size=10)
            ),
            margin=dict(l=20, r=20, t=60, b=20)  # Reduced margins for mobile
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    # Enhanced food comparison chart optimized for mobile
    if len(analysis_result.get("detected_foods", [])) > 1:
        foods_data = []
        for food in analysis_result["detected_foods"]:
            nutrition = food.get("nutrition", {})
            calories = safe_chart_value(nutrition.get("calories", 0))
            if calories > 0:
                food_name = str(food.get("food_name", "Unknown"))
                # Truncate long names for mobile display
                if len(food_name) > 12:
                    food_name = food_name[:12] + "..."

                foods_data.append({
                    "Food": food_name,
                    "Calories": calories,
                    "Protein": safe_chart_value(nutrition.get("protein_g", 0)),
                    "Carbs": safe_chart_value(nutrition.get("carbohydrates_g", 0)),
                    "Fat": safe_chart_value(nutrition.get("fat_g", 0))
                })

        if len(foods_data) > 1:
            fig_bar = go.Figure()

            colors = ['#667eea', '#764ba2', '#f093fb', '#4ecdc4', '#45b7d1']

            fig_bar.add_trace(go.Bar(
                name='Calories',
                x=[f["Food"] for f in foods_data],
                y=[f["Calories"] for f in foods_data],
                marker_color=colors[0],
                text=[f'{f["Calories"]:.0f}' for f in foods_data],
                textposition='auto',
                textfont=dict(color='white', size=12, family='Inter', weight='bold')
            ))

            fig_bar.update_layout(
                title={
                    'text': "📊 Calorie Comparison", 
                    'x': 0.5,
                    'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter', 'weight': 'bold'}
                },
                xaxis_title="Food Items",
                yaxis_title="Calories",
                height=300,  # Reduced height for mobile
                paper_bgcolor='rgba(255,255,255,0.98)',
                plot_bgcolor='rgba(255,255,255,0.98)',
                font=dict(size=11, family='Inter', color='#1e293b'),
                xaxis=dict(
                    gridcolor='rgba(0,0,0,0.1)', 
                    tickfont=dict(color='#1e293b', size=10),
                    tickangle=45  # Angle text for better mobile readability
                ),
                yaxis=dict(gridcolor='rgba(0,0,0,0.1)', tickfont=dict(color='#1e293b', size=10)),
                margin=dict(l=40, r=20, t=60, b=80)  # Adjusted margins for mobile
            )

            st.plotly_chart(fig_bar, use_container_width=True)

# Detect if user is on mobile device
def detect_mobile():
    """Simple mobile detection based on user agent and screen width"""
    # This is a simplified detection - in a real app you might use JavaScript
    # For now, we'll use session state to track mobile preference
    if 'is_mobile' not in st.session_state:
        st.session_state.is_mobile = False

    # Add a toggle for users to manually set mobile mode
    # mobile_mode = st.sidebar.checkbox("📱 Mobile Mode", value=st.session_state.get('is_mobile', False))               ###HIDING MOBILE MOBE
    mobile_mode = False
    st.session_state.is_mobile = mobile_mode

    return mobile_mode

# Keep the original MealAnalyzer class (same functionality)
class MealAnalyzer:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def encode_image(self, image: Image.Image) -> str:
        """Encode image to base64 string"""
        buffered = io.BytesIO()
        # Optimize image size for API efficiency
        if max(image.size) > 2048:
            ratio = 2048 / max(image.size)
            new_size = tuple([int(x * ratio) for x in image.size])
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        image.save(buffered, format="PNG", optimize=True)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def create_analysis_prompt(self, cultural_context: str = "", analysis_depth: str = "Standard") -> str:
        """Create structured prompt for food analysis"""
        base_prompt = """
You are an expert nutritionist and food analyst. Analyze this food image and provide a detailed JSON response.

CRITICAL CONSISTENCY REQUIREMENTS:
1. EXAMINE THE ENTIRE IMAGE systematically - scan from left to right, top to bottom
2. IDENTIFY EVERY VISIBLE FOOD ITEM, even small garnishes, sauces, or partially hidden items
3. If uncertain about an item, include it with lower confidence rather than omitting it
4. Look for overlapping foods, items behind others, and foods that blend together
5. Consider that one "dish" might contain multiple distinct food components
6. Be thorough - missing items is worse than over-identifying with low confidence

REQUIRED JSON STRUCTURE:
{
  "detected_foods": [
    {
      "food_name": "specific food name",
      "category": "food category (protein, grain, vegetable, etc.)",
      "preparation_method": "cooking method",
      "position_in_image": "location description",
      "visibility": "full/partial/mostly_hidden",
      "portion_estimate": {
        "weight_grams": numeric_value,
        "volume_ml": numeric_value,
        "serving_size": "description",
        "confidence_level": numeric_1_to_10
      },
      "nutrition": {
        "calories": numeric_value,
        "protein_g": numeric_value,
        "carbohydrates_g": numeric_value,
        "fat_g": numeric_value,
        "fiber_g": numeric_value,
        "sugar_g": numeric_value,
        "sodium_mg": numeric_value,
        "calcium_mg": numeric_value,
        "iron_mg": numeric_value,
        "vitamin_c_mg": numeric_value
      },
      "reference_objects": ["list of objects used for scale"],
      "identification_confidence": numeric_1_to_10
    }
  ],
  "total_nutrition": {
    "total_calories": sum_of_all_calories,
    "total_protein_g": sum_of_all_protein,
    "total_carbohydrates_g": sum_of_all_carbs,
    "total_fat_g": sum_of_all_fat,
    "total_fiber_g": sum_of_all_fiber,
    "total_sugar_g": sum_of_all_sugar,
    "total_sodium_mg": sum_of_all_sodium
  },
  "analysis_metadata": {
    "total_items_detected": count_of_food_items,
    "image_quality": "good/fair/poor",
    "reference_objects_detected": ["list of reference objects"],
    "lighting_conditions": "description",
    "overall_confidence": numeric_1_to_10,
    "cultural_context": "cuisine type if applicable",
    "analysis_thoroughness": "advanced/standard/limited",
    "potential_missed_items": ["list any items you might have missed"],
    "recommendations": ["list of nutritional recommendations"]
  }
}
        """

        if cultural_context and cultural_context != "None":
            base_prompt += f"\n\nCULTURAL CONTEXT: This appears to be {cultural_context} cuisine. Consider regional ingredients and preparation methods."

        if analysis_depth == "Advanced":
            base_prompt += "\n\nPROVIDE COMPREHENSIVE ANALYSIS: Include detailed ingredient breakdown and health impact assessment."

        base_prompt += """

IMPORTANT INSTRUCTIONS:
- Respond ONLY with valid JSON matching the exact structure above
- All numeric values must be numbers, not strings
- Always provide fiber_g values (estimate based on food type)
- Include empty arrays [] if no reference objects detected
- Ensure all required fields are present
- No text before or after the JSON response
"""
        return base_prompt

    def analyze_meal(self, image: Image.Image, cultural_context: str = "", 
                          analysis_depth: str = "Standard") -> Dict:
        """Analyze meal with single run"""
        return self.analyze_meal_single(image, cultural_context, analysis_depth)

    def safe_numeric(self, value, default=0):
        """Safely convert value to numeric"""
        if value is None:
            return default
        try:
            return float(value) if isinstance(value, (int, float, str)) else default
        except (ValueError, TypeError):
            return default

    def analyze_meal_single(self, image: Image.Image, cultural_context: str = "", analysis_depth: str = "Standard") -> Dict:
        """Single meal analysis run"""
        try:
            base64_image = self.encode_image(image)
            prompt = self.create_analysis_prompt(cultural_context, analysis_depth)

            temperature = 0.3 if analysis_depth == "Advanced" else 0.2

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }],
                temperature=temperature,
                response_format={"type": "json_object"},
                max_tokens=4000
            )

            # Parse JSON response
            result = json.loads(response.choices[0].message.content)

            # Validate and clean the response
            result = self.validate_and_clean_response(result)
            return result

        except json.JSONDecodeError as e:
            st.error(f"JSON parsing error: {str(e)}")
            return self.create_fallback_response()
        except Exception as e:
            st.error(f"Analysis error: {str(e)}")
            return self.create_fallback_response()

    def validate_and_clean_response(self, result: Dict) -> Dict:
        """Validate and clean the response"""
        # Ensure main structure exists
        if "detected_foods" not in result or not isinstance(result["detected_foods"], list):
            result["detected_foods"] = []

        if "total_nutrition" not in result or not isinstance(result["total_nutrition"], dict):
            result["total_nutrition"] = {
                "total_calories": 0,
                "total_protein_g": 0,
                "total_carbohydrates_g": 0,
                "total_fat_g": 0,
                "total_fiber_g": 0,
                "total_sugar_g": 0,
                "total_sodium_mg": 0
            }

        if "analysis_metadata" not in result or not isinstance(result["analysis_metadata"], dict):
            result["analysis_metadata"] = {
                "total_items_detected": len(result.get("detected_foods", [])),
                "image_quality": "unknown",
                "reference_objects_detected": [],
                "lighting_conditions": "unknown",
                "overall_confidence": 5,
                "cultural_context": "unknown",
                "analysis_thoroughness": "standard",
                "potential_missed_items": [],
                "recommendations": []
            }

        # Clean detected foods
        cleaned_foods = []
        for food in result["detected_foods"]:
            if not isinstance(food, dict):
                continue

            cleaned_food = {
                "food_name": food.get("food_name", "unknown food"),
                "category": food.get("category", "unknown"),
                "preparation_method": food.get("preparation_method", "unknown"),
                "position_in_image": food.get("position_in_image", "unknown"),
                "visibility": food.get("visibility", "full"),
                "portion_estimate": {},
                "nutrition": {},
                "reference_objects": [],
                "identification_confidence": self.safe_numeric(food.get("identification_confidence"), 5)
            }

            # Clean portion estimate
            portion = food.get("portion_estimate", {})
            if not isinstance(portion, dict):
                portion = {}

            cleaned_food["portion_estimate"] = {
                "weight_grams": self.safe_numeric(portion.get("weight_grams"), 0),
                "volume_ml": self.safe_numeric(portion.get("volume_ml"), 0),
                "serving_size": portion.get("serving_size", "unknown") if portion.get("serving_size") else "unknown",
                "confidence_level": self.safe_numeric(portion.get("confidence_level"), 5)
            }

            # Clean nutrition data
            nutrition = food.get("nutrition", {})
            if not isinstance(nutrition, dict):
                nutrition = {}

            cleaned_food["nutrition"] = {
                "calories": self.safe_numeric(nutrition.get("calories"), 0),
                "protein_g": self.safe_numeric(nutrition.get("protein_g"), 0),
                "carbohydrates_g": self.safe_numeric(nutrition.get("carbohydrates_g"), 0),
                "fat_g": self.safe_numeric(nutrition.get("fat_g"), 0),
                "fiber_g": self.safe_numeric(nutrition.get("fiber_g"), 0),
                "sugar_g": self.safe_numeric(nutrition.get("sugar_g"), 0),
                "sodium_mg": self.safe_numeric(nutrition.get("sodium_mg"), 0),
                "calcium_mg": self.safe_numeric(nutrition.get("calcium_mg"), 0),
                "iron_mg": self.safe_numeric(nutrition.get("iron_mg"), 0),
                "vitamin_c_mg": self.safe_numeric(nutrition.get("vitamin_c_mg"), 0)
            }

            # Clean reference objects
            ref_objects = food.get("reference_objects", [])
            if isinstance(ref_objects, list):
                cleaned_food["reference_objects"] = [str(obj) for obj in ref_objects if obj is not None]
            else:
                cleaned_food["reference_objects"] = []

            cleaned_foods.append(cleaned_food)

        result["detected_foods"] = cleaned_foods

        # Clean total nutrition
        total_nutrition = result["total_nutrition"]
        for key in ["total_calories", "total_protein_g", "total_carbohydrates_g", "total_fat_g", 
                   "total_fiber_g", "total_sugar_g", "total_sodium_mg"]:
            total_nutrition[key] = self.safe_numeric(total_nutrition.get(key), 0)

        # Clean analysis metadata
        metadata = result["analysis_metadata"]
        metadata["total_items_detected"] = len(cleaned_foods)
        metadata["image_quality"] = metadata.get("image_quality", "unknown") if metadata.get("image_quality") else "unknown"
        metadata["lighting_conditions"] = metadata.get("lighting_conditions", "unknown") if metadata.get("lighting_conditions") else "unknown"
        metadata["cultural_context"] = metadata.get("cultural_context", "unknown") if metadata.get("cultural_context") else "unknown"
        metadata["overall_confidence"] = self.safe_numeric(metadata.get("overall_confidence"), 5)
        metadata["analysis_thoroughness"] = metadata.get("analysis_thoroughness", "standard")

        # Ensure lists
        for list_field in ["reference_objects_detected", "recommendations", "potential_missed_items"]:
            if not isinstance(metadata.get(list_field), list):
                metadata[list_field] = []

        return result

    def create_fallback_response(self) -> Dict:
        """Create a fallback response when analysis fails"""
        return {
            "detected_foods": [],
            "total_nutrition": {
                "total_calories": 0,
                "total_protein_g": 0,
                "total_carbohydrates_g": 0,
                "total_fat_g": 0,
                "total_fiber_g": 0,
                "total_sugar_g": 0,
                "total_sodium_mg": 0
            },
            "analysis_metadata": {
                "total_items_detected": 0,
                "image_quality": "analysis_failed",
                "reference_objects_detected": [],
                "lighting_conditions": "unknown",
                "overall_confidence": 0,
                "cultural_context": "unknown",
                "analysis_thoroughness": "failed",
                "potential_missed_items": [],
                "recommendations": ["Analysis failed - please try with a clearer image"]
            }
        }

    def recalculate_totals(self, result: Dict):
        """Recalculate total nutrition from detected foods"""
        totals = {
            "total_calories": 0,
            "total_protein_g": 0,
            "total_carbohydrates_g": 0,
            "total_fat_g": 0,
            "total_fiber_g": 0,
            "total_sugar_g": 0,
            "total_sodium_mg": 0
        }

        for food in result.get("detected_foods", []):
            nutrition = food.get("nutrition", {})
            for key in totals:
                clean_key = key.replace("total_", "").replace("_g", "_g").replace("_mg", "_mg")
                if clean_key == "calories":
                    clean_key = "calories"
                elif clean_key == "carbohydrates":
                    clean_key = "carbohydrates_g"
                elif clean_key == "protein":
                    clean_key = "protein_g"
                elif clean_key == "fat":
                    clean_key = "fat_g"
                elif clean_key == "fiber":
                    clean_key = "fiber_g"
                elif clean_key == "sugar":
                    clean_key = "sugar_g"
                elif clean_key == "sodium_mg":
                    clean_key = "sodium_mg"

                value = nutrition.get(clean_key, 0)
                totals[key] += self.safe_numeric(value, 0)

        result["total_nutrition"] = totals

# Mobile-optimized main function
def main():
    """Mobile-first Streamlit application"""
    # Detect mobile and apply appropriate styling
    is_mobile = detect_mobile()
    apply_mobile_friendly_styling()

    # Render mobile-optimized header
    render_mobile_header()

    # API Key handling
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        st.markdown("""
        <div class="floating-card" style="text-align: center; background: rgba(251, 191, 36, 0.9); border-color: rgba(251, 191, 36, 1);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔑</div>
            <h3 style="color: #1e293b; margin-bottom: 1rem;">API Key Required</h3>
            <p style="color: #1e293b; margin-bottom: 0;">
                Please set your OpenAI API key to use the analyzer
            </p>
        </div>
        """, unsafe_allow_html=True)

        api_key = st.text_input(
            "Enter OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Get your API key from OpenAI"
        )

        if not api_key:
            st.stop()

    # Initialize analyzer
    try:
        analyzer = MealAnalyzer(api_key)
    except Exception as e:
        st.error(f"❌ Error initializing analyzer: {str(e)}")
        return

    # Mobile-optimized sidebar
    cultural_context, analysis_depth, show_confidence_scores, min_confidence_threshold = render_mobile_sidebar()

    # Mobile-first main content layout
    if is_mobile:
        # Single column layout for mobile
        st.markdown('<div class="modern-section-header">📸 Upload Your Meal</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear photo of your meal for AI analysis"
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="📷 Your Meal Image", use_container_width=True)

            # Mobile-optimized image info
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.write(f"**Dimensions:** {image.size[0]}×{image.size[1]}px")
                
            with col_info2:
                # brightness calculation code stays the same
                brightness_status = "Good" if 50 < brightness < 200 else "Poor"
                st.write(f"**Brightness:** {brightness_status}")
                image_array = np.array(image)
                brightness = np.mean(image_array)
                brightness_status = "Good" if 50 <= brightness <= 200 else "Poor"
                brightness_color = "#22c55e" if brightness_status == "Good" else "#ef4444"

                st.markdown(f"""
                <div style="background: {brightness_color}; padding: 0.8rem; border-radius: 8px; text-align: center; color: white;">
                    <div style="font-weight: 600; font-size: 0.85rem;">Brightness</div>
                    <div style="font-size: 0.8rem;">{brightness_status}</div>
                </div>
                """, unsafe_allow_html=True)

            # Mobile-optimized analyze button
            if st.button("🔍 Analyze My Meal", type="primary", use_container_width=True):
                start_time = time.time()

                # Mobile-optimized loading animation
                # with st.spinner(""):
                st.markdown("""
                <div class="modern-loading-container">
                    <div class="modern-loading-spinner"></div>
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">🤖 AI is analyzing...</h3>
                    <p style="color: #64748b; margin: 0;">This may take a moment</p>
                </div>
                """, unsafe_allow_html=True)

                # Perform analysis
                result = analyzer.analyze_meal(image, cultural_context, analysis_depth)

                # Filter by confidence threshold
                if min_confidence_threshold > 0 and result.get("detected_foods"):
                    filtered_foods = []
                    for food in result["detected_foods"]:
                        confidence = food.get("identification_confidence", 
                                            food.get("portion_estimate", {}).get("confidence_level", 0))
                        try:
                            confidence = float(confidence) if confidence is not None else 0.0
                        except (ValueError, TypeError):
                            confidence = 0.0

                        if confidence >= min_confidence_threshold:
                            filtered_foods.append(food)

                    result["detected_foods"] = filtered_foods
                    analyzer.recalculate_totals(result)
                    if "analysis_metadata" in result:
                        result["analysis_metadata"]["total_items_detected"] = len(filtered_foods)

                processing_time = time.time() - start_time

                # Store results
                st.session_state.analysis_result = result
                st.session_state.analysis_timestamp = datetime.now()
                st.session_state.processing_time = processing_time
                st.session_state.analysis_depth = analysis_depth
                st.session_state.show_confidence_scores = show_confidence_scores

                st.success(f"✅ Analysis completed in {processing_time:.2f} seconds!")
                st.rerun()

        # Display results in mobile layout
        if 'analysis_result' in st.session_state:
            st.markdown("---")

            # Mobile-optimized timestamp info
            if 'analysis_timestamp' in st.session_state:
                timestamp = st.session_state.analysis_timestamp
                processing_time = st.session_state.get('processing_time', 0)

                st.markdown(f"""
                <div class="floating-card" style="text-align: center; padding: 1rem; margin-bottom: 1.5rem;">
                    <div style="font-size: 0.8rem; color: #64748b; font-weight: 500;">
                        ⏰ <strong style="color: #1e293b;">{timestamp.strftime('%H:%M:%S')}</strong> • 
                        ⚡ <strong style="color: #1e293b;">{processing_time:.2f}s</strong> • 
                        🔬 <strong style="color: #1e293b;">{st.session_state.get('analysis_depth', 'Standard')}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Display mobile-optimized results
            display_mobile_analysis_results(
                st.session_state.analysis_result, 
                st.session_state.get('analysis_depth', 'Standard'),
                st.session_state.get('show_confidence_scores', True)
            )

            # Mobile-optimized download section
            st.markdown("---")
            st.markdown('<div class="modern-section-header">💾 Export Results</div>', unsafe_allow_html=True)

            col_download1, col_download2 = st.columns(2)

            with col_download1:
                json_str = json.dumps(st.session_state.analysis_result, indent=2)
                st.download_button(
                    label="📄 JSON",
                    data=json_str,
                    file_name=f"meal_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )

            with col_download2:
                if st.session_state.analysis_result.get("detected_foods"):
                    foods_data = []
                    for food in st.session_state.analysis_result["detected_foods"]:
                        nutrition = food.get("nutrition", {})
                        confidence = food.get("identification_confidence", 
                                           food.get("portion_estimate", {}).get("confidence_level", 0))
                        try:
                            confidence = float(confidence) if confidence is not None else 0.0
                        except (ValueError, TypeError):
                            confidence = 0.0

                        def safe_csv_value(value, default=0.0):
                            if value is None:
                                return default
                            try:
                                return float(value)
                            except (ValueError, TypeError):
                                return default

                        foods_data.append({
                            "Food Name": food.get("food_name", ""),
                            "Category": food.get("category", ""),
                            "Calories": safe_csv_value(nutrition.get("calories", 0)),
                            "Protein (g)": safe_csv_value(nutrition.get("protein_g", 0)),
                            "Carbs (g)": safe_csv_value(nutrition.get("carbohydrates_g", 0)),
                            "Fat (g)": safe_csv_value(nutrition.get("fat_g", 0)),
                            "Fiber (g)": safe_csv_value(nutrition.get("fiber_g", 0)),
                            "Confidence": confidence
                        })

                    df = pd.DataFrame(foods_data)
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="📊 CSV",
                        data=csv_data,
                        file_name=f"meal_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

        else:
            # Mobile-optimized welcome message
            st.markdown("""
            <div class="modern-welcome">
                <div class="modern-welcome-icon">🤖</div>
                <h3>Ready to Analyze!</h3>
                <p>Upload a meal image and I'll identify foods and calculate nutrition</p>

                <div style="display: grid; grid-template-columns: 1fr; gap: 0.5rem; margin-top: 1.5rem; max-width: 280px; margin-left: auto; margin-right: auto;">
                    <div style="display: flex; align-items: center; color: #64748b; font-size: 0.85rem; font-weight: 500; justify-content: center;">
                        <span style="margin-right: 0.5rem;">🎯</span> AI-Powered Detection
                    </div>
                    <div style="display: flex; align-items: center; color: #64748b; font-size: 0.85rem; font-weight: 500; justify-content: center;">
                        <span style="margin-right: 0.5rem;">📊</span> Detailed Nutrition
                    </div>
                    <div style="display: flex; align-items: center; color: #64748b; font-size: 0.85rem; font-weight: 500; justify-content: center;">
                        <span style="margin-right: 0.5rem;">⚡</span> Fast Analysis
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        # Desktop layout with two columns
        col1, col2 = st.columns([2, 3], gap="large")

        with col1:
            st.markdown('<div class="modern-section-header">📸 Upload Your Meal</div>', unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=["jpg", "jpeg", "png"],
                help="Upload a clear photo of your meal for AI analysis"
            )

            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="📷 Your Meal Image", use_container_width=True)

                # Desktop image info
                # col_info1, col_info2 = st.columns(2)
                # with col_info1:
                #     st.markdown(f"""
                #     <div style="background: rgba(102, 126, 234, 0.9); padding: 0.8rem; border-radius: 8px; text-align: center; color: white;">
                #         <div style="font-weight: 600;">Dimensions</div>
                #         <div style="font-size: 0.9rem;">{image.size[0]}×{image.size[1]}px</div>
                #     </div>
                #     """, unsafe_allow_html=True)

                # with col_info2:
                #     image_array = np.array(image)
                #     brightness = np.mean(image_array)
                #     brightness_status = "Good" if 50 <= brightness <= 200 else "Poor"
                #     brightness_color = "#22c55e" if brightness_status == "Good" else "#ef4444"

                #     st.markdown(f"""
                #     <div style="background: {brightness_color}; padding: 0.8rem; border-radius: 8px; text-align: center; color: white;">
                #         <div style="font-weight: 600;">Brightness</div>
                #         <div style="font-size: 0.9rem;">{brightness_status}</div>
                #     </div>
                #     """, unsafe_allow_html=True)

                # Desktop analyze button
                if st.button("🔍 Analyze My Meal", type="primary", use_container_width=True):
                    start_time = time.time()

                    # with st.spinner(""):
                    st.markdown("""
                        <style>
                            .modern-loading-overlay {
                                position: fixed;
                                top: 0;
                                left: 0;
                                width: 100vw;
                                height: 100vh;
                                backdrop-filter: blur(8px);
                                -webkit-backdrop-filter: blur(8px);
                                background: rgba(255, 255, 255, 0.1);
                                z-index: 9998;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                            }
                            
                            .modern-loading-container {
                                text-align: center;
                                background: transparent !important;  /* Force transparency */
                                padding: 0 !important;  /* Remove all padding */
                                border-radius: 0 !important;  /* Remove border radius */
                                box-shadow: none !important;  /* Remove shadow */
                                backdrop-filter: none !important;  /* Remove backdrop filter */
                                -webkit-backdrop-filter: none !important;  /* Remove webkit backdrop filter */
                                border: none !important;  /* Remove border */
                                z-index: 9999;
                            }
                            
                            .modern-loading-spinner {
                                width: 50px;
                                height: 50px;
                                border: 4px solid #f3f4f6;
                                border-top: 4px solid #3b82f6;
                                border-radius: 50%;
                                animation: spin 1s linear infinite;
                                margin: 0 auto 1.5rem auto;
                            }
                            
                            @keyframes spin {
                                0% { transform: rotate(0deg); }
                                100% { transform: rotate(360deg); }
                            }
                        </style>
                        
                        <div class="modern-loading-overlay">
                            <div class="modern-loading-container">
                                <div class="modern-loading-spinner"></div>
                                <h3 style="color: #1e293b; margin-bottom: 1rem;">🤖 AI is analyzing your meal...</h3>
                                <p style="color: #64748b; margin: 0;">This may take a few seconds</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)



                    # st.markdown("""
                    #     <style>
                    #         .modern-loading-overlay {
                    #             position: fixed;
                    #             top: 0;
                    #             left: 0;
                    #             width: 100vw;
                    #             height: 100vh;
                    #             backdrop-filter: blur(8px);
                    #             -webkit-backdrop-filter: blur(8px);
                    #             background: rgba(255, 255, 255, 0.1);
                    #             z-index: 9998;
                    #             display: flex;
                    #             align-items: center;
                    #             justify-content: center;
                    #         }
                            
                    #         .modern-loading-container {
                    #             text-align: center;
                    #             background: rgba(0, 0, 0, 0);
                    #             padding: 2.5rem;
                    #             border-radius: 16px;
                    #             box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
                    #             backdrop-filter: blur(10px);
                    #             -webkit-backdrop-filter: blur(10px);
                    #             border: 1px solid rgba(255, 255, 255, 0.2);
                    #             z-index: 9999;
                    #         }
                            
                    #         .modern-loading-spinner {
                    #             width: 50px;
                    #             height: 50px;
                    #             border: 4px solid #f3f4f6;
                    #             border-top: 4px solid #3b82f6;
                    #             border-radius: 50%;
                    #             animation: spin 1s linear infinite;
                    #             margin: 0 auto 1.5rem auto;
                    #         }
                            
                    #         @keyframes spin {
                    #             0% { transform: rotate(0deg); }
                    #             100% { transform: rotate(360deg); }
                    #         }
                    #     </style>
                        
                    #     <div class="modern-loading-overlay">
                    #         <div class="modern-loading-container">
                    #             <div class="modern-loading-spinner"></div>
                    #             <h3 style="color: #1e293b; margin-bottom: 1rem;">🤖 AI is analyzing your meal...</h3>
                    #             <p style="color: #64748b; margin: 0;">This may take a few moments</p>
                    #         </div>
                    #     </div>
                    # """, unsafe_allow_html=True)


                    # st.markdown("""
                    #     <style>
                    #         .modern-loading-container {
                    #             position: fixed;
                    #             top: 50%;
                    #             left: 50%;
                    #             transform: translate(-50%, -50%);
                    #             z-index: 9999;
                    #             text-align: center;
                    #             background: rgba(255, 255, 255, 0.9);
                    #             padding: 2rem;
                    #             border-radius: 12px;
                    #             box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                    #         }
                            
                    #         .modern-loading-spinner {
                    #             width: 50px;
                    #             height: 50px;
                    #             border: 4px solid #f3f4f6;
                    #             border-top: 4px solid #3b82f6;
                    #             border-radius: 50%;
                    #             animation: spin 1s linear infinite;
                    #             margin: 0 auto 1rem auto;
                    #         }
                            
                    #         @keyframes spin {
                    #             0% { transform: rotate(0deg); }
                    #             100% { transform: rotate(360deg); }
                    #         }
                    #     </style>
                        
                    #     <div class="modern-loading-container">
                    #         <div class="modern-loading-spinner"></div>
                    #         <h3 style="color: #1e293b; margin-bottom: 1rem;">🤖 AI is analyzing your meal...</h3>
                    #         <p style="color: #64748b; margin: 0;">This may take a few moments</p>
                    #     </div>
                    # """, unsafe_allow_html=True)


                    result = analyzer.analyze_meal(image, cultural_context, analysis_depth)

                    # Filter by confidence threshold
                    if min_confidence_threshold > 0 and result.get("detected_foods"):
                        filtered_foods = []
                        for food in result["detected_foods"]:
                            confidence = food.get("identification_confidence", 
                                                food.get("portion_estimate", {}).get("confidence_level", 0))
                            try:
                                confidence = float(confidence) if confidence is not None else 0.0
                            except (ValueError, TypeError):
                                confidence = 0.0

                            if confidence >= min_confidence_threshold:
                                filtered_foods.append(food)

                        result["detected_foods"] = filtered_foods
                        analyzer.recalculate_totals(result)
                        if "analysis_metadata" in result:
                            result["analysis_metadata"]["total_items_detected"] = len(filtered_foods)

                    processing_time = time.time() - start_time

                    st.session_state.analysis_result = result
                    st.session_state.analysis_timestamp = datetime.now()
                    st.session_state.processing_time = processing_time
                    st.session_state.analysis_depth = analysis_depth
                    st.session_state.show_confidence_scores = show_confidence_scores

                    st.success(f"✅ Analysis completed in {processing_time:.2f} seconds!")
                    st.rerun()

        with col2:
            if 'analysis_result' in st.session_state:
                # Desktop timestamp info
                if 'analysis_timestamp' in st.session_state:
                    timestamp = st.session_state.analysis_timestamp
                    processing_time = st.session_state.get('processing_time', 0)

                    # \
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1.5rem; margin-bottom: 2rem; 
                        background: linear-gradient(135deg, rgba(219, 234, 254, 0.8), rgba(191, 219, 254, 0.9)); 
                        border-radius: 15px; 
                        border: 1px solid rgba(203, 213, 225, 0.6);">
                        <div style="font-size: 0.9rem; color: #64748b; font-weight: 500;">
                        Image analysis completed in: <strong style="color: #1e293b;">{processing_time:.2f}s</strong> 
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Display desktop results
                display_mobile_analysis_results(
                    st.session_state.analysis_result, 
                    st.session_state.get('analysis_depth', 'Standard'),
                    st.session_state.get('show_confidence_scores', True)
                )

                # Desktop download section
                st.markdown("---")
                st.markdown('<div class="modern-section-header">💾 Export Results</div>', unsafe_allow_html=True)

                col_download1, col_download2 = st.columns(2)

                with col_download1:
                    json_str = json.dumps(st.session_state.analysis_result, indent=2)
                    st.download_button(
                        label="📄 Download JSON",
                        data=json_str,
                        file_name=f"meal_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )

                with col_download2:
                    if st.session_state.analysis_result.get("detected_foods"):
                        foods_data = []
                        for food in st.session_state.analysis_result["detected_foods"]:
                            nutrition = food.get("nutrition", {})
                            confidence = food.get("identification_confidence", 
                                               food.get("portion_estimate", {}).get("confidence_level", 0))
                            try:
                                confidence = float(confidence) if confidence is not None else 0.0
                            except (ValueError, TypeError):
                                confidence = 0.0

                            def safe_csv_value(value, default=0.0):
                                if value is None:
                                    return default
                                try:
                                    return float(value)
                                except (ValueError, TypeError):
                                    return default

                            foods_data.append({
                                "Food Name": food.get("food_name", ""),
                                "Category": food.get("category", ""),
                                "Calories": safe_csv_value(nutrition.get("calories", 0)),
                                "Protein (g)": safe_csv_value(nutrition.get("protein_g", 0)),
                                "Carbs (g)": safe_csv_value(nutrition.get("carbohydrates_g", 0)),
                                "Fat (g)": safe_csv_value(nutrition.get("fat_g", 0)),
                                "Fiber (g)": safe_csv_value(nutrition.get("fiber_g", 0)),
                                "Confidence": confidence
                            })

                        df = pd.DataFrame(foods_data)
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            label="📊 Download CSV",
                            data=csv_data,
                            file_name=f"meal_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

            else:
                # Desktop welcome message
                st.markdown("""
                <div class="modern-welcome">
                    <div class="modern-welcome-icon">🤖</div>
                    <h3>Ready to Analyze!</h3>
                    <p>Upload a meal image and I'll identify foods and calculate nutrition with precision</p>
                    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 2rem;">
                        <div style="display: flex; align-items: center; color: #64748b; font-size: 0.9rem; font-weight: 500;">
                            <span style="margin-right: 0.5rem;">🎯</span> AI-Powered Detection
                        </div>
                        <div style="display: flex; align-items: center; color: #64748b; font-size: 0.9rem; font-weight: 500;">
                            <span style="margin-right: 0.5rem;">📊</span> Detailed Nutrition
                        </div>
                        <div style="display: flex; align-items: center; color: #64748b; font-size: 0.9rem; font-weight: 500;">
                            <span style="margin-right: 0.5rem;">⚡</span> Fast Analysis
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Mobile-optimized footer
    # st.markdown("---")
    # st.markdown("""
    # <div class="modern-footer">
    #     <h3>🍽️ AI Nutrition Analyzer Pro</h3>
    #     <p>Powered by OpenAI GPT-4o Vision</p>
    #     <p>Get accurate nutritional insights from your meal photos</p>
    # </div>
    # """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
