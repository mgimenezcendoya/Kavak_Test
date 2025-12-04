"""
Login View
Authentication interface for users
"""

import streamlit as st
from utils.auth import DUMMY_USERS, ROLE_CAPABILITIES, login_user


def render_login_page():
    """
    Render login page with Kavak branding
    """
    # Apply Kavak brand styling for login page
    st.markdown(
        """
        <style>
        .login-container {
            background: linear-gradient(135deg, #0B4FD6 0%, #003DAC 100%);
            padding: 3rem;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(11,79,214,0.2);
        }
        .login-header {
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }
        .kavak-logo {
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: 0.1em;
            color: white;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .login-subtitle {
            color: rgba(255,255,255,0.9);
            text-align: center;
            font-size: 1.1rem;
            font-weight: 400;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Kavak branding
        st.markdown(
            """
            <div class="login-header">
                <div class="kavak-logo">KAVAK</div>
                <div class="login-subtitle">Performance Dashboard</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Login form
        with st.form("login_form"):
            st.markdown("### 🔐 Iniciar Sesión")

            email = st.text_input(
                "Email",
                placeholder="usuario@kavak.com",
                help="Ingresa tu email corporativo",
            )

            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="••••••••",
                help="Ingresa tu contraseña",
            )

            submit = st.form_submit_button("Ingresar", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("❌ Por favor ingresa email y contraseña")
                else:
                    success, error = login_user(email, password)

                    if success:
                        st.success("✅ ¡Login exitoso! Redirigiendo...")
                        st.rerun()
                    else:
                        st.error(f"❌ {error}")

        # Demo users section
        st.markdown("---")

        with st.expander("👥 Usuarios Demo (MVP)", expanded=False):
            st.markdown("**Para probar la aplicación, usa estos usuarios:**")
            st.markdown("")

            # CEO
            st.markdown("**🎯 Kavak Admin (Acceso Total)**")
            st.code("Email: admin@kavak.com\nContraseña: admin123")
            st.caption("✓ Ve todos los países y hubs")
            st.caption("✓ Acceso a todas las vistas")
            st.markdown("")

            # Director Regional
            st.markdown("**🌎 Director Regional México**")
            st.code("Email: director.mexico@kavak.com\nContraseña: dir123")
            st.caption("✓ Ve solo México (todos los hubs)")
            st.caption("✓ Acceso a Executive y City Manager")
            st.markdown("")

            # City Manager
            st.markdown("**📍 City Manager CDMX Norte**")
            st.code("Email: manager.cdmx@kavak.com\nContraseña: mgr123")
            st.caption("✓ Ve solo CDMX Norte")
            st.caption("✓ Acceso a City Manager")
            st.markdown("")

            # Kavako
            st.markdown("**👤 Agente (Kavako) CDMX Norte**")
            st.code("Email: agente1@kavak.com\nContraseña: agt123")
            st.caption("✓ Ve solo su información personal")
            st.caption("✓ Acceso a Mi Dashboard")

        # SSO note
        st.markdown("---")
        st.info("🔮 **Próximamente:** Integración con Google SSO para login automático")

        # Footer
        st.markdown("---")
        st.caption("© 2025 Kavak. Todos los derechos reservados.")


def render_role_info_card():
    """
    Render information about roles and permissions
    """
    st.markdown("### 🎭 Roles y Permisos")

    for role, capabilities in ROLE_CAPABILITIES.items():
        with st.expander(f"**{role}**"):
            st.markdown(f"**Descripción:** {capabilities['description']}")
            st.markdown(
                f"**Vistas disponibles:** {', '.join(capabilities['tabs_visible'])}"
            )
            st.markdown(
                f"**Drill-down:** {'Sí ✅' if capabilities['can_drill_down'] else 'No ❌'}"
            )
