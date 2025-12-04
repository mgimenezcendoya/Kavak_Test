# 👤 Vista Kavako (Agente) - Dashboard Personal

## ✨ Nueva Vista Implementada

Se ha agregado un **dashboard personal completo** para que cada agente (Kavako) pueda gestionar su día a día, ver su cartera activa, agenda de citas, score personal y métricas de performance.

---

## 📍 Ubicación

**Tab:** "👤 Mi Dashboard (Kavako/Agente)" (tercer tab)
**Usuario:** Cada agente individual
**Login:** Simulado mediante selector en sidebar (en producción sería automático)

---

## 🎯 Objetivo

Dar a cada agente una vista **personal, clara y accionable** de:
- Su cartera de leads activos
- Sus citas próximas
- Su score y ranking
- Sus métricas de performance
- Sus objetivos e incentivos

---

## 📊 Componentes del Dashboard

### 1. Resumen Personal (Header)

**Incluye:**
- 👤 **Nombre del agente** y ubicación (hub, país)
- 🏆 **Ranking en el hub** (#X de Y agentes)
  - Si es #1: Badge especial "Líder del hub!"
- 🎯 **Mi Conversión** (% con comparación vs hub)
- 💼 **Ventas del Periodo** (con delta vs promedio)

**Ejemplo:**
```
┌────────────────────────────────────────────────────────────┐
│ 👤 Juan García            🏆 Ranking: #2 de 8             │
│ 📍 CDMX Norte, México     🎯 Mi Conv: 22.3% (+3.8% vs hub) │
│                           💼 Ventas: 42 (+12 vs promedio) │
└────────────────────────────────────────────────────────────┘
```

---

### 2. Cartera Activa (📋 Mi Cartera Activa)

**Métricas:**
- Leads en seguimiento (backlog)
- Oportunidades totales
- % Aprovechamiento

**Tabla de Leads Activos (Top 5 Prioritarios):**
| Lead ID | Días en Cartera | Score | Estado | Prioridad | Próxima Acción |
|---------|-----------------|-------|--------|-----------|----------------|
| LD-1000 | 18 días | 85 | Caliente | 🔴 Alta | Seguimiento |
| LD-1001 | 12 días | 72 | Negociación | 🟡 Media | Cerrar |
| LD-1002 | 3 días | 68 | Nuevo | 🟢 Baja | Agendar cita |

**Priorización automática:**
- 🔴 **Alta**: > 15 días + score > 70
- 🟡 **Media**: > 7 días o score > 60
- 🟢 **Baja**: Otros

**Estados posibles:**
- Nuevo
- En Contacto
- Seguimiento
- Caliente
- Negociación

---

### 3. Agenda de Citas (📅 Mis Citas Próximas)

**Métricas:**
- Citas agendadas (total)
- % Utilización de agenda

**Tabla de Próximas 7 Días:**
| Fecha | Hora | Cliente | Tipo | Interés |
|-------|------|---------|------|---------|
| 27/11/2025 | 10:00 | Cliente-100 | Demo Programada | SUV |
| 27/11/2025 | 14:00 | Cliente-101 | Seguimiento | Sedán |
| 28/11/2025 | 11:00 | Cliente-102 | Cierre Esperado | Premium |

**Tipos de cita:**
- Prospecto Nuevo
- Seguimiento
- Demo Programada
- Cierre Esperado

**Acciones Rápidas:**
- ➕ Agendar Nueva Cita
- 📞 Confirmar Citas del Día

---

### 4. Score Personal (🏆 Mi Score Personal)

**Puntos Totales:**
- Suma de puntos por objetivos logrados
- Display grande: "# 270" puntos
- Caption: "De 330 puntos posibles"

**Insignias Logradas:**
Lista de badges conseguidos:
- 🏆 Conversor Elite
- ⭐ NPS Maestro
- 🎯 Cita Perfecta
- 🚀 Cerrador

**Ranking en Gamificación:**
- Posición en el hub por puntos
- Badge especial si es #1: "🥇 Líder!"

**Ejemplo:**
```
┌─────────────────────────────────────┐
│ 🎯 Puntos Totales      🏅 Insignias │
│                                     │
│     270                 ✅ 🏆      │
│                         ✅ ⭐      │
│ De 330 posibles         ✅ 🎯      │
│                                     │
│ 📊 Ranking: #2 de 8                │
└─────────────────────────────────────┘
```

---

### 5. Métricas de Performance (📊 Mis Métricas)

**KPIs personales:**
- Ventas
- Conversión %
- NPS
- Leads
- Citas
- No-Show %

Formato de métricas sencillo y claro.

---

### 6. Mi Funnel Personal (🔀 Mi Funnel Personal)

**Visualización:**
- Gráfico de embudo con mis números
- Leads → Citas → Reservas → Ventas

**Tasas de Conversión:**
- Lead → Cita: X%
- Cita → Reserva: Y%
- Reserva → Venta: Z%
- **Total: W%**

**Recomendaciones Automáticas:**
Sistema inteligente que detecta:
- ⚠️ Si Lead → Cita < 50%: "Contactar leads en menos de 1 hora"
- ⚠️ Si Cita → Reserva < 45%: "Preparar mejor las demos"
- ⚠️ Si Reserva → Venta < 65%: "Seguimiento más cercano"
- ✅ Si todo está bien: "Tu funnel está saludable!"

---

### 7. Mis Objetivos e Incentivos (🎯 Mis Objetivos)

**Expandibles por objetivo:**

Cada objetivo muestra:
- Nombre y puntos
- Descripción
- Tu valor actual
- Meta a alcanzar
- Barra de progreso
- Estado (✅ Logrado / ⏳ En progreso)

**Ejemplo de objetivo:**
```
⏳ 🏆 Conversor Elite (100 puntos)

Objetivo: Conversión > 30%
Tu valor actual: 22.3%
Meta: 30%

Progreso: ████████░░ 74%

ℹ️ Te faltan 7.7 puntos porcentuales
```

**Objetivos disponibles:**
1. 🏆 Conversor Elite (100 pts)
2. ⭐ NPS Maestro (80 pts)
3. 🎯 Cita Perfecta (60 pts)
4. 🚀 Cerrador (90 pts)

---

### 8. Comparación vs Hub (📊 Mi Performance vs Promedio)

**Métricas comparativas:**

| Métrica | Mi Valor | Delta vs Hub |
|---------|----------|--------------|
| Conversión | 22.3% | +3.8% 📈 |
| NPS | 75 | +9 pts 📈 |
| Ventas | 42 | +12 📈 |

**Resumen de Performance:**
- 🌟 **3/3 arriba**: "¡Estás superando el promedio del hub en todas las métricas!"
- 👍 **2/3 arriba**: "Buen desempeño - Estás por encima en la mayoría"
- ⚠️ **1/3 arriba**: "Hay oportunidad de mejora"
- 📉 **0/3 arriba**: "Necesitas apoyo - Habla con tu manager"

---

## 🎨 Diseño y UX

### Layout en 2 Columnas

```
┌─────────────────────────────┬─────────────────────────────┐
│ Columna Izquierda           │ Columna Derecha             │
├─────────────────────────────┼─────────────────────────────┤
│ 📋 Mi Cartera Activa        │ 📅 Mis Citas Próximas      │
│ • Leads en seguimiento      │ • Citas agendadas           │
│ • Top 5 prioritarios        │ • Próximos 7 días           │
│ • Próximas acciones         │ • Acciones rápidas          │
├─────────────────────────────┼─────────────────────────────┤
│ 🏆 Mi Score Personal        │ 📊 Mis Métricas            │
│ • Puntos totales            │ • Ventas, Conversión        │
│ • Insignias logradas        │ • NPS, Leads, Citas         │
│ • Ranking en hub            │ • No-Show                   │
└─────────────────────────────┴─────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🔀 Mi Funnel Personal                                       │
│ [Gráfico de embudo] + [Tasas] + [Recomendaciones]          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🎯 Mis Objetivos e Incentivos                               │
│ [Expandibles con progreso de cada objetivo]                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 📊 Mi Performance vs Promedio del Hub                       │
│ [Comparación en 3 columnas] + [Resumen]                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Selección de Agente

### En Sidebar:

**Paso 1: Seleccionar Hub**
- Dropdown con todos los hubs disponibles

**Paso 2: Seleccionar Agente**
- Dropdown con agentes del hub seleccionado

**En Producción:**
- Esto sería automático con login
- El agente vería solo su información
- Sin necesidad de selección manual

---

## 💡 Casos de Uso

### Caso 1: Inicio del Día
```
Workflow:
1. Abrir app → Tab "Mi Dashboard"
2. Revisar "Mis Citas Próximas"
3. Clic en "Confirmar Citas del Día"
4. Revisar cartera activa para priorizar seguimientos
```

### Caso 2: Gestión de Cartera
```
Workflow:
1. Ir a "Mi Cartera Activa"
2. Identificar leads 🔴 Alta prioridad
3. Ver "Próxima Acción" sugerida
4. Ejecutar acciones (llamar, agendar, etc.)
```

### Caso 3: Seguimiento de Performance
```
Workflow:
1. Revisar "Mis Métricas"
2. Ir a "Mi Funnel Personal"
3. Leer recomendaciones automáticas
4. Ver "Performance vs Hub"
5. Identificar áreas de mejora
```

### Caso 4: Gamificación
```
Workflow:
1. Revisar "Mi Score Personal"
2. Ver ranking en hub
3. Ir a "Mis Objetivos e Incentivos"
4. Expandir objetivos no logrados
5. Ver qué falta para conseguirlos
6. Trabajar en esos objetivos
```

---

## 📊 Datos Mostrados

### Datos Reales (del agente):
- Ventas, conversión, NPS
- Leads, citas, reservas
- Backlog de cartera
- Utilización de agenda
- Stock asignado y calidad
- Ranking en hub

### Datos Simulados (ejemplos):
- Leads individuales en cartera (ID, días, score, estado)
- Citas específicas futuras (fecha, hora, cliente)

**Nota:** En producción, estos datos vendrían de CRM real.

---

## 🎯 Beneficios

### Para el Agente:
- ✅ **Visibilidad clara** de su situación actual
- ✅ **Priorización** de tareas (leads y citas)
- ✅ **Motivación** a través de gamificación
- ✅ **Feedback inmediato** sobre su performance
- ✅ **Autonomía** para gestionar su trabajo
- ✅ **Transparencia** en métricas y objetivos

### Para la Organización:
- ✅ **Accountability** individual
- ✅ **Visibilidad** de actividad diaria
- ✅ **Engagement** a través de gamificación
- ✅ **Mejora continua** con recomendaciones
- ✅ **Datos** para coaching y desarrollo

---

## 🚀 Cómo Usar

### Paso 1: Ejecutar App
```bash
streamlit run app.py
```

### Paso 2: Ir al Tab Kavako
Seleccionar: "👤 Mi Dashboard (Kavako/Agente)"

### Paso 3: Seleccionar Usuario (Sidebar)
1. **Tu Hub:** CDMX Norte
2. **Tu Nombre:** Juan García

### Paso 4: Explorar el Dashboard
- Revisar resumen personal (arriba)
- Ver cartera y citas (2 columnas)
- Analizar funnel personal
- Revisar objetivos
- Comparar con el hub

---

## 🔄 Integración con Otras Vistas

### Relación con City Manager:
- City Manager ve agregado de todos los agentes
- Kavako ve solo su información individual
- Mismas métricas, diferente nivel de agregación

### Relación con Gamificación:
- Los objetivos son los mismos (config.py)
- City Manager ve ranking completo
- Kavako ve su posición individual

---

## 📈 Métricas Clave Monitoreadas

### Personales:
- Ventas
- Conversión %
- NPS
- Leads asignados
- Citas agendadas
- No-Show %

### De Cartera:
- Leads en seguimiento
- Días promedio en cartera
- Oportunidades totales
- % Aprovechamiento

### De Agenda:
- Utilización %
- Slots disponibles
- Citas próximas

### De Gamificación:
- Puntos totales
- Insignias logradas
- Ranking en hub

---

## 🎨 Características Visuales

### Colores y Estados:
- 🔴 **Rojo**: Alta prioridad, crítico
- 🟡 **Amarillo**: Media prioridad, advertencia
- 🟢 **Verde**: Baja prioridad, saludable
- 🥇 **Dorado**: Líder, #1

### Iconos:
- 👤 Agente
- 📋 Cartera
- 📅 Agenda
- 🏆 Score
- 🎯 Objetivos
- 📊 Métricas
- ✅ Logrado
- ⏳ En progreso

### Badges:
- 🥇 Líder del hub
- ✅ Objetivo logrado
- 🌟 Superando promedio
- 📈 Por encima del hub

---

## 💻 Código y Arquitectura

### Archivos:
- `views/kavako_dashboard.py` - Vista completa
- `app.py` - Agregado tercer tab
- `views/__init__.py` - Export actualizado

### Funciones Principales:
1. `render_kavako_dashboard()` - Orquestador principal
2. `render_agent_selector()` - Selector en sidebar
3. `get_agent_data()` - Obtiene datos del agente
4. `render_personal_summary()` - Header con resumen
5. `render_active_portfolio()` - Cartera activa
6. `render_upcoming_appointments()` - Agenda
7. `render_my_score()` - Score y ranking
8. `render_performance_metrics()` - KPIs
9. `render_my_funnel()` - Funnel personal
10. `render_my_objectives()` - Objetivos
11. `render_vs_hub_comparison()` - Comparación

---

## 🧪 Testing

```bash
✓ Agent data retrieval funciona
✓ Todas las métricas disponibles
✓ Cálculo de ranking correcto
✓ Comparación vs hub funcional
✓ Todas las secciones renderean
```

---

## 🔮 Mejoras Futuras

### Corto Plazo:
1. Integrar con CRM real para cartera
2. Calendario interactivo para citas
3. Acciones directas (llamar, agendar)
4. Notificaciones push

### Mediano Plazo:
5. Historial de performance (gráficos temporales)
6. Recomendaciones personalizadas con ML
7. Chat con manager integrado
8. Recursos de capacitación por métrica

### Largo Plazo:
9. App móvil nativa
10. Voz para navegación
11. Integración con WhatsApp Business
12. Dashboard en smartwatch

---

## ✅ Resumen

**Estado:** ✅ Implementado y funcionando
**Archivos:** 3 modificados, 1 creado
**Líneas de código:** ~500 líneas
**Secciones:** 8 secciones completas
**Tests:** ✅ Passing

**El agente ahora tiene:**
- 📋 Vista de su cartera activa
- 📅 Agenda de citas próximas
- 🏆 Score personal y ranking
- 📊 Métricas de performance
- 🎯 Objetivos e incentivos
- 💡 Recomendaciones personalizadas
- 📊 Comparación vs promedio del hub

---

**Última actualización:** Noviembre 2025
**Versión:** 3.0.0 - Kavako View
**Estado:** ✅ Implementado y listo
