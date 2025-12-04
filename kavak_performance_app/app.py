"""
Kavak Performance App - Streamlit Dashboard
Aplicación de performance y operación para CEO y City Managers
Con sistema de autenticación y control de acceso por roles
"""

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

# Import authentication
from utils.auth import (
    can_view_tab,
    get_accessible_tabs,
    get_current_user,
    get_filtered_data_for_user,
    init_session_state,
    is_authenticated,
    render_user_info_sidebar,
)
from utils.components import (
    apply_custom_styles,
    render_alert_box,
    render_kpi_card,
    render_metric_comparison,
)
from utils.mobile_styles import apply_mobile_styles

# Import custom modules
from utils.data_generator import generate_sample_data
from views.ceo_dashboard import render_ceo_dashboard
from views.city_manager_dashboard import render_city_manager_dashboard
from views.customer_profile import render_customer_profile
from views.kavako_dashboard import render_kavako_dashboard
from views.login import render_login_page

# Page configuration
st.set_page_config(
    page_title="Kavak Performance App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom styling
apply_custom_styles()

# Apply mobile-responsive styles (archivo separado para iterar fácilmente)
apply_mobile_styles()

# Initialize authentication state
init_session_state()

# Initialize session state for data
if "data" not in st.session_state:
    st.session_state.data = generate_sample_data()

# Check authentication
if not is_authenticated():
    # Show login page
    render_login_page()
else:
    # User is authenticated
    user_info = get_current_user()

    # Render user info in sidebar
    render_user_info_sidebar()

    # Get filtered data based on user role
    filtered_data = get_filtered_data_for_user(st.session_state.data)

    # Check if we're in a drill-down view
    navigation_view = st.session_state.get("navigation_view", None)
    selected_customer = st.session_state.get("selected_customer_id", None)

    if navigation_view == "agent_profile":
        # Show agent profile using unified kavako dashboard (drill-down from city manager)
        render_kavako_dashboard(st.session_state.data, from_city_manager=True)
    elif navigation_view == "customer_profile":
        # Show customer profile (drill-down from agent/kavako)
        render_customer_profile(st.session_state.data)
    else:
        # Show normal tab view
        # Main header
        st.title(f"🚗 Kavak Performance App")
        st.markdown(f"### Bienvenido, {user_info['name']}")
        st.markdown("---")

        # Get accessible tabs for this user
        accessible_tabs = get_accessible_tabs()

        if not accessible_tabs:
            st.error("⛔ No tienes permisos para acceder a ninguna vista")
            st.info("Contacta al administrador para solicitar acceso")
        else:
            # Create tabs based on permissions
            tabs_to_show = []
            tab_renderers = []

            if "Executive Dashboard (Kavak Admin)" in str(accessible_tabs):
                tabs_to_show.append("📊 Executive Dashboard (Kavak Admin)")
                tab_renderers.append(("ceo", render_ceo_dashboard, "filtered"))

            if "Team Performance (City Manager)" in str(accessible_tabs):
                tabs_to_show.append("👥 Team Performance (City Manager)")
                tab_renderers.append(
                    ("city_manager", render_city_manager_dashboard, "filtered")
                )

            if "Mi Dashboard (Kavako/Agente)" in str(accessible_tabs):
                tabs_to_show.append("👤 Mi Dashboard (Kavako/Agente)")
                tab_renderers.append(("kavako", render_kavako_dashboard, "full"))

            # Add Clientes tab for all roles
            tabs_to_show.append("🧑‍💼 Clientes")
            tab_renderers.append(("clientes", render_customer_profile, "full"))

            # Check if we should render customer profile directly (drill-down from other views)
            selected_customer = st.session_state.get("selected_customer_id", None)

            if selected_customer:
                # Render customer profile directly without tabs
                render_customer_profile(st.session_state.data)
            else:
                # Create tabs dynamically
                if len(tabs_to_show) == 1:
                    # Only one tab, no need for tabs UI
                    st.markdown(f"### {tabs_to_show[0]}")
                    _, renderer, data_type = tab_renderers[0]
                    data_to_pass = (
                        st.session_state.data if data_type == "full" else filtered_data
                    )
                    renderer(data_to_pass)
                else:
                    # Multiple tabs
                    tabs = st.tabs(tabs_to_show)

                    for idx, (tab_key, renderer, data_type) in enumerate(tab_renderers):
                        with tabs[idx]:
                            data_to_pass = (
                                st.session_state.data
                                if data_type == "full"
                                else filtered_data
                            )
                            renderer(data_to_pass)

        # Footer
        st.markdown("---")
        st.caption(
            f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
