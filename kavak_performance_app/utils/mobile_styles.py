"""
Mobile-specific styles for Kavak Performance App
Responsive design optimizations for mobile devices

Este archivo contiene todos los estilos responsivos para móvil.
Puedes iterar aquí sin afectar los estilos principales de desktop.
"""

import streamlit as st


def apply_mobile_styles():
    """
    Apply mobile-responsive CSS styles
    Optimiza la experiencia en dispositivos móviles
    """
    st.markdown(
        """
        <style>
        /* ═══════════════════════════════════════════════════════════════════
           MOBILE RESPONSIVE STYLES - Kavak Performance App
           Breakpoints:
           - Mobile: max-width 768px
           - Small Mobile: max-width 480px
           - Tablet: max-width 1024px
        ═══════════════════════════════════════════════════════════════════ */

        /* ═══════════════════════════════════════════════════════════════════
           GENERAL MOBILE LAYOUT
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            /* Reduce padding on mobile */
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-top: 1rem !important;
                max-width: 100% !important;
            }
            
            /* Hide sidebar by default on mobile */
            [data-testid="stSidebar"] {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }
            
            [data-testid="stSidebar"][aria-expanded="true"] {
                transform: translateX(0);
            }
            
            /* Main content full width */
            .main .block-container {
                max-width: 100% !important;
                padding: 0.5rem !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           COLUMNS - Stack vertically on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            /* Force columns to stack vertically */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }
            
            /* Horizontal layout container - make it wrap */
            .stHorizontalBlock,
            [data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
                gap: 0.5rem !important;
            }
            
            /* Special handling for 2-column layouts - allow side by side */
            .stHorizontalBlock:has([data-testid="column"]:nth-child(2):last-child) [data-testid="column"] {
                width: 48% !important;
                flex: 1 1 48% !important;
                min-width: 140px !important;
            }
        }
        
        /* Extra small screens - always stack */
        @media (max-width: 480px) {
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }
            
            .stHorizontalBlock:has([data-testid="column"]:nth-child(2):last-child) [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           TYPOGRAPHY - Smaller on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            h1 {
                font-size: 1.5rem !important;
                line-height: 1.2 !important;
            }
            
            h2 {
                font-size: 1.25rem !important;
                line-height: 1.3 !important;
            }
            
            h3 {
                font-size: 1.1rem !important;
                line-height: 1.3 !important;
            }
            
            h4, h5, h6 {
                font-size: 1rem !important;
            }
            
            p, span, div {
                font-size: 0.9rem !important;
            }
            
            /* Streamlit specific text */
            .stMarkdown p {
                font-size: 0.9rem !important;
            }
        }
        
        @media (max-width: 480px) {
            h1 {
                font-size: 1.3rem !important;
            }
            
            h2 {
                font-size: 1.1rem !important;
            }
            
            h3 {
                font-size: 1rem !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           METRICS / KPIs - Compact on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            /* Metric container */
            [data-testid="stMetric"] {
                padding: 0.5rem !important;
                background: white;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                margin-bottom: 0.5rem !important;
            }
            
            /* Metric value - smaller */
            [data-testid="stMetricValue"] {
                font-size: 1.25rem !important;
                line-height: 1.2 !important;
            }
            
            /* Metric label - compact */
            [data-testid="stMetricLabel"] {
                font-size: 0.65rem !important;
                letter-spacing: 0.03em !important;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            /* Metric delta - smaller */
            [data-testid="stMetricDelta"] {
                font-size: 0.7rem !important;
            }
        }
        
        @media (max-width: 480px) {
            [data-testid="stMetricValue"] {
                font-size: 1.1rem !important;
            }
            
            [data-testid="stMetricLabel"] {
                font-size: 0.6rem !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           TABS - Scrollable on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            /* Make tabs container scrollable horizontally */
            .stTabs [data-baseweb="tab-list"] {
                overflow-x: auto !important;
                overflow-y: hidden !important;
                flex-wrap: nowrap !important;
                gap: 4px !important;
                padding: 4px !important;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none; /* Firefox */
                -ms-overflow-style: none; /* IE/Edge */
            }
            
            .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
                display: none; /* Chrome/Safari */
            }
            
            /* Smaller tabs */
            .stTabs [data-baseweb="tab"] {
                padding: 8px 12px !important;
                font-size: 0.75rem !important;
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           RADIO BUTTONS (Navigation Pills) - Scrollable on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            .stRadio > div {
                overflow-x: auto !important;
                flex-wrap: nowrap !important;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 8px;
            }
            
            .stRadio [role="radiogroup"] {
                flex-wrap: nowrap !important;
                gap: 6px !important;
            }
            
            .stRadio label {
                padding: 6px 12px !important;
                font-size: 0.75rem !important;
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           BUTTONS - Full width on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            .stButton > button {
                width: 100% !important;
                padding: 10px 16px !important;
                font-size: 0.85rem !important;
            }
            
            /* Smaller icon buttons */
            .stButton > button:has(only-child) {
                min-width: 44px !important;
                min-height: 44px !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           INPUTS / SELECTS - Full width and larger touch targets
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            .stTextInput > div > div > input,
            .stSelectbox > div > div,
            .stMultiSelect > div > div {
                font-size: 16px !important; /* Prevents zoom on iOS */
                padding: 12px !important;
                min-height: 44px !important;
            }
            
            .stSelectbox label,
            .stTextInput label,
            .stMultiSelect label {
                font-size: 0.8rem !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           DATAFRAMES / TABLES - Scrollable on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            [data-testid="stDataFrame"],
            .stDataFrame {
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch;
            }
            
            .dataframe {
                font-size: 0.75rem !important;
            }
            
            .dataframe th,
            .dataframe td {
                padding: 6px 8px !important;
                white-space: nowrap !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           EXPANDERS - Compact on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            .streamlit-expanderHeader {
                padding: 10px 12px !important;
                font-size: 0.85rem !important;
            }
            
            [data-testid="stExpander"] > div > div {
                padding: 0.5rem !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           ALERTS / INFO BOXES - Compact on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            .alert-critical,
            .alert-warning,
            .alert-info {
                padding: 12px 14px !important;
                font-size: 0.85rem !important;
                margin: 8px 0 !important;
            }
            
            .stAlert,
            .stSuccess,
            .stInfo,
            .stWarning,
            .stError {
                padding: 10px 12px !important;
                font-size: 0.85rem !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           CHARTS / PLOTLY - Responsive on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            [data-testid="stPlotlyChart"] {
                width: 100% !important;
            }
            
            .js-plotly-plot {
                width: 100% !important;
            }
            
            /* Reduce chart height on mobile */
            .js-plotly-plot .plotly {
                height: 250px !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           PROGRESS BARS - Compact on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            .stProgress > div > div {
                height: 6px !important;
            }
            
            .stProgress > div > div > div {
                height: 6px !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           CONTAINERS WITH BORDERS - Compact on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            [data-testid="stVerticalBlock"] > div:has(> [data-testid="stContainer"]) {
                padding: 0.5rem !important;
            }
            
            /* Container with border */
            [data-testid="stContainer"][data-testid="stVerticalBlockBorderWrapper"] {
                padding: 0.75rem !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           SIDEBAR - Mobile optimizations
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            [data-testid="stSidebar"] > div {
                padding-top: 1rem !important;
            }
            
            [data-testid="stSidebar"] .block-container {
                padding: 0.5rem !important;
            }
            
            /* Sidebar content smaller */
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                font-size: 1rem !important;
            }
            
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span {
                font-size: 0.85rem !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           DIVIDERS / SEPARATORS - Compact on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            hr {
                margin: 0.75rem 0 !important;
            }
            
            .stDivider {
                margin: 0.5rem 0 !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           CUSTOM MOBILE GRID - For KPI cards
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            /* Create a 2x2 grid for metrics on mobile */
            .mobile-kpi-grid {
                display: grid !important;
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 0.5rem !important;
            }
            
            .mobile-kpi-grid > * {
                min-width: 0 !important;
            }
        }
        
        @media (max-width: 480px) {
            .mobile-kpi-grid {
                grid-template-columns: 1fr !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           SCROLL IMPROVEMENTS - Smooth scrolling on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            html {
                scroll-behavior: smooth;
                -webkit-overflow-scrolling: touch;
            }
            
            /* Prevent horizontal scroll on main container */
            .main {
                overflow-x: hidden !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           TOUCH TARGETS - Minimum 44px for accessibility
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            /* Ensure minimum touch target size */
            button,
            [role="button"],
            a,
            input[type="checkbox"],
            input[type="radio"],
            .stRadio label {
                min-height: 44px !important;
                min-width: 44px !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           HIDE ELEMENTS ON MOBILE - Optional
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            /* Hide less important elements on mobile */
            .hide-on-mobile {
                display: none !important;
            }
            
            /* Show mobile-only elements */
            .show-on-mobile {
                display: block !important;
            }
        }
        
        @media (min-width: 769px) {
            .show-on-mobile {
                display: none !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           FOOTER - Fixed on mobile
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            footer {
                font-size: 0.7rem !important;
            }
            
            .stCaption {
                font-size: 0.7rem !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           VERTICAL SEPARATORS - Hide on mobile (don't make sense)
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            /* Hide vertical separators used between column groups */
            [data-testid="column"]:has(> div > div[style*="border-left"]) {
                display: none !important;
            }
        }

        /* ═══════════════════════════════════════════════════════════════════
           ANIMATION ADJUSTMENTS - Reduce motion for performance
        ═══════════════════════════════════════════════════════════════════ */
        
        @media (max-width: 768px) {
            @media (prefers-reduced-motion: reduce) {
                * {
                    animation: none !important;
                    transition: none !important;
                }
            }
            
            /* Faster animations on mobile */
            .element-container {
                animation-duration: 0.15s !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def get_mobile_column_config(num_columns, screen_size="default"):
    """
    Helper function to determine optimal column configuration based on screen size
    
    Args:
        num_columns: Number of columns requested
        screen_size: 'mobile', 'tablet', or 'default'
    
    Returns:
        Recommended number of columns for the screen size
    """
    if screen_size == "mobile":
        if num_columns <= 2:
            return num_columns
        elif num_columns <= 4:
            return 2
        else:
            return 1
    elif screen_size == "tablet":
        if num_columns <= 3:
            return num_columns
        elif num_columns <= 6:
            return 3
        else:
            return 2
    else:
        return num_columns


def render_mobile_friendly_metrics(metrics_list):
    """
    Render metrics in a mobile-friendly grid layout
    
    Args:
        metrics_list: List of dicts with 'label', 'value', 'delta' keys
    
    Example:
        render_mobile_friendly_metrics([
            {"label": "Ventas", "value": "150", "delta": "+10%"},
            {"label": "NPS", "value": "72", "delta": "-2"},
        ])
    """
    # Add CSS class for mobile grid
    st.markdown('<div class="mobile-kpi-grid">', unsafe_allow_html=True)
    
    # Create columns that will stack on mobile
    num_metrics = len(metrics_list)
    cols = st.columns(min(num_metrics, 4))
    
    for idx, metric in enumerate(metrics_list):
        with cols[idx % len(cols)]:
            st.metric(
                label=metric.get("label", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta"),
                delta_color=metric.get("delta_color", "normal")
            )
    
    st.markdown('</div>', unsafe_allow_html=True)


def add_mobile_navigation_hint():
    """
    Add a hint for mobile users about navigation
    """
    st.markdown(
        """
        <div class="show-on-mobile" style="
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.75rem;
            color: #1E40AF;
            text-align: center;
            margin-bottom: 1rem;
        ">
            👆 Desliza horizontalmente para ver más opciones
        </div>
        """,
        unsafe_allow_html=True,
    )
