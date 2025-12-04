"""
City Manager Dashboard View
Team performance, agent comparison, and fleet management
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
from config import (
    COLORS,
    COUNTRIES,
    HUBS,
    INCENTIVE_GOALS,
    OPERATION_TYPES,
    PERIOD_OPTIONS,
    THRESHOLDS,
    VEHICLE_SEGMENTS,
)
from utils.alert_detector import detect_operational_alerts
from utils.components import (
    render_agent_status_badge,
    render_alert_box,
    render_bar_chart,
    render_kpi_card,
    render_kpi_grid,
    render_metric_comparison,
    render_trend_chart,
)


def render_city_manager_dashboard(data):
    """
    Render the City Manager Dashboard
    Reorganized with Hero Zone + Navigation Pills for better UX
    """
    # ═══════════════════════════════════════════════════════════════════
    # HEADER + FILTERS (Compact)
    # ═══════════════════════════════════════════════════════════════════
    col_title, col_filters = st.columns([1, 3])

    with col_title:
        st.markdown("## 👥 City Manager")

    with col_filters:
        render_filters_compact()

    # Get filtered data
    country = st.session_state.get("cm_country", COUNTRIES[0])
    region = st.session_state.get(
        "cm_region", HUBS[country][0] if HUBS.get(country) else ""
    )
    hub = st.session_state.get("cm_hub", "Todos los Hubs")
    period = st.session_state.get("cm_period", "Últimos 30 días")
    operation_type = st.session_state.get("cm_operation_type", "all")

    filtered_data = filter_data(data, country, region, hub, period, operation_type)
    hub_label = f"{hub}" if hub != "Todos los Hubs" else f"{region}"

    # ═══════════════════════════════════════════════════════════════════
    # HERO ZONE - Always visible KPIs
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")
    render_hero_zone(data, filtered_data, hub_label, country)

    # ═══════════════════════════════════════════════════════════════════
    # NAVIGATION PILLS - Secondary navigation
    # ═══════════════════════════════════════════════════════════════════
    st.markdown("---")

    # Count alerts for badge
    alerts = detect_operational_alerts(filtered_data, hub_label)
    alert_count = len(alerts)
    alert_badge = f" ({alert_count})" if alert_count > 0 else ""

    # Navigation tabs
    selected_section = st.radio(
        "Sección",
        ["👥 Equipo", "🏆 Incentivos", "🎯 Leads", f"⚠️ Alertas{alert_badge}"],
        horizontal=True,
        key="cm_nav_section",
        label_visibility="collapsed",
    )

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════════════
    # CONTENT ZONE - Changes based on selected section
    # ═══════════════════════════════════════════════════════════════════
    if selected_section == "👥 Equipo":
        render_team_section(filtered_data, hub_label)

    elif selected_section == "🏆 Incentivos":
        render_incentives_module(filtered_data)

    elif selected_section == "🎯 Leads":
        render_leads_section(filtered_data)

    else:  # Alertas
        render_alerts_section(filtered_data, hub_label)


def render_filters_compact():
    """Render compact filter controls in a single row"""
    col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1.5, 1.5, 0.5])

    with col1:
        selected_country = st.selectbox(
            "País", COUNTRIES, key="cm_country", label_visibility="collapsed"
        )

    with col2:
        country_regions = HUBS.get(selected_country, [])
        st.selectbox(
            "Región", country_regions, key="cm_region", label_visibility="collapsed"
        )

    with col3:
        from config import REGIONS_HUBS

        region = st.session_state.get("cm_region", "")
        if selected_country and region in REGIONS_HUBS.get(selected_country, {}):
            hub_options = ["Todos los Hubs"] + REGIONS_HUBS[selected_country][region]
        else:
            hub_options = ["Todos los Hubs"]
        st.selectbox("Hub", hub_options, key="cm_hub", label_visibility="collapsed")

    with col4:
        st.selectbox(
            "Periodo",
            list(PERIOD_OPTIONS.keys()),
            key="cm_period",
            label_visibility="collapsed",
        )

    with col5:
        if st.button("🔄", use_container_width=True, help="Actualizar datos"):
            st.rerun()


def render_hero_zone(all_data, filtered_data, hub_label, country):
    """Render Hero Zone with main KPIs always visible"""
    df = filtered_data["daily_metrics"]

    if len(df) == 0:
        st.warning("No hay datos para este hub")
        return

    # Calculate metrics
    total_sales = df["sales"].sum()
    total_leads = df["leads"].sum()
    conversion = (total_sales / total_leads * 100) if total_leads > 0 else 0
    avg_nps = df["nps"].mean()

    # Calculate financing penetration
    agent_df = filtered_data.get("agent_performance", pd.DataFrame())
    if len(agent_df) > 0:
        total_financing_sold = agent_df["financing_sold"].sum()
        financing_penetration = (
            (total_financing_sold / total_sales * 100) if total_sales > 0 else 0
        )
        total_revenue = agent_df["revenue"].sum()
    else:
        financing_penetration = 0
        total_revenue = 0

    # Country averages for comparison
    country_df = all_data["daily_metrics"][
        all_data["daily_metrics"]["country"] == country
    ].copy()
    days = PERIOD_OPTIONS[st.session_state.get("cm_period", "Últimos 30 días")]
    cutoff_date = datetime.now() - timedelta(days=days)
    country_df = country_df[country_df["date"] >= cutoff_date]

    country_sales = country_df["sales"].sum()
    country_leads = country_df["leads"].sum()
    country_conversion = (
        (country_sales / country_leads * 100) if country_leads > 0 else 0
    )
    country_nps = country_df["nps"].mean()
    num_hubs = len(country_df["hub"].unique())
    avg_sales_per_hub = country_sales / num_hubs if num_hubs > 0 else 0

    # Calculate deltas
    sales_delta = (
        ((total_sales / avg_sales_per_hub) - 1) * 100 if avg_sales_per_hub > 0 else 0
    )
    conversion_delta = conversion - country_conversion
    nps_delta = avg_nps - country_nps

    # Hub label
    st.markdown(f"### 📍 {hub_label}")

    # Hero KPIs
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "🚗 Entregas",
            f"{total_sales:.0f}",
            f"{sales_delta:+.1f}% vs {country}",
            delta_color="normal" if sales_delta >= 0 else "inverse",
        )

    with col2:
        st.metric(
            "🎯 Conversión",
            f"{conversion:.1f}%",
            f"{conversion_delta:+.1f}pp vs {country}",
            delta_color="normal" if conversion_delta >= 0 else "inverse",
        )

    with col3:
        st.metric(
            "⭐ NPS",
            f"{avg_nps:.0f}",
            f"{nps_delta:+.0f} vs {country}",
            delta_color="normal" if nps_delta >= 0 else "inverse",
        )

    with col4:
        st.metric("💰 Revenue", f"${total_revenue:,.0f}")

    with col5:
        st.metric("📊 Financing", f"{financing_penetration:.1f}%")


def render_team_section(filtered_data, hub_label):
    """Render Team section with agent table and optimization"""
    # Quick stats
    agents_df = filtered_data["agent_performance"].copy()

    if len(agents_df) == 0:
        st.warning("No hay datos de agentes")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total Agentes", len(agents_df))

    with col2:
        avg_util = agents_df["utilization"].mean() * 100
        st.metric("📅 Utilización Prom.", f"{avg_util:.0f}%")

    with col3:
        if "ownership_score" in agents_df.columns:
            avg_ownership = agents_df["ownership_score"].mean()
            st.metric("🤝 Ownership Prom.", f"{avg_ownership:.0f}%")

    with col4:
        top_performers = len(
            agents_df[agents_df["conversion"] > agents_df["conversion"].quantile(0.75)]
        )
        st.metric("🔥 Top Performers", top_performers)

    st.markdown("---")

    # Agent table with tabs
    tab1, tab2 = st.tabs(["📊 Ranking de Agentes", "⚙️ Optimización"])

    with tab1:
        render_agent_table_improved(filtered_data)

    with tab2:
        render_agent_optimization(filtered_data)


def render_agent_table_improved(filtered_data):
    """Render improved agent table with inline metrics"""
    agents_df = filtered_data["agent_performance"].copy()

    if len(agents_df) == 0:
        return

    # Filters row
    col_filter, col_sort, col_search = st.columns([2, 2, 2])

    with col_filter:
        quick_filter = st.selectbox(
            "Filtro rápido",
            ["Todos", "🔥 Top Performers", "⚠️ Necesitan Apoyo", "📈 Alto Ownership"],
            key="agent_quick_filter",
        )

    with col_sort:
        sort_by = st.selectbox(
            "Ordenar por",
            ["Entregas", "CVR", "NPS", "Puntos", "Ownership"],
            key="agent_sort",
        )

    with col_search:
        search = st.text_input(
            "Buscar agente", placeholder="Nombre...", key="agent_search"
        )

    # Apply filters
    filtered_agents = agents_df.copy()

    if quick_filter == "🔥 Top Performers":
        threshold = filtered_agents["conversion"].quantile(0.75)
        filtered_agents = filtered_agents[filtered_agents["conversion"] >= threshold]
    elif quick_filter == "⚠️ Necesitan Apoyo":
        threshold = filtered_agents["conversion"].quantile(0.25)
        filtered_agents = filtered_agents[filtered_agents["conversion"] <= threshold]
    elif (
        quick_filter == "📈 Alto Ownership"
        and "ownership_score" in filtered_agents.columns
    ):
        filtered_agents = filtered_agents[filtered_agents["ownership_score"] >= 80]

    if search:
        filtered_agents = filtered_agents[
            filtered_agents["agent_name"].str.contains(search, case=False, na=False)
        ]

    # Sort
    sort_map = {
        "Entregas": "sales",
        "CVR": "conversion",
        "NPS": "nps",
        "Puntos": "total_points"
        if "total_points" in filtered_agents.columns
        else "sales",
        "Ownership": "ownership_score"
        if "ownership_score" in filtered_agents.columns
        else "sales",
    }
    filtered_agents = filtered_agents.sort_values(sort_map[sort_by], ascending=False)

    # Results count
    st.caption(f"Mostrando {len(filtered_agents)} de {len(agents_df)} agentes")

    # Render agent cards
    for idx, (_, agent) in enumerate(filtered_agents.head(15).iterrows()):
        render_agent_card(agent, idx + 1)


def render_agent_card(agent, rank):
    """Render a single agent card with key metrics"""
    # Determine level badge
    level = agent.get("incentive_level", "🥉 Bronze")
    ownership = agent.get("ownership_score", 0)

    # Status color based on performance
    cvr = agent["conversion"] * 100
    if cvr >= 18:
        status_color = "🟢"
    elif cvr >= 12:
        status_color = "🟡"
    else:
        status_color = "🔴"

    # Create card
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns([0.5, 2.5, 1, 1, 1, 1.5])

        with col1:
            st.markdown(f"**#{rank}**")

        with col2:
            st.markdown(f"**{agent['agent_name']}** {level}")
            if ownership > 0:
                st.progress(ownership / 100, text=f"Ownership: {ownership:.0f}%")

        with col3:
            st.metric("Entregas", f"{agent['sales']:.0f}", label_visibility="collapsed")
            st.caption("Entregas")

        with col4:
            st.metric("CVR", f"{cvr:.1f}%", label_visibility="collapsed")
            st.caption(f"{status_color} CVR")

        with col5:
            st.metric("NPS", f"{agent['nps']:.0f}", label_visibility="collapsed")
            st.caption("NPS")

        with col6:
            if st.button(
                "👁️ Ver Perfil",
                key=f"view_agent_{agent['agent_id']}_{rank}",
                use_container_width=True,
            ):
                st.session_state.navigation_view = "agent_profile"
                st.session_state.selected_agent_name = agent["agent_name"]
                st.session_state.kavako_agent = agent["agent_name"]
                st.session_state.kavako_hub_selector = agent.get("hub", "")
                st.session_state.nav_breadcrumb = [
                    {"label": "City Manager", "view": "city_manager"},
                    {"label": agent["agent_name"], "view": "agent_profile"},
                ]
                st.rerun()

        st.markdown(
            "<hr style='margin: 0.3rem 0; border: none; border-top: 1px solid #e0e0e0;'>",
            unsafe_allow_html=True,
        )


def render_leads_section(filtered_data):
    """Render Leads section with simulator and recommendations"""
    tab1, tab2 = st.tabs(["🎯 Simulador de Asignación", "💡 Recomendaciones"])

    with tab1:
        render_lead_assignment_simulator(filtered_data)

    with tab2:
        render_recommendations_module(filtered_data)


def render_alerts_section(filtered_data, hub_label):
    """Render Alerts section"""
    render_operational_alerts(filtered_data, hub_label)


def get_country_for_region(region):
    """Get country for a given region"""
    for country, regions in HUBS.items():
        if region in regions:
            return country
    return COUNTRIES[0]


def filter_data(data, country, region, hub, period, operation_type="all"):
    """Filter data for specific region, hub, period, and operation type"""
    # Filter daily metrics
    daily_metrics = data["daily_metrics"].copy()
    daily_metrics = daily_metrics[
        (daily_metrics["country"] == country) & (daily_metrics["region"] == region)
    ]

    # If specific hub is selected, filter by hub too
    if hub != "Todos los Hubs":
        daily_metrics = daily_metrics[daily_metrics["hub"] == hub]

    days = PERIOD_OPTIONS[period]
    cutoff_date = datetime.now() - timedelta(days=days)
    daily_metrics = daily_metrics[daily_metrics["date"] >= cutoff_date]

    # Filter agent performance
    agent_perf = data["agent_performance"].copy()
    agent_perf = agent_perf[
        (agent_perf["country"] == country) & (agent_perf["region"] == region)
    ]

    # If specific hub is selected, filter by hub too
    if hub != "Todos los Hubs":
        agent_perf = agent_perf[agent_perf["hub"] == hub]

    # Apply operation type filter to agent performance
    if operation_type != "all":
        agent_perf = apply_operation_filter(agent_perf, operation_type)

    # Filter inventory
    inventory = data["inventory"].copy()
    inventory = inventory[
        (inventory["country"] == country) & (inventory["region"] == region)
    ]

    # If specific hub is selected, filter by hub too
    if hub != "Todos los Hubs":
        inventory = inventory[inventory["hub"] == hub]

    # Filter funnel
    funnel = data["funnel"].copy()
    funnel = funnel[(funnel["country"] == country) & (funnel["region"] == region)]

    # If specific hub is selected, filter by hub too
    if hub != "Todos los Hubs":
        funnel = funnel[funnel["hub"] == hub]

    return {
        "daily_metrics": daily_metrics,
        "agent_performance": agent_perf,
        "inventory": inventory,
        "funnel": funnel,
        "operation_type": operation_type,  # Include in filtered data for reference
    }


def apply_operation_filter(agent_df, operation_type):
    """
    Apply operation type filter to agent performance data
    Adjusts metrics based on selected operation type
    """
    df = agent_df.copy()

    if operation_type == "sales":
        # Only count sales operations (sales_only + sales_tradein)
        df["sales"] = df["sales_only"] + df["sales_tradein"]
        df["conversion"] = df["sales"] / df["leads"]
        df["revenue"] = df["sales"] * 20000  # Approximate revenue per sale

    elif operation_type == "purchases":
        # Only count purchase operations
        df["sales"] = df["purchases_total"]  # Rename for compatibility
        df["conversion"] = df["purchases_total"] / df["leads"]
        df["revenue"] = df["purchases_total"] * 18000  # Approximate cost per purchase

    elif operation_type == "tradein":
        # Only count trade-in operations
        df["sales"] = df["sales_tradein"]  # Rename for compatibility
        df["conversion"] = df["sales_tradein"] / df["leads"]
        df["revenue"] = df["sales_tradein"] * 20000

    return df


def render_region_overview(filtered_data, region, country):
    """Render region performance KPIs"""
    st.subheader(f"📍 Performance de {region}")

    df = filtered_data["daily_metrics"]

    if len(df) == 0:
        st.warning("No hay datos para este hub")
        return

    # Aggregate metrics
    total_sales = df["sales"].sum()
    total_purchases = df["purchases"].sum()  # NEW: Total purchases
    total_leads = df["leads"].sum()
    total_appointments = df["appointments"].sum()
    total_reservations = df["reservations"].sum()
    total_cancellations = df["cancellations"].sum()
    avg_nps = df["nps"].mean()
    avg_sla = df["sla_lead_to_sale"].mean()

    conversion = (total_sales / total_leads * 100) if total_leads > 0 else 0

    # Get inventory data (current stock)
    inventory_df = filtered_data.get("inventory", pd.DataFrame())
    if len(inventory_df) > 0:
        total_stock = inventory_df["total_inventory"].sum()
        available_stock = inventory_df["available"].sum()
    else:
        total_stock = 0
        available_stock = 0

    # Calculate financing penetration from agent data
    agent_df = filtered_data.get("agent_performance", pd.DataFrame())
    if len(agent_df) > 0:
        # Aggregate financing metrics from all agents
        total_financing_sold = agent_df["financing_sold"].sum()
        financing_penetration = (
            (total_financing_sold / total_sales * 100) if total_sales > 0 else 0
        )
    else:
        financing_penetration = 0

    # First row: Main sales/purchase metrics
    st.markdown("#### 🚗 Ventas y Compras")
    kpis_row1 = [
        {"label": "Entregas del Hub", "value": total_sales, "format": "%.0f"},
        {"label": "Compras (Inbound)", "value": total_purchases, "format": "%.0f"},
        {"label": "Stock Total", "value": total_stock, "format": "%.0f"},
        {"label": "Stock Disponible", "value": available_stock, "format": "%.0f"},
        {"label": "% Financing", "value": financing_penetration, "format": "%.1f%%"},
    ]
    render_kpi_grid(kpis_row1, columns=5)

    # Second row: Conversion and quality metrics
    st.markdown("---")
    st.markdown("#### 📈 Conversión y Calidad")
    kpis_row2 = [
        {"label": "Conversión Total", "value": conversion, "format": "%.1f%%"},
        {"label": "NPS del Hub", "value": avg_nps, "format": "%.0f"},
        {"label": "Leads Entrantes", "value": total_leads, "format": "%.0f"},
    ]
    render_kpi_grid(kpis_row2, columns=3)

    # Third row: Operational metrics
    st.markdown("---")
    st.markdown("#### ⚙️ Operación")
    kpis_row3 = [
        {"label": "Citas Agendadas", "value": total_appointments, "format": "%.0f"},
        {"label": "Reservas Activas", "value": total_reservations, "format": "%.0f"},
        {"label": "Cancelaciones", "value": total_cancellations, "format": "%.0f"},
        {"label": "SLA Lead→Venta", "value": avg_sla, "format": "%.1f días"},
    ]
    render_kpi_grid(kpis_row3, columns=4)


def render_hub_comparison(all_data, filtered_data, hub_label, country):
    """Compare region/hub performance vs country average"""
    st.subheader(f"📊 Comparación vs Promedio {country}")

    # Hub metrics
    hub_df = filtered_data["daily_metrics"]
    hub_sales = hub_df["sales"].sum()
    hub_purchases = hub_df["purchases"].sum()
    hub_leads = hub_df["leads"].sum()
    hub_conversion = (hub_sales / hub_leads * 100) if hub_leads > 0 else 0
    hub_nps = hub_df["nps"].mean()

    # Country average
    country_df = all_data["daily_metrics"][
        all_data["daily_metrics"]["country"] == country
    ].copy()
    days = PERIOD_OPTIONS[st.session_state.get("cm_period", "Últimos 30 días")]
    cutoff_date = datetime.now() - timedelta(days=days)
    country_df = country_df[country_df["date"] >= cutoff_date]

    country_sales = country_df["sales"].sum()
    country_purchases = country_df["purchases"].sum()
    country_leads = country_df["leads"].sum()
    country_conversion = (
        (country_sales / country_leads * 100) if country_leads > 0 else 0
    )
    country_nps = country_df["nps"].mean()

    # Calculate hub average for fair comparison
    num_hubs = len(country_df["hub"].unique())
    avg_sales_per_hub = country_sales / num_hubs if num_hubs > 0 else 0
    avg_purchases_per_hub = country_purchases / num_hubs if num_hubs > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_comparison(
            "Entregas",
            hub_sales,
            avg_sales_per_hub,
            format_str="%.0f",
            country_name=country,
        )

    with col2:
        render_metric_comparison(
            "Compras",
            hub_purchases,
            avg_purchases_per_hub,
            format_str="%.0f",
            country_name=country,
        )

    with col3:
        render_metric_comparison(
            "Conversión",
            hub_conversion,
            country_conversion,
            format_str="%.1f",
            suffix="%",
            country_name=country,
        )

    with col4:
        render_metric_comparison(
            "NPS", hub_nps, country_nps, format_str="%.0f", country_name=country
        )

    # Ranking
    hub_rankings = (
        country_df.groupby("region")
        .agg({"sales": "sum", "leads": "sum", "nps": "mean"})
        .reset_index()
    )
    hub_rankings["conversion"] = hub_rankings["sales"] / hub_rankings["leads"] * 100
    hub_rankings = hub_rankings.sort_values("sales", ascending=False).reset_index(
        drop=True
    )

    hub_rank = (
        hub_rankings[hub_rankings["region"] == hub_label].index[0] + 1
        if len(hub_rankings[hub_rankings["region"] == hub_label]) > 0
        else 0
    )

    st.info(f"🏆 Ranking: **#{hub_rank}** de {len(hub_rankings)} regiones en {country}")


def render_agent_advanced_filter(filtered_data):
    """
    Render advanced agent filtering section
    Allows filtering agents by multiple dimensions to quickly identify top/bottom performers
    """
    st.subheader("🔍 Filtrado Avanzado de Agentes")
    st.caption(
        "Segmenta y filtra agentes por múltiples dimensiones para identificar rápidamente top performers o agentes que necesitan apoyo"
    )

    agents_df = filtered_data["agent_performance"].copy()

    if len(agents_df) == 0:
        st.warning("No hay datos de agentes para este hub")
        return

    # === FILTROS SECTION (Minimalist) ===
    with st.expander("🔍 Filtros Avanzados", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            # Ventas filter
            min_sales = int(agents_df["sales"].min())
            max_sales = int(agents_df["sales"].max())
            sales_range = st.slider(
                "💰 Ventas",
                min_value=min_sales,
                max_value=max_sales,
                value=(min_sales, max_sales),
                key="filter_sales",
            )

        with col2:
            # CVR filter
            min_cvr = float(agents_df["conversion"].min() * 100)
            max_cvr = float(agents_df["conversion"].max() * 100)
            cvr_range = st.slider(
                "🎯 CVR (%)",
                min_value=min_cvr,
                max_value=max_cvr,
                value=(min_cvr, max_cvr),
                step=0.1,
                key="filter_cvr",
            )

        with col3:
            # NPS filter
            min_nps = float(agents_df["nps"].min())
            max_nps = float(agents_df["nps"].max())
            nps_range = st.slider(
                "⭐ NPS",
                min_value=min_nps,
                max_value=max_nps,
                value=(min_nps, max_nps),
                step=1.0,
                key="filter_nps",
            )

        # Quick action buttons in a compact row
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🏆 Top Performers", use_container_width=True):
                # Top 20% in sales and CVR
                st.session_state.filter_sales = (
                    int(agents_df["sales"].quantile(0.8)),
                    max_sales,
                )
                st.session_state.filter_cvr = (
                    float(agents_df["conversion"].quantile(0.8) * 100),
                    max_cvr,
                )
                st.rerun()

        with col2:
            if st.button("⚠️ Necesitan Apoyo", use_container_width=True):
                # Bottom 20% in sales or CVR
                st.session_state.filter_cvr = (
                    min_cvr,
                    float(agents_df["conversion"].quantile(0.3) * 100),
                )
                st.rerun()

        with col3:
            if st.button("⭐ Alto NPS", use_container_width=True):
                # NPS > 70
                st.session_state.filter_nps = (70.0, max_nps)
                st.rerun()

        with col4:
            if st.button("🔄 Resetear", use_container_width=True):
                st.session_state.filter_sales = (min_sales, max_sales)
                st.session_state.filter_cvr = (min_cvr, max_cvr)
                st.session_state.filter_nps = (min_nps, max_nps)
                st.rerun()

    # === APPLY FILTERS ===
    filtered_agents = agents_df[
        (agents_df["sales"] >= sales_range[0])
        & (agents_df["sales"] <= sales_range[1])
        & (agents_df["conversion"] * 100 >= cvr_range[0])
        & (agents_df["conversion"] * 100 <= cvr_range[1])
        & (agents_df["nps"] >= nps_range[0])
        & (agents_df["nps"] <= nps_range[1])
    ].copy()

    # === RESULTS ===
    st.markdown("---")
    st.markdown(
        f"### 📊 Resultados: **{len(filtered_agents)}** de **{len(agents_df)}** agentes"
    )

    if len(filtered_agents) == 0:
        st.warning("❌ No hay agentes que cumplan con los filtros seleccionados")
        return

    # Summary stats of filtered agents
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_sales = filtered_agents["sales"].mean()
        st.metric("Ventas Promedio", f"{avg_sales:.1f}")

    with col2:
        avg_cvr = filtered_agents["conversion"].mean() * 100
        st.metric("CVR Promedio", f"{avg_cvr:.1f}%")

    with col3:
        avg_nps = filtered_agents["nps"].mean()
        st.metric("NPS Promedio", f"{avg_nps:.0f}")

    # Sort options
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("#### 👥 Agentes Filtrados")

    with col2:
        sort_by = st.selectbox(
            "Ordenar por:", ["Entregas", "CVR", "NPS"], key="sort_agents"
        )

    # Sort
    sort_mapping = {
        "Entregas": ("sales", False),
        "CVR": ("conversion", False),
        "NPS": ("nps", False),
    }

    sort_col, ascending = sort_mapping[sort_by]
    filtered_agents = filtered_agents.sort_values(sort_col, ascending=ascending)

    # Add status badge
    filtered_agents["status"] = filtered_agents.apply(
        lambda row: render_agent_status_badge(row["conversion"], row["nps"]), axis=1
    )

    # Display filtered agents in a table format (compact view)
    st.markdown("💡 *Haz clic en 'Ver Perfil' para ver detalles del agente*")

    # Create display dataframe for table
    for idx, (_, agent) in enumerate(filtered_agents.iterrows()):
        # Create a single row with all metrics and button - more compact columns
        col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1, 1, 1, 1.2, 1.8])

        with col1:
            # Agent name with ranking - smaller text
            st.markdown(f"**#{idx + 1} - {agent['agent_name']}**")

        with col2:
            st.markdown(
                f"<div style='text-align: center;'><h3 style='margin:0;'>{agent['sales']:.0f}</h3><small style='color: gray;'>ENTREGAS</small></div>",
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"<div style='text-align: center;'><h3 style='margin:0;'>{agent['conversion']*100:.1f}%</h3><small style='color: gray;'>CVR</small></div>",
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"<div style='text-align: center;'><h3 style='margin:0;'>{agent['nps']:.0f}</h3><small style='color: gray;'>NPS</small></div>",
                unsafe_allow_html=True,
            )

        with col5:
            st.markdown(
                f"<div style='text-align: center;'><h3 style='margin:0;'>{agent['leads']:.0f}</h3><small style='color: gray;'>LEADS</small></div>",
                unsafe_allow_html=True,
            )

        with col6:
            # Status badge and button - more compact
            st.markdown(
                f"<small>Estado: {agent['status']}</small>", unsafe_allow_html=True
            )
            if st.button(
                "👁️ Ver Perfil Completo",
                key=f"profile_filtered_{agent['agent_name']}_{idx}",
                use_container_width=True,
            ):
                # Set navigation state - now navigates to unified kavako dashboard
                st.session_state.navigation_view = "agent_profile"
                st.session_state.selected_agent_name = agent["agent_name"]
                # Also set the kavako_agent for compatibility with the kavako dashboard
                st.session_state.kavako_agent = agent["agent_name"]
                # Find and set the hub for the agent
                st.session_state.kavako_hub_selector = agent.get(
                    "hub", agent.get("region", "")
                )
                st.session_state.nav_breadcrumb = [
                    {"label": "City Manager", "view": "city_manager"},
                    {"label": agent["agent_name"], "view": "agent_profile"},
                ]
                st.rerun()

        # Add separator between agents - thinner
        if idx < len(filtered_agents) - 1:
            st.markdown(
                "<hr style='margin: 0.5rem 0; border: none; border-top: 1px solid #e0e0e0;'>",
                unsafe_allow_html=True,
            )


def render_agent_optimization(filtered_data):
    """
    Render agent optimization section with dealership approach
    Focus on maximizing each agent's efficiency
    """
    st.subheader("🎯 Optimización de Agentes")
    st.caption("Maximiza la eficiencia de cada agente")

    agents_df = filtered_data["agent_performance"].copy()

    if len(agents_df) == 0:
        st.warning("No hay datos de agentes para este hub")
        return

    # === SECCIÓN 1: CAPACIDAD VS UTILIZACIÓN ===
    st.markdown("### 📅 Capacidad vs Utilización")

    col1, col2 = st.columns(2)

    with col1:
        # Tabla de capacidad
        capacity_df = agents_df[
            [
                "agent_name",
                "slots_per_week",
                "appointments",
                "available_slots",
                "utilization",
                "backlog_cartera",
            ]
        ].copy()

        capacity_df = capacity_df.sort_values("utilization", ascending=False)

        capacity_display = capacity_df.copy()
        capacity_display.columns = [
            "Agente",
            "Slots Semanales",
            "Citas Agendadas",
            "Slots Disponibles",
            "Utilización %",
            "Backlog Cartera",
        ]
        capacity_display["Utilización %"] = (
            capacity_display["Utilización %"] * 100
        ).round(1)

        # Style by utilization
        def style_utilization(row):
            util = row["Utilización %"]
            if util >= 80:
                return ["background-color: #c8e6c9"] * len(
                    row
                )  # Verde - alta utilización
            elif util < 60:
                return ["background-color: #fff9c4"] * len(
                    row
                )  # Amarillo - baja utilización
            else:
                return [""] * len(row)

        styled_capacity = capacity_display.style.apply(
            style_utilization, axis=1
        ).format(
            {
                "Slots Semanales": "{:.0f}",
                "Citas Agendadas": "{:.0f}",
                "Slots Disponibles": "{:.0f}",
                "Utilización %": "{:.1f}%",
                "Backlog Cartera": "{:.0f}",
            }
        )

        st.dataframe(styled_capacity, use_container_width=True, height=350)

    with col2:
        # Insights de capacidad
        st.markdown("**💡 Insights de Capacidad**")

        avg_utilization = agents_df["utilization"].mean() * 100
        total_available_slots = agents_df["available_slots"].sum()
        total_backlog = agents_df["backlog_cartera"].sum()

        st.metric("Utilización Promedio del Hub", f"{avg_utilization:.1f}%")
        st.metric("Total Slots Disponibles", f"{total_available_slots:.0f}")
        st.metric("Total Backlog de Cartera", f"{total_backlog:.0f}")

        # Agentes con capacidad disponible
        underutilized = agents_df[agents_df["utilization"] < 0.70]
        if len(underutilized) > 0:
            st.warning(f"⚠️ {len(underutilized)} agente(s) con utilización < 70%")
            for _, agent in underutilized.head(3).iterrows():
                st.caption(
                    f"• {agent['agent_name']}: {agent['available_slots']:.0f} slots disponibles"
                )
        else:
            st.success("✅ Todos los agentes bien utilizados")

    st.markdown("---")

    # === SECCIÓN 3: CALIDAD DEL STOCK ASIGNADO ===
    st.markdown("### 🚗 Calidad del Stock Asignado")

    col3, col4 = st.columns(2)

    with col3:
        # Tabla de stock
        stock_df = agents_df[
            [
                "agent_name",
                "stock_assigned",
                "stock_avg_age",
                "stock_attractiveness",
                "lead_match_score",
            ]
        ].copy()

        stock_df = stock_df.sort_values("stock_attractiveness", ascending=False)

        stock_display = stock_df.copy()
        stock_display.columns = [
            "Agente",
            "Autos Asignados",
            "Edad Promedio (días)",
            "Atractivo",
            "Match con Leads",
        ]

        # Style by stock attractiveness
        def style_stock(row):
            attr = row["Atractivo"]
            if attr >= 75:
                return ["background-color: #c8e6c9"] * len(row)
            elif attr < 60:
                return ["background-color: #ffccbc"] * len(row)
            else:
                return [""] * len(row)

        styled_stock = stock_display.style.apply(style_stock, axis=1).format(
            {
                "Autos Asignados": "{:.0f}",
                "Edad Promedio (días)": "{:.0f}",
                "Atractivo": "{:.0f}/100",
                "Match con Leads": "{:.0f}/100",
            }
        )

        st.dataframe(styled_stock, use_container_width=True, height=350)

    with col4:
        st.markdown("**📊 Análisis de Stock**")

        avg_stock_quality = agents_df["stock_attractiveness"].mean()
        avg_age = agents_df["stock_avg_age"].mean()
        avg_match = agents_df["lead_match_score"].mean()

        st.metric("Atractivo Promedio del Stock", f"{avg_stock_quality:.0f}/100")
        st.metric("Edad Promedio del Stock", f"{avg_age:.0f} días")
        st.metric("Match Promedio con Leads", f"{avg_match:.0f}/100")

        # Agentes con stock de baja calidad
        low_stock = agents_df[agents_df["stock_attractiveness"] < 65]
        if len(low_stock) > 0:
            st.warning(f"⚠️ {len(low_stock)} agente(s) con stock poco atractivo")
            for _, agent in low_stock.head(3).iterrows():
                st.caption(
                    f"• {agent['agent_name']}: {agent['stock_attractiveness']:.0f}/100 (edad: {agent['stock_avg_age']:.0f}d)"
                )
        else:
            st.success("✅ Todo el stock tiene buena calidad")


def render_incentives_module(filtered_data):
    """Render unified gamification and incentives module with composite points"""
    st.subheader("🏆 Sistema de Incentivos Unificado")
    st.caption(
        "Puntos compuestos basados en entregas, productos adicionales y ownership"
    )

    agents_df = filtered_data["agent_performance"].copy()

    if len(agents_df) == 0:
        st.info("No hay datos de agentes")
        return

    # Check if new columns exist
    has_composite_points = "total_points" in agents_df.columns

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(
        ["📊 Ranking & Niveles", "🤝 Ownership Score", "📋 Objetivos Tradicionales"]
    )

    with tab1:
        if has_composite_points:
            render_composite_points_tab(agents_df)
        else:
            st.info("⏳ Reinicia la app para cargar las nuevas métricas de puntos")

    with tab2:
        if has_composite_points:
            render_ownership_tab(agents_df)
        else:
            st.info("⏳ Reinicia la app para cargar las nuevas métricas de ownership")

    with tab3:
        render_traditional_goals_tab(agents_df)


def render_composite_points_tab(agents_df):
    """Render composite points ranking and levels"""
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_points = agents_df["total_points"].mean()
        st.metric("Puntos Promedio", f"{avg_points:,.0f}")

    with col2:
        avg_pts_delivery = agents_df["points_per_delivery"].mean()
        st.metric("Pts/Entrega Prom.", f"{avg_pts_delivery:.0f}")

    with col3:
        diamond = len(agents_df[agents_df["incentive_level"] == "💎 Diamond"])
        gold = len(agents_df[agents_df["incentive_level"] == "🥇 Gold"])
        st.metric("💎 Diamond + 🥇 Gold", f"{diamond + gold}")

    with col4:
        total_revenue = agents_df["revenue"].sum()
        st.metric("Revenue Total", f"${total_revenue:,.0f}")

    st.markdown("---")

    # Leaderboard by points
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("#### 📊 Ranking por Puntos Compuestos")

        # Sort by total points
        leaderboard = agents_df.sort_values("total_points", ascending=False).head(10)

        for idx, (_, agent) in enumerate(leaderboard.iterrows()):
            expander_label = f"#{idx + 1} {agent['agent_name']} - {agent['incentive_level']} ({agent['total_points']:,.0f} pts)"

            with st.expander(expander_label, expanded=idx == 0):
                # Use simple text layout instead of columns to avoid overlap
                st.markdown("**📊 Desglose de Puntos:**")
                st.text(
                    f"Base: {agent['base_points']:,.0f} | "
                    f"Financing: +{agent['financing_points']:,.0f} | "
                    f"Garantía: +{agent['warranty_points']:,.0f} | "
                    f"Seguro: +{agent['insurance_points']:,.0f} | "
                    f"Trade-in: +{agent['tradein_points']:,.0f} | "
                    f"NPS Bonus: +{agent['nps_bonus']:,.0f}"
                )

                st.markdown("**📈 Penetraciones:**")
                st.text(
                    f"Financing: {agent['financing_penetration']:.1f}% | "
                    f"Ancillaries: {agent['ancillary_penetration']:.1f}% | "
                    f"Seguro: {agent['insurance_penetration']:.1f}% | "
                    f"Garantía: {agent['extended_warranty_penetration']:.1f}% | "
                    f"NPS: {agent['nps']:.0f}"
                )

                st.markdown("**🎯 Eficiencia:**")
                st.text(
                    f"Pts/Entrega: {agent['points_per_delivery']:.0f} | "
                    f"Revenue/Slot: ${agent['revenue_per_slot']:,.0f} | "
                    f"Entregas: {agent['sales']:.0f} | "
                    f"Ownership: {agent['ownership_score']:.1f}%"
                )

    with col_right:
        st.markdown("#### 📋 Distribución por Nivel")

        level_counts = agents_df["incentive_level"].value_counts()

        for level in ["💎 Diamond", "🥇 Gold", "🥈 Silver", "🥉 Bronze"]:
            count = level_counts.get(level, 0)
            pct = count / len(agents_df) * 100 if len(agents_df) > 0 else 0
            st.markdown(f"**{level}:** {count} ({pct:.0f}%)")

        st.markdown("---")
        st.markdown("#### 💡 Cómo ganar puntos")
        st.caption("• Base: 100 pts/entrega")
        st.caption("• Financing: +50 pts")
        st.caption("• Kavak Total: +30 pts")
        st.caption("• Seguro: +20 pts")
        st.caption("• Trade-in: +20 pts")
        st.caption("• NPS ≥80: +25 pts")


def render_ownership_tab(agents_df):
    """Render ownership score analysis"""
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_ownership = agents_df["ownership_score"].mean()
        st.metric("Ownership Promedio", f"{avg_ownership:.1f}%")

    with col2:
        total_handoffs = agents_df["handoffs"].sum()
        st.metric("Handoffs Totales", f"{total_handoffs:.0f}")

    with col3:
        high_ownership = len(agents_df[agents_df["ownership_score"] >= 85])
        st.metric("Ownership ≥85%", f"{high_ownership}")

    with col4:
        low_ownership = len(agents_df[agents_df["ownership_score"] < 70])
        st.metric("Ownership <70%", f"{low_ownership}", delta_color="inverse")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🌟 Top Ownership (Mayor autonomía)")

        top_ownership = agents_df.sort_values("ownership_score", ascending=False).head(
            5
        )

        for _, agent in top_ownership.iterrows():
            ownership = agent["ownership_score"]
            if ownership >= 90:
                emoji = "🏆"
            elif ownership >= 80:
                emoji = "⭐"
            else:
                emoji = "👍"

            st.success(
                f"{emoji} **{agent['agent_name']}** - {ownership:.1f}% "
                f"({agent['sales']:.0f} entregas, {agent['handoffs']:.0f} handoffs)"
            )

    with col_right:
        st.markdown("#### ⚠️ Oportunidad de Mejora")

        low_ownership = agents_df.sort_values("ownership_score", ascending=True).head(5)

        for _, agent in low_ownership.iterrows():
            ownership = agent["ownership_score"]
            handoffs = agent["handoffs"]

            st.warning(
                f"**{agent['agent_name']}** - {ownership:.1f}% "
                f"({handoffs:.0f} handoffs)"
            )
            if handoffs > 3:
                st.caption("   → Reducir traspasos mejorará ownership y experiencia")

    st.markdown("---")
    st.markdown("#### 💡 ¿Qué es Ownership Score?")
    st.info(
        "El **Ownership Score** mide qué porcentaje de clientes cada agente "
        "maneja de principio a fin sin traspasos (handoffs). Un alto ownership "
        "significa mejor experiencia del cliente y mayor responsabilidad del agente."
    )


def render_traditional_goals_tab(agents_df):
    """Render traditional incentive goals"""
    # Calculate points for each agent based on traditional goals
    agents_df = agents_df.copy()
    agents_df["goal_points"] = 0

    for goal in INCENTIVE_GOALS:
        metric = goal["metric"]
        threshold = goal["threshold"]
        points = goal["points"]
        is_inverse = goal.get("inverse", False)

        if metric in agents_df.columns:
            if is_inverse:
                agents_df.loc[agents_df[metric] <= threshold, "goal_points"] += points
            else:
                agents_df.loc[agents_df[metric] >= threshold, "goal_points"] += points

    # Sort by points
    agents_df = agents_df.sort_values("goal_points", ascending=False)

    # Display goals
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("**🎯 Objetivos Activos:**")
        for goal in INCENTIVE_GOALS:
            st.markdown(
                f"• **{goal['name']}**: {goal['description']} (+{goal['points']} pts)"
            )

    with col2:
        st.markdown("**📊 Ranking por Objetivos:**")

        leaderboard = agents_df[["agent_name", "goal_points"]].head(10).copy()
        leaderboard.columns = ["Agente", "Puntos Objetivos"]
        leaderboard.index = range(1, len(leaderboard) + 1)

        st.dataframe(leaderboard, use_container_width=True)


def render_recommendations_module(filtered_data):
    """Render automatic recommendations for agents"""
    st.subheader("💡 Recomendaciones Automáticas")

    agents_df = filtered_data["agent_performance"].copy()

    if len(agents_df) == 0:
        st.info("No hay datos de agentes")
        return

    recommendations = []

    for _, agent in agents_df.iterrows():
        agent_recs = []

        # Check utilization
        if agent["utilization"] < 0.70:
            agent_recs.append(
                f"📅 Baja utilización ({agent['utilization']*100:.0f}%) - Asignar más leads para llenar {agent['available_slots']:.0f} slots disponibles"
            )
        elif agent["utilization"] > 0.90:
            agent_recs.append(
                f"✅ Alta utilización ({agent['utilization']*100:.0f}%) - Agente bien aprovechado"
            )

        # Check stock quality
        if agent["stock_attractiveness"] < 65:
            agent_recs.append(
                f"🚗 Stock poco atractivo ({agent['stock_attractiveness']:.0f}/100, edad: {agent['stock_avg_age']:.0f}d) - Renovar inventario asignado"
            )

        # Check aprovechamiento
        if agent["aprovechamiento_pct"] < 15:
            agent_recs.append(
                f"⚠️ Bajo aprovechamiento ({agent['aprovechamiento_pct']:.1f}%) - Capacitación en cierre o mejorar calidad de leads"
            )

        # Check backlog
        if agent["backlog_cartera"] > 20:
            agent_recs.append(
                f"📋 Alto backlog ({agent['backlog_cartera']:.0f} leads) - Priorizar seguimiento de cartera"
            )

        if agent_recs:
            recommendations.append(
                {"agent": agent["agent_name"], "recommendations": agent_recs}
            )

    if recommendations:
        # Show top recommendations
        for rec in recommendations[:5]:  # Top 5 agentes con recomendaciones
            with st.expander(f"🎯 {rec['agent']}", expanded=False):
                for r in rec["recommendations"]:
                    st.markdown(f"- {r}")
    else:
        st.success("✅ No hay recomendaciones críticas - Hub operando óptimamente")


def render_operational_alerts(filtered_data, hub_label):
    """Render operational alerts with dynamic detection - collapsible by type"""
    st.subheader("🚨 Alertas Operativas")

    # Detect alerts dynamically
    alerts = detect_operational_alerts(filtered_data, hub_label)

    if len(alerts) == 0:
        st.success(
            "✅ No hay alertas operativas activas - Hub funcionando correctamente"
        )
        return

    # Separate alerts by type
    critical_alerts = [a for a in alerts if a["type"] == "critical"]
    warning_alerts = [a for a in alerts if a["type"] == "warning"]

    # Display alert summary
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🚨 Críticas", len(critical_alerts))
    with col2:
        st.metric("⚠️ Advertencias", len(warning_alerts))

    st.markdown("---")

    # Render critical alerts in expandable section
    if critical_alerts:
        with st.expander(f"🚨 **Críticas** ({len(critical_alerts)})", expanded=False):
            for alert in critical_alerts:
                render_alert_box(
                    alert["type"],
                    alert["title"],
                    alert["description"],
                    alert.get("timestamp"),
                )

    # Render warning alerts in expandable section
    if warning_alerts:
        with st.expander(
            f"⚠️ **Advertencias** ({len(warning_alerts)})", expanded=False
        ):
            for alert in warning_alerts:
                render_alert_box(
                    alert["type"],
                    alert["title"],
                    alert["description"],
                    alert.get("timestamp"),
                )


def render_lead_assignment_simulator(filtered_data):
    """Render lead assignment simulator for optimal distribution"""
    st.subheader("🎯 Simulador de Asignación de Leads")
    st.caption(
        "Simula la asignación óptima de nuevos leads basada en capacidad y eficiencia"
    )

    agents_df = filtered_data["agent_performance"].copy()

    if len(agents_df) == 0:
        st.warning("No hay datos de agentes")
        return

    if "capacity_for_leads" not in agents_df.columns:
        st.info("⏳ Reinicia la app para cargar las nuevas métricas")
        return

    # Input: How many leads to assign
    col_input, col_method = st.columns(2)

    with col_input:
        new_leads = st.number_input(
            "📥 Nuevos leads a asignar",
            min_value=1,
            max_value=100,
            value=20,
            step=5,
            key="simulator_leads",
        )

    with col_method:
        method = st.radio(
            "Método de asignación",
            ["🎯 Óptimo (por eficiencia)", "⚖️ Uniforme", "📊 Por capacidad"],
            key="simulator_method",
            horizontal=True,
        )

    st.markdown("---")

    # Calculate assignments
    agents_df = agents_df.copy()

    if method == "🎯 Óptimo (por eficiencia)":
        # Prioritize by efficiency_composite, limited by capacity
        agents_df["priority_score"] = (
            agents_df["efficiency_composite"] * 0.6
            + (1 - agents_df["utilization"]) * 100 * 0.4
        )
        agents_df = agents_df.sort_values("priority_score", ascending=False)

        remaining_leads = new_leads
        assignments = []

        for _, agent in agents_df.iterrows():
            if remaining_leads <= 0:
                break
            # Assign up to their capacity
            can_take = min(agent["capacity_for_leads"], remaining_leads)
            if can_take > 0:
                assignments.append(
                    {
                        "agent": agent["agent_name"],
                        "leads": int(can_take),
                        "efficiency": agent["efficiency_composite"],
                        "capacity": agent["capacity_for_leads"],
                        "revenue_per_slot": agent["revenue_per_slot"],
                    }
                )
                remaining_leads -= can_take

    elif method == "⚖️ Uniforme":
        # Distribute evenly
        leads_per_agent = new_leads // len(agents_df)
        remainder = new_leads % len(agents_df)

        assignments = []
        for idx, (_, agent) in enumerate(agents_df.iterrows()):
            leads = leads_per_agent + (1 if idx < remainder else 0)
            assignments.append(
                {
                    "agent": agent["agent_name"],
                    "leads": leads,
                    "efficiency": agent["efficiency_composite"],
                    "capacity": agent["capacity_for_leads"],
                    "revenue_per_slot": agent["revenue_per_slot"],
                }
            )

    else:  # Por capacidad
        # Distribute proportionally to available capacity
        total_capacity = agents_df["capacity_for_leads"].sum()
        assignments = []

        for _, agent in agents_df.iterrows():
            if total_capacity > 0:
                pct = agent["capacity_for_leads"] / total_capacity
                leads = int(new_leads * pct)
            else:
                leads = 0
            assignments.append(
                {
                    "agent": agent["agent_name"],
                    "leads": leads,
                    "efficiency": agent["efficiency_composite"],
                    "capacity": agent["capacity_for_leads"],
                    "revenue_per_slot": agent["revenue_per_slot"],
                }
            )

    # Calculate expected revenue
    assignments_df = pd.DataFrame(assignments)
    assignments_df = assignments_df[assignments_df["leads"] > 0]

    # Estimate revenue (leads * conversion * avg ticket)
    avg_conversion = 0.15  # 15% conversion
    avg_ticket = 22000

    assignments_df["expected_revenue"] = (
        assignments_df["leads"]
        * avg_conversion
        * avg_ticket
        * (assignments_df["efficiency"] / 100)
    )

    total_expected_revenue = assignments_df["expected_revenue"].sum()

    # Display results
    col_results, col_summary = st.columns([2, 1])

    with col_results:
        st.markdown("#### 📋 Asignación Propuesta")

        if len(assignments_df) > 0:
            for _, row in assignments_df.iterrows():
                efficiency_color = (
                    "🟢"
                    if row["efficiency"] > 70
                    else "🟡"
                    if row["efficiency"] > 50
                    else "🔴"
                )
                st.markdown(
                    f"**{row['agent']}:** +{row['leads']} leads | "
                    f"Efic: {efficiency_color} {row['efficiency']:.0f} | "
                    f"Revenue Est: ${row['expected_revenue']:,.0f}"
                )
        else:
            st.warning("No hay agentes con capacidad disponible")

    with col_summary:
        st.markdown("#### 📈 Resumen")
        st.metric("Leads a asignar", new_leads)
        st.metric("Agentes involucrados", len(assignments_df))
        st.metric("Revenue Esperado", f"${total_expected_revenue:,.0f}")

        # Compare with uniform
        if method == "🎯 Óptimo (por eficiencia)":
            # Calculate uniform revenue for comparison
            uniform_efficiency = agents_df["efficiency_composite"].mean()
            uniform_revenue = (
                new_leads * avg_conversion * avg_ticket * (uniform_efficiency / 100)
            )
            improvement = (
                (total_expected_revenue - uniform_revenue) / uniform_revenue * 100
                if uniform_revenue > 0
                else 0
            )
            if improvement > 0:
                st.success(f"📈 +{improvement:.1f}% vs distribución uniforme")

    # Action button (simulated)
    st.markdown("---")
    if st.button("✅ Aplicar Asignación", use_container_width=True, type="primary"):
        st.success(
            "✅ Asignación aplicada (simulado). Los leads se distribuirán según el plan."
        )
