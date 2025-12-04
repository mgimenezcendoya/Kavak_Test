# Kavak Performance App

Aplicación interna de performance y operación para Kavak que permite dar visibilidad ejecutiva al CEO y al leadership, además de permitir a los City Managers gestionar y comparar la performance de su equipo y flota.

## 🎯 Objetivo

Construir una aplicación que permita:
- Dar visibilidad ejecutiva al CEO y al leadership (visión país / hub)
- Permitir a los City Managers gestionar y comparar la performance de su equipo
- Gestionar el dimensionamiento de flota y operaciones

## 🚀 Características

### 📊 Vista CEO (Executive Dashboard)

**Filtros:**
- País (México, Brasil, Argentina, Chile)
- Hub (específico o todos)
- Periodo (últimos 7, 30, 90 días, YTD)

**KPIs Estratégicos:**
1. **Financieros**: Ventas totales, Revenue, Ticket promedio
2. **Salud de la demanda**: Leads totales, Conversión, Costo por Lead/Venta
3. **Experiencia de cliente**: NPS, CSAT, % Detractores
4. **Operación/Eficiencia**: SLA Lead→Venta, Cancelaciones
5. **Tendencias**: Series temporales de ventas, conversión, NPS
6. **Funnel agregado**: Lead → Cita → Reserva → Venta
7. **Alertas estratégicas**: Caídas en conversión, inventario crítico, NPS

### 👥 Vista City Manager (Team Performance)

**Filtros:**
- Hub (hub actual del manager)
- Periodo (últimos 7, 30 días, etc.)

**Funcionalidades:**
1. **Performance del Hub**: KPIs agregados del hub
2. **Comparación vs Promedio País**: Métricas del hub vs promedio
3. **Ranking de Agentes**: Tabla comparativa con estados (🔥 Excelente, ⭐ Bueno, ⚠️ Atención)
4. **Módulo de Incentivos**: Sistema de gamificación con objetivos y puntos
5. **Dimensionamiento de Flota**: Inventario actual, crítico, y demanda estimada
6. **Funnel del Hub**: Análisis detallado del funnel de conversión
7. **Alertas Operativas**: Agentes con baja conversión, inventario envejecido, no-show alto

### 🤖 Celeste Copilot (NUEVO)

**Asistente inteligente para agentes con:**
- **Chat interactivo**: Consultas en tiempo real desde el sidebar
- **Acciones rápidas**:
  - 🚗 Alternativas de vehículos similares
  - 💬 Tips de cierre personalizados
  - 📊 Análisis del perfil del cliente
  - 💰 Cálculos de financiamiento
- **Contexto automático**: Respuestas basadas en los datos del cliente activo
- **Insights proactivos**: Card de "Celeste dice" con recomendaciones

## 📁 Estructura del Proyecto

```
kavak_performance_app/
├── app.py                          # Aplicación principal
├── config.py                       # Configuración y constantes
├── requirements.txt                # Dependencias
├── README.md                       # Este archivo
├── docs/                           # 📚 Documentación completa
│   ├── README.md                   # Índice de documentación
│   ├── AUTH_SYSTEM.md              # Sistema de autenticación
│   ├── KAVAKO_VIEW.md              # Vista del agente
│   ├── ARCHITECTURE.md             # Arquitectura del sistema
│   └── ... (más docs)              # Otros documentos
├── utils/
│   ├── __init__.py
│   ├── auth.py                     # Sistema de autenticación
│   ├── components.py               # Componentes UI reutilizables
│   ├── data_generator.py           # Generador de datos de ejemplo
│   └── alert_detector.py           # Detector de alertas
└── views/
    ├── __init__.py
    ├── login.py                    # Vista de login
    ├── ceo_dashboard.py            # Vista CEO
    ├── city_manager_dashboard.py  # Vista City Manager
    ├── kavako_dashboard.py         # Vista Kavako (agente)
    ├── agent_profile_detail.py     # Perfil de agente
    └── customer_profile.py         # Perfil de cliente
```

## 📚 Documentación

Para documentación detallada sobre features específicas, arquitectura y guías de uso, consulta la carpeta **[`docs/`](./docs/)**

**Documentos destacados:**
- 🔐 **[Sistema de Autenticación](./docs/AUTH_SYSTEM.md)** - Roles, permisos y usuarios
- 👤 **[Vista Kavako](./docs/KAVAKO_VIEW.md)** - Dashboard del agente
- 🏗️ **[Arquitectura](./docs/ARCHITECTURE.md)** - Estructura completa del sistema
- 🚀 **[Quick Start](./docs/QUICKSTART.md)** - Guía de inicio rápido
- ✨ **[Features Summary](./docs/FEATURES_SUMMARY.md)** - Todas las funcionalidades

Ver **[índice completo de documentación](./docs/README.md)**.

## 🛠️ Instalación

### Requisitos previos
- Python 3.8 o superior
- pip

### Pasos de instalación

1. Clonar o navegar al directorio del proyecto:
```bash
cd kavak_performance_app
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

Para ejecutar la aplicación:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📊 Datos

Actualmente la aplicación utiliza datos de ejemplo generados automáticamente. Los datos incluyen:

- **daily_metrics**: Métricas diarias por país/hub (últimos 90 días)
- **agent_performance**: Performance por agente
- **inventory**: Inventario por hub y segmento
- **funnel**: Datos del funnel de conversión
- **alerts**: Alertas del sistema

### Conexión a datos reales

Para conectar a fuentes de datos reales (Snowflake, Databricks, etc.), modifica el archivo `utils/data_generator.py` y reemplaza la función `generate_sample_data()` con consultas a tu base de datos.

Ejemplo con Snowflake:
```python
import snowflake.connector

def generate_sample_data():
    conn = snowflake.connector.connect(
        user='TU_USUARIO',
        password='TU_PASSWORD',
        account='TU_CUENTA',
        warehouse='TU_WAREHOUSE',
        database='TU_DATABASE',
        schema='TU_SCHEMA'
    )

    # Ejecutar queries
    daily_metrics = pd.read_sql("SELECT * FROM daily_metrics", conn)
    # ... más queries

    return {
        'daily_metrics': daily_metrics,
        # ... resto de datos
    }
```

## 🎨 Personalización

### Colores y estilos
Los colores principales se definen en `config.py`:
```python
COLORS = {
    "primary": "#FF6B35",
    "success": "#4CAF50",
    "warning": "#FFA726",
    "danger": "#EF5350",
    "info": "#42A5F5"
}
```

### Umbrales de KPIs
Los umbrales para alertas se configuran en `config.py`:
```python
THRESHOLDS = {
    "conversion_good": 0.25,
    "conversion_warning": 0.15,
    "nps_good": 70,
    "nps_warning": 50,
    # ...
}
```

### Objetivos de incentivos
Los objetivos de gamificación se definen en `config.py` en la lista `INCENTIVE_GOALS`.

## 🔮 Roadmap / Futuras Mejoras

### ✅ Implementado
- [x] Vista Kavako (agente individual)
- [x] Sistema de autenticación con roles
- [x] Deep dive de cliente
- [x] Drill-down completo (Hub → Agente → Cliente)
- [x] Comparación entre hubs
- [x] Optimización de agentes (dealership approach)
- [x] Sistema de gamificación e incentivos
- [x] Alertas dinámicas estratégicas y operativas

### 🚧 En Desarrollo / Próximo
- [ ] Integración Google SSO
- [ ] Conexión a datos reales (Snowflake/Databricks)
- [ ] Exportación de reportes en PDF/Excel
- [ ] Notificaciones por email/Slack

### 💡 Futuro
- [ ] Módulo de inventario avanzado
- [ ] Análisis predictivo con ML
- [ ] Integración con Tableau/PowerBI
- [ ] Dashboard de análisis de churn
- [ ] Módulo de forecasting de demanda

## 🤝 Contribución

Para contribuir al proyecto:
1. Crea una rama feature: `git checkout -b feature/nueva-funcionalidad`
2. Haz tus cambios y commits: `git commit -am 'Agregar nueva funcionalidad'`
3. Push a la rama: `git push origin feature/nueva-funcionalidad`
4. Crea un Pull Request

## 📄 Licencia

Uso interno de Kavak.

## 📞 Soporte

Para preguntas o soporte, contacta al equipo de Data & Analytics.

---

**Última actualización**: Noviembre 2025
**Versión**: 4.0.0 (MVP con autenticación y drill-down completo)
**Features:** Login, 4 roles, 3 vistas principales, drill-down completo, comparación de hubs
