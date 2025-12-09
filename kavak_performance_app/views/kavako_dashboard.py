"""
Kavako Dashboard View
Personal agent view with portfolio, appointments, score and performance metrics
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
from config import COLORS, INCENTIVE_GOALS, OPERATION_TYPES, THRESHOLDS
from utils.components import (
    render_alert_box,
    render_funnel_chart,
    render_kpi_card,
    render_kpi_grid,
    render_trend_chart,
)


def render_kavako_dashboard(data, from_city_manager=False):
    """
    Render the Kavako (Agent) personal dashboard
    Redesigned with Hero Header + Today's Focus + Navigation Pills

    Args:
        data: The data dictionary
        from_city_manager: Whether this is being viewed from City Manager drill-down
    """
    # Check if coming from City Manager navigation
    is_drill_down = st.session_state.get("navigation_view") == "agent_profile"
    selected_agent_from_cm = st.session_state.get("selected_agent_name", None)

    if is_drill_down and selected_agent_from_cm:
        # Render breadcrumb navigation for drill-down
        render_breadcrumb_navigation()
        selected_agent = selected_agent_from_cm
    else:
        # Agent selector (in production, this would come from login)
        render_agent_selector(data)
        selected_agent = st.session_state.get("kavako_agent", None)

        if not selected_agent:
            st.info("👈 Selecciona tu nombre en el menú lateral para ver tu dashboard")
            return

    # Get agent data
    operation_type = st.session_state.get("kavako_operation_type", "all")
    agent_data = get_agent_data(data, selected_agent, operation_type)

    if not agent_data:
        st.warning("No se encontraron datos para este agente")
        return

    # ═══════════════════════════════════════════════════════════════════
    # HERO HEADER - Avatar + Name + Level + KPIs
    # ═══════════════════════════════════════════════════════════════════
    render_hero_header(agent_data)

    # ═══════════════════════════════════════════════════════════════════
    # TODAY'S FOCUS - Next appointment with context
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")
    render_todays_focus(agent_data, data)

    # ═══════════════════════════════════════════════════════════════════
    # NAVIGATION PILLS - Secondary sections
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")

    backlog = agent_data.get("backlog_cartera", 0)
    appointments = agent_data.get("appointments", 0)

    selected_section = st.radio(
        "Sección",
        [
            f"📋 Cartera ({backlog:.0f})",
            f"📅 Agenda ({appointments:.0f})",
            "🏆 Mis Puntos",
            "🎯 Objetivos",
        ],
        horizontal=True,
        key="kavako_nav_section",
        label_visibility="collapsed",
    )

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════════════
    # CONTENT ZONE - Based on selected section
    # ═══════════════════════════════════════════════════════════════════
    if "Cartera" in selected_section:
        render_active_portfolio(agent_data, data)

    elif "Agenda" in selected_section:
        render_upcoming_appointments(agent_data, data)

    elif "Puntos" in selected_section:
        render_my_ownership_points(agent_data)

    else:  # Objetivos
        render_my_objectives(agent_data)


def render_hero_header(agent_data):
    """Render Hero Header with avatar, name, level, and KPIs (native Streamlit)"""
    # Get level info
    level = agent_data.get("incentive_level", "🥉 Bronze")
    total_points = agent_data.get("total_points", 0)
    rank = agent_data.get("rank_in_hub", 0)
    total_agents = agent_data.get("total_agents_in_hub", 0)

    # Header row: Info + Level
    col_info, col_level = st.columns([3, 2])

    with col_info:
        st.markdown(f"## 👤 {agent_data['agent_name']}")
        st.caption(
            f"📍 {agent_data['hub']}, {agent_data['country']} • 🏆 **#{rank}** de {total_agents} agentes"
        )

    with col_level:
        st.metric("Nivel", level)
        st.caption(f"**{total_points:,.0f}** puntos")

        # Progress to next level
        levels = [
            ("🥉 Bronze", 0),
            ("🥈 Silver", 500),
            ("🥇 Gold", 1000),
            ("💎 Diamond", 1500),
        ]
        for i, (lvl, threshold) in enumerate(levels):
            if lvl == level and i < len(levels) - 1:
                next_level, next_threshold = levels[i + 1]
                progress = total_points / next_threshold if next_threshold > 0 else 1
                st.progress(min(progress, 1.0), text=f"→ {next_level}")
                break

    # KPIs row
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Entregas",
            f"{agent_data['sales']:.0f}",
            f"{agent_data['sales'] - agent_data['hub_avg_sales']:+.0f}",
        )

    with col2:
        purchases = agent_data.get("purchases_total", 0)
        st.metric("Compras", f"{purchases:.0f}")

    with col3:
        cvr = agent_data["conversion"] * 100
        cvr_delta = (agent_data["conversion"] - agent_data["hub_avg_conversion"]) * 100
        st.metric("CVR", f"{cvr:.1f}%", f"{cvr_delta:+.1f}%")

    with col4:
        nps = agent_data["nps"]
        nps_delta = nps - agent_data["hub_avg_nps"]
        st.metric("NPS", f"{nps:.0f}", f"{nps_delta:+.0f}")

    with col5:
        ownership = agent_data.get("ownership_score", 0)
        st.metric("Ownership", f"{ownership:.0f}%")


def render_todays_focus(agent_data, data):
    """Render Today's Focus widget with next appointment (native Streamlit)"""
    st.markdown("### 🎯 Tu Foco de Hoy")

    customers_df = data.get("customers", pd.DataFrame())

    if len(customers_df) == 0:
        st.info("No hay citas programadas para hoy")
        return

    # Get appointments for this agent's hub
    agent_customers = customers_df[customers_df["hub"] == agent_data["hub"]]

    if len(agent_customers) == 0:
        st.info("No hay citas programadas para hoy")
        return

    # Get next appointment (simulated - take highest score customer)
    next_customer = agent_customers.nlargest(1, "customer_score").iloc[0]

    # Get Celeste context
    celeste_summary = next_customer.get("celeste_summary", "")
    budget = next_customer.get("celeste_budget_range", "No especificado")
    vehicles = next_customer.get("celeste_vehicles_shown", [])
    objections = next_customer.get("celeste_main_objections", [])
    recommendations = next_customer.get("celeste_recommendations", [])

    # Appointment time (simulated - use cached value)
    cache_key = f"focus_time_{agent_data['agent_id']}"
    if cache_key not in st.session_state:
        st.session_state[cache_key] = f"{np.random.randint(9, 14)}:00"
    appt_time = st.session_state[cache_key]

    # Main focus card using container
    with st.container(border=True):
        col_header, col_score = st.columns([3, 1])

        with col_header:
            st.markdown(f"### ⏰ {appt_time} - Demo Programada")
            st.markdown(f"## {next_customer['customer_name']}")
            st.caption(f"💰 Presupuesto: {budget}")

        with col_score:
            score = next_customer["customer_score"]
            score_emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
            st.metric("Sentinel", f"{score_emoji} {score}/100")

        # Celeste summary
        if celeste_summary:
            st.info(f"💬 **Resumen Celeste:** {celeste_summary}")

        # Key info row
        col_info1, col_info2, col_info3 = st.columns(3)

        with col_info1:
            if vehicles:
                fav = vehicles[0]
                st.success(
                    f"🚗 **{fav['brand']} {fav['model']} {fav['year']}**\n\n📍 Lote {fav['lote']}"
                )

        with col_info2:
            if objections:
                st.warning(
                    "**⚠️ Dudas:**\n\n"
                    + "\n".join([f"• {obj}" for obj in objections[:2]])
                )

        with col_info3:
            if recommendations:
                st.info(f"**💡 Tip:**\n\n{recommendations[0]}")

        # Actions row
        st.markdown("---")
        col_a1, col_a2, col_a3 = st.columns(3)

        with col_a1:
            if st.button(
                "📱 Ver Contexto Completo", key="focus_context", use_container_width=True
            ):
                st.session_state.selected_customer_id = next_customer["customer_id"]
                st.session_state.navigation_view = "customer_profile"
                st.rerun()

        with col_a2:
            if st.button("📞 Llamar", key="focus_call", use_container_width=True):
                st.toast(f"📱 {next_customer['phone']}")

        with col_a3:
            if vehicles:
                if st.button(
                    "📍 Ubicar Auto", key="focus_locate", use_container_width=True
                ):
                    st.toast(f"📍 Ir a Lote {vehicles[0]['lote']}")

        # Celeste Copilot hint
        st.markdown("---")
        st.markdown(
            """
            <div style="
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 16px;
                background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(91, 33, 182, 0.1) 100%);
                border-radius: 10px;
                border-left: 4px solid #7C3AED;
            ">
                <span style="font-size: 1.5rem;">🤖</span>
                <div>
                    <div style="font-weight: 600; color: #5B21B6;">¿Necesitas ayuda con este cliente?</div>
                    <div style="font-size: 0.85rem; color: #6B7280;">Usa el botón <strong>"Celeste"</strong> abajo a la derecha para consultar alternativas, tips y más.</div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Upcoming appointments preview
    st.markdown("---")
    st.caption("**Próximas citas:**")

    # Get more customers for preview
    other_customers = agent_customers.nlargest(4, "customer_score").iloc[1:4]

    if len(other_customers) > 0:
        cols = st.columns(len(other_customers))
        for idx, (_, c) in enumerate(other_customers.iterrows()):
            with cols[idx]:
                st.caption(f"🕐 {10 + idx * 2}:00 - {c['customer_name']}")


def render_breadcrumb_navigation():
    """Render navigation breadcrumb for drill-down from City Manager"""
    breadcrumb = st.session_state.get("nav_breadcrumb", [])

    if len(breadcrumb) > 0:
        cols = st.columns(len(breadcrumb) * 2 - 1 if len(breadcrumb) > 1 else 1)

        for i, crumb in enumerate(breadcrumb):
            with cols[i * 2] if len(breadcrumb) > 1 else cols[0]:
                if i < len(breadcrumb) - 1:
                    # Clickeable - navigate back
                    if st.button(f"🏠 {crumb['label']}", key=f"breadcrumb_{i}"):
                        st.session_state.navigation_view = None
                        st.session_state.selected_agent_name = None
                        st.session_state.nav_breadcrumb = []
                        st.rerun()
                else:
                    # Current page
                    st.markdown(f"**📍 {crumb['label']}**")

            if i < len(breadcrumb) - 1 and len(breadcrumb) > 1:
                with cols[i * 2 + 1]:
                    st.markdown("**→**")

        st.markdown("---")


def render_agent_selector(data):
    """Render agent selector in sidebar"""
    agents_df = data["agent_performance"]

    with st.sidebar:
        st.markdown("### 👤 Selecciona tu usuario")

        # Group by hub for better organization
        hub_options = sorted(agents_df["hub"].unique())
        selected_hub = st.selectbox("Tu Hub", hub_options, key="kavako_hub_selector")

        # Filter agents by hub
        hub_agents = agents_df[agents_df["hub"] == selected_hub]["agent_name"].tolist()
        selected_agent = st.selectbox("Tu Nombre", hub_agents, key="kavako_agent")

        # Store customer context for Celeste Copilot (floating widget)
        customers_df = data.get("customers", pd.DataFrame())

        if len(customers_df) > 0 and selected_agent:
            # Find agent's hub customers for context
            agent_row = agents_df[agents_df["agent_name"] == selected_agent]
            if len(agent_row) > 0:
                agent_hub = agent_row.iloc[0]["hub"]
                agent_customers = customers_df[customers_df["hub"] == agent_hub]
                if len(agent_customers) > 0:
                    # Use highest score customer as context
                    top_customer = agent_customers.nlargest(1, "customer_score").iloc[0]
                    st.session_state.copilot_customer_context = top_customer.to_dict()


def apply_agent_operation_filter(agent_dict, operation_type):
    """
    Apply operation type filter to a single agent's data
    Returns modified agent_dict with adjusted metrics
    """
    if operation_type == "sales":
        # Only count sales operations
        agent_dict["sales"] = agent_dict.get("sales_only", 0) + agent_dict.get(
            "sales_tradein", 0
        )
        agent_dict["conversion"] = (
            agent_dict["sales"] / agent_dict["leads"]
            if agent_dict.get("leads", 0) > 0
            else 0
        )
        agent_dict["revenue"] = agent_dict["sales"] * 20000

    elif operation_type == "purchases":
        # Only count purchase operations
        agent_dict["sales"] = agent_dict.get("purchases_total", 0)
        agent_dict["conversion"] = (
            agent_dict["sales"] / agent_dict["leads"]
            if agent_dict.get("leads", 0) > 0
            else 0
        )
        agent_dict["revenue"] = agent_dict["sales"] * 18000

    elif operation_type == "tradein":
        # Only count trade-in operations
        agent_dict["sales"] = agent_dict.get("sales_tradein", 0)
        agent_dict["conversion"] = (
            agent_dict["sales"] / agent_dict["leads"]
            if agent_dict.get("leads", 0) > 0
            else 0
        )
        agent_dict["revenue"] = agent_dict["sales"] * 20000

    return agent_dict


def get_agent_data(data, agent_name, operation_type="all"):
    """Get all data for a specific agent, filtered by operation type"""
    agents_df = data["agent_performance"].copy()

    agent_row = agents_df[agents_df["agent_name"] == agent_name]

    if len(agent_row) == 0:
        return None

    agent_info = agent_row.iloc[0].to_dict()

    # Apply operation type filter
    if operation_type != "all":
        agent_info = apply_agent_operation_filter(agent_info, operation_type)

    # Add hub data for comparison
    hub = agent_info["hub"]
    country = agent_info["country"]
    hub_agents = agents_df[
        (agents_df["hub"] == hub) & (agents_df["country"] == country)
    ]

    # Apply same filter to hub comparison
    if operation_type != "all":
        hub_agents = hub_agents.apply(
            lambda row: pd.Series(
                apply_agent_operation_filter(row.to_dict(), operation_type)
            ),
            axis=1,
        )

    agent_info["hub_agents"] = hub_agents
    agent_info["hub_avg_conversion"] = hub_agents["conversion"].mean()
    agent_info["hub_avg_nps"] = hub_agents["nps"].mean()
    agent_info["hub_avg_sales"] = hub_agents["sales"].mean()
    agent_info["operation_type"] = operation_type

    # Calculate rank in hub
    sorted_agents = hub_agents.sort_values("sales", ascending=False).reset_index(
        drop=True
    )
    agent_info["rank_in_hub"] = (
        sorted_agents[sorted_agents["agent_name"] == agent_name].index[0] + 1
    )
    agent_info["total_agents_in_hub"] = len(hub_agents)

    return agent_info


def render_personal_summary(agent_data, operation_type="all"):
    """Render personal summary header"""
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"### 👤 {agent_data['agent_name']}")
        st.caption(f"📍 {agent_data['hub']}, {agent_data['country']}")

        # Show ranking in hub
        rank = agent_data.get("rank_in_hub", 0)
        total_agents = agent_data.get("total_agents_in_hub", 0)
        st.caption(f"🏆 Ranking: **#{rank}** de {total_agents} agentes")

        # Show operation type filter status
        if operation_type != "all":
            operation_label = OPERATION_TYPES.get(operation_type, "")
            st.caption(f"🔍 Filtrando: **{operation_label}**")

    with col2:
        # Entregas del Periodo
        if operation_type == "purchases":
            label = "🔵 Compras del Periodo"
        elif operation_type == "tradein":
            label = "🔄 Trade-ins del Periodo"
        else:
            label = "🚗 Entregas del Periodo"

        st.metric(
            label,
            f"{agent_data['sales']:.0f}",
            f"{agent_data['sales'] - agent_data['hub_avg_sales']:+.0f} vs promedio",
        )

    with col3:
        # Compras (purchases) - mostrar solo si es "all" o no hay filtro
        purchases = agent_data.get("purchases_total", 0)
        st.metric(
            "🔵 Compras",
            f"{purchases:.0f}",
        )

    with col4:
        # Conversión
        conversion_pct = agent_data["conversion"] * 100
        conversion_vs_hub = (
            (agent_data["conversion"] / agent_data["hub_avg_conversion"]) - 1
        ) * 100

        st.metric(
            "🎯 Conversión",
            f"{conversion_pct:.1f}%",
            f"{conversion_vs_hub:+.1f}% vs hub",
        )

    with col5:
        # NPS metric
        my_nps = agent_data["nps"]
        hub_nps = agent_data["hub_avg_nps"]
        diff_nps = my_nps - hub_nps

        st.metric(
            "⭐ NPS",
            f"{my_nps:.0f}",
            f"{diff_nps:+.0f} pts vs hub",
        )

    # Second row: Ancillaries metrics
    st.markdown("---")
    st.markdown("#### 🛡️ Venta de Ancilares y Financiamiento")

    col_anc1, col_anc2, col_anc3, col_anc4 = st.columns(4)

    with col_anc1:
        insurance_penetration = agent_data.get("insurance_penetration", 0)
        insurance_sold = agent_data.get("insurance_sold", 0)
        st.metric(
            "🛡️ Seguros",
            f"{insurance_penetration:.1f}%",
            f"{insurance_sold:.0f} vendidos",
        )

    with col_anc2:
        warranty_penetration = agent_data.get("extended_warranty_penetration", 0)
        warranty_sold = agent_data.get("extended_warranty_sold", 0)
        st.metric(
            "⭐ Kavak Total (Garantía)",
            f"{warranty_penetration:.1f}%",
            f"{warranty_sold:.0f} vendidos",
        )

    with col_anc3:
        financing_penetration = agent_data.get("financing_penetration", 0)
        financing_sold = agent_data.get("financing_sold", 0)
        st.metric(
            "💰 Financing",
            f"{financing_penetration:.1f}%",
            f"{financing_sold:.0f} financiados",
        )

    with col_anc4:
        total_ancillary_penetration = agent_data.get("ancillary_penetration", 0)
        total_ancillaries = agent_data.get("total_ancillaries", 0)
        st.metric(
            "📦 Penetración Ancilares",
            f"{total_ancillary_penetration:.1f}%",
            f"{total_ancillaries:.0f} productos",
        )


def render_active_portfolio(agent_data, data):
    """Render active portfolio (cartera activa) linked to real customers"""
    st.subheader("📋 Mi Cartera Activa")

    # Portfolio stats
    backlog = agent_data.get("backlog_cartera", 0)
    total_opportunities = agent_data.get("total_opportunities", 0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Leads en Seguimiento", f"{backlog:.0f}")

    with col2:
        st.metric("Oportunidades Totales", f"{total_opportunities:.0f}")

    with col3:
        conversion_on_opportunities = agent_data.get("aprovechamiento_pct", 0)
        st.metric("% Aprovechamiento", f"{conversion_on_opportunities:.1f}%")

    # Get real customers for this agent
    customers_df = data.get("customers", pd.DataFrame())

    if len(customers_df) > 0:
        # Filter customers for this agent's hub and status that are active leads
        agent_customers = customers_df[
            (customers_df["hub"] == agent_data["hub"])
            & (customers_df["status"].isin(["Nuevo", "Activo"]))
        ]

        # Take top 5 by score
        top_customers = agent_customers.nlargest(5, "customer_score")

        st.markdown("#### Leads Activos (Top 5 Prioritarios)")
        st.caption(
            "💡 Haz clic en 'Ver Perfil' para acceder al historial completo del cliente"
        )

        if len(top_customers) > 0:
            # Prepare data for table
            portfolio_data = []
            for idx, (_, customer) in enumerate(top_customers.iterrows()):
                days_registered = customer["days_since_registration"]
                days_since_last = (
                    datetime.now() - customer["last_interaction_date"]
                ).days

                # Priority based on score and time since last contact
                if customer["customer_score"] > 70 and days_since_last < 7:
                    priority = "🔴 Alta"
                elif customer["customer_score"] > 50 or days_since_last < 14:
                    priority = "🟡 Media"
                else:
                    priority = "🟢 Baja"

                # Determine next action
                if days_since_last > 7:
                    next_action = "Contactar pronto"
                elif customer["customer_score"] > 70:
                    next_action = "Agendar cita"
                else:
                    next_action = "Seguimiento"

                portfolio_data.append(
                    {
                        "Lead ID": customer["customer_id"],
                        "Días en Cartera": days_registered,
                        "Días desde última interacción": days_since_last,
                        "Sentinel Score": customer["customer_score"],
                        "Estado": customer["status"],
                        "Prioridad": priority,
                        "Próxima Acción": next_action,
                    }
                )

            # Display table
            portfolio_df = pd.DataFrame(portfolio_data)
            st.dataframe(portfolio_df, use_container_width=True, hide_index=True)
        else:
            st.info("✅ No tienes leads activos en cartera")
    else:
        st.warning("No hay datos de clientes disponibles")


def render_upcoming_appointments(agent_data, data):
    """Render upcoming appointments calendar using appointments dataframe"""
    st.subheader("📅 Mis Citas Próximas")

    # Appointment stats
    appointments_count = agent_data.get("appointments", 0)
    utilization = agent_data.get("utilization", 0) * 100

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Citas Agendadas", f"{appointments_count:.0f}")

    with col2:
        st.metric("Utilización Agenda", f"{utilization:.0f}%")

    # Get appointments dataframe
    appointments_df = data.get("appointments", pd.DataFrame())
    customers_df = data.get("customers", pd.DataFrame())

    if len(appointments_df) == 0:
        st.warning("No hay datos de citas disponibles")
        return

    # Filter appointments for this agent's hub and future dates
    today = datetime.now().date()
    week_ahead = today + timedelta(days=7)

    hub_appointments = appointments_df[
        (appointments_df["hub"] == agent_data["hub"])
        & (appointments_df["date"] >= today)
        & (appointments_df["date"] <= week_ahead)
        & (appointments_df["status"].isin(["Confirmada", "Pendiente", "Por Confirmar"]))
    ].copy()

    # Sort by datetime
    hub_appointments = hub_appointments.sort_values("datetime")

    st.markdown("#### Próximos 7 Días")
    st.caption(
        "💡 Revisa el contexto de Celeste antes de cada cita para una mejor atención"
    )

    if len(hub_appointments) == 0:
        st.info("No tienes citas agendadas en los próximos 7 días")
        return

    # Show count
    st.caption(f"**{len(hub_appointments)} citas programadas**")

    # Render appointments in scrollable container
    with st.container(height=600):
        for idx, (_, appt) in enumerate(hub_appointments.iterrows()):
            date_str = appt["date"].strftime("%d/%m/%Y")

            # Status color
            status_colors = {
                "Confirmada": "green",
                "Pendiente": "orange",
                "Por Confirmar": "red",
            }
            status_color = status_colors.get(appt["status"], "gray")

            # Compact header row with key info and button
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1.5, 1])

            with col1:
                st.markdown(f"**{date_str} {appt['time']}**")

            with col2:
                st.markdown(f"**{appt['customer_name']}**")

            with col3:
                st.caption(f"**{appt['type_icon']} {appt['appointment_type']}**")

            with col4:
                st.markdown(f"**Estado:** :{status_color}[{appt['status']}]")

            with col5:
                # Button to view customer profile
                button_clicked = st.button(
                    "👁️ Ver",
                    key=f"view_appt_{appt['appointment_id']}_{idx}",
                    help="Ver perfil del cliente",
                    use_container_width=True,
                )

            # Handle button click
            if button_clicked:
                st.session_state.selected_customer_id = appt["customer_id"]
                st.session_state.navigation_view = "customer_profile"
                st.rerun()

            # Expandable details
            with st.expander(f"📱 Detalles - {appt['customer_name']}", expanded=False):
                col_detail1, col_detail2 = st.columns(2)

                with col_detail1:
                    st.markdown("**📋 Datos de la Cita:**")
                    st.caption(f"• ID: {appt['appointment_id']}")
                    st.caption(f"• Tipo: {appt['appointment_type']}")
                    st.caption(f"• Duración: {appt['duration_min']} min")
                    st.caption(f"• Prioridad: {appt['priority']}")

                with col_detail2:
                    st.markdown("**🚗 Vehículo de Interés:**")
                    st.success(f"{appt['vehicle_interest']}")
                    st.caption(f"Precio: ${appt['vehicle_price']:,.0f}")

                # Notes
                if appt.get("notes"):
                    st.info(f"📝 **Notas:** {appt['notes']}")

                # Try to get customer context from customers_df
                if len(customers_df) > 0:
                    customer_match = customers_df[
                        customers_df["customer_id"] == appt["customer_id"]
                    ]
                    if len(customer_match) > 0:
                        customer = customer_match.iloc[0]
                        celeste_summary = customer.get("celeste_summary", "")
                        if celeste_summary:
                            st.markdown("---")
                            st.info(f"🤖 **Contexto Celeste:** {celeste_summary}")

                        recommendations = customer.get("celeste_recommendations", [])
                        if recommendations:
                            st.markdown("**💡 Tips:**")
                            for rec in recommendations[:2]:
                                st.success(f"✅ {rec}")

                # Contact info
                st.markdown("---")
                st.caption(f"📱 {appt['customer_phone']}")

            st.markdown("---")


def render_my_objectives(agent_data):
    """Render personal objectives and progress"""

    with st.expander("🎯 Mis Objetivos e Incentivos", expanded=False):
        st.markdown("#### Objetivos Disponibles")

        for goal in INCENTIVE_GOALS:
            metric = goal["metric"]
            threshold = goal["threshold"]
            points = goal["points"]
            is_inverse = goal.get("inverse", False)

            if metric in agent_data:
                current_value = agent_data[metric]

                # Determine if achieved
                if is_inverse:
                    achieved = current_value <= threshold
                    progress = (
                        (threshold / current_value * 100) if current_value > 0 else 0
                    )
                else:
                    achieved = current_value >= threshold
                    progress = (current_value / threshold * 100) if threshold > 0 else 0

                progress = min(100, progress)

                st.markdown(
                    f"**{'✅' if achieved else '⏳'} {goal['name']} ({points} puntos)**"
                )
                st.markdown(f"_{goal['description']}_")

                # Format current value
                if metric == "conversion" or metric == "noshow":
                    current_display = f"{current_value * 100:.1f}%"
                    threshold_display = f"{threshold * 100:.0f}%"
                else:
                    current_display = f"{current_value:.1f}"
                    threshold_display = f"{threshold:.0f}"

                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"Tu valor: {current_display}")
                with col2:
                    st.caption(f"Meta: {threshold_display}")

                # Progress bar
                st.progress(progress / 100)

                if achieved:
                    st.success(f"🎉 ¡Objetivo logrado! +{points} puntos")
                else:
                    remaining = (
                        threshold - current_value
                        if not is_inverse
                        else current_value - threshold
                    )
                    if metric == "conversion" or metric == "noshow":
                        st.info(
                            f"Te faltan {abs(remaining) * 100:.1f} puntos porcentuales"
                        )
                    else:
                        st.info(f"Te faltan {abs(remaining):.0f} para lograrlo")

                st.markdown("---")


def render_my_ownership_points(agent_data):
    """Render the agent's ownership score and composite points (native Streamlit)"""
    st.subheader("🏆 Mis Puntos & Ownership")

    # Check if new columns exist
    if "total_points" not in agent_data:
        st.info("⏳ Reinicia la aplicación para cargar las nuevas métricas")
        return

    # Get data
    total_points = agent_data.get("total_points", 0)
    level = agent_data.get("incentive_level", "🥉 Bronze")
    ownership = agent_data.get("ownership_score", 0)

    # Levels for progress calculation
    levels = [("🥉 Bronze", 0), ("🥈 Silver", 500), ("🥇 Gold", 1000), ("💎 Diamond", 1500)]

    # Find current and next level
    next_level = None
    next_threshold = 0
    progress_pct = 100
    for i, (lvl, threshold) in enumerate(levels):
        if lvl == level and i < len(levels) - 1:
            next_level, next_threshold = levels[i + 1]
            progress_pct = (
                (total_points / next_threshold * 100) if next_threshold > 0 else 100
            )
            break

    # ═══════════════════════════════════════════════════════════════════
    # LEVEL + PROGRESS
    # ═══════════════════════════════════════════════════════════════════
    col_level, col_progress = st.columns([1, 2])

    with col_level:
        st.metric("Nivel Actual", level)
        st.metric("Puntos Totales", f"{total_points:,.0f}")

    with col_progress:
        if next_level:
            st.markdown(f"**Próximo nivel:** {next_level}")
            st.progress(min(progress_pct / 100, 1.0))
            st.caption(f"Faltan **{next_threshold - total_points:,.0f}** puntos")
        else:
            st.success("🎉 ¡Ya estás en el nivel máximo!")

    # ═══════════════════════════════════════════════════════════════════
    # POINTS BREAKDOWN
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("#### 📊 Desglose de Puntos")

    breakdown = [
        ("🚗 Base (entregas)", agent_data.get("base_points", 0)),
        ("💰 Financing", agent_data.get("financing_points", 0)),
        ("⭐ Kavak Total", agent_data.get("warranty_points", 0)),
        ("🛡️ Seguro", agent_data.get("insurance_points", 0)),
        ("🔄 Trade-in", agent_data.get("tradein_points", 0)),
        ("📈 NPS Bonus", agent_data.get("nps_bonus", 0)),
    ]

    total = sum([b[1] for b in breakdown])

    cols = st.columns(3)
    for idx, (label, points) in enumerate(breakdown):
        pct = (points / total * 100) if total > 0 else 0
        with cols[idx % 3]:
            st.metric(label, f"+{points:,.0f} pts", f"{pct:.0f}%")

    # ═══════════════════════════════════════════════════════════════════
    # OWNERSHIP + TIPS
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")

    col_own, col_tips = st.columns(2)

    with col_own:
        st.markdown("#### 🤝 Ownership Score")

        handoffs = agent_data.get("handoffs", 0)
        sales = agent_data.get("sales", 0)

        # Progress bar for ownership
        st.progress(
            ownership / 100,
            text=f"{ownership:.0f}% de clientes manejados de inicio a fin",
        )

        col_o1, col_o2 = st.columns(2)
        with col_o1:
            st.metric("Entregas", f"{sales:.0f}")
        with col_o2:
            st.metric("Handoffs", f"{handoffs:.0f}")

        # Status indicator
        if ownership >= 90:
            st.success("🌟 Excelente autonomía")
        elif ownership >= 75:
            st.info("👍 Buen ownership")
        else:
            st.warning("📊 Reducir handoffs mejorará tu score")

    with col_tips:
        st.markdown("#### 💡 Cómo ganar más puntos")

        tips = []

        if agent_data.get("financing_penetration", 0) < 50:
            tips.append(("📈 Aumenta financing", "+50 pts/venta"))

        if agent_data.get("ancillary_penetration", 0) < 40:
            tips.append(("🛡️ Ofrece Kavak Total", "+30 pts"))

        if agent_data.get("nps", 0) < 80:
            tips.append(("⭐ Mejora NPS a 80+", "+25 pts/entrega"))

        if not tips:
            st.success("✅ ¡Estás maximizando tus puntos!")
        else:
            for tip, reward in tips:
                with st.container(border=True):
                    col_t1, col_t2 = st.columns([3, 1])
                    with col_t1:
                        st.caption(tip)
                    with col_t2:
                        st.caption(f"**{reward}**")
