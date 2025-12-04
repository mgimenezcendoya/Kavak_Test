"""
Authentication and Authorization System
MVP: Dummy data with role-based access control
Future: Google SSO integration
"""

from datetime import datetime

import streamlit as st

# Dummy users database (MVP)
# In production, this would come from a database or Google SSO
DUMMY_USERS = {
    "admin@kavak.com": {
        "password": "admin123",
        "name": "Carlos Mendoza",
        "role": "CEO",
        "country": "Todos",
        "hub": "Todos",
        "permissions": [
            "executive_dashboard",
            "city_manager_dashboard",
            "kavako_dashboard",
            "reports",
            "admin",
        ],
    },
    "director.mexico@kavak.com": {
        "password": "dir123",
        "name": "María González",
        "role": "Director Regional",
        "country": "México",
        "hub": "Todos",
        "permissions": ["executive_dashboard", "city_manager_dashboard", "reports"],
    },
    "manager.cdmx@kavak.com": {
        "password": "mgr123",
        "name": "Juan Pérez",
        "role": "City Manager",
        "country": "México",
        "hub": "CDMX Norte",
        "permissions": ["city_manager_dashboard", "reports"],
    },
    "agente1@kavak.com": {
        "password": "agt123",
        "name": "Ana Martínez",
        "role": "Kavako",
        "country": "México",
        "hub": "CDMX Norte",
        "agent_id": 1,
        "permissions": ["kavako_dashboard"],
    },
    "agente2@kavak.com": {
        "password": "agt123",
        "name": "Luis García",
        "role": "Kavako",
        "country": "México",
        "hub": "Guadalajara",
        "agent_id": 9,
        "permissions": ["kavako_dashboard"],
    },
}

# Role hierarchy and capabilities
ROLE_CAPABILITIES = {
    "CEO": {
        "description": "Acceso total a todas las vistas y datos",
        "can_view": ["executive", "city_manager", "agent", "customer"],
        "can_filter_by": ["all_countries", "all_hubs"],
        "can_drill_down": True,
        "tabs_visible": [
            "Executive Dashboard (Kavak Admin)",
            "Team Performance (City Manager)",
            "Mi Dashboard (Kavako/Agente)",
        ],
    },
    "Director Regional": {
        "description": "Acceso a su país y todos sus hubs",
        "can_view": ["executive", "city_manager", "agent"],
        "can_filter_by": ["own_country", "all_hubs_in_country"],
        "can_drill_down": True,
        "tabs_visible": [
            "Executive Dashboard (Kavak Admin)",
            "Team Performance (City Manager)",
        ],
    },
    "City Manager": {
        "description": "Acceso a su hub y sus agentes",
        "can_view": ["city_manager", "agent", "customer"],
        "can_filter_by": ["own_hub"],
        "can_drill_down": True,
        "tabs_visible": ["Team Performance (City Manager)"],
    },
    "Kavako": {
        "description": "Acceso solo a su dashboard personal",
        "can_view": ["agent", "customer"],
        "can_filter_by": ["own_data"],
        "can_drill_down": False,
        "tabs_visible": ["Mi Dashboard (Kavako/Agente)"],
    },
}


def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    if "login_time" not in st.session_state:
        st.session_state.login_time = None


def authenticate(email, password):
    """
    Authenticate user with email and password
    Returns: (success: bool, user_info: dict, error_message: str)
    """
    if email in DUMMY_USERS:
        user = DUMMY_USERS[email]
        if user["password"] == password:
            # Successful authentication
            user_info = {
                "email": email,
                "name": user["name"],
                "role": user["role"],
                "country": user["country"],
                "hub": user["hub"],
                "permissions": user["permissions"],
                "agent_id": user.get("agent_id", None),
            }
            return True, user_info, None
        else:
            return False, None, "Contraseña incorrecta"
    else:
        return False, None, "Usuario no encontrado"


def login_user(email, password):
    """
    Login user and set session state
    """
    success, user_info, error = authenticate(email, password)

    if success:
        st.session_state.authenticated = True
        st.session_state.user_email = email
        st.session_state.user_info = user_info
        st.session_state.login_time = datetime.now()
        return True, None
    else:
        return False, error


def logout_user():
    """
    Logout user and clear session state
    """
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_info = None
    st.session_state.login_time = None
    # Clear navigation state
    if "navigation_view" in st.session_state:
        del st.session_state.navigation_view
    if "selected_customer_id" in st.session_state:
        del st.session_state.selected_customer_id
    if "selected_agent_name" in st.session_state:
        del st.session_state.selected_agent_name


def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)


def get_current_user():
    """Get current user info"""
    return st.session_state.get("user_info", None)


def get_user_role():
    """Get current user role"""
    user_info = get_current_user()
    return user_info["role"] if user_info else None


def has_permission(permission):
    """Check if current user has specific permission"""
    user_info = get_current_user()
    if not user_info:
        return False
    return permission in user_info.get("permissions", [])


def can_view_tab(tab_name):
    """Check if current user can view specific tab"""
    role = get_user_role()
    if not role:
        return False

    capabilities = ROLE_CAPABILITIES.get(role, {})
    tabs_visible = capabilities.get("tabs_visible", [])

    # Check if tab is in visible list (partial match)
    for visible_tab in tabs_visible:
        if visible_tab in tab_name or tab_name in visible_tab:
            return True

    return False


def get_accessible_tabs():
    """Get list of tabs accessible to current user"""
    role = get_user_role()
    if not role:
        return []

    capabilities = ROLE_CAPABILITIES.get(role, {})
    return capabilities.get("tabs_visible", [])


def can_access_country(country):
    """Check if user can access data from specific country"""
    user_info = get_current_user()
    if not user_info:
        return False

    role = user_info["role"]
    user_country = user_info.get("country", None)

    # CEO can access all countries
    if role == "CEO":
        return True

    # Others can only access their own country
    if user_country == "Todos":
        return True

    return country == user_country


def can_access_hub(country, hub):
    """Check if user can access data from specific hub"""
    user_info = get_current_user()
    if not user_info:
        return False

    role = user_info["role"]
    user_country = user_info.get("country", None)
    user_hub = user_info.get("hub", None)

    # CEO can access all hubs
    if role == "CEO":
        return True

    # Check country first
    if user_country != "Todos" and country != user_country:
        return False

    # Director Regional can access all hubs in their country
    if role == "Director Regional":
        return True

    # City Manager and Kavako can only access their own hub
    if user_hub == "Todos":
        return True

    return hub == user_hub


def get_filtered_data_for_user(data):
    """
    Filter data based on user's role and permissions
    Returns filtered data dictionary
    """
    user_info = get_current_user()
    if not user_info:
        return data

    role = user_info["role"]

    # CEO sees everything
    if role == "CEO":
        return data

    # Filter based on country and hub
    user_country = user_info.get("country", "Todos")
    user_hub = user_info.get("hub", "Todos")

    filtered_data = {}

    for key, df in data.items():
        if df is None or len(df) == 0:
            filtered_data[key] = df
            continue

        # Check if dataframe has country/hub columns
        if "country" in df.columns:
            if user_country != "Todos":
                df = df[df["country"] == user_country]

            if "hub" in df.columns and user_hub != "Todos":
                df = df[df["hub"] == user_hub]

        filtered_data[key] = df

    return filtered_data


def get_role_description(role):
    """Get description of role capabilities"""
    return ROLE_CAPABILITIES.get(role, {}).get("description", "")


def render_user_info_sidebar():
    """Render user info in sidebar"""
    user_info = get_current_user()

    if user_info:
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 Usuario Actual")
            st.markdown(f"**{user_info['name']}**")
            st.caption(f"📧 {user_info['email']}")
            st.caption(f"🎭 {user_info['role']}")

            if user_info["country"] != "Todos":
                st.caption(f"🌎 {user_info['country']}")

            if user_info["hub"] != "Todos":
                st.caption(f"📍 {user_info['hub']}")

            # Logout button
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                logout_user()
                st.rerun()

            st.markdown("---")

            # Role capabilities
            with st.expander("ℹ️ Mis Permisos"):
                role_desc = get_role_description(user_info["role"])
                st.caption(role_desc)
