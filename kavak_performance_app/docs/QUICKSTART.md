# 🚀 Quick Start Guide - Kavak Performance App

## Inicio Rápido (5 minutos)

### Opción 1: Usando el script automático (recomendado)

```bash
cd kavak_performance_app
./run.sh
```

El script automáticamente:
- Crea el entorno virtual (si no existe)
- Instala las dependencias
- Ejecuta la aplicación

### Opción 2: Instalación manual

1. **Crear entorno virtual:**
```bash
cd kavak_performance_app
python3 -m venv venv
```

2. **Activar entorno virtual:**

En macOS/Linux:
```bash
source venv/bin/activate
```

En Windows:
```cmd
venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
streamlit run app.py
```

## 🎯 Primeros Pasos

Una vez que la aplicación esté corriendo:

1. **Navegación:**
   - La app se abre en `http://localhost:8501`
   - Usa las tabs superiores para cambiar entre vistas

2. **Vista CEO:**
   - Selecciona país, hub y periodo
   - Explora los KPIs financieros, de demanda, y experiencia de cliente
   - Revisa las tendencias semanales
   - Consulta las alertas estratégicas

3. **Vista City Manager:**
   - Selecciona tu hub
   - Revisa la performance del hub vs promedio país
   - Analiza el ranking de agentes
   - Consulta el módulo de incentivos
   - Verifica el dimensionamiento de flota
   - Revisa el funnel y alertas operativas

## 📊 Datos de Ejemplo

La aplicación incluye datos sintéticos generados automáticamente:

- **90 días de histórico** de métricas diarias
- **4 países**: México, Brasil, Argentina, Chile
- **Múltiples hubs** por país
- **~8 agentes por hub** con métricas de performance
- **Inventario por segmento** (Sedán, SUV, Pickup, etc.)
- **Alertas** de ejemplo

## 🔧 Configuración

### Personalizar países y hubs

Edita `config.py`:

```python
COUNTRIES = ["México", "Brasil", "Argentina", "Chile"]

HUBS = {
    "México": ["CDMX Norte", "CDMX Sur", "Guadalajara", ...],
    # ...
}
```

### Personalizar umbrales de KPIs

Edita `config.py`:

```python
THRESHOLDS = {
    "conversion_good": 0.25,      # 25%
    "conversion_warning": 0.15,   # 15%
    "nps_good": 70,
    "nps_warning": 50,
    # ...
}
```

### Personalizar objetivos de incentivos

Edita `config.py` en la lista `INCENTIVE_GOALS`.

## 🔌 Conectar a Datos Reales

### Snowflake

1. Instalar conector:
```bash
pip install snowflake-connector-python
```

2. Editar `utils/data_generator.py`:

```python
import snowflake.connector

def generate_sample_data():
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse='YOUR_WAREHOUSE',
        database='YOUR_DATABASE',
        schema='YOUR_SCHEMA'
    )

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
        FROM daily_metrics_table
        WHERE date >= DATEADD(day, -90, CURRENT_DATE())
    """, conn)

    # Similar para agent_performance, inventory, funnel

    return {
        'daily_metrics': daily_metrics,
        'agent_performance': agent_performance,
        'inventory': inventory,
        'funnel': funnel,
        'alerts': alerts
    }
```

### Variables de entorno

Crea un archivo `.env`:

```bash
SNOWFLAKE_USER=tu_usuario
SNOWFLAKE_PASSWORD=tu_password
SNOWFLAKE_ACCOUNT=tu_cuenta
```

Instala python-dotenv:
```bash
pip install python-dotenv
```

Carga en `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 🎨 Personalización de UI

### Cambiar colores

Edita `config.py`:

```python
COLORS = {
    "primary": "#FF6B35",      # Color principal
    "success": "#4CAF50",      # Verde éxito
    "warning": "#FFA726",      # Naranja alerta
    "danger": "#EF5350",       # Rojo peligro
    "info": "#42A5F5"          # Azul información
}
```

### Personalizar estilos CSS

Edita `utils/components.py` en la función `apply_custom_styles()`.

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
streamlit run app.py --server.port 8502
```

### Error de datos vacíos
- Verifica que los filtros no sean demasiado restrictivos
- Revisa que `data_generator.py` esté generando datos correctamente

### La app no se actualiza
- Presiona el botón "🔄 Actualizar" en los filtros
- O usa `Ctrl+R` / `Cmd+R` en el navegador
- O en la terminal presiona `R` para recargar

## 📚 Recursos Adicionales

- [Documentación de Streamlit](https://docs.streamlit.io)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)

## 💡 Tips

1. **Performance**: Si la app es lenta, usa `@st.cache_data` para cachear datos
2. **Testing**: Usa diferentes combinaciones de filtros para probar la app
3. **Deployment**: Considera usar Streamlit Cloud para deployment
4. **Mobile**: La app es responsive y funciona en tablets

## 🆘 Soporte

Para preguntas o problemas:
1. Revisa este guide y el README.md
2. Contacta al equipo de Data & Analytics
3. Crea un issue en el repositorio interno

---

¡Disfruta explorando los datos de Kavak! 🚗✨
