"""
Data generator for sample/placeholder data
Uses real delivery data from CSV to create realistic metrics
"""

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from config import AGENTS_PER_HUB, COUNTRIES, HUBS, REGIONS_HUBS, VEHICLE_SEGMENTS

# Real delivery data from Mexico
REAL_DELIVERIES_DATA = {
    "MX": {
        "Ciudad de México": {
            "2025-11": 2465,
            "2025-10": 3327,
            "2025-09": 2973,
            "2025-08": 1390,
        },
        "Guadalajara": {
            "2025-11": 355,
            "2025-10": 544,
            "2025-09": 413,
            "2025-08": 154,
        },
        "Monterrey": {
            "2025-11": 268,
            "2025-10": 436,
            "2025-09": 430,
            "2025-08": 127,
        },
        "Puebla": {
            "2025-11": 209,
            "2025-10": 253,
            "2025-09": 221,
            "2025-08": 116,
        },
        "Querétaro": {
            "2025-11": 262,
            "2025-10": 350,
            "2025-09": 278,
            "2025-08": 108,
        },
        "Cuernavaca": {
            "2025-11": 77,
            "2025-10": 113,
            "2025-09": 73,
            "2025-08": 41,
        },
    }
}


def generate_sample_data():
    """
    Generate comprehensive sample data for the application
    """
    np.random.seed(42)
    random.seed(42)

    # Date range: last 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    data = {
        "daily_metrics": generate_daily_metrics(date_range),
        "agent_performance": generate_agent_performance(),
        "inventory": generate_inventory_data(),
        "funnel": generate_funnel_data(date_range),
        "alerts": generate_alerts(),
        "customers": generate_customer_data(),
    }

    return data


def generate_daily_metrics(date_range):
    """Generate daily aggregated metrics by country, region and hub using real delivery data"""
    records = []

    for country in COUNTRIES:
        # Get regions for this country
        regions = HUBS[country]  # These are now region names

        # Get real delivery data if available for this country
        country_deliveries = REAL_DELIVERIES_DATA.get(country, {})

        for region in regions:
            # Get real deliveries for this region (using legacy name mapping)
            hub_deliveries = country_deliveries.get(region, {})

            for date in date_range:
                # Try to get real delivery data for this month
                month_key = date.strftime("%Y-%m")

                # Base sales/deliveries from real data or fallback to random
                if month_key in hub_deliveries:
                    # Use real data and distribute across days of the month
                    monthly_deliveries = hub_deliveries[month_key]
                    days_in_month = (date.replace(day=28) + timedelta(days=4)).replace(
                        day=1
                    ) - timedelta(days=1)
                    avg_daily = monthly_deliveries / days_in_month.day
                    # Add some daily variation
                    sales = int(avg_daily * np.random.uniform(0.7, 1.3))
                else:
                    # Fallback to generated data with region-specific scaling
                    region_scale = {
                        "Ciudad de México": 3.0,
                        "Guadalajara": 0.5,
                        "Monterrey": 0.4,
                        "Puebla": 0.25,
                        "Querétaro": 0.3,
                        "Cuernavaca": 0.1,
                        "León": 0.2,
                        "San Luis Potosí": 0.15,
                        "Santiago": 1.0,
                        "Valparaíso": 0.4,
                        "Concepción": 0.3,
                        "São Paulo": 2.0,
                        "Río de Janeiro": 1.5,
                        "Brasilia": 0.8,
                        "Buenos Aires": 1.5,
                        "Córdoba": 0.6,
                        "Rosario": 0.5,
                    }.get(region, 1.0)

                    # Add some seasonality and trends
                    day_factor = 1 + 0.1 * np.sin(2 * np.pi * date.dayofyear / 365)
                    trend_factor = 1 + 0.02 * (date - date_range[0]).days / len(
                        date_range
                    )

                    sales = int(
                        np.random.poisson(15) * day_factor * trend_factor * region_scale
                    )

                # Calculate funnel metrics backwards from sales (deliveries)
                # Typical conversion: Leads → Appointments (60%) → Reservations (50%) → Sales (75%)
                reservations = int(sales / np.random.uniform(0.7, 0.8))
                appointments = int(reservations / np.random.uniform(0.45, 0.55))
                leads = int(appointments / np.random.uniform(0.55, 0.65))

                # Purchases (Rotation model: buy to sell)
                # Reposition ratio varies slightly to simulate stock building/depletion
                reposition_ratio = np.random.uniform(0.9, 1.2)
                purchases = int(sales * reposition_ratio)

                records.append(
                    {
                        "date": date,
                        "country": country,
                        "region": region,  # NEW: Region column
                        "hub": region,  # For backwards compatibility, hub = region for now
                        "leads": leads,
                        "appointments": appointments,
                        "reservations": reservations,
                        "sales": sales,  # This is actually deliveries
                        "purchases": purchases,
                        "cancellations": int(
                            reservations * np.random.uniform(0.05, 0.15)
                        ),
                        "noshow": int(appointments * np.random.uniform(0.1, 0.25)),
                        "nps": np.random.uniform(50, 85),
                        "csat": np.random.uniform(70, 95),
                        "revenue": sales * np.random.uniform(10000, 22000),
                        "ticket_avg": np.random.uniform(10000, 22000),
                        "cost_per_lead": np.random.uniform(60, 120),
                        "sla_lead_to_sale": np.random.uniform(3, 10),
                    }
                )

    return pd.DataFrame(records)


def generate_agent_performance():
    """Generate agent-level performance data with capacity and opportunity metrics"""
    records = []
    agent_id = 1

    for country in COUNTRIES:
        regions = HUBS[country]  # These are now region names
        for region in regions:
            # Get hubs for this region
            region_hubs = REGIONS_HUBS.get(country, {}).get(region, [region])

            # If no specific hubs, use region name as hub
            if not region_hubs:
                region_hubs = [region]

            # Select a few hubs for this region (or just one if few available)
            num_hubs_to_use = min(3, len(region_hubs))
            hubs_to_use = (
                random.sample(region_hubs, num_hubs_to_use)
                if len(region_hubs) > 0
                else [region]
            )

            for hub in hubs_to_use:
                for i in range(AGENTS_PER_HUB):
                    # Generate agent name - lista ampliada para más variedad
                    first_names = [
                        "Juan",
                        "María",
                        "Carlos",
                        "Ana",
                        "Luis",
                        "Carmen",
                        "José",
                        "Patricia",
                        "Miguel",
                        "Laura",
                        "Fernando",
                        "Elena",
                        "Ricardo",
                        "Isabel",
                        "Diego",
                        "Sofía",
                        "Andrés",
                        "Valentina",
                        "Pablo",
                        "Camila",
                        "Daniel",
                        "Mariana",
                        "Roberto",
                        "Gabriela",
                        "Sergio",
                        "Alejandra",
                        "Francisco",
                        "Daniela",
                        "Eduardo",
                        "Paulina",
                        "Javier",
                        "Fernanda",
                        "Oscar",
                        "Andrea",
                        "Raúl",
                    ]
                    last_names = [
                        "García",
                        "Rodríguez",
                        "Martínez",
                        "López",
                        "González",
                        "Pérez",
                        "Sánchez",
                        "Ramírez",
                        "Torres",
                        "Flores",
                        "Rivera",
                        "Gómez",
                        "Hernández",
                        "Díaz",
                        "Morales",
                        "Vargas",
                        "Rojas",
                        "Castro",
                        "Ortiz",
                        "Ruiz",
                        "Jiménez",
                        "Moreno",
                        "Medina",
                        "Aguilar",
                        "Cruz",
                    ]
                    agent_name = (
                        f"{random.choice(first_names)} {random.choice(last_names)}"
                    )

                # CAPACITY METRICS (como concesionaria)
                slots_per_week = 40  # 8 slots/día × 5 días
                appointments = int(
                    np.random.uniform(25, 40)
                )  # Citas agendadas - aumentado
                utilization = appointments / slots_per_week
                available_slots = max(0, slots_per_week - appointments)

                # BACKLOG DE CARTERA (leads no convertidos aún)
                backlog_cartera = int(
                    np.random.uniform(15, 50)
                )  # Aumentado para más leads

                # LEADS Y CONVERSIÓN
                leads_nuevos = int(np.random.uniform(150, 400))
                total_opportunities = (
                    appointments + backlog_cartera
                )  # Oportunidades reales

                reservations = int(appointments * np.random.uniform(0.3, 0.7))
                sales = int(reservations * np.random.uniform(0.5, 0.9))

                # CONVERSIÓN REAL = conversiones / oportunidades totales
                conversion_real = (
                    sales / total_opportunities if total_opportunities > 0 else 0
                )

                # DESGLOSE POR TIPO DE OPERACIÓN
                # Sales (Ventas puras): 60-70% del total
                sales_only = int(sales * np.random.uniform(0.60, 0.70))

                # Trade-in (Cliente entrega auto como parte de pago): 20-30%
                sales_tradein = int(sales * np.random.uniform(0.20, 0.30))

                # Purchases (Compras puras): diferentes volumen
                purchases = int(
                    np.random.uniform(sales * 0.8, sales * 1.3)
                )  # Compras pueden ser más

                # Purchases con trade-in (ya contadas en trade-in):
                # Esto es para evitar doble conteo - el trade-in ya incluye una compra
                purchases_pure = purchases - sales_tradein  # Compras sin trade-in

                # Total de operaciones de venta y compra
                total_sales_ops = sales_only + sales_tradein  # Total debe ser = sales
                total_purchase_ops = purchases_pure + sales_tradein  # Total compras

                # CALIDAD DEL STOCK ASIGNADO
                # Número de autos asignados al agente
                stock_assigned = int(np.random.uniform(8, 20))

                # Edad promedio del stock (días)
                stock_avg_age = np.random.uniform(10, 65)

                # Atractivo del stock (0-100)
                # Factores: edad, precio competitivo, demanda del segmento
                age_factor = max(0, 100 - stock_avg_age * 1.2)  # Penaliza edad
                demand_factor = np.random.uniform(60, 95)  # Demanda del segmento
                price_factor = np.random.uniform(70, 100)  # Competitividad de precio
                stock_attractiveness = (
                    age_factor * 0.4 + demand_factor * 0.3 + price_factor * 0.3
                )

                # Match con leads (qué tan bien coincide el stock con lo que buscan los leads)
                lead_match_score = np.random.uniform(50, 100)

                # EFICIENCIA AJUSTADA (conversión × calidad de stock)
                efficiency_score = conversion_real * (stock_attractiveness / 100)

                # ANCILLARIES (Productos adicionales)
                # Seguros: 30-70% de penetración
                insurance_sold = int(sales * np.random.uniform(0.30, 0.70))
                insurance_penetration = (
                    (insurance_sold / sales * 100) if sales > 0 else 0
                )

                # Garantías Extendidas (Kavak Total): 20-50% de penetración
                extended_warranty_sold = int(sales * np.random.uniform(0.20, 0.50))
                extended_warranty_penetration = (
                    (extended_warranty_sold / sales * 100) if sales > 0 else 0
                )

                # Penetración total de ancilares
                total_ancillaries = insurance_sold + extended_warranty_sold
                ancillary_penetration = (
                    (total_ancillaries / (sales * 2) * 100) if sales > 0 else 0
                )  # Sobre total de oportunidades

                # FINANCING (Financiamiento)
                # 35-55% de las ventas se financian
                financing_sold = int(sales * np.random.uniform(0.35, 0.55))
                financing_penetration = (
                    (financing_sold / sales * 100) if sales > 0 else 0
                )

                # ═══════════════════════════════════════════════════════════
                # OWNERSHIP & PUNTOS COMPUESTOS (Nuevo sistema de incentivos)
                # ═══════════════════════════════════════════════════════════

                # Ownership Score: % de clientes manejados de principio a fin
                # Simula handoffs (clientes que cambiaron de agente)
                handoffs = int(sales * np.random.uniform(0.05, 0.25))
                ownership_score = ((sales - handoffs) / sales * 100) if sales > 0 else 0

                # NPS personal del agente
                nps_personal = np.random.uniform(45, 90)

                # CÁLCULO DE PUNTOS COMPUESTOS
                # Base: 100 pts por entrega
                base_points = sales * 100

                # Multiplicadores por financing (+50 pts por venta financiada)
                financing_points = financing_sold * 50

                # Multiplicadores por ancillaries
                # Kavak Total (garantía): +30 pts
                warranty_points = extended_warranty_sold * 30
                # Seguro: +20 pts
                insurance_points = insurance_sold * 20

                # Multiplicador por trade-in (+20 pts)
                tradein_points = sales_tradein * 20

                # Bonus por NPS alto (si NPS >= 80, +25 pts por entrega)
                nps_bonus = (sales * 25) if nps_personal >= 80 else 0

                # Total de puntos
                total_points = (
                    base_points
                    + financing_points
                    + warranty_points
                    + insurance_points
                    + tradein_points
                    + nps_bonus
                )

                # Puntos promedio por entrega
                points_per_delivery = total_points / sales if sales > 0 else 0

                # Nivel basado en puntos
                if total_points >= 1500:
                    incentive_level = "💎 Diamond"
                elif total_points >= 1000:
                    incentive_level = "🥇 Gold"
                elif total_points >= 500:
                    incentive_level = "🥈 Silver"
                else:
                    incentive_level = "🥉 Bronze"

                # MÉTRICAS DE EFICIENCIA PARA CITY MANAGER
                # Revenue per slot (eficiencia del uso de capacidad)
                revenue_generated = sales * np.random.uniform(18000, 28000)
                slots_used = appointments
                revenue_per_slot = (
                    revenue_generated / slots_used if slots_used > 0 else 0
                )

                # Eficiencia compuesta (considera revenue Y penetrations)
                efficiency_composite = (
                    (financing_penetration / 100 * 0.3)
                    + (ancillary_penetration / 100 * 0.3)
                    + (ownership_score / 100 * 0.2)
                    + (min(nps_personal, 100) / 100 * 0.2)
                ) * 100

                # Cuadrante de optimización
                # Alta utilización = >75%, Alta eficiencia = efficiency_composite > 60
                if utilization > 0.75 and efficiency_composite > 60:
                    optimization_quadrant = "🟢 Estrella"
                elif utilization <= 0.75 and efficiency_composite > 60:
                    optimization_quadrant = "🔵 Potencial"
                elif utilization > 0.75 and efficiency_composite <= 60:
                    optimization_quadrant = "🔴 Saturado"
                else:
                    optimization_quadrant = "🟡 Revisar"

                # Capacidad disponible para más leads
                capacity_for_leads = int(available_slots * 0.8)  # 80% de slots libres

                records.append(
                    {
                        "agent_id": agent_id,
                        "agent_name": agent_name,
                        "country": country,
                        "region": region,  # NEW: Region column
                        "hub": hub,  # Specific hub within region
                        # Métricas tradicionales
                        "leads": leads_nuevos,
                        "appointments": appointments,
                        "reservations": reservations,
                        "sales": sales,
                        "conversion": sales / leads_nuevos
                        if leads_nuevos > 0
                        else 0,  # Conversión tradicional
                        # DESGLOSE POR TIPO DE OPERACIÓN
                        "sales_only": sales_only,  # Ventas puras
                        "sales_tradein": sales_tradein,  # Ventas con trade-in
                        "purchases_pure": purchases_pure,  # Compras puras
                        "purchases_total": purchases,  # Total compras (incluye trade-in)
                        "total_operations": sales + purchases_pure,  # Total operaciones
                        # NUEVAS MÉTRICAS DE CAPACIDAD
                        "slots_per_week": slots_per_week,
                        "available_slots": available_slots,
                        "utilization": utilization,
                        # NUEVAS MÉTRICAS DE OPORTUNIDADES
                        "backlog_cartera": backlog_cartera,
                        "total_opportunities": total_opportunities,
                        "conversion_real": conversion_real,  # Conversiones / Oportunidades
                        "aprovechamiento_pct": (sales / total_opportunities * 100)
                        if total_opportunities > 0
                        else 0,
                        # NUEVAS MÉTRICAS DE STOCK
                        "stock_assigned": stock_assigned,
                        "stock_avg_age": stock_avg_age,
                        "stock_attractiveness": stock_attractiveness,
                        "lead_match_score": lead_match_score,
                        "efficiency_score": efficiency_score,
                        # NUEVAS MÉTRICAS DE ANCILLARIES
                        "insurance_sold": insurance_sold,
                        "insurance_penetration": insurance_penetration,
                        "extended_warranty_sold": extended_warranty_sold,
                        "extended_warranty_penetration": extended_warranty_penetration,
                        "total_ancillaries": total_ancillaries,
                        "ancillary_penetration": ancillary_penetration,
                        # FINANCING
                        "financing_sold": financing_sold,
                        "financing_penetration": financing_penetration,
                        # Métricas existentes
                        "nps": nps_personal,
                        "csat": np.random.uniform(65, 95),
                        "noshow": appointments
                        * np.random.uniform(0.05, 0.30)
                        / appointments
                        if appointments > 0
                        else 0,
                        "avg_response_time": np.random.uniform(0.5, 4),  # hours
                        "revenue": revenue_generated,
                        # ══════════════════════════════════════════════
                        # OWNERSHIP & PUNTOS COMPUESTOS
                        # ══════════════════════════════════════════════
                        "handoffs": handoffs,
                        "ownership_score": ownership_score,
                        # Puntos compuestos
                        "base_points": base_points,
                        "financing_points": financing_points,
                        "warranty_points": warranty_points,
                        "insurance_points": insurance_points,
                        "tradein_points": tradein_points,
                        "nps_bonus": nps_bonus,
                        "total_points": total_points,
                        "points_per_delivery": points_per_delivery,
                        "incentive_level": incentive_level,
                        # Métricas de eficiencia para City Manager
                        "revenue_per_slot": revenue_per_slot,
                        "efficiency_composite": efficiency_composite,
                        "optimization_quadrant": optimization_quadrant,
                        "capacity_for_leads": capacity_for_leads,
                    }
                )
                agent_id += 1

    return pd.DataFrame(records)


def generate_inventory_data():
    """Generate inventory data by region and segment"""
    records = []

    for country in COUNTRIES:
        regions = HUBS[country]
        for region in regions:
            for segment in VEHICLE_SEGMENTS:
                total_inventory = int(np.random.uniform(20, 100))
                reserved = int(total_inventory * np.random.uniform(0.1, 0.3))
                vip = int(total_inventory * np.random.uniform(0.05, 0.15))

                records.append(
                    {
                        "country": country,
                        "region": region,  # NEW: Region column
                        "hub": region,  # For backwards compatibility
                        "segment": segment,
                        "total_inventory": total_inventory,
                        "available": total_inventory - reserved - vip,
                        "reserved": reserved,
                        "vip": vip,
                        "aging_0_30": int(
                            total_inventory * np.random.uniform(0.4, 0.6)
                        ),
                        "aging_30_60": int(
                            total_inventory * np.random.uniform(0.2, 0.4)
                        ),
                        "aging_60_plus": int(
                            total_inventory * np.random.uniform(0.05, 0.2)
                        ),
                        "avg_days_in_inventory": np.random.uniform(15, 60),
                    }
                )

    return pd.DataFrame(records)


def generate_funnel_data(date_range):
    """Generate funnel conversion data"""
    records = []

    for country in COUNTRIES:
        regions = HUBS[country]
        for region in regions:
            # Last 30 days aggregate
            leads = int(np.random.uniform(1000, 3000))
            appointments = int(leads * np.random.uniform(0.5, 0.7))
            reservations = int(appointments * np.random.uniform(0.4, 0.6))
            sales = int(reservations * np.random.uniform(0.6, 0.8))

            records.append(
                {
                    "country": country,
                    "region": region,  # NEW: Region column
                    "hub": region,  # For backwards compatibility
                    "leads": leads,
                    "appointments": appointments,
                    "reservations": reservations,
                    "sales": sales,
                    "cvr_lead_to_appointment": appointments / leads if leads > 0 else 0,
                    "cvr_appointment_to_reservation": reservations / appointments
                    if appointments > 0
                    else 0,
                    "cvr_reservation_to_sale": sales / reservations
                    if reservations > 0
                    else 0,
                    "cvr_total": sales / leads if leads > 0 else 0,
                }
            )

    return pd.DataFrame(records)


def generate_alerts():
    """Generate sample alerts"""
    alerts = [
        {
            "type": "critical",
            "title": "Caída en conversión - CDMX Sur",
            "description": "Conversión bajó 15% vs semana anterior",
            "timestamp": datetime.now() - timedelta(hours=2),
        },
        {
            "type": "warning",
            "title": "Inventario envejecido - Monterrey",
            "description": "25 vehículos con más de 60 días en inventario",
            "timestamp": datetime.now() - timedelta(hours=5),
        },
        {
            "type": "info",
            "title": "NPS mejorado - Guadalajara",
            "description": "NPS subió a 82 (+8 puntos)",
            "timestamp": datetime.now() - timedelta(hours=8),
        },
        {
            "type": "critical",
            "title": "Alta tasa de no-show - São Paulo",
            "description": "No-show rate: 32% (límite: 25%)",
            "timestamp": datetime.now() - timedelta(hours=12),
        },
    ]

    return pd.DataFrame(alerts)


def generate_customer_data():
    """Generate customer/user data with detailed transaction history and ancillaries"""
    customers = []
    customer_id = 1000

    # Ancillary products/services
    ancillary_products = [
        {"name": "Seguro Total", "price": 12000, "category": "Insurance"},
        {"name": "Seguro Básico", "price": 6000, "category": "Insurance"},
        {"name": "Garantía Extendida 2 años", "price": 15000, "category": "Warranty"},
        {"name": "Garantía Extendida 3 años", "price": 22000, "category": "Warranty"},
        {"name": "GPS Tracking", "price": 3500, "category": "Tech"},
        {"name": "Mantenimiento Premium", "price": 8000, "category": "Service"},
        {"name": "Dashcam", "price": 2500, "category": "Tech"},
        {"name": "Llantas Premium", "price": 12000, "category": "Accessories"},
        {"name": "Polarizado", "price": 2000, "category": "Accessories"},
    ]

    # Generate 200 customers across all regions
    for country in COUNTRIES:
        regions = HUBS[country]
        for region in regions:
            # Get hubs for this region
            region_hubs = REGIONS_HUBS.get(country, {}).get(region, [region])

            # If no specific hubs, use region name as hub
            if not region_hubs:
                region_hubs = [region]

            # Select a few hubs for this region
            num_hubs_to_use = min(3, len(region_hubs))
            hubs_to_use = (
                random.sample(region_hubs, num_hubs_to_use)
                if len(region_hubs) > 0
                else [region]
            )

            for hub in hubs_to_use:
                num_customers = np.random.randint(
                    25, 45
                )  # 25-45 customers per hub - aumentado significativamente

                for _ in range(num_customers):
                    # Customer basic info
                    first_names = [
                        "Carlos",
                        "María",
                        "José",
                        "Ana",
                        "Luis",
                        "Carmen",
                        "Miguel",
                        "Laura",
                        "Fernando",
                        "Patricia",
                        "Ricardo",
                        "Elena",
                        "Jorge",
                        "Isabel",
                        "Diego",
                    ]
                last_names = [
                    "González",
                    "Rodríguez",
                    "Martínez",
                    "López",
                    "García",
                    "Hernández",
                    "Pérez",
                    "Sánchez",
                    "Ramírez",
                    "Torres",
                    "Flores",
                    "Rivera",
                    "Gómez",
                ]

                customer_name = (
                    f"{random.choice(first_names)} {random.choice(last_names)}"
                )
                email = f"cliente{customer_id}@email.com"
                phone = f"+52 55 {np.random.randint(1000, 9999)} {np.random.randint(1000, 9999)}"

                # Customer status - más clientes activos para tener cartera
                status_options = ["Nuevo", "Activo", "VIP", "Recurrente", "Inactivo"]
                status_weights = [
                    0.35,
                    0.45,
                    0.08,
                    0.10,
                    0.02,
                ]  # Mayor peso a Nuevo y Activo
                status = np.random.choice(status_options, p=status_weights)

                # VIP flag
                is_vip = status == "VIP" or np.random.random() < 0.1

                # Registration date
                days_since_registration = np.random.randint(30, 365)
                registration_date = datetime.now() - timedelta(
                    days=days_since_registration
                )

                # Transaction history
                num_transactions = 0
                if status == "Nuevo":
                    num_transactions = np.random.randint(0, 2)
                elif status == "Activo":
                    num_transactions = np.random.randint(1, 3)
                elif status == "VIP" or status == "Recurrente":
                    num_transactions = np.random.randint(2, 5)
                else:  # Inactivo
                    num_transactions = np.random.randint(1, 2)

                # Sales and cancellations
                num_sales = min(
                    num_transactions, np.random.randint(0, num_transactions + 1)
                )
                num_cancellations = num_transactions - num_sales

                # Generate detailed transactions
                transactions = []
                for i in range(num_transactions):
                    trans_date = registration_date + timedelta(
                        days=np.random.randint(0, days_since_registration)
                    )
                    is_sale = i < num_sales

                    # Vehicle details
                    vehicle_brand = random.choice(
                        [
                            "Toyota",
                            "Honda",
                            "Nissan",
                            "Mazda",
                            "Volkswagen",
                            "Ford",
                            "Chevrolet",
                        ]
                    )
                    vehicle_model = random.choice(
                        ["Sedan", "SUV", "Pickup", "Hatchback"]
                    )
                    vehicle_year = np.random.randint(2018, 2024)
                    vehicle_name = f"{vehicle_brand} {vehicle_model} {vehicle_year}"
                    vehicle_price = np.random.uniform(150000, 350000)

                    if is_sale:
                        # Successful sale
                        # Ancillaries sold with this transaction
                        num_ancillaries = np.random.randint(1, 4)
                        selected_ancillaries = random.sample(
                            ancillary_products, num_ancillaries
                        )
                        ancillaries_total = sum(
                            [a["price"] for a in selected_ancillaries]
                        )

                        transactions.append(
                            {
                                "transaction_id": f"TRX-{customer_id}-{i+1}",
                                "date": trans_date,
                                "type": "Venta",
                                "vehicle": vehicle_name,
                                "vehicle_price": vehicle_price,
                                "ancillaries": selected_ancillaries,
                                "ancillaries_total": ancillaries_total,
                                "total_amount": vehicle_price + ancillaries_total,
                                "financing": random.choice([True, False]),
                                "down_payment": vehicle_price
                                * np.random.uniform(0.15, 0.3)
                                if random.choice([True, False])
                                else vehicle_price,
                            }
                        )
                    else:
                        # Cancellation
                        cancel_reasons = [
                            "Financiamiento no aprobado",
                            "Cambió de opinión",
                            "Encontró mejor precio",
                            "No le gustó el vehículo",
                            "Problemas económicos",
                            "Compró en otro lado",
                        ]
                        transactions.append(
                            {
                                "transaction_id": f"TRX-{customer_id}-{i+1}",
                                "date": trans_date,
                                "type": "Cancelación",
                                "vehicle": vehicle_name,
                                "vehicle_price": vehicle_price,
                                "cancel_reason": random.choice(cancel_reasons),
                                "stage": random.choice(
                                    [
                                        "Reserva",
                                        "Test Drive",
                                        "Negociación",
                                        "Documentos",
                                    ]
                                ),
                            }
                        )

                # Total revenue
                total_revenue = sum(
                    [
                        t.get("total_amount", 0)
                        for t in transactions
                        if t["type"] == "Venta"
                    ]
                )
                total_ancillaries_revenue = sum(
                    [
                        t.get("ancillaries_total", 0)
                        for t in transactions
                        if t["type"] == "Venta"
                    ]
                )

                # Last purchase date
                sales_transactions = [t for t in transactions if t["type"] == "Venta"]
                if sales_transactions:
                    last_purchase_date = max([t["date"] for t in sales_transactions])
                else:
                    last_purchase_date = None

                # Vehicle interests
                interests = []
                num_interests = np.random.randint(1, 4)
                for _ in range(num_interests):
                    interests.append(random.choice(VEHICLE_SEGMENTS))
                vehicle_interests = ", ".join(list(set(interests)))

                # Preferred brands (based on transactions or random)
                if transactions:
                    brands_seen = [
                        t["vehicle"].split()[0] for t in transactions if "vehicle" in t
                    ]
                    preferred_brands = (
                        ", ".join(list(set(brands_seen))[:3])
                        if brands_seen
                        else "Sin preferencia"
                    )
                else:
                    preferred_brands = random.choice(
                        [
                            "Toyota, Honda",
                            "Nissan, Mazda",
                            "Volkswagen",
                            "Ford, Chevrolet",
                            "Sin preferencia",
                        ]
                    )

                # Assign to agent (from the hub)
                agent_id = np.random.randint(1, AGENTS_PER_HUB + 1)

                # Customer score (propensity to buy)
                if status == "VIP":
                    customer_score = np.random.randint(80, 100)
                elif status == "Recurrente":
                    customer_score = np.random.randint(70, 90)
                elif status == "Activo":
                    customer_score = np.random.randint(50, 80)
                elif status == "Nuevo":
                    customer_score = np.random.randint(40, 70)
                else:  # Inactivo
                    customer_score = np.random.randint(20, 50)

                # NPS rating (if they bought)
                if num_sales > 0:
                    if is_vip:
                        nps_rating = np.random.randint(8, 11)
                    else:
                        nps_rating = np.random.randint(0, 11)
                else:
                    nps_rating = None

                # Last interaction
                days_since_last_interaction = np.random.randint(1, 30)
                last_interaction_date = datetime.now() - timedelta(
                    days=days_since_last_interaction
                )

                # Interaction history (calls, messages, visits)
                num_calls = np.random.randint(0, 10)
                num_messages = np.random.randint(0, 15)
                num_visits = np.random.randint(0, 5)

                # Notes / comments
                notes_options = [
                    "Cliente muy interesado en SUVs",
                    "Busca financiamiento flexible",
                    "Prefiere modelos recientes (2020+)",
                    "Tiene trade-in disponible",
                    "Cliente corporativo - descuento aplicable",
                    "Busca entrega rápida (< 1 semana)",
                    "Sensible al precio - negociar",
                    "Cliente referido por Ana López",
                    "Quiere test drive antes de decidir",
                    "Interesado en paquete completo con seguros",
                ]
                notes = random.choice(notes_options)

                # Generate Celeste (AI) conversation data
                celeste_data = generate_celeste_conversation(
                    customer_id, vehicle_interests, customer_score, status
                )

                customers.append(
                    {
                        "customer_id": f"CL-{customer_id}",
                        "customer_name": customer_name,
                        "email": email,
                        "phone": phone,
                        "country": country,
                        "region": region,  # NEW: Region column
                        "hub": hub,  # Specific hub within region
                        "status": status,
                        "is_vip": is_vip,
                        "registration_date": registration_date,
                        "last_interaction_date": last_interaction_date,
                        "last_purchase_date": last_purchase_date,
                        "assigned_agent_id": agent_id,
                        "num_transactions": num_transactions,
                        "num_sales": num_sales,
                        "num_cancellations": num_cancellations,
                        "total_revenue": total_revenue,
                        "total_ancillaries_revenue": total_ancillaries_revenue,
                        "vehicle_interests": vehicle_interests,
                        "preferred_brands": preferred_brands,
                        "customer_score": customer_score,
                        "nps_rating": nps_rating,
                        "num_calls": num_calls,
                        "num_messages": num_messages,
                        "num_visits": num_visits,
                        "notes": notes,
                        "days_since_registration": days_since_registration,
                        "transactions": transactions,  # Full transaction history
                        # Celeste AI conversation data
                        "celeste_conversation": celeste_data["conversation"],
                        "celeste_summary": celeste_data["summary"],
                        "celeste_recommendations": celeste_data["recommendations"],
                        "celeste_vehicles_shown": celeste_data["vehicles_shown"],
                        "celeste_last_interaction": celeste_data["last_interaction"],
                        "celeste_messages_count": celeste_data["messages_count"],
                        "celeste_main_objections": celeste_data["main_objections"],
                        "celeste_budget_range": celeste_data["budget_range"],
                        "celeste_financing_interest": celeste_data[
                            "financing_interest"
                        ],
                        "celeste_tradein_info": celeste_data["tradein_info"],
                    }
                )

                customer_id += 1

    return pd.DataFrame(customers)


def generate_celeste_conversation(customer_id, vehicle_interests, score, status):
    """Generate simulated Celeste AI conversation data for a customer"""

    # Last interaction with Celeste
    hours_ago = np.random.randint(1, 72)
    last_interaction = datetime.now() - timedelta(hours=hours_ago)

    # Number of messages exchanged
    messages_count = np.random.randint(5, 45)

    # Budget range based on score
    budget_options = [
        ("$150,000 - $200,000", 175000),
        ("$200,000 - $250,000", 225000),
        ("$250,000 - $300,000", 275000),
        ("$300,000 - $350,000", 325000),
        ("$350,000 - $450,000", 400000),
    ]
    budget_range = random.choice(budget_options)

    # Financing interest
    financing_options = [
        {"interested": True, "months": 24, "down_payment_pct": 30},
        {"interested": True, "months": 36, "down_payment_pct": 20},
        {"interested": True, "months": 48, "down_payment_pct": 15},
        {"interested": True, "months": 60, "down_payment_pct": 10},
        {"interested": False, "months": 0, "down_payment_pct": 100},
    ]
    financing_interest = random.choice(financing_options)

    # Trade-in info
    tradein_options = [
        None,
        {"brand": "Nissan", "model": "Versa", "year": 2018, "estimated_value": 95000},
        {
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2019,
            "estimated_value": 145000,
        },
        {"brand": "Honda", "model": "Civic", "year": 2017, "estimated_value": 125000},
        {"brand": "Mazda", "model": "3", "year": 2020, "estimated_value": 175000},
        {
            "brand": "Volkswagen",
            "model": "Jetta",
            "year": 2018,
            "estimated_value": 115000,
        },
    ]
    tradein_info = random.choice(tradein_options)

    # Main objections/concerns
    objection_options = [
        "Precio inicial le pareció alto",
        "Quiere ver el vehículo en persona antes de decidir",
        "Dudas sobre la garantía extendida",
        "Preocupación por el kilometraje",
        "Necesita aprobación de financiamiento primero",
        "Comparando con otras opciones",
        "Tiempo de entrega muy largo",
        "Quiere negociar el precio del trade-in",
    ]
    num_objections = np.random.randint(0, 3)
    main_objections = random.sample(objection_options, num_objections)

    # Vehicles shown by Celeste
    vehicle_brands = ["Toyota", "Honda", "Nissan", "Mazda", "Volkswagen", "Ford"]
    vehicle_models = {
        "SUV": ["RAV4", "CR-V", "X-Trail", "CX-5", "Tiguan", "Escape"],
        "Sedán": ["Corolla", "Civic", "Sentra", "3", "Jetta", "Focus"],
        "Pickup": ["Hilux", "Ridgeline", "Frontier", "BT-50", "Amarok", "Ranger"],
        "Hatchback": ["Yaris", "Fit", "March", "2", "Polo", "Fiesta"],
        "Premium": ["Camry", "Accord", "Altima", "6", "Passat", "Fusion"],
    }

    # Get vehicle type from interests
    interest_type = (
        vehicle_interests.split(",")[0].strip() if vehicle_interests else "SUV"
    )
    if interest_type not in vehicle_models:
        interest_type = "SUV"

    vehicles_shown = []
    num_vehicles = np.random.randint(2, 5)
    lotes = ["A1", "A2", "B1", "B2", "B3", "C1", "C2", "D1"]

    for i in range(num_vehicles):
        brand = random.choice(vehicle_brands)
        model = random.choice(vehicle_models[interest_type])
        year = np.random.randint(2019, 2024)
        price = int(budget_range[1] * np.random.uniform(0.85, 1.15))
        vin = f"VIN-{np.random.randint(10000, 99999)}"
        lote = random.choice(lotes)

        vehicles_shown.append(
            {
                "brand": brand,
                "model": model,
                "year": year,
                "price": price,
                "vin": vin,
                "lote": lote,
                "is_favorite": i == 0,  # First one is favorite
            }
        )

    # Generate conversation summary
    summary_templates = [
        f"Busca {interest_type} familiar, presupuesto {budget_range[0]}",
        f"Interesado en {interest_type}, {'con' if financing_interest['interested'] else 'sin'} financiamiento",
        f"Cliente {'VIP' if status == 'VIP' else 'activo'} buscando {interest_type}",
    ]
    summary_base = random.choice(summary_templates)

    if financing_interest["interested"]:
        summary_base += (
            f". Preguntó por financiamiento a {financing_interest['months']} meses"
        )

    if tradein_info:
        summary_base += f". Tiene {tradein_info['brand']} {tradein_info['model']} {tradein_info['year']} para trade-in"

    if main_objections:
        summary_base += f". Duda principal: {main_objections[0].lower()}"

    # Generate recommendations for the agent
    recommendations = []

    if financing_interest["interested"]:
        recommendations.append(
            f"Ten preparada cotización de financiamiento a {financing_interest['months']} meses "
            f"con enganche del {financing_interest['down_payment_pct']}%"
        )

    if tradein_info:
        recommendations.append(
            f"Verificar estado del trade-in ({tradein_info['brand']} {tradein_info['model']} "
            f"{tradein_info['year']}) - valor estimado ${tradein_info['estimated_value']:,}"
        )

    if vehicles_shown:
        fav = vehicles_shown[0]
        recommendations.append(
            f"Su vehículo favorito es el {fav['brand']} {fav['model']} {fav['year']} "
            f"- está en Lote {fav['lote']}"
        )

    if "Precio" in str(main_objections):
        recommendations.append("Sensible al precio - mencionar promociones actuales")

    if "garantía" in str(main_objections).lower():
        recommendations.append(
            "Explicar beneficios de Kavak Total (garantía extendida)"
        )

    if score > 75:
        recommendations.append("Cliente con alta propensión - priorizar cierre")

    # Generate sample conversation messages
    conversation_messages = generate_sample_conversation(
        interest_type, budget_range[0], financing_interest, tradein_info, vehicles_shown
    )

    return {
        "conversation": conversation_messages,
        "summary": summary_base,
        "recommendations": recommendations,
        "vehicles_shown": vehicles_shown,
        "last_interaction": last_interaction,
        "messages_count": messages_count,
        "main_objections": main_objections,
        "budget_range": budget_range[0],
        "financing_interest": financing_interest,
        "tradein_info": tradein_info,
    }


def generate_sample_conversation(interest_type, budget, financing, tradein, vehicles):
    """Generate sample conversation messages between customer and Celeste"""
    messages = []

    # Opening
    messages.append(
        {
            "sender": "customer",
            "message": f"Hola, estoy buscando un {interest_type}",
            "timestamp": datetime.now() - timedelta(hours=np.random.randint(2, 48)),
        }
    )

    messages.append(
        {
            "sender": "celeste",
            "message": f"¡Hola! Soy Celeste, tu asesora virtual de Kavak. "
            f"Me encanta ayudarte a encontrar tu {interest_type} ideal. "
            f"¿Tienes algún presupuesto en mente?",
            "timestamp": datetime.now() - timedelta(hours=np.random.randint(2, 48)),
        }
    )

    messages.append(
        {
            "sender": "customer",
            "message": f"Sí, estoy pensando en algo entre {budget}",
            "timestamp": datetime.now() - timedelta(hours=np.random.randint(1, 24)),
        }
    )

    if financing and financing.get("interested"):
        messages.append(
            {
                "sender": "customer",
                "message": f"¿Tienen opciones de financiamiento? Me interesaría a {financing['months']} meses",
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(1, 12)),
            }
        )

        messages.append(
            {
                "sender": "celeste",
                "message": f"¡Claro! Tenemos excelentes opciones de financiamiento. "
                f"A {financing['months']} meses con un enganche del {financing['down_payment_pct']}% "
                f"tendrías mensualidades muy accesibles. ¿Te gustaría ver una cotización detallada?",
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(1, 12)),
            }
        )

    if tradein:
        messages.append(
            {
                "sender": "customer",
                "message": f"Tengo un {tradein['brand']} {tradein['model']} {tradein['year']} "
                f"que me gustaría dar a cuenta",
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(1, 6)),
            }
        )

        messages.append(
            {
                "sender": "celeste",
                "message": f"¡Perfecto! El trade-in es una excelente opción. "
                f"Tu {tradein['brand']} {tradein['model']} {tradein['year']} podría tener "
                f"un valor estimado de ${tradein['estimated_value']:,}. "
                f"Un especialista lo evaluará cuando vengas al hub.",
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(1, 6)),
            }
        )

    if vehicles:
        fav = vehicles[0]
        messages.append(
            {
                "sender": "celeste",
                "message": f"Basado en lo que me cuentas, te recomiendo ver el "
                f"{fav['brand']} {fav['model']} {fav['year']} a ${fav['price']:,}. "
                f"Tiene excelentes reviews y está dentro de tu presupuesto.",
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(1, 3)),
            }
        )

        messages.append(
            {
                "sender": "customer",
                "message": "Se ve muy bien, me gustaría verlo en persona",
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(0, 2)),
            }
        )

        messages.append(
            {
                "sender": "celeste",
                "message": f"¡Excelente! Te agendo una cita en el hub. "
                f"El {fav['brand']} {fav['model']} está disponible en el Lote {fav['lote']}. "
                f"¿Qué día te queda mejor?",
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(0, 1)),
            }
        )

    return messages
