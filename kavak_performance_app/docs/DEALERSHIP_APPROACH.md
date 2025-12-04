# 🏆 Enfoque Concesionaria - Optimización de Agentes

## 🎯 Objetivo

Maximizar la eficiencia de cada agente tratándolo como una **concesionaria individual**, midiendo su performance según **todas las oportunidades** que tuvo para convertir, considerando la **calidad del stock** asignado.

---

## 📊 Nuevo Paradigma

### ❌ Antes (Enfoque Tradicional)
- Conversión = Ventas / Leads totales
- No consideraba capacidad real del agente
- No medía calidad del inventario asignado
- Dimensionamiento de flota a nivel hub (agregado)

### ✅ Ahora (Enfoque Concesionaria)
- **Oportunidades Reales** = Citas agendadas + Backlog de cartera
- **Conversión Real** = Ventas / Oportunidades reales
- **Eficiencia Ajustada** = Conversión × Calidad del stock
- **Capacidad medida** = Utilización de agenda (slots disponibles)

---

## 🆕 Nuevas Métricas Implementadas

### 1. Capacidad del Agente

| Métrica | Descripción | Fórmula |
|---------|-------------|---------|
| **Slots por Semana** | Capacidad total de agenda | 40 slots (8 por día × 5 días) |
| **Citas Agendadas** | Slots ocupados con citas | Count de appointments |
| **Slots Disponibles** | Capacidad no utilizada | Slots totales - Citas agendadas |
| **Utilización %** | Porcentaje de capacidad usada | Citas agendadas / Slots totales |

**Thresholds:**
- 🟢 **≥ 80%**: Alta utilización (óptimo)
- 🟡 **60-79%**: Utilización normal
- 🔴 **< 60%**: Subutilización (oportunidad de mejora)

### 2. Oportunidades Reales

| Métrica | Descripción | Fórmula |
|---------|-------------|---------|
| **Backlog de Cartera** | Leads asignados pero no cerrados | Leads en seguimiento |
| **Oportunidades Totales** | Total de chances de conversión | Citas agendadas + Backlog |
| **Conversión Real** | Tasa sobre oportunidades | Ventas / Oportunidades totales |
| **% Aprovechamiento** | Porcentaje de oportunidades cerradas | (Ventas / Oportunidades) × 100 |

**Thresholds:**
- 🟢 **≥ 25%**: Excelente aprovechamiento
- 🟡 **15-24%**: Aprovechamiento normal
- 🔴 **< 15%**: Bajo aprovechamiento (revisar)

### 3. Calidad del Stock Asignado

| Métrica | Descripción | Fórmula |
|---------|-------------|---------|
| **Autos Asignados** | Inventario a cargo del agente | Count de vehículos |
| **Edad Promedio** | Días promedio en inventario | Promedio de días desde llegada |
| **Atractivo del Stock** | Score de calidad (0-100) | Ver fórmula abajo |
| **Match con Leads** | Coincidencia con búsquedas | Score de alineación (0-100) |

**Fórmula de Atractivo:**
```
Atractivo = (Factor Edad × 40%) + (Factor Demanda × 30%) + (Factor Precio × 30%)

Donde:
- Factor Edad = max(0, 100 - edad_días × 1.2)
- Factor Demanda = Demanda del segmento (0-100)
- Factor Precio = Competitividad de precio (0-100)
```

**Thresholds:**
- 🟢 **≥ 75**: Stock muy atractivo
- 🟡 **60-74**: Stock aceptable
- 🔴 **< 60**: Stock poco atractivo (renovar)

### 4. Eficiencia Ajustada

| Métrica | Descripción | Fórmula |
|---------|-------------|---------|
| **Eficiencia Ajustada** | Conversión ajustada por calidad | Conversión Real × (Atractivo / 100) |

Esta métrica permite comparar agentes de forma justa, considerando que algunos tienen mejor stock que otros.

---

## 📋 Nueva Sección en City Manager Dashboard

### 🎯 Optimización de Agentes

#### Sección 1: Capacidad vs Utilización
**Tabla interactiva mostrando:**
- Slots semanales totales
- Citas agendadas actuales
- Slots disponibles sin usar
- % de utilización
- Backlog de cartera pendiente

**Coloración:**
- 🟢 Verde: Utilización ≥ 80%
- 🟡 Amarillo: Utilización < 60%

**Insights automáticos:**
- Utilización promedio del hub
- Total de slots disponibles
- Total de backlog pendiente
- Alerta de agentes subutilizados

#### Sección 2: Oportunidades vs Conversión Real
**Tabla interactiva mostrando:**
- Oportunidades totales (citas + backlog)
- Citas agendadas
- Backlog de cartera
- Conversiones logradas
- % de aprovechamiento
- Atractivo del stock asignado

**Coloración:**
- 🟢 Verde: Aprovechamiento ≥ 25%
- 🔴 Rojo: Aprovechamiento < 15%

#### Sección 3: Calidad del Stock Asignado
**Tabla interactiva mostrando:**
- Autos asignados al agente
- Edad promedio del stock
- Score de atractivo (0-100)
- Match con leads (0-100)

**Coloración:**
- 🟢 Verde: Atractivo ≥ 75
- 🔴 Rojo: Atractivo < 60

**Análisis automático:**
- Atractivo promedio del hub
- Edad promedio del stock
- Match promedio con leads
- Alerta de stock de baja calidad

#### Sección 4: Ranking de Eficiencia Ajustada
**Tabla ranking mostrando:**
- Rank del agente
- Eficiencia ajustada (considera calidad de stock)
- % de aprovechamiento
- Calidad del stock
- Ventas totales
- Oportunidades totales

**Highlight:**
- 🥇🥈🥉 Top 3 agentes destacados en amarillo dorado

#### Sección 5: Recomendaciones Automáticas
**Sistema inteligente que genera acciones específicas:**

Ejemplo de recomendaciones:
```
🎯 Juan García:
   ✅ Alta utilización (85%) - Agente bien aprovechado
   🚗 Stock poco atractivo (58/100, edad: 52d) - Renovar inventario
   💡 Acción: Asignar stock más fresco para mejorar conversión

⚠️ María López:
   📅 Baja utilización (58%) - 17 slots disponibles
   📋 Alto backlog (24 leads) - Priorizar seguimiento
   💡 Acciones: 1) Agendar más citas de backlog
               2) Asignar leads nuevos para llenar capacidad
```

---

## 🚨 Nuevas Alertas Inteligentes

### 1. Agentes Subutilizados
**Trigger:** Utilización < 60%
**Descripción:** Detecta agentes con capacidad disponible que no está siendo aprovechada
**Acción sugerida:** Asignar más leads para llenar slots disponibles

### 2. Stock de Baja Calidad
**Trigger:** Atractivo del stock < 60
**Descripción:** Stock envejecido o poco atractivo afecta la conversión
**Acción sugerida:** Renovar inventario asignado al agente

### 3. Alto Backlog sin Capacidad
**Trigger:** Backlog > 20 leads Y Slots disponibles < 5
**Descripción:** Agente sobrecargado con leads pero sin tiempo para atenderlos
**Acción sugerida:** Redistribuir cartera o aumentar capacidad

### 4. Bajo Aprovechamiento de Oportunidades
**Trigger:** Aprovechamiento < 15%
**Descripción:** Agente no está convirtiendo sus oportunidades
**Acción sugerida:** Revisar calidad de leads o capacitación en cierre

### 5. Mismatch Stock-Leads
**Trigger:** Match Score < 60
**Descripción:** El inventario no coincide con lo que buscan los leads
**Acción sugerida:** Reasignar stock más alineado con el perfil de leads

---

## 📈 Impacto Esperado

### Para City Managers:
- ✅ **Visibilidad real** de capacidad disponible
- ✅ **Identificación rápida** de agentes subutilizados
- ✅ **Decisiones basadas en datos** para asignación de inventario
- ✅ **Optimización** de la utilización del equipo
- ✅ **Comparación justa** entre agentes (considerando calidad de stock)

### Para Agentes:
- ✅ Medición más **justa** (considera calidad del stock)
- ✅ **Claridad** sobre su capacidad y utilización
- ✅ **Visibilidad** del backlog a gestionar
- ✅ **Feedback** sobre calidad del inventario asignado

### Para el Negocio:
- ✅ **Maximización** de la capacidad del equipo
- ✅ **Reducción** de stock envejecido
- ✅ **Mejora** en conversión por mejor asignación
- ✅ **Optimización** de recursos (tiempo de agentes)

---

## 🎮 Casos de Uso

### Caso 1: Agente Subutilizado
```
Situación:
- Juan tiene 40 slots/semana
- Solo 24 citas agendadas (60% utilización)
- 16 slots disponibles sin usar
- Backlog de solo 8 leads

Acción:
1. Asignar 12-15 leads nuevos de alta calidad
2. Objetivo: llevar utilización a 80-85%
3. Monitorear conversión en próxima semana
```

### Caso 2: Stock de Baja Calidad
```
Situación:
- María tiene 15 autos asignados
- Edad promedio: 58 días
- Atractivo: 52/100
- Conversión: 12% (baja)

Acción:
1. Rotar stock: asignar 10 autos más frescos
2. Reasignar autos envejecidos a otro canal (online, promociones)
3. Monitorear mejora en conversión
```

### Caso 3: Alto Backlog
```
Situación:
- Carlos tiene 28 citas agendadas (70% utilización)
- Backlog de 32 leads
- Total oportunidades: 60
- Aprovechamiento: 18%

Acción:
1. Priorizar seguimiento de backlog
2. No asignar leads nuevos temporalmente
3. Agendar 5-8 citas más del backlog
4. Capacitación en cierre para mejorar aprovechamiento
```

### Caso 4: Mismatch Stock-Leads
```
Situación:
- Ana tiene leads buscando SUVs y Premium
- Stock asignado: mayoría Sedán y Hatchback
- Match Score: 45/100
- Conversión: 14%

Acción:
1. Reasignar stock: más SUVs y Premium
2. Intercambiar inventario con otro agente
3. Actualizar perfil de leads asignados
4. Monitorear mejora en conversión
```

---

## 🔧 Configuración

Todas las métricas y thresholds son configurables en `config.py`:

```python
# Capacity thresholds
CAPACITY_THRESHOLDS = {
    "utilization_good": 0.80,     # 80%+: Alta utilización
    "utilization_warning": 0.60,  # <60%: Subutilizado
    "backlog_high": 20,           # 20+ leads: Alto backlog
    "available_slots_low": 5      # <5 slots: Baja capacidad
}

# Opportunity thresholds
OPPORTUNITY_THRESHOLDS = {
    "aprovechamiento_good": 0.25,    # 25%+: Excelente
    "aprovechamiento_warning": 0.15  # <15%: Bajo
}

# Stock quality thresholds
STOCK_THRESHOLDS = {
    "attractiveness_good": 75,    # 75+: Stock muy atractivo
    "attractiveness_warning": 60, # <60: Stock poco atractivo
    "age_critical": 60,           # 60+ días: Envejecido
    "match_warning": 60           # <60: Bajo match
}
```

---

## 📊 Métricas Clave a Monitorear

### Diarias:
- Utilización promedio del hub
- Slots disponibles totales
- Agentes subutilizados (< 60%)
- Stock con baja calidad (< 60)

### Semanales:
- Aprovechamiento promedio (conversión real)
- Backlog total del hub
- Rotación de inventario asignado
- Top 3 agentes por eficiencia ajustada

### Mensuales:
- Tendencia de utilización
- Tendencia de calidad de stock
- Impacto de reasignaciones
- Comparativa mes anterior

---

## ✅ Implementación Completa

- ✅ Generador de datos actualizado con todas las métricas
- ✅ Nueva sección completa en City Manager Dashboard
- ✅ 5 tipos nuevos de alertas inteligentes
- ✅ Sistema de recomendaciones automáticas
- ✅ Tablas interactivas con coloración por thresholds
- ✅ Insights y análisis automáticos
- ✅ Tests funcionando correctamente

---

## 🚀 Cómo Usar

1. **Ejecutar la app:**
   ```bash
   streamlit run app.py
   ```

2. **Ir a tab "Team Performance (City Manager)"**

3. **Navegar a sección "🎯 Optimización de Agentes"**

4. **Explorar las 5 subsecciones:**
   - Capacidad vs Utilización
   - Oportunidades vs Conversión Real
   - Calidad del Stock Asignado
   - Ranking de Eficiencia Ajustada
   - Recomendaciones Automáticas

5. **Revisar alertas operativas** (incluyen las nuevas alertas de concesionaria)

---

## 📞 Beneficios del Nuevo Enfoque

### 🎯 Para Toma de Decisiones:
- Visibilidad clara de capacidad disponible
- Identificación de cuellos de botella
- Asignación óptima de recursos
- Medición justa de performance

### 💰 Para el Negocio:
- Maximización de utilización de agentes
- Reducción de inventario envejecido
- Mejora en conversión general
- Optimización de costos operativos

### 👥 Para el Equipo:
- Medición más justa y transparente
- Feedback claro y accionable
- Reconocimiento del contexto (calidad de stock)
- Claridad en objetivos y oportunidades

---

**Última actualización:** Noviembre 2025
**Versión:** 2.0.0 - Dealership Approach
**Estado:** ✅ Implementado y funcionando
