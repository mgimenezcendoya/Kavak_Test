"""
CEO Executive Dashboard View
High-level strategic view with country/hub filters
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
from config import COLORS, COUNTRIES, HUBS, PERIOD_OPTIONS
from utils.alert_detector import detect_strategic_alerts
from utils.components import (
    render_alert_box,
    render_bar_chart,
    render_funnel_chart,
    render_kpi_card,
    render_kpi_grid,
    render_trend_chart,
)


def render_ceo_dashboard(data):
    """
    Render the CEO Executive Dashboard
    """
    st.header("📊 Executive Dashboard")
    st.markdown("Visión macro del negocio por país / hub")

    # Filters
    render_filters()

    # Get filtered data
    filtered_data = filter_data(
        data,
        st.session_state.get("ceo_country", "Todos"),
        st.session_state.get("ceo_region", "Todos"),
        st.session_state.get("ceo_hub", "Todos los Hubs"),
        st.session_state.get("ceo_period", "Últimos 30 días"),
    )

    # KPI Section
    st.markdown("---")
    render_kpi_section(filtered_data)

    # Hub Comparison Section
    st.markdown("---")
    country_filter = st.session_state.get("ceo_country", "Todos")
    hub_filter = st.session_state.get("ceo_hub", "Todos")
    if hub_filter == "Todos":  # Only show comparison when viewing multiple hubs
        render_hub_comparison_section(filtered_data, country_filter)

    # Performance Table Section (NEW - Collapsible)
    st.markdown("---")
    render_performance_table_section(data, country_filter)

    # Alerts Section (Dynamic)
    st.markdown("---")
    period_days = PERIOD_OPTIONS[st.session_state.get("ceo_period", "Últimos 30 días")]
    render_alerts_section(data, period_days)


def render_filters():
    """Render filter controls"""
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])

    with col1:
        country_options = ["Todos"] + COUNTRIES
        country = st.selectbox("País", country_options, key="ceo_country")

    with col2:
        if country != "Todos":
            region_options = ["Todos"] + HUBS.get(country, [])
        else:
            region_options = ["Todos"]

        region = st.selectbox("Región", region_options, key="ceo_region")

    with col3:
        # Get hubs for selected region from REGIONS_HUBS
        from config import REGIONS_HUBS

        hub_options = ["Todos los Hubs"]
        if country != "Todos" and region != "Todos":
            if region in REGIONS_HUBS.get(country, {}):
                hub_options = ["Todos los Hubs"] + REGIONS_HUBS[country][region]

        hub = st.selectbox("Hub", hub_options, key="ceo_hub")

    with col4:
        period = st.selectbox("Periodo", list(PERIOD_OPTIONS.keys()), key="ceo_period")

    with col5:
        if st.button("🔄 Actualizar", use_container_width=True):
            st.rerun()


def filter_data(data, country, region, hub, period):
    """Filter data based on selections"""
    daily_metrics = data["daily_metrics"].copy()
    inventory = data["inventory"].copy()
    funnel = data["funnel"].copy()

    # Filter by country
    if country != "Todos":
        daily_metrics = daily_metrics[daily_metrics["country"] == country]
        inventory = inventory[inventory["country"] == country]
        funnel = funnel[funnel["country"] == country]

    # Filter by region
    if region != "Todos":
        daily_metrics = daily_metrics[daily_metrics["region"] == region]
        inventory = inventory[inventory["region"] == region]
        funnel = funnel[funnel["region"] == region]

    # Filter by hub
    if hub != "Todos los Hubs":
        daily_metrics = daily_metrics[daily_metrics["hub"] == hub]
        inventory = inventory[inventory["hub"] == hub]
        funnel = funnel[funnel["hub"] == hub]

    # Filter by period
    days = PERIOD_OPTIONS[period]
    cutoff_date = datetime.now() - timedelta(days=days)
    daily_metrics = daily_metrics[daily_metrics["date"] >= cutoff_date]

    return {
        "daily_metrics": daily_metrics,
        "agent_performance": data["agent_performance"],
        "inventory": inventory,
        "funnel": funnel,
    }


def render_kpi_section(filtered_data):
    """Render KPI cards grouped by category using real unit economics from data"""
    df = filtered_data["daily_metrics"]

    if len(df) == 0:
        st.warning("No hay datos para los filtros seleccionados")
        return

    # Calculate aggregated metrics
    total_sales = df["sales"].sum()
    total_purchases = df["purchases"].sum()
    total_revenue = df["revenue"].sum()
    avg_ticket = df["ticket_avg"].mean()
    total_leads = df["leads"].sum()
    total_conversions = total_sales / total_leads if total_leads > 0 else 0
    avg_cost_per_lead = df["cost_per_lead"].mean()
    avg_nps = df["nps"].mean()
    avg_csat = df["csat"].mean()
    avg_sla = df["sla_lead_to_sale"].mean()
    total_cancellations = df["cancellations"].sum()

    # Calculate inventory metrics
    inventory_df = filtered_data.get("inventory", pd.DataFrame())
    if len(inventory_df) > 0:
        total_inventory = inventory_df["total_inventory"].sum()
        available_inventory = inventory_df["available"].sum()
    else:
        total_inventory = 0
        available_inventory = 0

    # Use real unit economics from data (now comes from data_generator with real values)
    full_margin = df["full_margin"].mean() if "full_margin" in df.columns else 950
    fin_ins_unit_economic = df["fin_ins"].mean() if "fin_ins" in df.columns else 1200
    warranty_unit_economic = (
        df["kt"].mean() if "kt" in df.columns else 150
    )  # KT = Kavak Trade

    # PC1 from data or calculate
    pc1 = (
        df["pc1"].mean()
        if "pc1" in df.columns
        else (full_margin + fin_ins_unit_economic + warranty_unit_economic)
    )

    # eCAC from data
    current_ecac = df["ecac"].mean() if "ecac" in df.columns else 350

    # PC1 - eCAC
    pc1_minus_ecac = (
        df["pc1_minus_ecac"].mean()
        if "pc1_minus_ecac" in df.columns
        else (pc1 - current_ecac)
    )

    # Gross Margin Stock
    potential_revenue = (
        avg_ticket * available_inventory if available_inventory > 0 else 0
    )
    gross_margin_stock = (
        potential_revenue / available_inventory if available_inventory > 0 else 0
    )

    # Calculate deltas (compare to previous period)
    prev_period_df = get_previous_period_data(df)

    # Previous period metrics for deltas
    if len(prev_period_df) > 0:
        prev_sales = prev_period_df["sales"].sum()
        prev_purchases = prev_period_df["purchases"].sum()
        prev_revenue = prev_period_df["revenue"].sum()
        prev_leads = prev_period_df["leads"].sum()
        prev_cost_per_lead = prev_period_df["cost_per_lead"].mean()
        prev_avg_ticket = prev_revenue / prev_sales if prev_sales > 0 else 0

        # Previous unit economics from data
        prev_full_margin = (
            prev_period_df["full_margin"].mean()
            if "full_margin" in prev_period_df.columns
            else full_margin
        )
        prev_fin_ins_unit_economic = (
            prev_period_df["fin_ins"].mean()
            if "fin_ins" in prev_period_df.columns
            else fin_ins_unit_economic
        )
        prev_warranty_unit_economic = (
            prev_period_df["kt"].mean()
            if "kt" in prev_period_df.columns
            else warranty_unit_economic
        )
        prev_pc1 = (
            prev_period_df["pc1"].mean() if "pc1" in prev_period_df.columns else pc1
        )
        prev_ecac = (
            prev_period_df["ecac"].mean()
            if "ecac" in prev_period_df.columns
            else current_ecac
        )
        prev_pc1_minus_ecac = (
            prev_period_df["pc1_minus_ecac"].mean()
            if "pc1_minus_ecac" in prev_period_df.columns
            else pc1_minus_ecac
        )
        prev_conversion = prev_sales / prev_leads if prev_leads > 0 else 0
    else:
        prev_sales = total_sales
        prev_purchases = total_purchases
        prev_revenue = total_revenue
        prev_leads = total_leads
        prev_cost_per_lead = avg_cost_per_lead
        prev_full_margin = full_margin
        prev_avg_ticket = avg_ticket
        prev_conversion = total_conversions
        prev_fin_ins_unit_economic = fin_ins_unit_economic
        prev_warranty_unit_economic = warranty_unit_economic
        prev_pc1 = pc1
        prev_ecac = current_ecac
        prev_pc1_minus_ecac = pc1_minus_ecac

    # 1. FINANCIEROS
    st.subheader("💰 Financieros")

    # KPIs en una sola fila con separadores visuales entre secciones
    col1, col2, sep1, col3, col4, col5, sep2, col6, col7, col8 = st.columns(
        [1, 1, 0.1, 1, 1, 1, 0.1, 1, 1, 1]
    )

    # Sección 1: Volumen
    with col1:
        delta_sales = calculate_delta(total_sales, prev_sales)
        st.metric("Entregas", f"{total_sales:,.0f}", delta_sales)
    with col2:
        delta_purchases = calculate_delta(total_purchases, prev_purchases)
        st.metric("Compras", f"{total_purchases:,.0f}", delta_purchases)

    # Separador vertical 1
    with sep1:
        st.markdown(
            "<div style='border-left: 2px solid #CBD5E1; height: 60px; margin: 0 auto;'></div>",
            unsafe_allow_html=True,
        )

    # Sección 2: Unit Economics
    with col3:
        delta_margin = calculate_delta(full_margin, prev_full_margin)
        st.metric("Full Margin", f"${full_margin:,.0f}", delta_margin)
    with col4:
        delta_fin_ins = calculate_delta(
            fin_ins_unit_economic, prev_fin_ins_unit_economic
        )
        st.metric("Fin & Ins", f"${fin_ins_unit_economic:,.0f}", delta_fin_ins)
    with col5:
        delta_warranty = calculate_delta(
            warranty_unit_economic, prev_warranty_unit_economic
        )
        st.metric("KT", f"${warranty_unit_economic:,.0f}", delta_warranty)

    # Separador vertical 2
    with sep2:
        st.markdown(
            "<div style='border-left: 2px solid #CBD5E1; height: 60px; margin: 0 auto;'></div>",
            unsafe_allow_html=True,
        )

    # Sección 3: Contribution & CAC
    with col6:
        delta_pc1 = calculate_delta(pc1, prev_pc1)
        st.metric("PC1", f"${pc1:,.0f}", delta_pc1)
    with col7:
        delta_ecac = calculate_delta(current_ecac, prev_ecac)
        st.metric("eCAC", f"${current_ecac:,.0f}", delta_ecac, delta_color="inverse")
    with col8:
        delta_pc1_ecac = calculate_delta(pc1_minus_ecac, prev_pc1_minus_ecac)
        st.metric("PC1 - eCAC", f"${pc1_minus_ecac:,.0f}", delta_pc1_ecac)

    # 2. SALUD DE LA DEMANDA
    st.markdown("---")
    st.subheader("📈 Salud de la Demanda")

    demand_kpis = [
        {
            "label": "Leads Totales",
            "value": total_leads,
            "format": "%.0f",
            "delta": calculate_delta(total_leads, prev_leads),
        },
        {
            "label": "Conversión Total",
            "value": total_conversions * 100,
            "format": "%.1f%%",
            "delta": calculate_delta(total_conversions, prev_conversion),
        },
        {
            "label": "Costo por Lead",
            "value": avg_cost_per_lead,
            "format": "$%.0f",
            "delta": calculate_delta(avg_cost_per_lead, prev_cost_per_lead),
            "delta_color": "inverse",
        },
    ]
    render_kpi_grid(demand_kpis, columns=3)

    # 3. EXPERIENCIA DE CLIENTE
    st.markdown("---")
    st.subheader("😊 Experiencia de Cliente")

    # Mock NPS breakdowns (Buyer/Seller/Relational) based on avg_nps
    nps_buyer = avg_nps + 2  # Buyers usually happier
    nps_seller = avg_nps - 3  # Sellers often more critical on price
    nps_relational = avg_nps  # Proxy

    cx_kpis = [
        {"label": "NPS Promedio", "value": avg_nps, "format": "%.0f", "delta": None},
        {"label": "NPS Buyer", "value": nps_buyer, "format": "%.0f", "delta": None},
        {"label": "NPS Seller", "value": nps_seller, "format": "%.0f", "delta": None},
        {
            "label": "NPS Relacional",
            "value": nps_relational,
            "format": "%.0f",
            "delta": None,
        },
    ]
    render_kpi_grid(cx_kpis, columns=4)

    # 4. OPERACIÓN / EFICIENCIA
    st.markdown("---")
    st.subheader("⚙️ Operación / Eficiencia")

    # Calculate inventory metrics
    inventory_df = filtered_data.get("inventory", pd.DataFrame())
    if len(inventory_df) > 0:
        total_inventory = inventory_df["total_inventory"].sum()
        available_inventory = inventory_df["available"].sum()
        reserved_inventory = inventory_df["reserved"].sum()
        vip_inventory = inventory_df["vip"].sum()
        aged_inventory = inventory_df["aging_60_plus"].sum()
        avg_days_in_inv = inventory_df["avg_days_in_inventory"].mean()

        # Calculate Backlog (Total - Available - Reserved)
        # This assumes backlog are cars in process/preparation not ready for sale
        backlog_inventory = total_inventory - available_inventory - reserved_inventory

        # Calculate inventory velocity (turnover rate)
        if total_inventory > 0 and avg_days_in_inv > 0:
            inventory_velocity = 30 / avg_days_in_inv  # Monthly turnover rate
        else:
            inventory_velocity = 0
    else:
        total_inventory = available_inventory = reserved_inventory = vip_inventory = 0
        aged_inventory = avg_days_in_inv = inventory_velocity = 0
        backlog_inventory = 0

    # ROW 1: INVENTORY COMPOSITION (The "Stock Flow")
    st.markdown("##### 📦 Composición de Inventario")

    # Calculate percentages
    disponible_pct = (
        (available_inventory / total_inventory * 100) if total_inventory > 0 else 0
    )
    reservado_pct = (
        (reserved_inventory / total_inventory * 100) if total_inventory > 0 else 0
    )
    backlog_pct = (
        (backlog_inventory / total_inventory * 100) if total_inventory > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Inventario Total", f"{total_inventory:.0f}")

    with col2:
        st.metric("Disponible", f"{available_inventory:.0f}")
        st.caption(f"**{disponible_pct:.1f}%** del total")

    with col3:
        st.metric("Reservado", f"{reserved_inventory:.0f}")
        st.caption(f"**{reservado_pct:.1f}%** del total")

    with col4:
        st.metric("Backlog (Prep/WIP)", f"{backlog_inventory:.0f}")
        st.caption(f"**{backlog_pct:.1f}%** del total")

    # ROW 2: OPERATIONAL EFFICIENCY
    st.markdown("##### ⚡ Eficiencia Operativa")

    aging_pct = (aged_inventory / total_inventory * 100) if total_inventory > 0 else 0

    ops_kpis = [
        {
            "label": "SLA Lead → Venta",
            "value": avg_sla,
            "format": "%.1f días",
            "delta": None,
        },
        {
            "label": "Velocity Inventario",
            "value": inventory_velocity,
            "format": "%.2fx/mes",
            "delta": None,
        },
        {
            "label": "Aging 60+ días",
            "value": aged_inventory,
            "format": "%.0f",
            "delta": f"{aging_pct:.1f}%",
            "delta_color": "inverse",
        },
        {
            "label": "Cancelaciones",
            "value": total_cancellations,
            "format": "%.0f",
            "delta": None,
            "delta_color": "inverse",
        },
    ]
    render_kpi_grid(ops_kpis, columns=4)


def render_hub_comparison_section(filtered_data, country_filter):
    """
    Render comprehensive hub comparison with all KPIs
    """
    st.subheader("🏢 Comparación Completa entre Hubs")

    if country_filter != "Todos":
        st.caption(f"Comparación de hubs en {country_filter}")
    else:
        st.caption("Comparación de todos los hubs")

    df = filtered_data["daily_metrics"]

    if len(df) == 0:
        st.warning("No hay datos para comparar")
        return

    # Aggregate by hub
    hub_comparison = (
        df.groupby(["country", "hub"])
        .agg(
            {
                "sales": "sum",
                "leads": "sum",
                "appointments": "sum",
                "reservations": "sum",
                "cancellations": "sum",
                "noshow": "sum",
                "nps": "mean",
                "csat": "mean",
                "revenue": "sum",
                "sla_lead_to_sale": "mean",
            }
        )
        .reset_index()
    )

    # Calculate derived metrics
    hub_comparison["conversion"] = (
        hub_comparison["sales"] / hub_comparison["leads"] * 100
    ).round(1)
    hub_comparison["cvr_lead_to_appointment"] = (
        hub_comparison["appointments"] / hub_comparison["leads"] * 100
    ).round(1)
    hub_comparison["cvr_appointment_to_reservation"] = (
        hub_comparison["reservations"] / hub_comparison["appointments"] * 100
    ).round(1)
    hub_comparison["cvr_reservation_to_sale"] = (
        hub_comparison["sales"] / hub_comparison["reservations"] * 100
    ).round(1)
    hub_comparison["cancellation_rate"] = (
        hub_comparison["cancellations"] / hub_comparison["reservations"] * 100
    ).round(1)
    hub_comparison["noshow_rate"] = (
        hub_comparison["noshow"] / hub_comparison["appointments"] * 100
    ).round(1)
    hub_comparison["ticket_promedio"] = (
        hub_comparison["revenue"] / hub_comparison["sales"]
    ).round(0)

    # Add inventory data
    inventory_df = filtered_data.get("inventory", pd.DataFrame())
    if len(inventory_df) > 0:
        inventory_by_hub = (
            inventory_df.groupby(["country", "hub"])
            .agg({"total_inventory": "sum", "available": "sum", "aging_60_plus": "sum"})
            .reset_index()
        )

        inventory_by_hub["aging_pct"] = (
            inventory_by_hub["aging_60_plus"]
            / inventory_by_hub["total_inventory"]
            * 100
        ).round(1)

        hub_comparison = hub_comparison.merge(
            inventory_by_hub[
                ["country", "hub", "total_inventory", "aging_60_plus", "aging_pct"]
            ],
            on=["country", "hub"],
            how="left",
        )

    # Sort by sales descending
    hub_comparison = hub_comparison.sort_values("sales", ascending=False)

    # === TABS FOR DIFFERENT VIEWS ===
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 KPIs Principales",
            "🔀 Funnel de Conversión",
            "😊 Experiencia de Cliente",
            "🚗 Inventario",
        ]
    )

    with tab1:
        st.markdown("#### KPIs Principales por Hub")

        # Prepare display dataframe
        kpi_display = hub_comparison[
            [
                "hub",
                "sales",
                "conversion",
                "revenue",
                "ticket_promedio",
                "leads",
                "sla_lead_to_sale",
            ]
        ].copy()

        kpi_display.columns = [
            "Hub",
            "Ventas",
            "CVR %",
            "Revenue",
            "Ticket Promedio",
            "Leads",
            "SLA (días)",
        ]

        # Add ranking
        kpi_display.insert(0, "🏆 Rank", range(1, len(kpi_display) + 1))

        # Style function for ranking
        def style_ranking(row):
            rank = row["🏆 Rank"]
            if rank == 1:
                return ["background-color: #ffd700"] * len(row)  # Gold
            elif rank == 2:
                return ["background-color: #c0c0c0"] * len(row)  # Silver
            elif rank == 3:
                return ["background-color: #cd7f32"] * len(row)  # Bronze
            else:
                return [""] * len(row)

        styled_kpi = kpi_display.style.apply(style_ranking, axis=1).format(
            {
                "Ventas": "{:.0f}",
                "CVR %": "{:.1f}%",
                "Revenue": "${:,.0f}",
                "Ticket Promedio": "${:,.0f}",
                "Leads": "{:.0f}",
                "SLA (días)": "{:.1f}",
            }
        )

        st.dataframe(styled_kpi, use_container_width=True, height=400)

        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Hub Líder en Ventas", hub_comparison.iloc[0]["hub"])
        with col2:
            best_cvr_hub = hub_comparison.loc[
                hub_comparison["conversion"].idxmax(), "hub"
            ]
            best_cvr_value = hub_comparison["conversion"].max()
            st.metric("Hub Líder en Conversión", best_cvr_hub, f"{best_cvr_value:.1f}%")
        with col3:
            total_hubs = len(hub_comparison)
            st.metric("Total de Hubs", f"{total_hubs}")

    with tab2:
        st.markdown("#### Funnel de Conversión por Hub")

        funnel_display = hub_comparison[
            [
                "hub",
                "cvr_lead_to_appointment",
                "cvr_appointment_to_reservation",
                "cvr_reservation_to_sale",
                "conversion",
                "cancellation_rate",
                "noshow_rate",
            ]
        ].copy()

        funnel_display.columns = [
            "Hub",
            "Lead → Cita %",
            "Cita → Reserva %",
            "Reserva → Venta %",
            "CVR Total %",
            "Cancelación %",
            "No-Show %",
        ]

        # Style by performance
        def style_funnel(row):
            cvr = row["CVR Total %"]
            if cvr >= 25:
                return ["background-color: #c8e6c9"] * len(row)
            elif cvr < 15:
                return ["background-color: #ffccbc"] * len(row)
            else:
                return [""] * len(row)

        styled_funnel = funnel_display.style.apply(style_funnel, axis=1).format(
            {
                "Lead → Cita %": "{:.1f}%",
                "Cita → Reserva %": "{:.1f}%",
                "Reserva → Venta %": "{:.1f}%",
                "CVR Total %": "{:.1f}%",
                "Cancelación %": "{:.1f}%",
                "No-Show %": "{:.1f}%",
            }
        )

        st.dataframe(styled_funnel, use_container_width=True, height=400)

        # Identify bottlenecks
        st.markdown("---")
        st.markdown("**🔍 Identificación de Estrangulamientos**")

        bottlenecks = []
        for _, row in hub_comparison.iterrows():
            hub_bottlenecks = []
            if row["cvr_lead_to_appointment"] < 50:
                hub_bottlenecks.append("Lead → Cita baja")
            if row["cvr_appointment_to_reservation"] < 45:
                hub_bottlenecks.append("Cita → Reserva baja")
            if row["cvr_reservation_to_sale"] < 65:
                hub_bottlenecks.append("Reserva → Venta baja")
            if row["noshow_rate"] > 20:
                hub_bottlenecks.append("Alto no-show")

            if hub_bottlenecks:
                bottlenecks.append({"hub": row["hub"], "issues": hub_bottlenecks})

        if bottlenecks:
            for item in bottlenecks[:5]:
                with st.expander(f"⚠️ {item['hub']}", expanded=False):
                    for issue in item["issues"]:
                        st.markdown(f"- {issue}")
        else:
            st.success("✅ Todos los hubs tienen funnels saludables")

    with tab3:
        st.markdown("#### Experiencia de Cliente por Hub")

        cx_display = hub_comparison[
            [
                "hub",
                "nps",
                "csat",
                "noshow_rate",
                "cancellation_rate",
                "sla_lead_to_sale",
            ]
        ].copy()

        cx_display.columns = [
            "Hub",
            "NPS",
            "CSAT",
            "No-Show %",
            "Cancelación %",
            "SLA (días)",
        ]

        # Style by NPS
        def style_cx(row):
            nps = row["NPS"]
            if nps >= 70:
                return ["background-color: #c8e6c9"] * len(row)
            elif nps < 50:
                return ["background-color: #ffccbc"] * len(row)
            else:
                return [""] * len(row)

        styled_cx = cx_display.style.apply(style_cx, axis=1).format(
            {
                "NPS": "{:.0f}",
                "CSAT": "{:.0f}",
                "No-Show %": "{:.1f}%",
                "Cancelación %": "{:.1f}%",
                "SLA (días)": "{:.1f}",
            }
        )

        st.dataframe(styled_cx, use_container_width=True, height=400)

    with tab4:
        st.markdown("#### Inventario por Hub")

        if "total_inventory" in hub_comparison.columns:
            inv_display = hub_comparison[
                ["hub", "total_inventory", "aging_60_plus", "aging_pct"]
            ].copy()

            inv_display.columns = [
                "Hub",
                "Inventario Total",
                "Aging 60+ días",
                "% Aging",
            ]

            # Style by aging percentage
            def style_inventory(row):
                aging_pct = row["% Aging"]
                if aging_pct >= 15:
                    return ["background-color: #ffccbc"] * len(row)
                elif aging_pct >= 10:
                    return ["background-color: #fff9c4"] * len(row)
                else:
                    return ["background-color: #c8e6c9"] * len(row)

            styled_inv = inv_display.style.apply(style_inventory, axis=1).format(
                {
                    "Inventario Total": "{:.0f}",
                    "Aging 60+ días": "{:.0f}",
                    "% Aging": "{:.1f}%",
                }
            )

            st.dataframe(styled_inv, use_container_width=True, height=400)

            # Summary
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                total_inv = hub_comparison["total_inventory"].sum()
                st.metric("Inventario Total", f"{total_inv:.0f}")
            with col2:
                total_aging = hub_comparison["aging_60_plus"].sum()
                st.metric("Total Aging 60+", f"{total_aging:.0f}")
            with col3:
                avg_aging_pct = (total_aging / total_inv * 100) if total_inv > 0 else 0
                st.metric("% Aging Promedio", f"{avg_aging_pct:.1f}%")

            # Chart
            st.markdown("---")
            render_bar_chart(
                hub_comparison.sort_values("aging_pct", ascending=False).head(10),
                "hub",
                "aging_pct",
                "Top 10 Hubs con Mayor % de Aging",
                color=COLORS["danger"],
            )
        else:
            st.info("No hay datos de inventario disponibles")


def render_performance_table_section(data, country_filter):
    """
    Render collapsible performance table by Region/Hub
    Shows key KPIs: Entregas, CVR, NPS, Inventario with dynamic aggregation
    Uses daily_metrics for BOTH views (now has hub-level data)
    """
    st.subheader("📋 Performance por Región / Hub")

    # Get period filter
    period = st.session_state.get("ceo_period", "Últimos 30 días")
    days = PERIOD_OPTIONS[period]
    cutoff_date = datetime.now() - timedelta(days=days)

    # Filter daily_metrics by period - this now has hub-level data
    daily_metrics = data["daily_metrics"].copy()
    daily_metrics = daily_metrics[daily_metrics["date"] >= cutoff_date]

    # Filter by country if selected
    if country_filter != "Todos":
        daily_metrics = daily_metrics[daily_metrics["country"] == country_filter]

    inventory_df = data.get("inventory", pd.DataFrame()).copy()
    if country_filter != "Todos" and len(inventory_df) > 0:
        inventory_df = inventory_df[inventory_df["country"] == country_filter]

    if len(daily_metrics) == 0:
        st.warning("No hay datos para mostrar")
        return

    # === LEVEL SELECTOR ===
    col_level, _ = st.columns([2, 1])

    with col_level:
        aggregation_level = st.radio(
            "Nivel de agregación",
            ["Por Región", "Por Hub"],
            horizontal=True,
            key="perf_table_level",
        )

    # === BUILD AGGREGATED DATA ===
    # Both views use the same daily_metrics source, just aggregated differently
    if aggregation_level == "Por Región":
        # Aggregate by country + region (sum all hubs within region)
        perf_df = (
            daily_metrics.groupby(["country", "region"])
            .agg(
                {
                    "sales": "sum",
                    "leads": "sum",
                    "nps": "mean",
                }
            )
            .reset_index()
        )

        # Add inventory data (already at region level)
        if len(inventory_df) > 0:
            inv_agg = (
                inventory_df.groupby(["country", "region"])
                .agg(
                    {
                        "total_inventory": "sum",
                        "available": "sum",
                        "aging_60_plus": "sum",
                    }
                )
                .reset_index()
            )
            perf_df = perf_df.merge(
                inv_agg, on=["country", "region"], how="left"
            ).fillna(0)
        else:
            perf_df["total_inventory"] = 0
            perf_df["available"] = 0
            perf_df["aging_60_plus"] = 0

        # Create display name
        perf_df["Ubicación"] = perf_df["country"] + " - " + perf_df["region"]

    else:  # Por Hub - Aggregate by hub (more granular, same source data)
        # Aggregate by country + region + hub
        perf_df = (
            daily_metrics.groupby(["country", "region", "hub"])
            .agg(
                {
                    "sales": "sum",
                    "leads": "sum",
                    "nps": "mean",
                }
            )
            .reset_index()
        )

        # Add inventory data by hub (distribute region inventory proportionally)
        if len(inventory_df) > 0:
            # Inventory is at region level, distribute proportionally by hub sales
            inv_by_region = (
                inventory_df.groupby(["country", "region"])
                .agg(
                    {
                        "total_inventory": "sum",
                        "available": "sum",
                        "aging_60_plus": "sum",
                    }
                )
                .reset_index()
            )

            # Count hubs per region for fallback distribution
            hubs_per_region = (
                perf_df.groupby(["country", "region"])
                .size()
                .reset_index(name="hub_count")
            )

            # Merge to get region inventory totals
            perf_df = perf_df.merge(
                inv_by_region, on=["country", "region"], how="left"
            ).fillna(0)

            perf_df = perf_df.merge(
                hubs_per_region, on=["country", "region"], how="left"
            ).fillna(1)

            # Calculate hub's proportion of region sales
            region_sales = perf_df.groupby(["country", "region"])["sales"].transform(
                "sum"
            )
            perf_df["sales_pct"] = np.where(
                region_sales > 0,
                perf_df["sales"] / region_sales,
                1 / perf_df["hub_count"],
            )

            # Distribute inventory proportionally
            perf_df["total_inventory"] = (
                perf_df["total_inventory"] * perf_df["sales_pct"]
            ).round(0)
            perf_df["available"] = (perf_df["available"] * perf_df["sales_pct"]).round(
                0
            )
            perf_df["aging_60_plus"] = (
                perf_df["aging_60_plus"] * perf_df["sales_pct"]
            ).round(0)

            # Clean up temp columns
            perf_df = perf_df.drop(columns=["hub_count", "sales_pct"])
        else:
            perf_df["total_inventory"] = 0
            perf_df["available"] = 0
            perf_df["aging_60_plus"] = 0

        # Create display name - show hub name
        perf_df["Ubicación"] = perf_df["hub"]

    # === CALCULATE DERIVED METRICS ===
    perf_df["CVR %"] = np.where(
        perf_df["leads"] > 0,
        (perf_df["sales"] / perf_df["leads"] * 100).round(1),
        0,
    )
    perf_df["Aging %"] = np.where(
        perf_df["total_inventory"] > 0,
        (perf_df["aging_60_plus"] / perf_df["total_inventory"] * 100).round(1),
        0,
    )

    # Fill NaN values
    perf_df = perf_df.fillna(0)

    # === PREPARE DISPLAY DATAFRAME ===
    display_df = perf_df[
        [
            "Ubicación",
            "sales",
            "CVR %",
            "nps",
            "total_inventory",
            "available",
            "Aging %",
        ]
    ].copy()

    display_df.columns = [
        "Ubicación",
        "Entregas",
        "CVR %",
        "NPS",
        "Inventario",
        "Disponible",
        "Aging 60+ %",
    ]

    # Sort by Entregas descending
    display_df = display_df.sort_values("Entregas", ascending=False)

    # === CALCULATE TOTALS ROW ===
    totals = {
        "Entregas": display_df["Entregas"].sum(),
        "CVR %": (perf_df["sales"].sum() / perf_df["leads"].sum() * 100)
        if perf_df["leads"].sum() > 0
        else 0,
        "NPS": display_df["NPS"].mean(),
        "Inventario": display_df["Inventario"].sum(),
    }

    # === RENDER IN EXPANDER ===
    level_label = "regiones" if aggregation_level == "Por Región" else "hubs"
    with st.expander(
        f"📊 Ver tabla detallada ({len(display_df)} {level_label})",
        expanded=False,
    ):
        # Summary metrics at top
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Entregas", f"{totals['Entregas']:,.0f}")
        with col2:
            st.metric("CVR Promedio", f"{totals['CVR %']:.1f}%")
        with col3:
            st.metric("NPS Promedio", f"{totals['NPS']:.0f}")
        with col4:
            st.metric("Inventario Total", f"{totals['Inventario']:,.0f}")

        st.markdown("---")

        # Style function for conditional formatting
        def style_performance(row):
            styles = [""] * len(row)

            # CVR coloring
            cvr_idx = 2  # CVR % column
            cvr = row.iloc[cvr_idx] if not pd.isna(row.iloc[cvr_idx]) else 0
            if cvr >= 25:
                styles[cvr_idx] = "background-color: #c8e6c9; color: #1b5e20"
            elif cvr < 15:
                styles[cvr_idx] = "background-color: #ffccbc; color: #bf360c"

            # NPS coloring
            nps_idx = 3  # NPS column
            nps = row.iloc[nps_idx] if not pd.isna(row.iloc[nps_idx]) else 0
            if nps >= 70:
                styles[nps_idx] = "background-color: #c8e6c9; color: #1b5e20"
            elif nps < 50:
                styles[nps_idx] = "background-color: #ffccbc; color: #bf360c"

            # Aging coloring
            aging_idx = 6  # Aging 60+ % column
            aging = row.iloc[aging_idx] if not pd.isna(row.iloc[aging_idx]) else 0
            if aging >= 15:
                styles[aging_idx] = "background-color: #ffccbc; color: #bf360c"
            elif aging < 8:
                styles[aging_idx] = "background-color: #c8e6c9; color: #1b5e20"

            return styles

        # Apply styling
        styled_df = display_df.style.apply(style_performance, axis=1).format(
            {
                "Entregas": "{:,.0f}",
                "CVR %": "{:.1f}%",
                "NPS": "{:.0f}",
                "Inventario": "{:,.0f}",
                "Disponible": "{:,.0f}",
                "Aging 60+ %": "{:.1f}%",
            }
        )

        # Display table
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=min(450, 50 + len(display_df) * 35),
            hide_index=True,
        )

        # Legend
        st.markdown("---")
        st.caption(
            "**Leyenda:** 🟢 Verde = Buen performance | 🔴 Rojo = Necesita atención"
        )

        # Export button
        col_export, _ = st.columns([1, 3])
        with col_export:
            st.download_button(
                "📥 Exportar CSV",
                display_df.to_csv(index=False).encode("utf-8"),
                f"performance_{level_label}_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                key="download_perf_table",
            )


def render_alerts_section(data, period_days):
    """Render strategic alerts with dynamic detection - collapsible by type"""
    st.subheader("🚨 Alertas Estratégicas")

    # Detect alerts dynamically
    alerts = detect_strategic_alerts(data, period_days)

    if len(alerts) == 0:
        st.success("✅ No hay alertas activas - Todas las métricas están saludables")
        return

    # Separate alerts by type
    critical_alerts = [a for a in alerts if a["type"] == "critical"]
    warning_alerts = [a for a in alerts if a["type"] == "warning"]
    info_alerts = [a for a in alerts if a["type"] == "info"]

    # Display alert summary
    col_summary1, col_summary2, col_summary3 = st.columns(3)
    with col_summary1:
        st.metric("🚨 Críticas", len(critical_alerts))
    with col_summary2:
        st.metric("⚠️ Advertencias", len(warning_alerts))
    with col_summary3:
        st.metric("ℹ️ Información", len(info_alerts))

    st.markdown("---")

    # Render critical alerts in expandable section
    if critical_alerts:
        with st.expander(f"🚨 **Críticas** ({len(critical_alerts)})", expanded=False):
            col1, col2 = st.columns(2)

            for idx, alert in enumerate(critical_alerts):
                col = col1 if idx % 2 == 0 else col2

                with col:
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
            col1, col2 = st.columns(2)

            for idx, alert in enumerate(warning_alerts):
                col = col1 if idx % 2 == 0 else col2

                with col:
                    render_alert_box(
                        alert["type"],
                        alert["title"],
                        alert["description"],
                        alert.get("timestamp"),
                    )

    # Render info alerts in expandable section
    if info_alerts:
        with st.expander(f"ℹ️ **Información** ({len(info_alerts)})", expanded=False):
            col1, col2 = st.columns(2)

            for idx, alert in enumerate(info_alerts):
                col = col1 if idx % 2 == 0 else col2

                with col:
                    render_alert_box(
                        alert["type"],
                        alert["title"],
                        alert["description"],
                        alert.get("timestamp"),
                    )


def get_previous_period_data(current_df):
    """Get data from previous period for delta calculation"""
    if len(current_df) == 0:
        return pd.DataFrame()

    min_date = current_df["date"].min()
    max_date = current_df["date"].max()

    # Calculate period length (add 1 day to include both start and end)
    period_length = (max_date - min_date).days + 1

    prev_end = min_date - timedelta(days=1)
    prev_start = prev_end - timedelta(days=period_length - 1)

    # Get full data from session state
    if "data" not in st.session_state:
        return pd.DataFrame()

    all_metrics = st.session_state.data["daily_metrics"]

    # Get current filters from session state
    country = st.session_state.get("ceo_country", "Todos")
    hub = st.session_state.get("ceo_hub", "Todos")

    # Apply filters to previous period data
    prev_df = all_metrics.copy()

    if country != "Todos":
        prev_df = prev_df[prev_df["country"] == country]

    if hub != "Todos":
        prev_df = prev_df[prev_df["hub"] == hub]

    # Filter by previous date range
    prev_df = prev_df[(prev_df["date"] >= prev_start) & (prev_df["date"] <= prev_end)]

    return prev_df


def calculate_delta(current, previous):
    """Calculate percentage delta"""
    if previous == 0 or previous == current:
        return None

    pct_change = ((current - previous) / previous) * 100
    return f"{pct_change:+.1f}%"
