"""
Dynamic Alert Detection System
Detects anomalies and issues in real-time based on thresholds and trends
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from config import THRESHOLDS


def detect_strategic_alerts(data, period_days=30):
    """
    Detect strategic alerts for CEO dashboard

    Returns:
        List of alert dictionaries with type, title, description, and timestamp
    """
    alerts = []

    # Get data for current and previous period
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_days)
    prev_start = start_date - timedelta(days=period_days)

    daily_df = data["daily_metrics"].copy()
    daily_df["date"] = pd.to_datetime(daily_df["date"])

    current_period = daily_df[daily_df["date"] >= start_date]
    previous_period = daily_df[
        (daily_df["date"] >= prev_start) & (daily_df["date"] < start_date)
    ]

    # 1. HUBS CON CAÍDA EN CONVERSIÓN
    alerts.extend(detect_conversion_drops(current_period, previous_period))

    # 2. INVENTARIO CON AGING CRÍTICO
    alerts.extend(detect_critical_inventory(data["inventory"]))

    # 3. CAÍDA ABRUPTA DE NPS
    alerts.extend(detect_nps_drops(current_period, previous_period))

    # 4. AUMENTO SIGNIFICATIVO DE CANCELACIONES
    alerts.extend(detect_cancellation_spikes(current_period, previous_period))

    # 5. VARIACIÓN SEMANAL DE CONVERSIÓN
    alerts.extend(detect_conversion_volatility(daily_df, period_days))

    # Sort by severity and timestamp
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    alerts.sort(
        key=lambda x: (severity_order.get(x["type"], 3), x["timestamp"]), reverse=True
    )

    return alerts


def detect_conversion_drops(current_period, previous_period, threshold_pct=10):
    """
    Detect hubs with significant conversion rate drops
    """
    alerts = []

    # Calculate conversion by hub for both periods
    current_by_hub = current_period.groupby("hub").agg({"sales": "sum", "leads": "sum"})
    current_by_hub["conversion"] = (
        current_by_hub["sales"] / current_by_hub["leads"] * 100
    )

    previous_by_hub = previous_period.groupby("hub").agg(
        {"sales": "sum", "leads": "sum"}
    )
    previous_by_hub["conversion"] = (
        previous_by_hub["sales"] / previous_by_hub["leads"] * 100
    )

    # Compare periods
    for hub in current_by_hub.index:
        if hub not in previous_by_hub.index:
            continue

        current_cvr = current_by_hub.loc[hub, "conversion"]
        previous_cvr = previous_by_hub.loc[hub, "conversion"]

        if previous_cvr > 0:
            drop_pct = ((current_cvr - previous_cvr) / previous_cvr) * 100

            if drop_pct < -threshold_pct:
                alert_type = "critical" if drop_pct < -20 else "warning"
                alerts.append(
                    {
                        "type": alert_type,
                        "title": f"Caída en conversión - {hub}",
                        "description": f"Conversión bajó {abs(drop_pct):.1f}% vs periodo anterior ({previous_cvr:.1f}% → {current_cvr:.1f}%)",
                        "timestamp": datetime.now(),
                        "metric": "conversion",
                        "hub": hub,
                        "value": drop_pct,
                    }
                )

    return alerts


def detect_critical_inventory(inventory_df, critical_days=60, warning_threshold=15):
    """
    Detect hubs with critical aging inventory
    """
    alerts = []

    # Group by hub
    hub_inventory = (
        inventory_df.groupby(["country", "hub"])
        .agg({"aging_60_plus": "sum", "total_inventory": "sum"})
        .reset_index()
    )

    for _, row in hub_inventory.iterrows():
        aging_count = row["aging_60_plus"]
        total = row["total_inventory"]

        if aging_count >= warning_threshold:
            aging_pct = (aging_count / total * 100) if total > 0 else 0
            alert_type = "critical" if aging_count >= 25 else "warning"

            alerts.append(
                {
                    "type": alert_type,
                    "title": f'Inventario envejecido - {row["hub"]}',
                    "description": f"{aging_count} vehículos con más de {critical_days} días en inventario ({aging_pct:.0f}% del total)",
                    "timestamp": datetime.now(),
                    "metric": "inventory_aging",
                    "hub": row["hub"],
                    "value": aging_count,
                }
            )

    return alerts


def detect_nps_drops(current_period, previous_period, threshold_points=5):
    """
    Detect significant NPS drops by hub
    """
    alerts = []

    # Calculate NPS by hub
    current_nps = current_period.groupby("hub")["nps"].mean()
    previous_nps = previous_period.groupby("hub")["nps"].mean()

    for hub in current_nps.index:
        if hub not in previous_nps.index:
            continue

        current = current_nps[hub]
        previous = previous_nps[hub]
        drop = previous - current

        # Check if below threshold
        if current < THRESHOLDS["nps_warning"]:
            alert_type = (
                "critical" if current < THRESHOLDS["nps_warning"] - 10 else "warning"
            )
            alerts.append(
                {
                    "type": alert_type,
                    "title": f"NPS bajo - {hub}",
                    "description": f'NPS actual: {current:.0f} (umbral: {THRESHOLDS["nps_warning"]})',
                    "timestamp": datetime.now(),
                    "metric": "nps",
                    "hub": hub,
                    "value": current,
                }
            )

        # Check for significant drop
        elif drop > threshold_points:
            alerts.append(
                {
                    "type": "warning",
                    "title": f"Caída en NPS - {hub}",
                    "description": f"NPS bajó {drop:.0f} puntos vs periodo anterior ({previous:.0f} → {current:.0f})",
                    "timestamp": datetime.now(),
                    "metric": "nps",
                    "hub": hub,
                    "value": -drop,
                }
            )

    return alerts


def detect_cancellation_spikes(current_period, previous_period, threshold_pct=25):
    """
    Detect significant increases in cancellations
    """
    alerts = []

    # Calculate cancellations by hub
    current_cancel = current_period.groupby("hub")["cancellations"].sum()
    previous_cancel = previous_period.groupby("hub")["cancellations"].sum()

    for hub in current_cancel.index:
        if hub not in previous_cancel.index or previous_cancel[hub] == 0:
            continue

        current = current_cancel[hub]
        previous = previous_cancel[hub]
        increase_pct = ((current - previous) / previous) * 100

        if increase_pct > threshold_pct:
            alert_type = "critical" if increase_pct > 50 else "warning"
            alerts.append(
                {
                    "type": alert_type,
                    "title": f"Aumento de cancelaciones - {hub}",
                    "description": f"Cancelaciones aumentaron {increase_pct:.0f}% vs periodo anterior ({previous:.0f} → {current:.0f})",
                    "timestamp": datetime.now(),
                    "metric": "cancellations",
                    "hub": hub,
                    "value": increase_pct,
                }
            )

    return alerts


def detect_conversion_volatility(daily_df, period_days=30):
    """
    Detect high volatility in conversion rates (instability indicator)
    """
    alerts = []

    # Get recent data
    end_date = daily_df["date"].max()
    start_date = end_date - timedelta(days=period_days)
    recent_data = daily_df[daily_df["date"] >= start_date].copy()

    # Calculate weekly conversion by hub
    recent_data["week"] = (
        recent_data["date"].dt.to_period("W").apply(lambda r: r.start_time)
    )

    weekly_conversion = (
        recent_data.groupby(["hub", "week"])
        .agg({"sales": "sum", "leads": "sum"})
        .reset_index()
    )

    weekly_conversion["conversion"] = (
        weekly_conversion["sales"] / weekly_conversion["leads"] * 100
    )

    # Calculate volatility (standard deviation)
    volatility = (
        weekly_conversion.groupby("hub")["conversion"]
        .agg(["std", "mean"])
        .reset_index()
    )
    volatility = volatility[volatility["std"].notna()]

    # Flag high volatility (coefficient of variation > 0.3)
    for _, row in volatility.iterrows():
        if row["mean"] > 0:
            cv = row["std"] / row["mean"]

            if cv > 0.3:  # 30% coefficient of variation
                alerts.append(
                    {
                        "type": "warning",
                        "title": f'Alta volatilidad en conversión - {row["hub"]}',
                        "description": f"Conversión inestable (CV: {cv:.1%}). Revisar consistencia operativa.",
                        "timestamp": datetime.now(),
                        "metric": "conversion_volatility",
                        "hub": row["hub"],
                        "value": cv,
                    }
                )

    return alerts


def detect_operational_alerts(filtered_data, hub_label=None):
    """
    Detect operational alerts for City Manager dashboard
    Includes dealership-approach alerts (capacity, opportunities, stock quality)

    Args:
        filtered_data: Pre-filtered data dictionary
        hub_label: Optional hub/region label (not currently used in logic)

    Returns:
        List of alert dictionaries
    """
    alerts = []

    agents_df = filtered_data.get("agent_performance", pd.DataFrame())
    inventory_df = filtered_data.get("inventory", pd.DataFrame())
    daily_df = filtered_data.get("daily_metrics", pd.DataFrame())

    # === NEW DEALERSHIP ALERTS ===

    # 1. AGENTES SUBUTILIZADOS (Capacidad disponible)
    if len(agents_df) > 0:
        underutilized = agents_df[agents_df["utilization"] < 0.60]
        if len(underutilized) > 0:
            total_available_slots = underutilized["available_slots"].sum()
            agent_names = ", ".join(underutilized["agent_name"].head(3).tolist())
            more_text = (
                f" y {len(underutilized) - 3} más" if len(underutilized) > 3 else ""
            )

            alerts.append(
                {
                    "type": "warning",
                    "title": f"{len(underutilized)} agente(s) subutilizado(s)",
                    "description": f"{total_available_slots:.0f} slots disponibles sin usar. Agentes: {agent_names}{more_text}. Asignar más leads.",
                    "timestamp": datetime.now(),
                    "metric": "agent_utilization",
                }
            )

    # 2. STOCK DE BAJA CALIDAD ASIGNADO
    if len(agents_df) > 0:
        low_quality_stock = agents_df[agents_df["stock_attractiveness"] < 60]
        if len(low_quality_stock) > 0:
            agent_names = ", ".join(low_quality_stock["agent_name"].head(3).tolist())
            more_text = (
                f" y {len(low_quality_stock) - 3} más"
                if len(low_quality_stock) > 3
                else ""
            )
            avg_age = low_quality_stock["stock_avg_age"].mean()

            alerts.append(
                {
                    "type": "critical",
                    "title": f"{len(low_quality_stock)} agente(s) con stock poco atractivo",
                    "description": f"Stock envejecido (promedio: {avg_age:.0f} días) afecta conversión. Agentes: {agent_names}{more_text}. Renovar inventario asignado.",
                    "timestamp": datetime.now(),
                    "metric": "stock_quality",
                }
            )

    # 3. ALTO BACKLOG SIN CAPACIDAD
    if len(agents_df) > 0:
        high_backlog_low_capacity = agents_df[
            (agents_df["backlog_cartera"] > 20) & (agents_df["available_slots"] < 5)
        ]
        if len(high_backlog_low_capacity) > 0:
            agent_names = ", ".join(
                high_backlog_low_capacity["agent_name"].head(3).tolist()
            )
            more_text = (
                f" y {len(high_backlog_low_capacity) - 3} más"
                if len(high_backlog_low_capacity) > 3
                else ""
            )

            alerts.append(
                {
                    "type": "warning",
                    "title": f"{len(high_backlog_low_capacity)} agente(s) con alto backlog y poca capacidad",
                    "description": f"Agentes: {agent_names}{more_text}. Redistribuir cartera o aumentar capacidad.",
                    "timestamp": datetime.now(),
                    "metric": "backlog_capacity",
                }
            )

    # 4. BAJO APROVECHAMIENTO DE OPORTUNIDADES
    if len(agents_df) > 0:
        low_aprovechamiento = agents_df[agents_df["aprovechamiento_pct"] < 15]
        if len(low_aprovechamiento) > 0:
            agent_names = ", ".join(low_aprovechamiento["agent_name"].head(3).tolist())
            more_text = (
                f" y {len(low_aprovechamiento) - 3} más"
                if len(low_aprovechamiento) > 3
                else ""
            )

            alerts.append(
                {
                    "type": "warning",
                    "title": f"{len(low_aprovechamiento)} agente(s) con bajo aprovechamiento",
                    "description": f"< 15% de oportunidades convertidas. Agentes: {agent_names}{more_text}. Revisar calidad de leads o capacitación.",
                    "timestamp": datetime.now(),
                    "metric": "aprovechamiento",
                }
            )

    # 5. MISMATCH ENTRE STOCK Y LEADS
    if len(agents_df) > 0:
        low_match = agents_df[agents_df["lead_match_score"] < 60]
        if len(low_match) > 0:
            agent_names = ", ".join(low_match["agent_name"].head(3).tolist())
            more_text = f" y {len(low_match) - 3} más" if len(low_match) > 3 else ""

            alerts.append(
                {
                    "type": "info",
                    "title": f"{len(low_match)} agente(s) con bajo match stock-leads",
                    "description": f"El inventario asignado no coincide con lo que buscan los leads. Agentes: {agent_names}{more_text}. Reasignar stock.",
                    "timestamp": datetime.now(),
                    "metric": "lead_match",
                }
            )

    # === TRADITIONAL ALERTS ===

    # 6. AGENTS WITH LOW CONVERSION (traditional)
    if len(agents_df) > 0:
        low_conv_agents = agents_df[
            agents_df["conversion"] < THRESHOLDS["conversion_warning"]
        ]
        if len(low_conv_agents) > 0:
            agent_names = ", ".join(low_conv_agents["agent_name"].head(3).tolist())
            more_text = (
                f" y {len(low_conv_agents) - 3} más" if len(low_conv_agents) > 3 else ""
            )

            alerts.append(
                {
                    "type": "warning",
                    "title": f"{len(low_conv_agents)} agente(s) con baja conversión",
                    "description": f'Agentes: {agent_names}{more_text}. Conversión < {THRESHOLDS["conversion_warning"]*100:.0f}%',
                    "timestamp": datetime.now(),
                    "metric": "agent_conversion",
                }
            )

    # 7. AGED INVENTORY
    if len(inventory_df) > 0:
        total_aged = inventory_df["aging_60_plus"].sum()
        total_inventory = inventory_df["total_inventory"].sum()

        if total_aged > 20:
            aging_pct = (
                (total_aged / total_inventory * 100) if total_inventory > 0 else 0
            )
            alert_type = "critical" if total_aged > 30 else "warning"

            alerts.append(
                {
                    "type": alert_type,
                    "title": f"Inventario envejecido: {total_aged} vehículos",
                    "description": f"{aging_pct:.0f}% del inventario con más de 60 días. Considerar ajuste de precios o promociones.",
                    "timestamp": datetime.now(),
                    "metric": "inventory_aging",
                }
            )

    # 8. HIGH NO-SHOW RATE
    if len(agents_df) > 0:
        high_noshow = agents_df[agents_df["noshow"] > THRESHOLDS["noshow_warning"]]
        if len(high_noshow) > 0:
            agent_names = ", ".join(high_noshow["agent_name"].head(3).tolist())
            more_text = f" y {len(high_noshow) - 3} más" if len(high_noshow) > 3 else ""

            alerts.append(
                {
                    "type": "warning",
                    "title": f"{len(high_noshow)} agente(s) con alta tasa de no-show",
                    "description": f"Agentes: {agent_names}{more_text}. Revisar proceso de confirmación de citas.",
                    "timestamp": datetime.now(),
                    "metric": "noshow_rate",
                }
            )

    # 9. NPS DROP (recent days)
    if len(daily_df) > 0:
        recent_nps = daily_df.tail(7)["nps"].mean()  # Last 7 days

        if recent_nps < THRESHOLDS["nps_warning"]:
            alert_type = (
                "critical" if recent_nps < THRESHOLDS["nps_warning"] - 10 else "warning"
            )
            alerts.append(
                {
                    "type": alert_type,
                    "title": "NPS por debajo del umbral",
                    "description": f'NPS promedio últimos 7 días: {recent_nps:.0f} (umbral: {THRESHOLDS["nps_warning"]}). Revisar experiencia de cliente.',
                    "timestamp": datetime.now(),
                    "metric": "nps",
                }
            )

    # 10. LOW INVENTORY
    if len(inventory_df) > 0 and len(daily_df) > 0:
        total_available = inventory_df["available"].sum()
        avg_sales_per_day = (
            daily_df["sales"].sum() / len(daily_df) if len(daily_df) > 0 else 0
        )

        if avg_sales_per_day > 0:
            days_of_inventory = total_available / avg_sales_per_day

            if days_of_inventory < 15:
                alerts.append(
                    {
                        "type": "warning",
                        "title": "Inventario bajo",
                        "description": f"Solo {days_of_inventory:.0f} días de inventario disponible. Considerar reabastecimiento.",
                        "timestamp": datetime.now(),
                        "metric": "inventory_low",
                    }
                )

    # 11. HIGH CANCELLATION RATE
    if len(daily_df) > 0:
        total_reservations = daily_df["reservations"].sum()
        total_cancellations = daily_df["cancellations"].sum()

        if total_reservations > 0:
            cancellation_rate = total_cancellations / total_reservations

            if cancellation_rate > 0.15:  # 15% cancellation rate
                alert_type = "critical" if cancellation_rate > 0.20 else "warning"
                alerts.append(
                    {
                        "type": alert_type,
                        "title": "Alta tasa de cancelaciones",
                        "description": f"{cancellation_rate:.0%} de las reservas son canceladas. Revisar proceso de cierre.",
                        "timestamp": datetime.now(),
                        "metric": "cancellation_rate",
                    }
                )

    return alerts
