# 🏗️ Architecture - Kavak Performance App

## Visión General

La aplicación está construida con una arquitectura modular y escalable usando Streamlit como framework principal.

## 📐 Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                         Usuario                              │
│                    (CEO / City Manager)                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   app.py (Main App)                          │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  Tab 1: CEO  │  │  Tab 2: CM   │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Views      │  │    Utils     │  │   Config     │
│              │  │              │  │              │
│ - CEO        │  │ - Components │  │ - Constants  │
│ - CityMgr    │  │ - DataGen    │  │ - Thresholds │
└──────────────┘  └──────────────┘  └──────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  Data Sources │
                  │               │
                  │ - Snowflake   │
                  │ - Databricks  │
                  │ - APIs        │
                  └───────────────┘
```

## 📁 Estructura de Archivos

```
kavak_performance_app/
│
├── app.py                          # 🎯 Entry point, navegación principal
│   └── Tabs: CEO / City Manager
│
├── config.py                       # ⚙️ Configuración global
│   ├── COUNTRIES
│   ├── HUBS
│   ├── THRESHOLDS
│   ├── INCENTIVE_GOALS
│   └── COLORS
│
├── views/                          # 📊 Vistas principales
│   ├── ceo_dashboard.py
│   │   ├── render_ceo_dashboard()
│   │   ├── render_filters()
│   │   ├── render_kpi_section()
│   │   ├── render_charts_section()
│   │   └── render_alerts_section()
│   │
│   └── city_manager_dashboard.py
│       ├── render_city_manager_dashboard()
│       ├── render_hub_overview()
│       ├── render_hub_comparison()
│       ├── render_agent_ranking()
│       ├── render_incentives_module()
│       ├── render_fleet_dimensioning()
│       ├── render_hub_funnel()
│       └── render_operational_alerts()
│
└── utils/                          # 🛠️ Utilidades
    ├── components.py               # Componentes UI reutilizables
    │   ├── render_kpi_card()
    │   ├── render_kpi_grid()
    │   ├── render_alert_box()
    │   ├── render_funnel_chart()
    │   ├── render_trend_chart()
    │   ├── render_bar_chart()
    │   └── apply_custom_styles()
    │
    └── data_generator.py           # Generación de datos
        ├── generate_sample_data()
        ├── generate_daily_metrics()
        ├── generate_agent_performance()
        ├── generate_inventory_data()
        ├── generate_funnel_data()
        └── generate_alerts()
```

## 🔄 Flujo de Datos

### 1. Inicialización de la App

```python
# app.py
st.set_page_config(...)
apply_custom_styles()

# Initialize session state with data
if 'data' not in st.session_state:
    st.session_state.data = generate_sample_data()
```

### 2. Generación de Datos

```python
# utils/data_generator.py
def generate_sample_data():
    return {
        'daily_metrics': DataFrame(...),      # Métricas por día/hub
        'agent_performance': DataFrame(...),  # Performance por agente
        'inventory': DataFrame(...),          # Inventario por segmento
        'funnel': DataFrame(...),             # Datos de funnel
        'alerts': DataFrame(...)              # Alertas activas
    }
```

### 3. Rendering de Vistas

```python
# views/ceo_dashboard.py
def render_ceo_dashboard(data):
    1. render_filters()              # Filtros interactivos
    2. filter_data()                 # Aplicar filtros
    3. render_kpi_section()          # KPIs agrupados
    4. render_charts_section()       # Gráficos
    5. render_alerts_section()       # Alertas
```

### 4. Interactividad

```
Usuario selecciona filtros
    ↓
Streamlit actualiza session_state
    ↓
Vista re-renderiza con datos filtrados
    ↓
Componentes UI muestran resultados
```

## 🧩 Componentes Principales

### 1. Main App (`app.py`)

**Responsabilidad:** Punto de entrada, navegación entre vistas

**Funciones clave:**
- Configuración de página
- Gestión de session state
- Navegación por tabs
- Header y footer

### 2. Config (`config.py`)

**Responsabilidad:** Configuración centralizada

**Contiene:**
- Listas de países y hubs
- Umbrales de KPIs
- Objetivos de incentivos
- Colores y estilos
- Opciones de periodo

### 3. Views (Dashboards)

#### CEO Dashboard
**Responsabilidad:** Vista ejecutiva estratégica

**Secciones:**
- Filtros (país, hub, periodo)
- 5 grupos de KPIs (financieros, demanda, CX, ops, riesgo)
- Tendencias semanales (ventas, conversión, NPS)
- Funnel agregado
- Comparación por hub
- Alertas estratégicas

#### City Manager Dashboard
**Responsabilidad:** Gestión táctica del equipo

**Secciones:**
- Filtros (hub, periodo)
- KPIs del hub
- Comparación vs país
- Ranking de agentes con estados
- Módulo de incentivos/gamificación
- Dimensionamiento de flota
- Funnel del hub
- Alertas operativas

### 4. Utils

#### Components (`components.py`)
**Responsabilidad:** Componentes UI reutilizables

**Componentes:**
- `render_kpi_card()`: Métrica individual
- `render_kpi_grid()`: Grid de múltiples métricas
- `render_alert_box()`: Caja de alerta con styling
- `render_funnel_chart()`: Gráfico de funnel
- `render_trend_chart()`: Gráfico de línea/tendencia
- `render_bar_chart()`: Gráfico de barras
- `apply_custom_styles()`: CSS customizado

#### Data Generator (`data_generator.py`)
**Responsabilidad:** Generación de datos sintéticos

**Funciones:**
- `generate_daily_metrics()`: 90 días × países × hubs
- `generate_agent_performance()`: ~8 agentes por hub
- `generate_inventory_data()`: Inventario por segmento
- `generate_funnel_data()`: Métricas de funnel
- `generate_alerts()`: Alertas de ejemplo

## 🎨 Sistema de Diseño

### Colores

```python
PRIMARY = "#FF6B35"    # Naranja Kavak (acciones, botones)
SUCCESS = "#4CAF50"    # Verde (métricas positivas)
WARNING = "#FFA726"    # Naranja (alertas)
DANGER = "#EF5350"     # Rojo (crítico)
INFO = "#42A5F5"       # Azul (información)
```

### Tipografía

- Headers: Default Streamlit (Sans-serif)
- Métricas: Bold, tamaño grande
- Texto: Regular, tamaño medio

### Layout

- **Grid de KPIs:** 3-4 columnas
- **Charts:** 2 columnas para comparación
- **Tablas:** Full width con height=400px
- **Alerts:** 2 columnas

## 🔐 Manejo de Estado

### Session State

```python
st.session_state = {
    'data': {                    # Datos principales
        'daily_metrics': DataFrame,
        'agent_performance': DataFrame,
        'inventory': DataFrame,
        'funnel': DataFrame,
        'alerts': DataFrame
    },
    'ceo_country': str,          # Filtro CEO: país
    'ceo_hub': str,              # Filtro CEO: hub
    'ceo_period': str,           # Filtro CEO: periodo
    'cm_hub': str,               # Filtro CM: hub
    'cm_period': str             # Filtro CM: periodo
}
```

## 📊 Modelo de Datos

### Daily Metrics
```python
{
    'date': datetime,
    'country': str,
    'hub': str,
    'leads': int,
    'appointments': int,
    'reservations': int,
    'sales': int,
    'cancellations': int,
    'noshow': int,
    'nps': float,
    'csat': float,
    'revenue': float,
    'ticket_avg': float,
    'cost_per_lead': float,
    'sla_lead_to_sale': float
}
```

### Agent Performance
```python
{
    'agent_id': int,
    'agent_name': str,
    'country': str,
    'hub': str,
    'leads': int,
    'appointments': int,
    'reservations': int,
    'sales': int,
    'conversion': float,
    'nps': float,
    'csat': float,
    'noshow': float,
    'avg_response_time': float,
    'revenue': float
}
```

### Inventory
```python
{
    'country': str,
    'hub': str,
    'segment': str,  # Sedán, SUV, etc.
    'total_inventory': int,
    'available': int,
    'reserved': int,
    'vip': int,
    'aging_0_30': int,
    'aging_30_60': int,
    'aging_60_plus': int,
    'avg_days_in_inventory': float
}
```

## 🚀 Performance & Optimización

### Estrategias Actuales

1. **Session State Caching:** Datos cargados una vez por sesión
2. **Filtrado Eficiente:** Uso de pandas queries optimizadas
3. **Lazy Loading:** Componentes se renderizan solo cuando están visibles

### Mejoras Futuras

```python
# Cache de datos con TTL
@st.cache_data(ttl=600)  # 10 minutos
def load_data():
    return fetch_from_database()

# Cache de transformaciones
@st.cache_data
def compute_aggregations(df):
    return df.groupby(...).agg(...)

# Paginación para tablas grandes
@st.cache_data
def paginate_dataframe(df, page_size=50):
    return df.head(page_size)
```

## 🔌 Integración con Fuentes de Datos

### Patrón Adapter

```python
# utils/data_sources.py (futuro)

class DataSource(ABC):
    @abstractmethod
    def fetch_daily_metrics(self, start_date, end_date):
        pass

class SnowflakeDataSource(DataSource):
    def fetch_daily_metrics(self, start_date, end_date):
        # Implementación Snowflake
        pass

class DatabricksDataSource(DataSource):
    def fetch_daily_metrics(self, start_date, end_date):
        # Implementación Databricks
        pass

# En data_generator.py
def generate_sample_data():
    source = get_data_source()  # Factory pattern
    return source.fetch_all_data()
```

## 🧪 Testing Strategy (Futuro)

```python
# tests/test_components.py
def test_render_kpi_card():
    result = render_kpi_card("Test", 100, "+10%")
    assert result is not None

# tests/test_data_generator.py
def test_generate_daily_metrics():
    data = generate_daily_metrics(date_range)
    assert len(data) > 0
    assert 'date' in data.columns
    assert 'sales' in data.columns
```

## 📈 Roadmap Técnico

### Fase 1: Foundation ✅ (Actual)
- [x] Estructura modular
- [x] Vista CEO
- [x] Vista City Manager
- [x] Datos sintéticos
- [x] Componentes reutilizables

### Fase 2: Data Integration
- [ ] Conexión a Snowflake
- [ ] Conexión a Databricks
- [ ] Cache distribuido (Redis)
- [ ] API REST backend

### Fase 3: Advanced Features
- [ ] Vista Kavako (agente)
- [ ] Deep dive cliente
- [ ] Predicciones ML
- [ ] Exportación de reportes

### Fase 4: Scale & Performance
- [ ] Multi-threading
- [ ] Pre-computación de agregaciones
- [ ] CDN para assets
- [ ] Load balancing

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Framework | Streamlit | 1.28+ |
| Data Processing | Pandas | 2.0+ |
| Visualización | Plotly | 5.17+ |
| Computación | NumPy | 1.24+ |
| Backend (futuro) | FastAPI | - |
| Database | Snowflake/Databricks | - |
| Cache (futuro) | Redis | - |

## 📚 Referencias

- [Streamlit Docs](https://docs.streamlit.io)
- [Plotly Python](https://plotly.com/python/)
- [Pandas User Guide](https://pandas.pydata.org/docs/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

**Mantenido por:** Data & Analytics Team
**Última actualización:** Noviembre 2025
