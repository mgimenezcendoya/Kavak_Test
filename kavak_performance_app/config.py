"""
Configuration file for Kavak Performance App
"""

# Countries
COUNTRIES = ["México", "Brasil", "Argentina", "Chile"]

# Regions and Hubs structure (based on real Kavak Mexico data)
# Each region contains multiple hubs/showrooms
REGIONS_HUBS = {
    "México": {
        "Ciudad de México": [
            "CDMX - El Rosario Town Center",
            "CDMX - Artz Pedregal",
            "CDMX - Antara Fashion Hall",
            "CDMX - San Ángel",
            "CDMX - Portal Centro",
            "CDMX - Florencia",
            "CDMX - Patio Tlalpan",
            "CDMX - Patio Santa Fe",
            "CDMX - Plaza Fortuna",
            "EDOMEX - Interlomas",
            "EDOMEX - Cosmopol",
            "EDOMEX - WH Lerma",
            "EDOMEX - Tlalnepantla",
            "Kavak Patio Tlalpan",
            "Kavak Cosmopol",
            "Kavak Plaza Fortuna",
            "Kavak Forum Cuernavaca",
            "Kavak Patio Santa Fe",
            "Kavak Artz Pedregal",
            "Kavak Puerta la Victoria",
            "Kavak Tlaquepaque",
            "Kavak Florencia",
            "Kavak Aliados - Nissan Toluca",
            "Kavak Aliados - Kia Coapa",
            "Kavak Midtown Guadalajara",
            "Kavak El Rosario Town Center",
            "Kavak Portal Centro",
            "Kavak Antara Fashion Hall",
            "Kavak Las Antenas",
            "Kavak Plaza Fortuna - Showroom",
            "Kavak Interlomas",
            "Kavak Aliado Omoda",
            "Kavak Aliado Nissan Metepec",
            "Kavak Tlalnepantla",
            "Kavak Portal San Ángel",
            "Kavak Lerma",
            "Carshop - Puerto Vallarta",
            "Nissan Torres Corzo Aliado",
            "Mi Domicio / Virtual",
            "HQ Explanada",
            "HQ Fashion Drive",
            "MTY - HQ FASHION DRIVE",
            "GDL - HQ Guadalajara",
            "GDL - Midtown",
            "PUE - EXPLANADA HQ",
            "QRO - PUERTA LA VICTORIA",
            "CUE - Fórum Cuernavaca",
            "WH - LERMA 2",
        ],
        "Monterrey": [
            "Kavak Tlaquepaque",
            "Kavak Patio Tlalpan",
            "Kavak Cosmopol",
            "EDOMEX - Tlalnepantla",
            "Kavak Portal San Ángel",
            "CDMX - Florencia",
            "Kavak Plaza Fortuna - Showroom",
            "Kavak Antara Fashion Hall",
            "Kavak Portal Centro",
            "Kavak Plaza Fortuna",
            "EDOMEX - Cosmopol",
            "HQ Explanada",
            "Kavak Aliado Omoda",
            "HQ Fashion Drive",
            "Kavak Patio Santa Fe",
            "Kavak Midtown Guadalajara",
            "Kavak Nuevo Sur",
            "Kavak El Rosario Town Center",
            "Kavak Artz Pedregal",
            "Kavak Puerta la Victoria",
            "QRO - PUERTA LA VICTORIA",
            "Kavak Aliado Nissan Metepec",
            "MTY - HQ FASHION DRIVE",
            "PUE - EXPLANADA HQ",
            "GDL - Midtown",
            "CDMX - Artz Pedregal",
            "Kavak Tlalnepantla",
            "Kavak Interlomas",
            "Kavak Lerma",
            "Kavak Florencia",
        ],
        "Guadalajara": [
            "Kavak Lerma",
            "Kavak Cosmopol",
            "GDL - Midtown",
            "Kavak Tlaquepaque",
            "Kavak Patio Santa Fe",
            "MTY - HQ FASHION DRIVE",
            "QRO - PUERTA LA VICTORIA",
            "Kavak Florencia",
            "CUE - Fórum Cuernavaca",
            "Kavak Plaza Fortuna - Showroom",
            "CDMX - Artz Pedregal",
            "Carshop - Puerto Vallarta",
            "HQ Explanada",
            "WH - LERMA 2",
            "EDOMEX - Cosmopol",
            "Kavak Portal Centro",
            "HQ Fashion Drive",
            "Kavak Forum Cuernavaca",
            "Kavak Artz Pedregal",
            "CDMX - Antara Fashion Hall",
            "Kavak Antara Fashion Hall",
            "Kavak Portal San Ángel",
            "Kavak Tlalnepantla",
            "Kavak Aliado Omoda",
            "CDMX - Plaza Fortuna",
            "Kavak Puerta la Victoria",
            "Kavak Midtown Guadalajara",
            "GDL - HQ Guadalajara",
        ],
        "Puebla": [
            "HQ Explanada",
            "QRO - PUERTA LA VICTORIA",
            "Kavak Antara Fashion Hall",
            "CDMX - San Ángel",
            "Kavak Midtown Guadalajara",
            "CDMX - Artz Pedregal",
            "Kavak Portal San Ángel",
            "Kavak Interlomas",
            "Kavak Tlaquepaque",
            "Kavak Cosmopol",
            "Kavak Plaza Fortuna",
            "Kavak Patio Santa Fe",
            "PUE - EXPLANADA HQ",
            "EDOMEX - Cosmopol",
            "GDL - Midtown",
            "Kavak Patio Tlalpan",
            "Kavak Florencia",
            "MTY - HQ FASHION DRIVE",
            "Kavak Forum Cuernavaca",
            "Kavak Portal Centro",
            "Kavak Plaza Fortuna - Showroom",
            "CUE - Fórum Cuernavaca",
            "Kavak Tlalnepantla",
            "Kavak Artz Pedregal",
            "GDL - HQ Guadalajara",
            "CDMX - Patio Santa Fe",
            "Kavak Lerma",
            "Kavak Aliados - Nissan Toluca",
        ],
        "Querétaro": [
            "CDMX - Florencia",
            "PUE - EXPLANADA HQ",
            "Kavak Forum Cuernavaca",
            "GDL - Midtown",
            "WH - LERMA 2",
            "CDMX - Patio Santa Fe",
            "Kavak Midtown Guadalajara",
            "CUE - Fórum Cuernavaca",
            "Kavak Portal San Ángel",
            "Kavak Puerta la Victoria",
            "Kavak Lerma",
            "Kavak Antara Fashion Hall",
            "CDMX - Portal Centro",
            "EDOMEX - Tlalnepantla",
            "HQ Explanada",
            "Kavak Tlaquepaque",
            "Kavak Aliado Omoda",
            "Kavak Aliado Nissan Metepec",
            "MTY - HQ FASHION DRIVE",
            "Kavak Artz Pedregal",
            "Kavak Plaza Fortuna",
            "Kavak Cosmopol",
            "CDMX - Plaza Fortuna",
            "Kavak El Rosario Town Center",
            "EDOMEX - Cosmopol",
            "CDMX - El Rosario Town Center",
            "HQ Fashion Drive",
            "Kavak Interlomas",
            "Kavak Patio Santa Fe",
            "Kavak Aliados - Nissan Toluca",
            "Nissan Torres Corzo Aliado",
            "Kavak Tlalnepantla",
            "Kavak Florencia",
            "Kavak Patio Tlalpan",
            "GDL - HQ Guadalajara",
            "CDMX - Patio Tlalpan",
            "QRO - PUERTA LA VICTORIA",
            "Kavak Plaza Fortuna - Showroom",
            "CDMX - Antara Fashion Hall",
            "Kavak Portal Centro",
        ],
        "Cuernavaca": [
            "CDMX - Antara Fashion Hall",
            "QRO - PUERTA LA VICTORIA",
            "CDMX - Plaza Fortuna",
            "CDMX - Patio Tlalpan",
            "CDMX - Portal Centro",
            "CDMX - El Rosario Town Center",
            "GDL - Midtown",
            "PUE - EXPLANADA HQ",
            "GDL - HQ Guadalajara",
            "EDOMEX - Tlalnepantla",
            "CDMX - San Ángel",
            "CUE - Fórum Cuernavaca",
            "CDMX - Artz Pedregal",
            "EDOMEX - Interlomas",
            "WH - LERMA 2",
        ],
        "León": [
            "Kavak Aliados - Kia Coapa",
            "HQ Fashion Drive",
            "Kavak Aliado Omoda",
            "Kavak Puerta la Victoria",
            "Nissan Torres Corzo Aliado",
            "Kavak Midtown Guadalajara",
            "Kavak Cosmopol",
            "Kavak Portal San Ángel",
            "Kavak Lerma",
            "Kavak Tlaquepaque",
            "HQ Explanada",
        ],
        "San Luis Potosí": [
            "HQ Fashion Drive",
            "Kavak Aliados - Nissan Toluca",
            "Nissan Torres Corzo Aliado",
            "Kavak Cosmopol",
            "Kavak Patio Santa Fe",
            "HQ Explanada",
        ],
    },
    # Para Brasil, Argentina y Chile: la región = país, los hubs son las ciudades/sucursales
    "Brasil": {
        "Brasil": [
            "Kavak São Paulo - Pinheiros",
            "Kavak São Paulo - Morumbi",
            "Kavak São Paulo - Tatuapé",
            "Kavak São Paulo - Santo André",
            "Kavak Rio de Janeiro - Barra",
            "Kavak Rio de Janeiro - Botafogo",
            "Kavak Rio de Janeiro - Norte Shopping",
            "Kavak Brasilia - Asa Norte",
            "Kavak Brasilia - Lago Sul",
            "Kavak Brasilia - Taguatinga",
        ],
    },
    "Argentina": {
        "Argentina": [
            "Kavak Buenos Aires - Palermo",
            "Kavak Buenos Aires - Belgrano",
            "Kavak Buenos Aires - Puerto Madero",
            "Kavak Buenos Aires - Nordelta",
            "Kavak Córdoba - Nueva Córdoba",
            "Kavak Córdoba - Cerro de las Rosas",
            "Kavak Rosario - Centro",
            "Kavak Rosario - Fisherton",
        ],
    },
    "Chile": {
        "Chile": [
            "Kavak Santiago - Las Condes",
            "Kavak Santiago - Providencia",
            "Kavak Santiago - La Dehesa",
            "Kavak Santiago - Vitacura",
            "Kavak Valparaíso - Viña del Mar",
            "Kavak Valparaíso - Centro",
            "Kavak Concepción - Centro",
            "Kavak Concepción - San Pedro",
        ],
    },
}

# Legacy HUBS structure for backwards compatibility (flat list per country)
# Para México: son las regiones (que contienen múltiples hubs)
# Para Brasil/Argentina/Chile: son las ciudades directamente
HUBS = {
    "México": [
        "Ciudad de México",
        "Monterrey",
        "Guadalajara",
        "Puebla",
        "Querétaro",
        "Cuernavaca",
        "León",
        "San Luis Potosí",
    ],
    "Brasil": ["Brasil"],  # Solo una región = país
    "Argentina": ["Argentina"],  # Solo una región = país
    "Chile": ["Chile"],  # Solo una región = país
}

# Agents per hub (sample) - Increased for better demo
AGENTS_PER_HUB = 25

# Agents per region (when filtering by region instead of specific hub)
AGENTS_PER_REGION = 40

# Vehicle segments
VEHICLE_SEGMENTS = ["Sedán", "SUV", "Pickup", "Hatchback", "Premium"]

# Operation types
OPERATION_TYPES = {
    "all": "Todas las Operaciones",
    "sales": "Ventas (Outbound)",
    "purchases": "Compras (Inbound)",
    "tradein": "Trade-in",
}

# Period options
PERIOD_OPTIONS = {
    "Últimos 7 días": 7,
    "Últimos 30 días": 30,
    "Últimos 90 días": 90,
    "YTD": 365,
}

# KPI thresholds
THRESHOLDS = {
    "conversion_good": 0.25,
    "conversion_warning": 0.15,
    "nps_good": 70,
    "nps_warning": 50,
    "aging_critical": 60,
    "aging_warning": 45,
    "noshow_warning": 0.20,
    "noshow_critical": 0.30,
}

# Incentive goals
INCENTIVE_GOALS = [
    {
        "name": "🏆 Conversor Elite",
        "description": "Conversión > 30%",
        "metric": "conversion",
        "threshold": 0.30,
        "points": 100,
    },
    {
        "name": "⭐ NPS Maestro",
        "description": "NPS > 80",
        "metric": "nps",
        "threshold": 80,
        "points": 80,
    },
    {
        "name": "🎯 Cita Perfecta",
        "description": "No-show < 10%",
        "metric": "noshow",
        "threshold": 0.10,
        "points": 60,
        "inverse": True,  # Lower is better
    },
    {
        "name": "🚀 Cerrador",
        "description": "10+ ventas en el periodo",
        "metric": "sales",
        "threshold": 10,
        "points": 90,
    },
]

# Colors - Kavak Brand Identity
COLORS = {
    "primary": "#0B4FD6",  # Kavak Blue (primary action color)
    "primary_dark": "#003DAC",  # Darker Kavak Blue
    "success": "#00C48C",  # Green for positive metrics
    "warning": "#FFA726",  # Orange for warnings
    "danger": "#FF4757",  # Red for critical alerts
    "info": "#42A5F5",  # Light blue for info
    "background": "#F8F9FA",  # Light gray background
    "text_primary": "#1A1A1A",  # Almost black for main text
    "text_secondary": "#6B7280",  # Gray for secondary text
    "border": "#E5E7EB",  # Light gray for borders
    "white": "#FFFFFF",
}
