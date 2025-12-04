# 🚀 Guía de Inicio Rápido - Kavak Performance App

## ⚡ Inicio Rápido (3 pasos)

### 1. Navegar al directorio
```bash
cd /Users/martingiminezcendoya/repos/data-lake-house/kavak_performance_app
```

### 2. (Opcional) Activar entorno virtual
```bash
# Si tienes un entorno virtual:
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate     # Windows
```

### 3. Ejecutar la aplicación
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## 📸 Vista Previa de la Aplicación

### Tab 1: Executive Dashboard (CEO)

```
┌─────────────────────────────────────────────────────────────┐
│ 📊 Executive Dashboard                                       │
│ Visión macro del negocio por país / hub                     │
├─────────────────────────────────────────────────────────────┤
│ Filtros: [País ▼] [Hub ▼] [Periodo ▼] [🔄 Actualizar]      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 💰 FINANCIEROS                                              │
│ ┌──────────────┬──────────────┬──────────────┐            │
│ │ Ventas       │ Revenue      │ Ticket       │            │
│ │ Totales      │ Total        │ Promedio     │            │
│ │ 2,453        │ $48.2M       │ $19,650      │            │
│ └──────────────┴──────────────┴──────────────┘            │
│                                                              │
│ 📈 SALUD DE LA DEMANDA                                      │
│ ┌────────┬────────┬────────┬────────┐                      │
│ │ Leads  │ Conv.  │ CPL    │ CPV    │                      │
│ │ 13,245 │ 18.5%  │ $87    │ $468   │                      │
│ └────────┴────────┴────────┴────────┘                      │
│                                                              │
│ 😊 EXPERIENCIA DE CLIENTE                                   │
│ ┌──────────┬──────────┬──────────┐                         │
│ │ NPS      │ CSAT     │ Detract. │                         │
│ │ 68       │ 82       │ 16%      │                         │
│ └──────────┴──────────┴──────────┘                         │
│                                                              │
│ 📊 TENDENCIAS Y ANÁLISIS                                    │
│ ┌─────────────────────┬─────────────────────┐              │
│ │ Ventas (Semanal)    │ Conversión (%)      │              │
│ │ [Gráfico línea]     │ [Gráfico línea]     │              │
│ └─────────────────────┴─────────────────────┘              │
│ ┌─────────────────────┬─────────────────────┐              │
│ │ NPS (Semanal)       │ Funnel Agregado     │              │
│ │ [Gráfico línea]     │ [Gráfico embudo]    │              │
│ └─────────────────────┴─────────────────────┘              │
│                                                              │
│ 🚨 ALERTAS ESTRATÉGICAS                                     │
│ ┌──────────────────────────────────────────┐               │
│ │ 🚨 Caída en conversión - CDMX Sur        │               │
│ │    Conversión bajó 15% vs semana ant.   │               │
│ └──────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

### Tab 2: Team Performance (City Manager)

```
┌─────────────────────────────────────────────────────────────┐
│ 👥 Team Performance (City Manager)                          │
│ Gestión de equipo, comparación de agentes y flota          │
├─────────────────────────────────────────────────────────────┤
│ Filtros: [Hub ▼] [Periodo ▼] [🔄]                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 📍 PERFORMANCE DE CDMX NORTE                                │
│ ┌────────┬────────┬────────┬────────┐                      │
│ │ Ventas │ Conv.  │ NPS    │ Leads  │                      │
│ │ 245    │ 22.3%  │ 71     │ 1,098  │                      │
│ └────────┴────────┴────────┴────────┘                      │
│                                                              │
│ 📊 COMPARACIÓN VS PROMEDIO PAÍS                             │
│ Ventas: 245 (+12.5% vs promedio)                           │
│ Conversión: 22.3% (+3.8% vs promedio)                      │
│ 🏆 Ranking: #3 de 12 hubs en México                        │
│                                                              │
│ 👤 RANKING DE AGENTES                                       │
│ ┌────────────────┬───────┬───────┬─────┬──────────┐        │
│ │ Agente         │Ventas │ CVR % │ NPS │ Estado   │        │
│ ├────────────────┼───────┼───────┼─────┼──────────┤        │
│ │ Juan García    │  42   │ 28.1% │ 83  │🔥 Excelen│        │
│ │ María López    │  38   │ 25.4% │ 78  │⭐ Bueno  │        │
│ │ Carlos Pérez   │  32   │ 21.7% │ 68  │⭐ Bueno  │        │
│ │ Ana Martínez   │  28   │ 18.2% │ 65  │⚠️ Atención│       │
│ └────────────────┴───────┴───────┴─────┴──────────┘        │
│                                                              │
│ 🏆 MÓDULO DE INCENTIVOS                                     │
│ Top 3: 1) Juan García (270 pts)                            │
│        2) María López (180 pts)                             │
│        3) Carlos Pérez (100 pts)                            │
│                                                              │
│ 🚗 DIMENSIONAMIENTO DE FLOTA                                │
│ Inventario Total: 85 | Disponible: 62                      │
│ Demanda Estimada: 75 autos/mes                             │
│ ✅ Nivel de inventario saludable                            │
│                                                              │
│ 🔀 FUNNEL DEL HUB                                           │
│ [Gráfico embudo] + Tasas de conversión                     │
│                                                              │
│ 🚨 ALERTAS OPERATIVAS                                       │
│ ⚠️ 2 agentes con baja conversión                            │
│ ⚠️ 3 agentes con alta tasa de no-show                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎮 Casos de Uso

### Para el CEO:
1. **Vista General del Negocio**
   - Seleccionar "Todos" en País y Hub
   - Ver KPIs consolidados de todos los países
   - Analizar tendencias semanales

2. **Deep Dive por País**
   - Seleccionar país específico (ej. México)
   - Comparar hubs dentro del país
   - Identificar hubs con mejor performance

3. **Análisis de Hub Específico**
   - Seleccionar país y hub específico
   - Ver métricas detalladas del hub
   - Revisar alertas estratégicas

### Para el City Manager:
1. **Performance del Equipo**
   - Seleccionar tu hub
   - Ver KPIs agregados del hub
   - Comparar vs promedio del país

2. **Gestión de Agentes**
   - Revisar ranking de agentes
   - Identificar top performers (🔥)
   - Detectar agentes que necesitan atención (⚠️)

3. **Competencia e Incentivos**
   - Ver ranking de puntos
   - Identificar quién alcanzó objetivos
   - Motivar al equipo con gamificación

4. **Dimensionamiento de Inventario**
   - Verificar nivel de inventario
   - Identificar autos envejecidos
   - Ajustar compras según demanda

5. **Optimización del Funnel**
   - Identificar estrangulamientos
   - Enfocar esfuerzos en etapa débil
   - Mejorar conversión total

---

## 🔧 Personalización

### Cambiar Umbrales de KPIs

Editar `config.py`:

```python
THRESHOLDS = {
    "conversion_good": 0.25,      # 25% = Excelente
    "conversion_warning": 0.15,   # 15% = Atención
    "nps_good": 70,               # NPS >= 70 = Bueno
    "nps_warning": 50,            # NPS < 50 = Atención
    # ...
}
```

### Agregar Nuevos Objetivos de Incentivos

Editar `config.py`:

```python
INCENTIVE_GOALS = [
    {
        "name": "🎯 Tu Objetivo",
        "description": "Descripción",
        "metric": "sales",          # Métrica a evaluar
        "threshold": 15,            # Umbral
        "points": 120,              # Puntos a otorgar
        "inverse": False            # True si menor es mejor
    },
    # ...
]
```

### Cambiar Colores

Editar `config.py`:

```python
COLORS = {
    "primary": "#FF6B35",    # Naranja Kavak
    "success": "#4CAF50",    # Verde
    "warning": "#FFA726",    # Amarillo
    "danger": "#EF5350",     # Rojo
    "info": "#42A5F5"        # Azul
}
```

---

## 🔌 Conectar a Datos Reales

### Opción 1: Snowflake

Editar `utils/data_generator.py`:

```python
import snowflake.connector
import pandas as pd

def generate_sample_data():
    # Conexión a Snowflake
    conn = snowflake.connector.connect(
        user='TU_USUARIO',
        password='TU_PASSWORD',
        account='TU_CUENTA',
        warehouse='TU_WAREHOUSE',
        database='TU_DATABASE',
        schema='TU_SCHEMA'
    )

    # Queries
    daily_metrics = pd.read_sql("""
        SELECT
            date,
            country,
            hub,
            leads,
            appointments,
            reservations,
            sales,
            -- ... más columnas
        FROM daily_metrics
        WHERE date >= DATEADD(day, -90, CURRENT_DATE())
    """, conn)

    # ... más queries

    conn.close()

    return {
        'daily_metrics': daily_metrics,
        # ...
    }
```

### Opción 2: Databricks

```python
from databricks import sql
import pandas as pd

def generate_sample_data():
    connection = sql.connect(
        server_hostname='<server-hostname>',
        http_path='<http-path>',
        access_token='<access-token>'
    )

    cursor = connection.cursor()

    daily_metrics = pd.read_sql("SELECT * FROM daily_metrics", connection)

    # ... más queries

    connection.close()

    return {
        'daily_metrics': daily_metrics,
        # ...
    }
```

### Opción 3: CSV Local (Testing)

```python
import pandas as pd

def generate_sample_data():
    return {
        'daily_metrics': pd.read_csv('data/daily_metrics.csv'),
        'agent_performance': pd.read_csv('data/agent_performance.csv'),
        'inventory': pd.read_csv('data/inventory.csv'),
        'funnel': pd.read_csv('data/funnel.csv'),
        'alerts': pd.read_csv('data/alerts.csv')
    }
```

---

## 🐛 Troubleshooting

### Error: "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"
```bash
# Cambiar puerto:
streamlit run app.py --server.port 8502
```

### App muy lenta
```bash
# Agregar caché en data_generator.py:
import streamlit as st

@st.cache_data(ttl=3600)  # Cache por 1 hora
def generate_sample_data():
    # ... código existente
```

### Datos no se actualizan
```bash
# Limpiar caché:
streamlit cache clear
```

---

## 📞 Soporte

Para preguntas o problemas:
- **Email:** data-analytics@kavak.com
- **Slack:** #kavak-performance-app
- **Documentación:** README.md

---

## 🎯 Próximos Pasos Recomendados

1. ✅ **Probar la app** con datos de ejemplo
2. 🔌 **Conectar** a Snowflake/Databricks
3. 🎨 **Personalizar** colores y umbrales
4. 🚨 **Implementar** alertas dinámicas
5. 👤 **Agregar** autenticación por rol
6. 📱 **Agregar** vista Kavako (agente individual)
7. 📊 **Integrar** con Tableau/PowerBI
8. 🤖 **Implementar** ML para forecasting

---

**¡Listo para empezar!** 🚀

```bash
streamlit run app.py
```
