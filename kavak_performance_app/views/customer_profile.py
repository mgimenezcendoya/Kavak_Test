"""
Customer Profile View
Comprehensive customer view with transaction history, interests, and interactions
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
from config import COLORS, VEHICLE_SEGMENTS
from utils.celeste_copilot import render_celeste_insights_card
from utils.components import render_alert_box, render_kpi_card


def render_customer_profile(data):
    """
    Render comprehensive customer profile
    Redesigned with Hero Brief first for quick context

    Can be accessed:
    1. Directly from Clientes tab (search interface)
    2. From agent's agenda (with selected_customer_id in session state)
    """
    # Check if customer_id is in session state (drill-down from agent)
    customer_id = st.session_state.get("selected_customer_id", None)

    if not customer_id:
        # Show search interface when accessed directly
        render_customer_search_improved(data)
        return

    # Get customer data
    customers_df = data.get("customers", pd.DataFrame())

    if len(customers_df) == 0:
        st.error("No hay datos de clientes disponibles")
        return

    customer = customers_df[customers_df["customer_id"] == customer_id]

    if len(customer) == 0:
        st.warning(f"Cliente {customer_id} no encontrado")
        st.session_state.selected_customer_id = None
        render_customer_search_improved(data)
        return

    customer_info = customer.iloc[0].to_dict()

    # Store customer context for Celeste Copilot
    st.session_state.copilot_customer_context = customer_info

    # ═══════════════════════════════════════════════════════════════════
    # BACK BUTTON (Compact)
    # ═══════════════════════════════════════════════════════════════════
    if st.button("⬅️ Volver a Clientes", key="back_to_clients"):
        st.session_state.selected_customer_id = None
        if "navigation_view" in st.session_state:
            st.session_state.navigation_view = None
        st.rerun()

    # ═══════════════════════════════════════════════════════════════════
    # HERO BRIEF - First thing agent sees (30 second summary)
    # ═══════════════════════════════════════════════════════════════════
    render_hero_brief(customer_info)

    # ═══════════════════════════════════════════════════════════════════
    # ACTION BAR - Quick actions
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")
    render_action_bar(customer_info)

    # ═══════════════════════════════════════════════════════════════════
    # TABS - Reordered by frequency of use
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📱 Contexto Celeste",
            "🚗 Vehículos",
            "🛒 Historial",
            "📞 Interacciones",
            "📊 Resumen",
        ]
    )

    with tab1:
        render_celeste_context_improved(customer_info)

    with tab2:
        render_vehicle_interests(customer_info)

    with tab3:
        render_transaction_history(customer_info)

    with tab4:
        render_interactions_log(customer_info)

    with tab5:
        render_customer_summary(customer_info, data)


def render_hero_brief(customer_info):
    """Render Hero Brief - The first thing agent sees (using native Streamlit)"""
    # Get data
    celeste_summary = customer_info.get("celeste_summary", "")
    budget = customer_info.get("celeste_budget_range", "No especificado")
    financing = customer_info.get("celeste_financing_interest", {})
    tradein = customer_info.get("celeste_tradein_info")
    vehicles = customer_info.get("celeste_vehicles_shown", [])
    objections = customer_info.get("celeste_main_objections", [])
    recommendations = customer_info.get("celeste_recommendations", [])
    score = customer_info["customer_score"]
    vip_badge = " ⭐ VIP" if customer_info["is_vip"] else ""

    # Score emoji
    score_emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"

    # Header row
    col_info, col_score = st.columns([4, 1])

    with col_info:
        st.markdown(f"## 👤 {customer_info['customer_name']}{vip_badge}")
        st.caption(
            f"{customer_info['customer_id']} • {customer_info['hub']}, {customer_info['country']}"
        )

    with col_score:
        st.metric("Sentinel Score", f"{score_emoji} {score}/100")

    # Summary
    if celeste_summary:
        st.info(f"💬 **{celeste_summary}**")

    # Key facts in metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Presupuesto", budget)

    with col2:
        financing_text = (
            f"{financing.get('months', 0)} meses"
            if financing and financing.get("interested")
            else "Contado"
        )
        st.metric("📋 Financiamiento", financing_text)

    with col3:
        tradein_text = (
            f"{tradein['brand']} {tradein['model']}" if tradein else "No tiene"
        )
        st.metric("🔄 Trade-in", tradein_text)

    with col4:
        obj_count = len(objections) if objections else 0
        st.metric("⚠️ Objeciones", f"{obj_count} registradas")

    # Favorite vehicle highlight
    if vehicles:
        fav = vehicles[0]
        st.markdown("---")

        col_car, col_loc = st.columns([3, 1])

        with col_car:
            st.success(
                f"🚗 **VEHÍCULO FAVORITO:** {fav['brand']} {fav['model']} {fav['year']} - ${fav['price']:,}"
            )

        with col_loc:
            st.success(f"📍 **Lote {fav['lote']}**")

    # Recommendations strip
    if recommendations:
        st.markdown("---")
        st.markdown("**💡 Recomendaciones para ti:**")
        cols = st.columns(min(len(recommendations), 3))
        for idx, rec in enumerate(recommendations[:3]):
            with cols[idx]:
                st.success(f"✅ {rec}")

    # Celeste Copilot Quick Insight Card
    st.markdown("---")
    render_celeste_insights_card(customer_info)


def render_action_bar(customer_info):
    """Render quick action buttons"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📞 Llamar", use_container_width=True, type="primary"):
            st.info(f"📱 {customer_info['phone']}")

    with col2:
        if st.button("💬 WhatsApp", use_container_width=True):
            st.info(f"Abrir WhatsApp: {customer_info['phone']}")

    with col3:
        if st.button("📧 Email", use_container_width=True):
            st.info(f"📧 {customer_info['email']}")

    with col4:
        vehicles = customer_info.get("celeste_vehicles_shown", [])
        if vehicles:
            if st.button("📍 Ubicar Auto", use_container_width=True):
                st.success(f"📍 Ir a Lote {vehicles[0]['lote']}")
        else:
            st.button("📍 Sin auto", use_container_width=True, disabled=True)


def render_celeste_context_improved(customer_info):
    """Render improved Celeste context with chat UI (native Streamlit)"""
    st.subheader("📱 Contexto de Celeste")

    # Stats row
    last_interaction = customer_info.get("celeste_last_interaction")
    messages_count = customer_info.get("celeste_messages_count", 0)
    conversation = customer_info.get("celeste_conversation", [])
    vehicles_shown = customer_info.get("celeste_vehicles_shown", [])
    objections = customer_info.get("celeste_main_objections", [])

    col1, col2, col3 = st.columns(3)

    with col1:
        if last_interaction:
            hours_ago = (datetime.now() - last_interaction).total_seconds() / 3600
            time_str = (
                f"Hace {int(hours_ago)}h"
                if hours_ago < 24
                else f"Hace {int(hours_ago/24)}d"
            )
        else:
            time_str = "Sin datos"
        st.metric("🕐 Última conversación", time_str)

    with col2:
        st.metric("💬 Mensajes", messages_count)

    with col3:
        st.metric("🚗 Vehículos vistos", len(vehicles_shown))

    st.markdown("---")

    # Two columns: Chat + Details
    col_chat, col_details = st.columns([2, 1])

    with col_chat:
        st.markdown("#### 💬 Conversación con Celeste")

        # Chat using native Streamlit chat components
        if conversation:
            with st.container(height=400):
                for msg in conversation[-15:]:
                    sender = msg.get("sender", "")
                    message = msg.get("message", "")

                    if sender == "customer":
                        # Customer message
                        with st.chat_message("user"):
                            st.write(message)
                    else:
                        # Celeste message
                        with st.chat_message("assistant", avatar="🤖"):
                            st.write(message)
        else:
            st.info("No hay historial de conversación disponible")

    with col_details:
        st.markdown("#### ⚠️ Objeciones Detectadas")

        if objections:
            for obj in objections:
                st.warning(f"• {obj}")
        else:
            st.success("✅ Sin objeciones registradas")

        st.markdown("---")

        st.markdown("#### 🚗 Vehículos de Interés")

        if vehicles_shown:
            for vehicle in vehicles_shown[:3]:
                is_fav = vehicle.get("is_favorite", False)
                badge = " ⭐ FAVORITO" if is_fav else ""

                if is_fav:
                    st.success(
                        f"**{vehicle['brand']} {vehicle['model']}{badge}**\n\n${vehicle['price']:,} • Lote {vehicle['lote']}"
                    )
                else:
                    st.info(
                        f"**{vehicle['brand']} {vehicle['model']}**\n\n${vehicle['price']:,} • Lote {vehicle['lote']}"
                    )
        else:
            st.info("No se mostraron vehículos")


def render_customer_search_improved(data):
    """Render improved customer search with quick filters and cards"""
    st.markdown("## 🧑‍💼 Clientes")

    customers_df = data.get("customers", pd.DataFrame())

    if len(customers_df) == 0:
        st.warning("No hay clientes disponibles")
        return

    # ═══════════════════════════════════════════════════════════════════
    # SEARCH BAR + QUICK FILTERS
    # ═══════════════════════════════════════════════════════════════════
    col_search, col_filter_btn = st.columns([5, 1])

    with col_search:
        search_term = st.text_input(
            "🔎",
            placeholder="Buscar por nombre, email o ID...",
            key="customer_search_input",
            label_visibility="collapsed",
        )

    with col_filter_btn:
        show_filters = st.toggle("🎚️", key="show_filters", help="Mostrar filtros")

    # Quick filter pills
    st.markdown("")  # Spacing

    quick_filter = st.radio(
        "Filtro rápido",
        ["Todos", "🔥 Hot Leads", "⭐ VIP", "📅 Contactar Hoy", "🔄 Retomar"],
        horizontal=True,
        key="quick_filter",
        label_visibility="collapsed",
    )

    # Advanced filters (collapsible)
    if show_filters:
        with st.expander("🎚️ Filtros Avanzados", expanded=True):
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)

            with col_f1:
                statuses = ["Todos"] + sorted(customers_df["status"].unique().tolist())
                status_filter = st.selectbox("Status", statuses, key="status_filter")

            with col_f2:
                score_range = st.slider(
                    "Sentinel Score", 0, 100, (0, 100), key="score_filter"
                )

            with col_f3:
                hubs = ["Todos"] + sorted(customers_df["hub"].unique().tolist())
                hub_filter = st.selectbox("Hub", hubs, key="hub_filter")

            with col_f4:
                sort_by = st.selectbox(
                    "Ordenar por",
                    ["Sentinel Score", "Ventas", "Revenue", "Último Contacto"],
                    key="sort_by",
                )
    else:
        status_filter = "Todos"
        score_range = (0, 100)
        hub_filter = "Todos"
        sort_by = "Sentinel Score"

    # ═══════════════════════════════════════════════════════════════════
    # APPLY FILTERS
    # ═══════════════════════════════════════════════════════════════════
    filtered = customers_df.copy()

    # Search term
    if search_term:
        filtered = filtered[
            filtered["customer_name"].str.contains(search_term, case=False, na=False)
            | filtered["email"].str.contains(search_term, case=False, na=False)
            | filtered["customer_id"].str.contains(search_term, case=False, na=False)
        ]

    # Quick filters
    if quick_filter == "🔥 Hot Leads":
        filtered = filtered[filtered["customer_score"] >= 70]
    elif quick_filter == "⭐ VIP":
        filtered = filtered[filtered["is_vip"] == True]
    elif quick_filter == "📅 Contactar Hoy":
        today = datetime.now()
        filtered = filtered[(today - filtered["last_interaction_date"]).dt.days >= 7]
    elif quick_filter == "🔄 Retomar":
        filtered = filtered[filtered["status"] == "Inactivo"]

    # Advanced filters
    if status_filter != "Todos":
        filtered = filtered[filtered["status"] == status_filter]

    filtered = filtered[
        (filtered["customer_score"] >= score_range[0])
        & (filtered["customer_score"] <= score_range[1])
    ]

    if hub_filter != "Todos":
        filtered = filtered[filtered["hub"] == hub_filter]

    # Sort
    sort_map = {
        "Sentinel Score": ("customer_score", False),
        "Ventas": ("num_sales", False),
        "Revenue": ("total_revenue", False),
        "Último Contacto": ("last_interaction_date", True),
    }
    sort_col, ascending = sort_map[sort_by]
    filtered = filtered.sort_values(sort_col, ascending=ascending)

    # ═══════════════════════════════════════════════════════════════════
    # RESULTS
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")

    col_count, col_view = st.columns([4, 1])

    with col_count:
        st.caption(f"👥 **{len(filtered)}** clientes encontrados")

    with col_view:
        view_mode = st.radio(
            "Vista",
            ["🃏 Cards", "📋 Lista"],
            horizontal=True,
            key="view_mode",
            label_visibility="collapsed",
        )

    # Display results
    if len(filtered) == 0:
        st.info("😔 No se encontraron clientes con los filtros seleccionados")
        return

    with st.container(height=600):
        if view_mode == "🃏 Cards":
            render_customer_cards(filtered.head(20))
        else:
            render_customer_list(filtered.head(20))


def render_customer_cards(filtered_df):
    """Render customers as cards in a grid"""
    # 3 cards per row
    rows = [filtered_df.iloc[i : i + 3] for i in range(0, len(filtered_df), 3)]

    for row_df in rows:
        cols = st.columns(3)

        for idx, (col, (_, customer)) in enumerate(zip(cols, row_df.iterrows())):
            with col:
                render_customer_card(customer, idx)


def render_customer_card(customer, idx):
    """Render a single customer card using native Streamlit components"""
    score = customer["customer_score"]
    score_emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
    vip_badge = " ⭐" if customer["is_vip"] else ""

    # Days since last contact
    days_since = (datetime.now() - customer["last_interaction_date"]).days
    urgency = "🔴" if days_since > 14 else "🟡" if days_since > 7 else "🟢"

    # Use native Streamlit container
    with st.container(border=True):
        # Header row
        col_name, col_score = st.columns([3, 1])

        with col_name:
            st.markdown(f"**{customer['customer_name']}{vip_badge}**")
            st.caption(f"{customer['status']} • {customer['hub']}")

        with col_score:
            st.markdown(f"{score_emoji} **{score}**")

        # Metrics row
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Ventas", customer["num_sales"], label_visibility="collapsed")
            st.caption("Ventas")

        with col2:
            st.metric(
                "Revenue",
                f"${customer['total_revenue']:,.0f}",
                label_visibility="collapsed",
            )
            st.caption("Revenue")

        with col3:
            st.markdown(f"{urgency} **{days_since}d**")
            st.caption("Último contacto")

        # Interests
        st.caption(f"🚗 {customer['vehicle_interests'][:35]}...")

        # Button
        if st.button(
            "👁️ Ver Perfil",
            key=f"card_{customer['customer_id']}_{idx}",
            use_container_width=True,
        ):
            st.session_state.selected_customer_id = customer["customer_id"]
            st.rerun()


def render_customer_list(filtered_df):
    """Render customers as a compact list"""
    for idx, (_, customer) in enumerate(filtered_df.iterrows()):
        score = customer["customer_score"]
        score_emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
        vip = " ⭐" if customer["is_vip"] else ""

        col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1.5, 1.5, 1])

        with col1:
            st.markdown(f"**{customer['customer_name']}{vip}**")
            st.caption(f"{customer['status']} • {customer['hub']}")

        with col2:
            st.markdown(f"{score_emoji} **{score}**/100")

        with col3:
            st.markdown(f"**{customer['num_sales']}** ventas")

        with col4:
            st.markdown(f"**${customer['total_revenue']:,.0f}**")

        with col5:
            if st.button("→", key=f"list_{customer['customer_id']}_{idx}"):
                st.session_state.selected_customer_id = customer["customer_id"]
                st.rerun()

        st.markdown(
            "<hr style='margin: 4px 0; border: none; border-top: 1px solid #E5E7EB;'>",
            unsafe_allow_html=True,
        )


def render_customer_search(data):
    """Legacy function - redirects to improved search"""
    render_customer_search_improved(data)


def render_customer_header(customer_info):
    """Render customer header with key info"""
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

    with col1:
        # Name and status
        vip_badge = " ⭐ VIP" if customer_info["is_vip"] else ""
        st.markdown(f"### 👤 {customer_info['customer_name']}{vip_badge}")
        st.caption(f"ID: {customer_info['customer_id']}")
        st.caption(f"📍 {customer_info['hub']}, {customer_info['country']}")

    with col2:
        # Status badge
        status = customer_info["status"]
        status_colors = {
            "VIP": "🟡",
            "Recurrente": "🟢",
            "Activo": "🔵",
            "Nuevo": "⚪",
            "Inactivo": "⚫",
        }
        st.metric("Estado", f"{status_colors.get(status, '')} {status}")

    with col3:
        # Sentinel Score
        score = customer_info["customer_score"]
        st.metric("Sentinel Score", f"{score}/100")

    with col4:
        # Total sales
        st.metric("Ventas", f"{customer_info['num_sales']}")

    with col5:
        # Total revenue
        revenue = customer_info["total_revenue"]
        st.metric("Revenue", f"${revenue:,.0f}")

    # Contact info
    st.markdown("---")
    col_contact1, col_contact2, col_contact3 = st.columns(3)

    with col_contact1:
        st.write(f"📧 **Email:** {customer_info['email']}")

    with col_contact2:
        st.write(f"📱 **Teléfono:** {customer_info['phone']}")

    with col_contact3:
        days_registered = customer_info["days_since_registration"]
        st.write(f"📅 **Cliente desde:** hace {days_registered} días")


def render_executive_brief(customer_info):
    """Render executive brief - 30 second summary for the agent"""
    st.markdown("### 🎯 Brief Ejecutivo")
    st.caption("Lo que necesitas saber en 30 segundos")

    # Get Celeste summary if available
    celeste_summary = customer_info.get("celeste_summary", "")
    budget = customer_info.get("celeste_budget_range", "No especificado")
    financing = customer_info.get("celeste_financing_interest", {})
    tradein = customer_info.get("celeste_tradein_info")
    vehicles = customer_info.get("celeste_vehicles_shown", [])
    objections = customer_info.get("celeste_main_objections", [])
    recommendations = customer_info.get("celeste_recommendations", [])

    # Main summary box
    col1, col2 = st.columns([2, 1])

    with col1:
        # Summary text
        if celeste_summary:
            st.info(f"💬 **Resumen de Celeste:** {celeste_summary}")
        else:
            interests = customer_info.get("vehicle_interests", "No especificado")
            st.info(f"💬 Cliente interesado en: {interests}")

        # Key facts in compact format
        facts_col1, facts_col2, facts_col3 = st.columns(3)

        with facts_col1:
            st.markdown(f"**💰 Presupuesto:** {budget}")
            if financing and financing.get("interested"):
                st.markdown(
                    f"**📋 Financiamiento:** {financing.get('months', 0)} meses, "
                    f"{financing.get('down_payment_pct', 0)}% enganche"
                )
            else:
                st.markdown("**📋 Financiamiento:** No / Contado")

        with facts_col2:
            if tradein:
                st.markdown(
                    f"**🔄 Trade-in:** {tradein['brand']} {tradein['model']} "
                    f"{tradein['year']}"
                )
                st.markdown(f"**Valor est.:** ${tradein['estimated_value']:,}")
            else:
                st.markdown("**🔄 Trade-in:** No tiene")

        with facts_col3:
            if objections:
                st.markdown("**⚠️ Dudas principales:**")
                for obj in objections[:2]:
                    st.caption(f"• {obj}")
            else:
                st.markdown("**⚠️ Sin objeciones registradas**")

    with col2:
        # Favorite vehicle if any
        if vehicles:
            fav = vehicles[0]
            st.markdown("**🚗 Vehículo Favorito:**")
            st.markdown(f"**{fav['brand']} {fav['model']} {fav['year']}**")
            st.markdown(f"${fav['price']:,}")
            st.success(f"📍 Lote {fav['lote']}")

    # Recommendations strip
    if recommendations:
        st.markdown("---")
        st.markdown("**💡 Recomendaciones para ti:**")
        rec_cols = st.columns(len(recommendations[:3]))
        for idx, rec in enumerate(recommendations[:3]):
            with rec_cols[idx]:
                st.success(f"✅ {rec}")


def render_celeste_context(customer_info):
    """Render Celeste AI conversation context tab"""
    st.subheader("📱 Contexto de Conversación con Celeste")

    # Conversation stats
    last_interaction = customer_info.get("celeste_last_interaction")
    messages_count = customer_info.get("celeste_messages_count", 0)
    conversation = customer_info.get("celeste_conversation", [])
    vehicles_shown = customer_info.get("celeste_vehicles_shown", [])
    recommendations = customer_info.get("celeste_recommendations", [])
    objections = customer_info.get("celeste_main_objections", [])
    financing = customer_info.get("celeste_financing_interest", {})
    tradein = customer_info.get("celeste_tradein_info")
    budget = customer_info.get("celeste_budget_range", "No especificado")

    # Stats row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if last_interaction:
            hours_ago = (datetime.now() - last_interaction).total_seconds() / 3600
            if hours_ago < 1:
                time_str = "Hace menos de 1 hora"
            elif hours_ago < 24:
                time_str = f"Hace {int(hours_ago)} horas"
            else:
                time_str = f"Hace {int(hours_ago/24)} días"
            st.metric("🕐 Última conversación", time_str)
        else:
            st.metric("🕐 Última conversación", "Sin datos")

    with col2:
        st.metric("💬 Mensajes intercambiados", messages_count)

    with col3:
        st.metric("🚗 Vehículos mostrados", len(vehicles_shown))

    with col4:
        score = customer_info.get("customer_score", 0)
        st.metric("🎯 Sentinel Score", f"{score}/100")

    st.markdown("---")

    # Two columns: Left for details, Right for vehicles
    col_left, col_right = st.columns([1, 1])

    with col_left:
        # Customer needs summary
        st.markdown("#### 📋 Lo que busca el cliente")

        st.markdown(f"**Presupuesto:** {budget}")

        if financing and financing.get("interested"):
            st.markdown(
                f"**Financiamiento:** Sí - {financing.get('months', 0)} meses, "
                f"enganche {financing.get('down_payment_pct', 0)}%"
            )
        else:
            st.markdown("**Financiamiento:** No / Pago de contado")

        if tradein:
            st.markdown(
                f"**Trade-in:** {tradein['brand']} {tradein['model']} {tradein['year']} "
                f"(~${tradein['estimated_value']:,})"
            )
        else:
            st.markdown("**Trade-in:** No tiene vehículo para entregar")

        # Objections
        st.markdown("---")
        st.markdown("#### ⚠️ Objeciones / Dudas")
        if objections:
            for obj in objections:
                st.warning(f"• {obj}")
        else:
            st.success("✅ Sin objeciones registradas")

    with col_right:
        # Vehicles shown
        st.markdown("#### 🚗 Vehículos que le interesaron")

        if vehicles_shown:
            for idx, vehicle in enumerate(vehicles_shown):
                is_fav = vehicle.get("is_favorite", False)
                fav_badge = " ⭐ FAVORITO" if is_fav else ""

                with st.expander(
                    f"{vehicle['brand']} {vehicle['model']} {vehicle['year']}{fav_badge}",
                    expanded=is_fav,
                ):
                    col_v1, col_v2 = st.columns(2)
                    with col_v1:
                        st.write(f"**Precio:** ${vehicle['price']:,}")
                        st.write(f"**VIN:** {vehicle['vin']}")
                    with col_v2:
                        st.success(f"**📍 Ubicación:** Lote {vehicle['lote']}")
                        if is_fav:
                            st.info("🎯 Llevar al cliente aquí primero")
        else:
            st.info("No se mostraron vehículos específicos")

    # Recommendations for agent
    st.markdown("---")
    st.markdown("#### 💡 Recomendaciones para el Agente")

    if recommendations:
        for rec in recommendations:
            st.success(f"✅ {rec}")
    else:
        st.info("Sin recomendaciones específicas")

    # Conversation preview
    st.markdown("---")
    st.markdown("#### 💬 Últimos mensajes de la conversación")

    if conversation:
        with st.container(height=400):
            for msg in conversation[-10:]:  # Last 10 messages
                sender = msg.get("sender", "")
                message = msg.get("message", "")

                if sender == "customer":
                    st.markdown(
                        f"<div style='background-color: #E3F2FD; padding: 10px; "
                        f"border-radius: 10px; margin: 5px 0; margin-left: 20%;'>"
                        f"<strong>👤 Cliente:</strong> {message}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div style='background-color: #F3E5F5; padding: 10px; "
                        f"border-radius: 10px; margin: 5px 0; margin-right: 20%;'>"
                        f"<strong>🤖 Celeste:</strong> {message}</div>",
                        unsafe_allow_html=True,
                    )
    else:
        st.info("No hay historial de conversación disponible")


def render_customer_summary(customer_info, data):
    """Render customer summary tab"""
    st.subheader("📊 Resumen del Cliente")

    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Transacciones Totales", customer_info["num_transactions"])

    with col2:
        st.metric("Ventas Completadas", customer_info["num_sales"])

    with col3:
        st.metric("Cancelaciones", customer_info["num_cancellations"])

    with col4:
        avg_ticket = (
            customer_info["total_revenue"] / customer_info["num_sales"]
            if customer_info["num_sales"] > 0
            else 0
        )
        st.metric("Ticket Promedio", f"${avg_ticket:,.0f}")

    with col5:
        # Ancillaries revenue
        anc_revenue = customer_info.get("total_ancillaries_revenue", 0)
        st.metric("Revenue Ancillaries", f"${anc_revenue:,.0f}")

    st.markdown("---")

    # Timeline and additional info in 2 columns
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 📅 Fechas Importantes")

        reg_date = customer_info["registration_date"]
        st.write(f"**Registro:** {reg_date.strftime('%d/%m/%Y')}")

        last_interaction = customer_info["last_interaction_date"]
        days_since = (datetime.now() - last_interaction).days
        st.write(
            f"**Última Interacción:** {last_interaction.strftime('%d/%m/%Y')} ({days_since} días)"
        )

        if customer_info["last_purchase_date"] is not None and pd.notna(
            customer_info["last_purchase_date"]
        ):
            last_purchase = customer_info["last_purchase_date"]
            days_since_purchase = (datetime.now() - last_purchase).days
            st.write(
                f"**Última Compra:** {last_purchase.strftime('%d/%m/%Y')} ({days_since_purchase} días)"
            )
        else:
            st.write("**Última Compra:** Sin compras")

        st.markdown("---")

        # Interaction stats
        st.markdown("#### 📞 Historial de Contacto")
        st.write(f"**Llamadas:** {customer_info.get('num_calls', 0)}")
        st.write(f"**Mensajes:** {customer_info.get('num_messages', 0)}")
        st.write(f"**Visitas al Hub:** {customer_info.get('num_visits', 0)}")

    with col_right:
        st.markdown("#### 🎯 Información del Cliente")

        st.write(f"**Intereses:** {customer_info['vehicle_interests']}")
        st.write(
            f"**Marcas Preferidas:** {customer_info.get('preferred_brands', 'Sin preferencia')}"
        )

        if customer_info["nps_rating"] is not None:
            nps_color = (
                "🟢"
                if customer_info["nps_rating"] >= 9
                else "🟡"
                if customer_info["nps_rating"] >= 7
                else "🔴"
            )
            st.write(f"**NPS Rating:** {nps_color} {customer_info['nps_rating']}/10")
        else:
            st.write("**NPS Rating:** Sin calificar")

        # Assigned agent info
        agents_df = data.get("agent_performance", pd.DataFrame())
        if len(agents_df) > 0:
            # Filter agents from same hub
            hub_agents = agents_df[agents_df["hub"] == customer_info["hub"]]
            if len(hub_agents) >= customer_info["assigned_agent_id"]:
                agent = hub_agents.iloc[customer_info["assigned_agent_id"] - 1]
                st.write(f"**Agente Asignado:** {agent['agent_name']}")

    # Revenue breakdown if has sales
    if customer_info["num_sales"] > 0:
        st.markdown("---")
        st.markdown("#### 💰 Desglose de Revenue")

        total_rev = customer_info["total_revenue"]
        anc_rev = customer_info.get("total_ancillaries_revenue", 0)
        vehicle_rev = total_rev - anc_rev

        col_rev1, col_rev2, col_rev3, col_rev4 = st.columns(4)

        with col_rev1:
            st.metric("Revenue Total", f"${total_rev:,.0f}")

        with col_rev2:
            st.metric("Revenue Vehículos", f"${vehicle_rev:,.0f}")

        with col_rev3:
            st.metric("Revenue Ancillaries", f"${anc_rev:,.0f}")

        with col_rev4:
            penetration = (anc_rev / total_rev * 100) if total_rev > 0 else 0
            st.metric("Penetración Anc.", f"{penetration:.1f}%")

    # Notes
    if customer_info["notes"]:
        st.markdown("---")
        st.markdown("#### 📝 Notas del Agente")
        st.info(customer_info["notes"])

    # Risk indicators
    st.markdown("---")
    st.markdown("#### ⚠️ Indicadores & Insights")

    warnings = []
    insights = []

    # Check for inactivity
    if customer_info["status"] == "Inactivo":
        warnings.append("Cliente inactivo - Requiere reactivación")

    # Check time since last interaction
    if days_since > 30:
        warnings.append(
            f"Sin interacción desde hace {days_since} días - Contactar pronto"
        )

    # Check cancellations
    if customer_info["num_cancellations"] > 2:
        warnings.append(
            f"Alto número de cancelaciones ({customer_info['num_cancellations']}) - Analizar razones"
        )

    # Check low score
    if customer_info["customer_score"] < 40:
        warnings.append(
            f"Sentinel Score bajo ({customer_info['customer_score']}/100) - Baja propensión de compra"
        )

    # Positive insights
    if customer_info["is_vip"]:
        insights.append("⭐ Cliente VIP - Prioridad máxima")

    if customer_info["num_sales"] > 1:
        insights.append("✅ Cliente recurrente - Alta lealtad")

    if customer_info["customer_score"] > 70:
        insights.append("🎯 Alta propensión de compra - Momento ideal para contactar")

    if customer_info.get("total_ancillaries_revenue", 0) > 0:
        insights.append("💰 Compra ancillaries - Cliente premium")

    # Display warnings
    if warnings:
        for warning in warnings:
            st.warning(f"⚠️ {warning}")

    # Display insights
    if insights:
        for insight in insights:
            st.success(insight)

    if not warnings and not insights:
        st.info("✅ Cliente saludable - Sin indicadores especiales")


def render_transaction_history(customer_info):
    """Render transaction history tab with real transaction data"""
    st.subheader("🛒 Historial de Transacciones Completo")

    transactions = customer_info.get("transactions", [])

    if not transactions or len(transactions) == 0:
        st.info("Este cliente no tiene transacciones registradas")
        return

    # Summary metrics
    total_sales = len([t for t in transactions if t["type"] == "Venta"])
    total_cancellations = len([t for t in transactions if t["type"] == "Cancelación"])
    total_revenue = sum(
        [t.get("total_amount", 0) for t in transactions if t["type"] == "Venta"]
    )
    total_ancillaries_revenue = sum(
        [t.get("ancillaries_total", 0) for t in transactions if t["type"] == "Venta"]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Transacciones", len(transactions))

    with col2:
        st.metric("Ventas", total_sales)

    with col3:
        st.metric("Cancelaciones", total_cancellations)

    with col4:
        conversion_rate = (
            (total_sales / len(transactions) * 100) if len(transactions) > 0 else 0
        )
        st.metric("Tasa de Conversión", f"{conversion_rate:.0f}%")

    # Análisis del Historial (moved here, before transaction list)
    st.markdown("---")
    st.markdown("#### 📊 Análisis del Historial")

    col_insight1, col_insight2 = st.columns(2)

    with col_insight1:
        st.metric("Revenue Total", f"${total_revenue:,.0f}")
        st.metric("Revenue de Ancillaries", f"${total_ancillaries_revenue:,.0f}")

        if total_sales > 0:
            avg_ticket = total_revenue / total_sales
            st.metric("Ticket Promedio", f"${avg_ticket:,.0f}")

    with col_insight2:
        if total_sales > 0:
            # Average ancillaries per sale
            avg_anc_revenue = total_ancillaries_revenue / total_sales
            st.metric("Ancillaries Prom. por Venta", f"${avg_anc_revenue:,.0f}")

            # Penetration rate
            penetration = (
                (total_ancillaries_revenue / total_revenue * 100)
                if total_revenue > 0
                else 0
            )
            st.metric("Penetración Ancillaries", f"{penetration:.1f}%")

        if total_cancellations > 0:
            st.metric(
                "Tasa de Cancelación",
                f"{(total_cancellations/len(transactions)*100):.0f}%",
            )

    # Display each transaction
    st.markdown("---")
    st.markdown("#### 📋 Detalle de Transacciones")

    for idx, transaction in enumerate(
        sorted(transactions, key=lambda x: x["date"], reverse=True)
    ):
        transaction_date = transaction["date"]
        transaction_type = transaction["type"]

        # Color and icon by type
        if transaction_type == "Venta":
            color = "🟢"
            status_color = "green"
        else:
            color = "🔴"
            status_color = "red"

        with st.expander(
            f"{color} {transaction_type} - {transaction_date.strftime('%d/%m/%Y')} - {transaction.get('vehicle', 'N/A')}",
            expanded=idx == 0,  # First one expanded
        ):
            if transaction_type == "Venta":
                # Sale transaction
                col_trans1, col_trans2 = st.columns(2)

                with col_trans1:
                    st.markdown("#### 🚗 Detalles del Vehículo")
                    st.write(f"**Vehículo:** {transaction['vehicle']}")
                    st.write(
                        f"**Precio Vehículo:** ${transaction['vehicle_price']:,.0f}"
                    )
                    st.write(f"**ID Transacción:** {transaction['transaction_id']}")

                    financing = transaction.get("financing", False)
                    if financing:
                        st.write(f"**Financiamiento:** ✅ Sí")
                        down_payment = transaction.get("down_payment", 0)
                        st.write(f"**Enganche:** ${down_payment:,.0f}")
                    else:
                        st.write(f"**Financiamiento:** ❌ No - Pago de contado")

                with col_trans2:
                    st.markdown("#### 🎁 Ancillaries Vendidos")

                    ancillaries = transaction.get("ancillaries", [])

                    if ancillaries:
                        for anc in ancillaries:
                            category_icons = {
                                "Insurance": "🛡️",
                                "Warranty": "⚙️",
                                "Tech": "📱",
                                "Service": "🔧",
                                "Accessories": "✨",
                            }
                            icon = category_icons.get(anc.get("category", ""), "📦")
                            st.write(f"{icon} **{anc['name']}** - ${anc['price']:,.0f}")

                        st.markdown("---")
                        st.write(
                            f"**Total Ancillaries:** ${transaction['ancillaries_total']:,.0f}"
                        )
                    else:
                        st.info("Sin ancillaries")

                # Total
                st.markdown("---")
                col_total1, col_total2, col_total3 = st.columns(3)

                with col_total1:
                    st.metric("💰 Total Venta", f"${transaction['total_amount']:,.0f}")

                with col_total2:
                    anc_percentage = (
                        (
                            transaction["ancillaries_total"]
                            / transaction["total_amount"]
                            * 100
                        )
                        if transaction["total_amount"] > 0
                        else 0
                    )
                    st.metric("% Ancillaries", f"{anc_percentage:.1f}%")

                with col_total3:
                    st.metric("Método Pago", "Financiado" if financing else "Contado")

            else:
                # Cancellation transaction
                col_cancel1, col_cancel2 = st.columns(2)

                with col_cancel1:
                    st.markdown("#### ❌ Detalles de la Cancelación")
                    st.write(f"**Vehículo de Interés:** {transaction['vehicle']}")
                    st.write(f"**Precio:** ${transaction['vehicle_price']:,.0f}")
                    st.write(f"**ID Transacción:** {transaction['transaction_id']}")

                with col_cancel2:
                    st.markdown("#### 📋 Información de Cancelación")
                    st.write(
                        f"**Razón:** {transaction.get('cancel_reason', 'No especificada')}"
                    )
                    st.write(
                        f"**Etapa:** {transaction.get('stage', 'No especificada')}"
                    )

                st.warning(
                    f"⚠️ Cancelación en etapa: {transaction.get('stage', 'No especificada')}"
                )


def render_vehicle_interests(customer_info):
    """Render vehicle interests tab"""
    st.subheader("🚗 Intereses y Preferencias de Vehículos")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Segmentos de Interés")

        interests = customer_info["vehicle_interests"].split(", ")

        for interest in interests:
            st.write(f"• **{interest}**")

        st.markdown("---")
        st.markdown("#### Preferencias")

        # Generate sample preferences
        preferences = {
            "Año": np.random.choice(["2020+", "2018+", "Cualquiera"]),
            "Kilometraje": np.random.choice(["< 50k km", "< 80k km", "Cualquiera"]),
            "Precio": np.random.choice(["$150k-$250k", "$250k-$350k", "> $350k"]),
            "Transmisión": np.random.choice(["Automática", "Manual", "Cualquiera"]),
            "Color": np.random.choice(["Blanco", "Negro", "Gris", "Cualquiera"]),
        }

        for key, value in preferences.items():
            st.write(f"**{key}:** {value}")

    with col2:
        st.markdown("#### Vehículos Vistos (Últimos 10)")

        # Generate sample viewed vehicles
        viewed_vehicles = []
        for i in range(10):
            brand = np.random.choice(["Toyota", "Nissan", "Honda", "Mazda", "VW"])
            model = np.random.choice(["Corolla", "Sentra", "Civic", "CX-5", "Jetta"])
            year = np.random.randint(2018, 2024)
            days_ago = np.random.randint(1, 30)

            viewed_vehicles.append(
                {
                    "Vehículo": f"{brand} {model} {year}",
                    "Fecha": f"Hace {days_ago} días",
                    "Veces Visto": np.random.randint(1, 4),
                }
            )

        viewed_df = pd.DataFrame(viewed_vehicles)
        st.dataframe(viewed_df, use_container_width=True, hide_index=True)

    # Recommendations
    st.markdown("---")
    st.markdown("#### 💡 Recomendaciones para el Agente")

    recommendations = []

    if customer_info["customer_score"] > 70:
        recommendations.append(
            "✅ Cliente con alta propensión de compra - Priorizar seguimiento"
        )

    if customer_info["num_sales"] > 1:
        recommendations.append("✅ Cliente recurrente - Ofrecer programa de lealtad")

    if customer_info["is_vip"]:
        recommendations.append("⭐ Cliente VIP - Asignar inventario premium")

    if customer_info["num_cancellations"] > 0:
        recommendations.append(
            "⚠️ Ha cancelado antes - Asegurar disponibilidad antes de reservar"
        )

    for rec in recommendations:
        st.info(rec)


def render_interactions_log(customer_info):
    """Render interactions log tab"""
    st.subheader("📞 Registro de Interacciones")

    # Generate sample interactions
    interactions = []

    num_interactions = np.random.randint(5, 15)

    for i in range(num_interactions):
        days_ago = np.random.randint(1, customer_info["days_since_registration"])
        interaction_date = datetime.now() - timedelta(days=days_ago)

        interaction_types = [
            "Llamada",
            "WhatsApp",
            "Email",
            "Visita Hub",
            "Demo Vehículo",
        ]
        interaction_type = np.random.choice(interaction_types)

        # Generate interaction note
        notes_by_type = {
            "Llamada": [
                "Cliente interesado en ver vehículos este fin de semana",
                "Seguimiento sobre cotización enviada",
                "Respondió preguntas sobre financiamiento",
                "No contestó - dejar mensaje",
            ],
            "WhatsApp": [
                "Envió fotos de vehículos de interés",
                "Preguntó sobre disponibilidad",
                "Solicitó agendar cita",
                "Compartió documentación para pre-aprobación",
            ],
            "Email": [
                "Envió cotización formal",
                "Compartió catálogo de vehículos",
                "Seguimiento post-demo",
                "Envió opciones de financiamiento",
            ],
            "Visita Hub": [
                "Cliente visitó showroom - vio 3 vehículos",
                "Realizó test drive de SUV",
                "Dejó documentos para evaluación",
                "Agendó segunda visita",
            ],
            "Demo Vehículo": [
                "Demo de Sedán - muy interesado",
                "Test drive de SUV - solicita cotización",
                "Cliente probó vehículo - quiere pensarlo",
                "Demo positiva - listo para reservar",
            ],
        }

        note = np.random.choice(notes_by_type[interaction_type])

        # Agent name
        agent_names = ["Juan García", "María López", "Carlos Pérez", "Ana Martínez"]
        agent = np.random.choice(agent_names)

        interactions.append(
            {
                "Fecha": interaction_date.strftime("%d/%m/%Y %H:%M"),
                "Tipo": interaction_type,
                "Nota": note,
                "Agente": agent,
            }
        )

    # Sort by date (most recent first)
    interactions_df = pd.DataFrame(interactions)

    st.dataframe(interactions_df, use_container_width=True, hide_index=True)

    # Add new interaction form
    st.markdown("---")
    st.markdown("#### ➕ Agregar Nueva Interacción")

    col_int1, col_int2 = st.columns(2)

    with col_int1:
        interaction_type = st.selectbox(
            "Tipo", ["Llamada", "WhatsApp", "Email", "Visita Hub", "Demo Vehículo"]
        )

    with col_int2:
        interaction_note = st.text_area(
            "Nota", placeholder="Describe la interacción..."
        )

    if st.button("💾 Guardar Interacción"):
        st.success("✅ Interacción registrada exitosamente")
