"""
Data generator for sample/placeholder data
Uses real delivery data and unit economics from actual Kavak dashboards
"""

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from config import AGENTS_PER_HUB, COUNTRIES, HUBS, REGIONS_HUBS, VEHICLE_SEGMENTS

# =============================================================================
# REAL DATA CONSTANTS - Based on actual Kavak dashboard (December 2024)
# =============================================================================

# Unit Economics by Country (in USD)
COUNTRY_UNIT_ECONOMICS = {
    "México": {
        "full_margin": (850, 1100),  # $979 USD avg
        "fin_ins": (1500, 2000),  # $1,738 USD avg (high attach rate)
        "kt": (180, 280),  # $228 USD avg (Kavak Trade)
        "pc1": (2700, 3200),  # $2,945 USD avg
        "ecac": (350, 450),  # $396 USD avg
        "ticket_avg": (12000, 18000),  # Average ticket in USD
        "nps_buyer": (38, 48),  # 41 L30D avg
        "nps_seller": (42, 52),  # 46 L30D avg
        "efficiency": (0.38, 0.48),  # 42% avg
    },
    "Brasil": {
        "full_margin": (850, 1100),  # $979 USD avg
        "fin_ins": (700, 1000),  # $855 USD avg (lower attach)
        "kt": (0, 50),  # $0 USD (not active)
        "pc1": (1600, 2100),  # $1,834 USD avg
        "ecac": (400, 520),  # $451 USD avg
        "ticket_avg": (8000, 14000),
        "nps_buyer": (72, 85),  # 79 L30D avg (high!)
        "nps_seller": (68, 80),  # 74 L30D avg
        "efficiency": (0.50, 0.62),  # 56% avg
    },
    "Argentina": {
        "full_margin": (1100, 1400),  # $1,254 USD avg (higher margin)
        "fin_ins": (450, 720),  # $584 USD avg
        "kt": (130, 200),  # $165 USD avg
        "pc1": (1800, 2200),  # $2,003 USD avg
        "ecac": (220, 320),  # $263 USD avg (efficient!)
        "ticket_avg": (10000, 16000),
        "nps_buyer": (42, 55),  # 48 L30D avg
        "nps_seller": (68, 80),  # 74 L30D avg
        "efficiency": (0.50, 0.62),  # 56% avg
    },
    "Chile": {
        "full_margin": (950, 1200),  # $1,083 USD avg
        "fin_ins": (380, 580),  # $479 USD avg
        "kt": (120, 185),  # $152 USD avg
        "pc1": (1500, 1950),  # $1,713 USD avg
        "ecac": (280, 380),  # $322 USD avg
        "ticket_avg": (11000, 17000),
        "nps_buyer": (55, 68),  # 60 L30D avg
        "nps_seller": (88, 98),  # 94 L30D avg (excellent!)
        "efficiency": (0.68, 0.82),  # 75% avg (best!)
    },
}

# Sales volume scale by country (relative to México = 1.0)
COUNTRY_VOLUME_SCALE = {
    "México": 1.0,  # ~480 MTD = ~16/day
    "Brasil": 0.23,  # ~110 MTD
    "Argentina": 0.20,  # ~98 MTD
    "Chile": 0.22,  # ~106 MTD
}

# Stock Health by Country (Aging distribution)
COUNTRY_STOCK_HEALTH = {
    "México": {"aging_0_30": 0.50, "aging_30_90": 0.393, "aging_90_plus": 0.108},
    "Brasil": {"aging_0_30": 0.447, "aging_30_90": 0.375, "aging_90_plus": 0.178},
    "Argentina": {"aging_0_30": 0.561, "aging_30_90": 0.279, "aging_90_plus": 0.160},
    "Chile": {"aging_0_30": 0.586, "aging_30_90": 0.287, "aging_90_plus": 0.127},
}

# Operational Health by Country
COUNTRY_OPERATIONAL = {
    "México": {"readiness": 0.98, "sell_rate_30d": 0.29, "sell_rate_60d": 0.72},
    "Brasil": {"readiness": 0.93, "sell_rate_30d": 0.48, "sell_rate_60d": 0.72},
    "Argentina": {"readiness": 0.66, "sell_rate_30d": 0.55, "sell_rate_60d": 0.84},
    "Chile": {"readiness": 0.81, "sell_rate_30d": 0.58, "sell_rate_60d": 0.87},
}

# Region-level data for México (from second image)
MEXICO_REGION_DATA = {
    "Ciudad de México": {
        "sales_pct": 0.63,  # ~303 of 480 (CDMX-N + C + P + S)
        "efficiency": (0.60, 1.0),
        "full_margin": (350, 450),  # Lower margin in CDMX
        "pc1": (450, 550),
    },
    "Guadalajara": {
        "sales_pct": 0.085,  # ~41 of 480
        "efficiency": (0.60, 0.72),
        "full_margin": (1100, 1350),  # Higher margin
        "pc1": (2100, 2450),
    },
    "Monterrey": {
        "sales_pct": 0.075,  # ~36 of 480
        "efficiency": (0.45, 0.58),
        "full_margin": (550, 750),
        "pc1": (1550, 1850),
    },
    "Puebla": {
        "sales_pct": 0.05,  # ~24 of 480
        "efficiency": (0.75, 0.88),
        "full_margin": (850, 1100),
        "pc1": (1850, 2150),
    },
    "Querétaro": {
        "sales_pct": 0.048,  # ~23 of 480
        "efficiency": (0.55, 0.68),
        "full_margin": (780, 1000),
        "pc1": (1800, 2100),
    },
    "Cuernavaca": {
        "sales_pct": 0.073,  # ~35 of 480 (CUE-PUE)
        "efficiency": (0.72, 0.88),
        "full_margin": (850, 1100),
        "pc1": (1900, 2200),
    },
    "León": {
        "sales_pct": 0.03,
        "efficiency": (0.50, 0.65),
        "full_margin": (700, 900),
        "pc1": (1600, 1900),
    },
    "San Luis Potosí": {
        "sales_pct": 0.02,
        "efficiency": (0.45, 0.60),
        "full_margin": (650, 850),
        "pc1": (1500, 1800),
    },
}

# Real delivery data from Mexico (historical)
REAL_DELIVERIES_DATA = {
    "México": {
        "Ciudad de México": {
            "2025-12": 303,  # MTD estimate
            "2025-11": 2465,
            "2025-10": 3327,
            "2025-09": 2973,
        },
        "Guadalajara": {
            "2025-12": 41,
            "2025-11": 355,
            "2025-10": 544,
            "2025-09": 413,
        },
        "Monterrey": {
            "2025-12": 36,
            "2025-11": 268,
            "2025-10": 436,
            "2025-09": 430,
        },
        "Puebla": {
            "2025-12": 24,
            "2025-11": 209,
            "2025-10": 253,
            "2025-09": 221,
        },
        "Querétaro": {
            "2025-12": 23,
            "2025-11": 262,
            "2025-10": 350,
            "2025-09": 278,
        },
        "Cuernavaca": {
            "2025-12": 35,
            "2025-11": 77,
            "2025-10": 113,
            "2025-09": 73,
        },
        "León": {
            "2025-12": 10,
            "2025-11": 65,
            "2025-10": 85,
            "2025-09": 70,
        },
        "San Luis Potosí": {
            "2025-12": 8,
            "2025-11": 45,
            "2025-10": 60,
            "2025-09": 50,
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
        "appointments": generate_appointments_data(),  # NEW: Citas/Agenda
        "kavakos": generate_kavakos_data(),  # NEW: Lista de Kavakos
    }

    return data


def generate_daily_metrics(date_range):
    """
    Generate daily aggregated metrics by country, region and hub.
    Uses real unit economics data from actual Kavak dashboards.
    Data is generated at HUB level (most granular), so aggregating by region
    will correctly sum all hubs within that region.
    """
    records = []

    for country in COUNTRIES:
        # Get country-specific unit economics
        country_ue = COUNTRY_UNIT_ECONOMICS.get(
            country,
            COUNTRY_UNIT_ECONOMICS["México"],  # Default to Mexico
        )
        volume_scale = COUNTRY_VOLUME_SCALE.get(country, 0.2)

        # Get regions for this country
        regions = HUBS[country]  # Region names

        # Get real delivery data if available for this country
        country_deliveries = REAL_DELIVERIES_DATA.get(country, {})

        for region in regions:
            # Get all hubs for this region
            region_hubs = REGIONS_HUBS.get(country, {}).get(region, [region])

            if not region_hubs:
                region_hubs = [region]

            # Get real deliveries for this region (to distribute among hubs)
            region_real_deliveries = country_deliveries.get(region, {})

            # Get region-specific data for México
            region_data = (
                MEXICO_REGION_DATA.get(region, None) if country == "México" else None
            )

            # Calculate hub weights based on hub name patterns (simulate different sizes)
            hub_weights = {}
            for hub in region_hubs:
                # Larger hubs get more weight
                if any(
                    x in hub.lower()
                    for x in [
                        "cdmx",
                        "fashion",
                        "hq",
                        "midtown",
                        "palermo",
                        "pinheiros",
                    ]
                ):
                    hub_weights[hub] = 1.5
                elif any(x in hub.lower() for x in ["aliado", "carshop", "wh"]):
                    hub_weights[hub] = 0.6
                else:
                    hub_weights[hub] = 1.0

            total_weight = sum(hub_weights.values())

            # Region scale for fallback data generation
            if region_data:
                region_scale = region_data["sales_pct"] * 30  # Scale factor
            else:
                region_scale = {
                    # México - regiones específicas (based on real MTD data)
                    "Ciudad de México": 10.0,  # ~303 MTD = ~10/day
                    "Guadalajara": 1.4,  # ~41 MTD
                    "Monterrey": 1.2,  # ~36 MTD
                    "Puebla": 0.8,  # ~24 MTD
                    "Querétaro": 0.77,  # ~23 MTD
                    "Cuernavaca": 1.17,  # ~35 MTD
                    "León": 0.33,  # ~10 MTD
                    "San Luis Potosí": 0.27,  # ~8 MTD
                    # Otros países - la región es el país
                    "Brasil": 3.7,  # ~110 MTD
                    "Argentina": 3.3,  # ~98 MTD
                    "Chile": 3.5,  # ~106 MTD
                }.get(region, 1.0)

            for hub in region_hubs:
                # Hub's proportion of region's total
                hub_proportion = hub_weights[hub] / total_weight

                for date in date_range:
                    month_key = date.strftime("%Y-%m")

                    # Base sales/deliveries
                    if month_key in region_real_deliveries:
                        # Use real data distributed by hub proportion
                        monthly_deliveries = region_real_deliveries[month_key]
                        hub_monthly = monthly_deliveries * hub_proportion
                        days_in_month = (
                            date.replace(day=28) + timedelta(days=4)
                        ).replace(day=1) - timedelta(days=1)
                        avg_daily = hub_monthly / days_in_month.day
                        sales = max(1, int(avg_daily * np.random.uniform(0.7, 1.3)))
                    else:
                        # Fallback: generate data scaled by region and hub proportion
                        day_factor = 1 + 0.1 * np.sin(2 * np.pi * date.dayofyear / 365)
                        trend_factor = 1 + 0.02 * (date - date_range[0]).days / len(
                            date_range
                        )

                        # Base sales per hub
                        base_sales = np.random.poisson(2) * hub_weights[hub]
                        sales = max(
                            1,
                            int(base_sales * day_factor * trend_factor * region_scale),
                        )

                    # Calculate funnel metrics backwards from sales
                    # Based on real efficiency: Sales/Purchases ratio
                    efficiency_range = country_ue["efficiency"]
                    efficiency = np.random.uniform(*efficiency_range)

                    # Purchases = Sales / Efficiency (efficiency < 1 means more purchases than sales)
                    purchases = max(1, int(sales / efficiency))

                    # Funnel: Leads → Appointments (60%) → Reservations (50%) → Sales (75%)
                    reservations = max(1, int(sales / np.random.uniform(0.70, 0.85)))
                    appointments = max(
                        1, int(reservations / np.random.uniform(0.45, 0.55))
                    )
                    leads = max(1, int(appointments / np.random.uniform(0.55, 0.65)))

                    # Unit economics from real data
                    ticket_avg = np.random.uniform(*country_ue["ticket_avg"])
                    full_margin = np.random.uniform(*country_ue["full_margin"])
                    fin_ins = np.random.uniform(*country_ue["fin_ins"])
                    kt = np.random.uniform(*country_ue["kt"])
                    pc1 = full_margin + fin_ins + kt  # PC1 = FM + F&I + KT
                    ecac_range = country_ue["ecac"]
                    ecac = np.random.uniform(*ecac_range)

                    # NPS from real data
                    nps_buyer = np.random.uniform(*country_ue["nps_buyer"])
                    nps_seller = np.random.uniform(*country_ue["nps_seller"])
                    # Average NPS for general metric
                    nps = (nps_buyer + nps_seller) / 2

                    # Cost per lead derived from eCAC
                    # eCAC = (CPL * Leads) / Sales, so CPL = (eCAC * Sales) / Leads
                    cost_per_lead = (ecac * sales) / leads if leads > 0 else ecac / 3

                    records.append(
                        {
                            "date": date,
                            "country": country,
                            "region": region,
                            "hub": hub,
                            "leads": leads,
                            "appointments": appointments,
                            "reservations": reservations,
                            "sales": sales,
                            "purchases": purchases,
                            "cancellations": int(
                                reservations * np.random.uniform(0.05, 0.12)
                            ),
                            "noshow": int(appointments * np.random.uniform(0.08, 0.18)),
                            "nps": nps,
                            "nps_buyer": nps_buyer,
                            "nps_seller": nps_seller,
                            "csat": np.random.uniform(75, 92),
                            "revenue": sales * ticket_avg,
                            "ticket_avg": ticket_avg,
                            "full_margin": full_margin,
                            "fin_ins": fin_ins,
                            "kt": kt,
                            "pc1": pc1,
                            "ecac": ecac,
                            "pc1_minus_ecac": pc1 - ecac,
                            "cost_per_lead": cost_per_lead,
                            "sla_lead_to_sale": np.random.uniform(4, 12),
                            "efficiency": efficiency,
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

            for hub in hubs_to_use[:3]:  # Use up to 3 hubs per region
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
    """Generate inventory data by region and segment using real stock health data"""
    records = []

    for country in COUNTRIES:
        # Get country-specific stock health data
        stock_health = COUNTRY_STOCK_HEALTH.get(country, COUNTRY_STOCK_HEALTH["México"])
        operational = COUNTRY_OPERATIONAL.get(country, COUNTRY_OPERATIONAL["México"])

        regions = HUBS[country]
        for region in regions:
            for segment in VEHICLE_SEGMENTS:
                # Scale inventory by country size
                base_inventory = {
                    "México": (40, 120),
                    "Brasil": (25, 80),
                    "Argentina": (20, 60),
                    "Chile": (20, 65),
                }.get(country, (20, 60))

                total_inventory = int(np.random.uniform(*base_inventory))

                # Reserved and VIP based on readiness
                readiness = operational["readiness"]
                reserved = int(total_inventory * np.random.uniform(0.08, 0.18))
                vip = int(total_inventory * np.random.uniform(0.03, 0.10))

                # Aging based on real stock health data
                aging_0_30_pct = stock_health["aging_0_30"] + np.random.uniform(
                    -0.05, 0.05
                )
                aging_30_90_pct = stock_health["aging_30_90"] + np.random.uniform(
                    -0.05, 0.05
                )
                aging_90_plus_pct = stock_health["aging_90_plus"] + np.random.uniform(
                    -0.03, 0.03
                )

                # Aging 60+ is approximately aging_30_90 * 0.4 + aging_90_plus
                aging_60_plus_pct = (aging_30_90_pct * 0.4) + aging_90_plus_pct

                records.append(
                    {
                        "country": country,
                        "region": region,
                        "hub": region,  # For backwards compatibility
                        "segment": segment,
                        "total_inventory": total_inventory,
                        "available": int(
                            (total_inventory - reserved - vip) * readiness
                        ),
                        "reserved": reserved,
                        "vip": vip,
                        "aging_0_30": int(total_inventory * aging_0_30_pct),
                        "aging_30_60": int(total_inventory * aging_30_90_pct * 0.6),
                        "aging_60_plus": int(total_inventory * aging_60_plus_pct),
                        "avg_days_in_inventory": np.random.uniform(18, 55),
                        "sell_rate_30d": operational["sell_rate_30d"]
                        + np.random.uniform(-0.05, 0.05),
                        "sell_rate_60d": operational["sell_rate_60d"]
                        + np.random.uniform(-0.05, 0.05),
                        "readiness": readiness + np.random.uniform(-0.03, 0.03),
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

            for hub in hubs_to_use[:3]:  # Up to 3 hubs per region
                num_customers = np.random.randint(
                    40, 70
                )  # 40-70 customers per hub - increased for better demo

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


def generate_appointments_data():
    """
    Generate appointments/agenda data for the current month
    Includes past, today, and future appointments
    """
    appointments = []
    appointment_id = 5000

    # Current date info
    today = datetime.now()
    current_month_start = today.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    # Calculate end of month
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    current_month_end = next_month - timedelta(days=1)

    # Appointment types
    appointment_types = [
        {"type": "Test Drive", "duration_min": 45, "icon": "🚗"},
        {"type": "Evaluación Trade-in", "duration_min": 30, "icon": "🔄"},
        {"type": "Firma de Contrato", "duration_min": 60, "icon": "📝"},
        {"type": "Entrega de Vehículo", "duration_min": 90, "icon": "🎉"},
        {"type": "Consulta Financiamiento", "duration_min": 30, "icon": "💰"},
        {"type": "Revisión de Vehículo", "duration_min": 45, "icon": "🔍"},
        {"type": "Primera Visita", "duration_min": 60, "icon": "👋"},
        {"type": "Seguimiento", "duration_min": 30, "icon": "📞"},
    ]

    # Appointment statuses
    statuses_past = ["Completada", "No Show", "Cancelada", "Reagendada"]
    statuses_future = ["Confirmada", "Pendiente", "Por Confirmar"]

    # Time slots (business hours)
    time_slots = [
        "09:00",
        "09:30",
        "10:00",
        "10:30",
        "11:00",
        "11:30",
        "12:00",
        "12:30",
        "13:00",
        "14:00",
        "14:30",
        "15:00",
        "15:30",
        "16:00",
        "16:30",
        "17:00",
        "17:30",
        "18:00",
    ]

    # Customer names for appointments
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
        "Sofía",
        "Andrés",
        "Valentina",
        "Pablo",
        "Camila",
        "Roberto",
        "Gabriela",
        "Sergio",
        "Alejandra",
        "Francisco",
        "Daniela",
        "Eduardo",
        "Paulina",
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
        "Díaz",
        "Morales",
        "Vargas",
        "Rojas",
        "Castro",
        "Ortiz",
        "Ruiz",
    ]

    # Vehicle options for appointments
    vehicles = [
        {"brand": "Toyota", "model": "RAV4", "year": 2022, "price": 385000},
        {"brand": "Honda", "model": "CR-V", "year": 2021, "price": 365000},
        {"brand": "Nissan", "model": "X-Trail", "year": 2023, "price": 420000},
        {"brand": "Mazda", "model": "CX-5", "year": 2022, "price": 395000},
        {"brand": "Volkswagen", "model": "Tiguan", "year": 2021, "price": 355000},
        {"brand": "Toyota", "model": "Corolla", "year": 2022, "price": 285000},
        {"brand": "Honda", "model": "Civic", "year": 2023, "price": 325000},
        {"brand": "Nissan", "model": "Sentra", "year": 2022, "price": 275000},
        {"brand": "Mazda", "model": "3", "year": 2021, "price": 295000},
        {"brand": "Ford", "model": "Escape", "year": 2022, "price": 375000},
        {"brand": "Chevrolet", "model": "Equinox", "year": 2021, "price": 345000},
        {"brand": "Hyundai", "model": "Tucson", "year": 2023, "price": 380000},
    ]

    # Generate appointments for each hub
    for country in COUNTRIES:
        regions = HUBS[country]
        for region in regions:
            region_hubs = REGIONS_HUBS.get(country, {}).get(region, [region])
            if not region_hubs:
                region_hubs = [region]

            for hub in region_hubs[:3]:  # Use up to 3 hubs per region
                # Get agents for this hub
                agent_ids = list(range(1, AGENTS_PER_HUB + 1))

                # Generate appointments for the entire month
                current_date = current_month_start
                while current_date <= current_month_end:
                    # Skip Sundays (day 6)
                    if current_date.weekday() == 6:
                        current_date += timedelta(days=1)
                        continue

                    # Number of appointments per day (more on weekends) - INCREASED
                    if current_date.weekday() == 5:  # Saturday
                        num_appointments = np.random.randint(15, 25)
                    else:
                        num_appointments = np.random.randint(10, 20)

                    for _ in range(num_appointments):
                        # Select random agent
                        agent_id = random.choice(agent_ids)

                        # Select appointment type
                        appt_type = random.choice(appointment_types)

                        # Select time slot
                        time_str = random.choice(time_slots)
                        hour, minute = map(int, time_str.split(":"))
                        appt_datetime = current_date.replace(hour=hour, minute=minute)

                        # Determine status based on date
                        if current_date.date() < today.date():
                            # Past appointment
                            status_weights = [0.70, 0.15, 0.10, 0.05]
                            status = np.random.choice(statuses_past, p=status_weights)
                        elif current_date.date() == today.date():
                            # Today's appointment
                            if appt_datetime < datetime.now():
                                status_weights = [0.75, 0.12, 0.08, 0.05]
                                status = np.random.choice(
                                    statuses_past, p=status_weights
                                )
                            else:
                                status_weights = [0.60, 0.25, 0.15]
                                status = np.random.choice(
                                    statuses_future, p=status_weights
                                )
                        else:
                            # Future appointment
                            status_weights = [0.55, 0.30, 0.15]
                            status = np.random.choice(statuses_future, p=status_weights)

                        # Customer info
                        customer_name = (
                            f"{random.choice(first_names)} {random.choice(last_names)}"
                        )
                        customer_id = f"CL-{np.random.randint(1000, 9999)}"
                        customer_phone = f"+52 55 {np.random.randint(1000, 9999)} {np.random.randint(1000, 9999)}"

                        # Vehicle of interest
                        vehicle = random.choice(vehicles)
                        vehicle_str = (
                            f"{vehicle['brand']} {vehicle['model']} {vehicle['year']}"
                        )

                        # Priority based on appointment type
                        if appt_type["type"] in [
                            "Firma de Contrato",
                            "Entrega de Vehículo",
                        ]:
                            priority = "Alta"
                        elif appt_type["type"] in ["Test Drive", "Evaluación Trade-in"]:
                            priority = "Media"
                        else:
                            priority = "Normal"

                        # Notes
                        notes_options = [
                            "Cliente muy interesado",
                            "Traerá acompañante",
                            "Ya vio el auto online",
                            "Tiene trade-in",
                            "Preguntó por financiamiento",
                            "Cliente referido",
                            "Segunda visita",
                            "Viene de otra ciudad",
                            "Prefiere pago de contado",
                            "Interesado en garantía extendida",
                            "",
                            "",
                        ]
                        notes = random.choice(notes_options)

                        # Result (for completed appointments)
                        result = None
                        if status == "Completada":
                            result_options = [
                                "Interesado - Seguimiento",
                                "Reservó vehículo",
                                "Firmó contrato",
                                "Pendiente decisión",
                                "No le interesó",
                                "Solicitó cotización",
                                "Agendó segunda cita",
                            ]
                            result_weights = [0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]
                            result = np.random.choice(result_options, p=result_weights)

                        appointments.append(
                            {
                                "appointment_id": f"APT-{appointment_id}",
                                "date": current_date.date(),
                                "time": time_str,
                                "datetime": appt_datetime,
                                "country": country,
                                "region": region,
                                "hub": hub,
                                "agent_id": agent_id,
                                "customer_id": customer_id,
                                "customer_name": customer_name,
                                "customer_phone": customer_phone,
                                "appointment_type": appt_type["type"],
                                "type_icon": appt_type["icon"],
                                "duration_min": appt_type["duration_min"],
                                "vehicle_interest": vehicle_str,
                                "vehicle_price": vehicle["price"],
                                "status": status,
                                "priority": priority,
                                "notes": notes,
                                "result": result,
                                "is_today": current_date.date() == today.date(),
                                "is_past": current_date.date() < today.date(),
                                "is_future": current_date.date() > today.date(),
                                "week_number": current_date.isocalendar()[1],
                                "day_of_week": current_date.strftime("%A"),
                                "day_of_week_es": [
                                    "Lunes",
                                    "Martes",
                                    "Miércoles",
                                    "Jueves",
                                    "Viernes",
                                    "Sábado",
                                    "Domingo",
                                ][current_date.weekday()],
                            }
                        )

                        appointment_id += 1

                    current_date += timedelta(days=1)

    return pd.DataFrame(appointments)


def generate_kavakos_data():
    """
    Generate detailed Kavako (agent) profiles with extended information
    """
    kavakos = []
    kavako_id = 1

    # Extended first names
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
        "Natalia",
        "Arturo",
        "Mónica",
        "Héctor",
        "Verónica",
        "Alberto",
        "Claudia",
        "Rafael",
        "Lorena",
        "Guillermo",
        "Sandra",
        "Enrique",
        "Adriana",
        "Armando",
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
        "Reyes",
        "Herrera",
        "Navarro",
        "Domínguez",
        "Vega",
        "Mendoza",
    ]

    # Specializations
    specializations = [
        "SUVs y Crossovers",
        "Sedanes Premium",
        "Vehículos Familiares",
        "Autos Compactos",
        "Pickups y Comerciales",
        "Financiamiento Especializado",
        "Trade-in Expert",
        "Clientes Corporativos",
        "Vehículos de Lujo",
        "Primera Compra",
    ]

    # Languages
    languages_options = [
        ["Español"],
        ["Español", "Inglés"],
        ["Español", "Inglés", "Portugués"],
        ["Español", "Francés"],
    ]

    # Certifications
    certifications_pool = [
        "Certificado Kavak Pro",
        "Especialista en Financiamiento",
        "Experto Trade-in",
        "Asesor Premium",
        "Certificación NPS Excellence",
        "Top Performer Q3 2024",
        "Mejor Vendedor Regional",
        "Curso Servicio al Cliente Avanzado",
    ]

    today = datetime.now()

    for country in COUNTRIES:
        regions = HUBS[country]
        for region in regions:
            region_hubs = REGIONS_HUBS.get(country, {}).get(region, [region])
            if not region_hubs:
                region_hubs = [region]

            for hub in region_hubs[:3]:  # Up to 3 hubs per region
                # Generate 15-25 kavakos per hub
                num_kavakos = np.random.randint(15, 26)

                for i in range(num_kavakos):
                    name = f"{random.choice(first_names)} {random.choice(last_names)}"
                    email = f"{name.lower().replace(' ', '.').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')}@kavak.com"

                    # Seniority
                    months_at_kavak = np.random.randint(3, 48)
                    hire_date = today - timedelta(days=months_at_kavak * 30)

                    if months_at_kavak >= 24:
                        seniority = "Senior"
                        base_conversion = np.random.uniform(0.18, 0.28)
                    elif months_at_kavak >= 12:
                        seniority = "Mid"
                        base_conversion = np.random.uniform(0.14, 0.22)
                    else:
                        seniority = "Junior"
                        base_conversion = np.random.uniform(0.10, 0.18)

                    # Performance metrics (current month)
                    leads_assigned = np.random.randint(80, 200)
                    appointments_scheduled = int(
                        leads_assigned * np.random.uniform(0.35, 0.55)
                    )
                    appointments_completed = int(
                        appointments_scheduled * np.random.uniform(0.70, 0.90)
                    )
                    reservations = int(
                        appointments_completed * np.random.uniform(0.40, 0.65)
                    )
                    sales = int(reservations * np.random.uniform(0.60, 0.85))

                    # Calculate metrics
                    conversion_rate = (
                        sales / leads_assigned if leads_assigned > 0 else 0
                    )
                    show_rate = (
                        appointments_completed / appointments_scheduled
                        if appointments_scheduled > 0
                        else 0
                    )

                    # Today's schedule
                    appointments_today = np.random.randint(3, 8)
                    appointments_completed_today = np.random.randint(
                        0, min(appointments_today, 4)
                    )
                    appointments_pending_today = (
                        appointments_today - appointments_completed_today
                    )

                    # This week
                    appointments_this_week = np.random.randint(15, 35)
                    sales_this_week = np.random.randint(2, 8)

                    # Ancillaries
                    financing_penetration = np.random.uniform(0.35, 0.65)
                    insurance_penetration = np.random.uniform(0.40, 0.70)
                    warranty_penetration = np.random.uniform(0.25, 0.55)

                    # NPS & CSAT
                    nps = np.random.uniform(55, 92)
                    csat = np.random.uniform(70, 98)

                    # Response time (hours)
                    avg_response_time = np.random.uniform(0.3, 3.5)

                    # Points and level
                    total_points = int(
                        sales * 100
                        + sales * financing_penetration * 50
                        + sales * insurance_penetration * 20
                        + sales * warranty_penetration * 30
                    )

                    if total_points >= 1500:
                        level = "💎 Diamond"
                    elif total_points >= 1000:
                        level = "🥇 Gold"
                    elif total_points >= 500:
                        level = "🥈 Silver"
                    else:
                        level = "🥉 Bronze"

                    # Ownership score
                    ownership_score = np.random.uniform(75, 98)

                    # Specialization and certifications
                    specialization = random.choice(specializations)
                    num_certs = np.random.randint(1, 4)
                    certifications = random.sample(certifications_pool, num_certs)
                    languages = random.choice(languages_options)

                    # Status
                    status_options = [
                        "Disponible",
                        "En cita",
                        "Ocupado",
                        "Almuerzo",
                        "Disponible",
                    ]
                    status_weights = [0.40, 0.25, 0.15, 0.05, 0.15]
                    current_status = np.random.choice(status_options, p=status_weights)

                    # Avatar placeholder
                    avatar_colors = [
                        "#7C3AED",
                        "#10B981",
                        "#F59E0B",
                        "#EF4444",
                        "#3B82F6",
                        "#EC4899",
                    ]

                    kavakos.append(
                        {
                            "kavako_id": kavako_id,
                            "name": name,
                            "email": email,
                            "phone": f"+52 55 {np.random.randint(1000, 9999)} {np.random.randint(1000, 9999)}",
                            "country": country,
                            "region": region,
                            "hub": hub,
                            "seniority": seniority,
                            "months_at_kavak": months_at_kavak,
                            "hire_date": hire_date,
                            "specialization": specialization,
                            "certifications": certifications,
                            "languages": languages,
                            "current_status": current_status,
                            "avatar_color": random.choice(avatar_colors),
                            # Monthly metrics
                            "leads_assigned": leads_assigned,
                            "appointments_scheduled": appointments_scheduled,
                            "appointments_completed": appointments_completed,
                            "reservations": reservations,
                            "sales": sales,
                            "conversion_rate": conversion_rate,
                            "show_rate": show_rate,
                            # Today
                            "appointments_today": appointments_today,
                            "appointments_completed_today": appointments_completed_today,
                            "appointments_pending_today": appointments_pending_today,
                            # This week
                            "appointments_this_week": appointments_this_week,
                            "sales_this_week": sales_this_week,
                            # Ancillaries
                            "financing_penetration": financing_penetration,
                            "insurance_penetration": insurance_penetration,
                            "warranty_penetration": warranty_penetration,
                            # Quality
                            "nps": nps,
                            "csat": csat,
                            "avg_response_time": avg_response_time,
                            "ownership_score": ownership_score,
                            # Incentives
                            "total_points": total_points,
                            "level": level,
                            # Capacity
                            "slots_available_today": max(0, 8 - appointments_today),
                            "slots_available_week": max(0, 40 - appointments_this_week),
                        }
                    )

                    kavako_id += 1

    return pd.DataFrame(kavakos)
