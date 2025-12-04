# 🗺️ Kavak Performance App - ROADMAP

Hoja de ruta de desarrollo con todas las mejoras y funcionalidades futuras.

---

## 📊 ESTADO ACTUAL (v5.0.0)

### ✅ Implementado

- [x] Sistema de autenticación con roles (CEO, Director Regional, City Manager, Kavako)
- [x] Executive Dashboard (CEO) con KPIs estratégicos
- [x] City Manager Dashboard con gestión de equipo
- [x] Kavako Dashboard (vista del agente)
- [x] Vista de perfil de usuario/cliente completa
- [x] Drill-down completo (Hub → Agente → Cliente)
- [x] Comparación entre hubs
- [x] Optimización de agentes (dealership approach)
- [x] Sistema de gamificación e incentivos
- [x] Alertas dinámicas (estratégicas y operativas)
- [x] Filtrado avanzado de agentes por dimensiones
- [x] Filtro de país con etiquetas dinámicas
- [x] Sentinel Score (renombrado desde "Score")
- [x] **Contexto Celeste IA** - Nueva tab con historial de conversación
- [x] **Brief Ejecutivo** - Resumen de 30 segundos para agentes
- [x] **Citas Próximas mejoradas** - Con preview de contexto Celeste

---

## 🤖 CELESTE CO-PILOT: VISIÓN ESTRATÉGICA

### 📋 El Problema

El cliente experimenta **fricción** al pasar de la interacción online con Celeste (IA) al hub físico con un agente humano:

```
┌─────────────────────────────────────────────────────────────────────┐
│  EXPERIENCIA ACTUAL                                                 │
│                                                                     │
│  Celeste (IA)                    Agente Físico                     │
│  ─────────────                   ──────────────                    │
│  ✅ Contexto completo            ❌ Empieza de cero                 │
│  ✅ Respuestas instantáneas      ❌ Tiempo de respuesta mayor       │
│  ✅ Consistente 24/7             ❌ Variabilidad entre agentes      │
│  ✅ Personalizado                ❌ Depende de memoria/habilidad    │
│                                                                     │
│  RESULTADO: El cliente siente que "retrocede" al ir al hub         │
└─────────────────────────────────────────────────────────────────────┘
```

### 🎯 La Visión: Celeste Omnipresente

**Celeste no desaparece cuando el cliente llega al hub.** Se transforma en un Co-Pilot que asiste al agente en tiempo real, creando una experiencia continua para el cliente.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CELESTE CO-PILOT                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PRE-VISITA          DURANTE VISITA         POST-VISITA           │
│  ───────────         ──────────────         ───────────           │
│  • Brief al agente   • Sugerencias          • Feedback cliente    │
│  • WhatsApp cliente  • Checklist            • Notas del agente    │
│  • Notificación      • Alertas tiempo real  • Celeste aprende     │
│                                                                     │
│  El agente nunca está solo - Celeste siempre asiste               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ✅ FASE 0: CONTEXTO CELESTE (COMPLETADO - Dic 2024)

### Implementado

- [x] **Datos de conversación con Celeste**
  - Resumen de la conversación
  - Vehículos mostrados (con ubicación en lote)
  - Presupuesto y preferencias de financiamiento
  - Información de trade-in
  - Objeciones/dudas principales
  - Historial de mensajes

- [x] **Brief Ejecutivo** (visible al inicio del perfil)
  - Resumen de 30 segundos
  - Lo que busca el cliente
  - Vehículo favorito y ubicación
  - Recomendaciones para el agente

- [x] **Tab "Contexto Celeste"**
  - Estadísticas de conversación
  - Vehículos que le interesaron
  - Objeciones registradas
  - Recomendaciones para el agente
  - Preview de la conversación

- [x] **Citas Próximas mejoradas**
  - Preview de contexto Celeste
  - Vehículo favorito y lote
  - Recomendaciones rápidas

---

## 🚧 FASE 1: NOTIFICACIONES Y PREPARACIÓN (Q1 2025)

### Objetivo
Asegurar que el agente esté preparado ANTES de que llegue el cliente.

### Features

#### 🔔 Sistema de Notificaciones Pre-Cita
- [ ] **Push notification 15 min antes**
  - Nombre del cliente
  - Vehículo favorito y ubicación
  - Resumen de 1 línea de Celeste
  - Deep link al perfil completo

- [ ] **WhatsApp al cliente**
  - "Tu resumen está listo"
  - "Juan te espera en el hub"
  - Confirmación de cita
  - El cliente sabe que el agente tiene contexto

- [ ] **Dashboard "Mis Citas de Hoy"**
  - Vista rápida de todas las citas del día
  - Indicador de "preparado" / "no preparado"
  - Tiempo hasta cada cita

#### ✅ Checklist de Conversación
- [ ] **Checklist interactivo**
  - El agente marca qué temas ya cubrió
  - "☐ Mencioné el financiamiento a 48 meses"
  - "☐ Expliqué Kavak Total"
  - "☐ Mostré el vehículo favorito"
  - Progreso visual (3/5 completados)

- [ ] **Alertas de temas faltantes**
  - Si el agente no marcó algo importante
  - "Recuerda mencionar el trade-in"

---

## 🚧 FASE 2: FEEDBACK LOOP (Q2 2025)

### Objetivo
Celeste aprende de cada interacción en el hub para mejorar.

### Features

#### 📝 Notas del Agente → Celeste
- [ ] **Notas estructuradas post-visita**
  - ¿Qué funcionó?
  - ¿Qué objeciones nuevas surgieron?
  - ¿Cuál es el siguiente paso?
  - Estado del cliente (interesado, tibio, frío)

- [ ] **Celeste incorpora las notas**
  - Próxima conversación online incluye contexto del hub
  - "Sé que visitaste el hub y te interesó el RAV4..."
  - Continuidad perfecta

#### 📊 Feedback del Cliente
- [ ] **Encuesta post-visita**
  - WhatsApp automático: "¿Cómo te fue con Juan?"
  - Rating 1-5
  - ¿El agente conocía tu historial?
  - ¿Te sentiste atendido?

- [ ] **Dashboard de feedback**
  - NPS por agente
  - "% de clientes que sintieron continuidad"
  - Correlación: uso de Celeste → satisfacción

#### 🔄 Celeste Aprende
- [ ] **Modelo de aprendizaje**
  - Qué recomendaciones funcionaron
  - Qué objeciones son más comunes
  - Qué agentes usan mejor el contexto
  - Mejora continua de sugerencias

---

## 🚧 FASE 3: CO-PILOT EN TIEMPO REAL (Q3 2025)

### Objetivo
Celeste asiste al agente DURANTE la conversación.

### Features

#### 💬 Sugerencias en Tiempo Real
- [ ] **Panel de sugerencias dinámico**
  - Mientras el agente atiende, Celeste sugiere
  - "El cliente preguntó sobre garantía, aquí está la info"
  - "Menciona la promoción actual de financiamiento"
  - Actualización basada en contexto

- [ ] **Detección de conversación** (futuro)
  - Voice-to-text de la conversación
  - Celeste entiende de qué están hablando
  - Sugiere respuestas relevantes

#### 📱 Tablet/Kiosko en el Hub
- [ ] **Celeste presente físicamente**
  - El cliente puede seguir hablando con Celeste
  - Mientras el agente hace papelería
  - Continuidad total

- [ ] **División de roles**
  - Celeste: Información, dudas, recomendaciones
  - Agente: Acciones físicas, negociación, cierre

#### 🎧 Auricular/Wearable (Futuro)
- [ ] **Celeste susurra al agente**
  - Auricular discreto
  - Información en tiempo real
  - El cliente percibe un agente experto

---

## 📊 MÉTRICAS DE ÉXITO

### KPIs de Adopción
- [ ] % de agentes que leen el brief antes de la cita
- [ ] % de checklists completados
- [ ] Tiempo promedio de preparación pre-cita
- [ ] # de notas ingresadas post-visita

### KPIs de Impacto
- [ ] NPS post-visita (con Celeste vs sin Celeste)
- [ ] "¿El agente conocía tu historial?" (encuesta)
- [ ] Tasa de conversión por uso de contexto
- [ ] Tiempo de cierre (días)

### KPIs de Aprendizaje
- [ ] Precisión de recomendaciones de Celeste
- [ ] % de objeciones predichas correctamente
- [ ] Mejora en sugerencias over time

---

## 🎯 ROADMAP POR VISTA

### 📊 **Performance General / Executive Dashboard**

#### ✅ Ya Implementado
- [x] Ventas + Target
- [x] Conversion Rate general
- [x] NPS y CSAT
- [x] Comparación entre hubs
- [x] Tendencias temporales
- [x] Funnel agregado

#### 🚧 Por Implementar

##### **Inventario Avanzado** (ALTA PRIORIDAD)
- [ ] **Velocity de inventario**
  - Tiempo promedio hasta la venta
  - Días en stock por segmento
  - Velocidad por hub

- [ ] **Rotación de inventario**
  - Turnover ratio
  - Stock turnover por categoría
  - Análisis de stock slow-moving

- [ ] **Aging de inventario**
  - Distribución por edad (días en stock)
  - Buckets de aging: 0-30, 31-60, 61-90, 90+ días
  - Inventario envejecido crítico (>90 días)
  - Proyección de aging futuro

- [ ] **Experiencia de compra vinculada a inventario**
  - NPS por calidad de inventario
  - CASI (Customer Acquisition Satisfaction Index)
  - Correlación stock quality vs NPS

##### **Financials** (MEDIA PRIORIDAD)
- [ ] P&L por hub
- [ ] Margen bruto y neto
- [ ] Costo de adquisición por lead/venta
- [ ] ROI por canal de marketing
- [ ] Break-even analysis

##### **Forecasting** (MEDIA PRIORIDAD)
- [ ] Predicción de ventas (ML)
- [ ] Forecast de demanda por segmento
- [ ] Proyección de inventario necesario
- [ ] Seasonality analysis

---

### 👥 **City Manager Dashboard**

#### ✅ Ya Implementado
- [x] Filtrado por hub
- [x] Comparación de conversión entre agentes
- [x] Identificación de mejores y peores performers
- [x] Definición de incentivos y gamificación
- [x] Performance individual de agentes
- [x] Filtrado avanzado de agentes por múltiples dimensiones
- [x] Drill-down a perfil de agente
- [x] **Sistema de Incentivos Unificado** ✨ NUEVO
  - Módulo consolidado con tabs: Ranking & Niveles, Ownership Score, Objetivos Tradicionales
  - Puntos Compuestos: Base (100 pts/entrega), Financing (+50), Kavak Total (+30), Seguro (+20), Trade-in (+20), NPS Bonus (+25)
  - Niveles: Bronze → Silver → Gold → Diamond
  - Ownership Score: % de clientes manejados de principio a fin
  - Tracking de handoffs (traspasos)
  - Análisis de penetraciones (Financing, Ancillaries, Seguro, Garantía)
- [x] **Panel Capacidad vs Eficiencia** ✨ NUEVO
  - Revenue per slot
  - Efficiency composite (financing + ancillaries + ownership + NPS)
  - Capacidad disponible para más leads
- [x] **Simulador de Asignación de Leads** ✨ NUEVO
  - 3 métodos: Óptimo por eficiencia, Uniforme, Por capacidad
  - Estimación de revenue esperado
  - Comparación vs distribución uniforme

#### 🚧 Por Implementar

##### **Gestión de Equipo Avanzada** (ALTA PRIORIDAD)
- [ ] **Coaching Recommendations**
  - Sugerencias automáticas de coaching basadas en métricas
  - Scripts de conversación para agentes con bajo performance
  - Training needs identificados por IA

- [ ] **Team Planning**
  - Scheduler de turnos
  - Cobertura de horarios óptima
  - Distribución de leads automática

- [ ] **Incentivos Dinámicos**
  - Configuración de metas por ciclo
  - Tracking en tiempo real
  - Leaderboards en vivo
  - Notificaciones de logros

##### **Operación** (MEDIA PRIORIDAD)
- [ ] Asignación automática de agente a lead
  - Por carga de trabajo
  - Por especialización (segmento de vehículo)
  - Por performance histórico
  - Round-robin inteligente

- [ ] Reasignación de leads
  - Si agente no responde en X tiempo
  - Si lead está "frío"
  - Balanceo de carga

- [ ] Alertas operativas en tiempo real
  - Lead sin contactar en 1h
  - Cita sin confirmar
  - No-show detectado

---

### 👤 **Agente / Kavako Dashboard**

#### ✅ Ya Implementado
- [x] Login con cartera activa
- [x] Backlog visible
- [x] Agenda del día con citas
- [x] Link a perfil de usuario desde agenda
- [x] Métricas de performance personal
- [x] Score y gamificación
- [x] Comparación vs hub
- [x] **Panel de Ownership & Puntos Compuestos** ✨ NUEVO
  - Total de puntos acumulados
  - Nivel de incentivo (Bronze → Diamond)
  - Ownership score personal
  - Puntos por entrega promedio
- [x] **Desglose de Puntos** ✨ NUEVO
  - Visualización de contribución por categoría
  - Base, Financing, Garantía, Seguro, Trade-in, NPS Bonus
  - % de contribución de cada fuente
- [x] **Progreso a Siguiente Nivel** ✨ NUEVO
  - Puntos faltantes para subir de nivel
  - Barra de progreso visual
  - Tips personalizados para ganar más puntos
- [x] **Detalles de Ownership** ✨ NUEVO
  - Entregas totales vs handoffs
  - Score de ownership con indicador visual
  - Recomendaciones para mejorar

#### 🚧 Por Implementar

##### **Gestión de Cartera** (ALTA PRIORIDAD)
- [ ] **Call to Action automatizado**
  - "Contactar a este usuario AHORA" (lead caliente)
  - Templates de mensajes pre-escritos
  - Botón de WhatsApp directo
  - Botón de llamada directa

- [ ] **Seguimiento estructurado**
  - Próximos pasos sugeridos por lead
  - Recordatorios automáticos
  - Checklist de seguimiento
  - Log de todas las interacciones

- [ ] **Priorización inteligente**
  - Leads ordenados por propensión a comprar
  - Score de "hot leads"
  - Urgencia calculada (días sin contactar)

##### **Productividad** (MEDIA PRIORIDAD)
- [ ] Integración con CRM
- [ ] Quick actions desde el dashboard
  - Agendar cita en 1 click
  - Enviar cotización
  - Marcar como contactado

- [ ] Mobile app para agentes en campo
- [ ] Voice-to-text para notas rápidas

---

### 🧑‍💼 **Usuario / Cliente Profile**

#### ✅ Ya Implementado
- [x] Transacciones históricas completas
- [x] Identificación de VIPs
- [x] Bookings activos
- [x] Cancelaciones con razones
- [x] Intereses de vehículos
- [x] Ancillaries vendidos
- [x] Historial de interacciones
- [x] Datos de contacto
- [x] Score del cliente

#### 🚧 Por Implementar

##### **Inteligencia de Cliente** (ALTA PRIORIDAD)
- [ ] **Alternativas para ofrecerle**
  - Motor de recomendación de vehículos
  - Basado en:
    - Historial de búsquedas
    - Transacciones previas
    - Perfil demográfico
    - Budget estimado
  - "Clientes similares compraron..."

- [ ] **Sentinel Score**
  - Propensión a comprar (0-100)
  - Factores que influyen
  - Próximos mejores pasos
  - Probabilidad de cierre

- [ ] **Customer Journey Mapping**
  - Línea de tiempo visual
  - Todos los touchpoints
  - Stage actual en el funnel
  - Tiempo promedio hasta cierre

##### **Experiencia** (MEDIA PRIORIDAD)
- [ ] NPS por transacción
- [ ] Feedback cualitativo
- [ ] Quejas y resoluciones
- [ ] Post-sale satisfaction tracking

##### **Engagement** (MEDIA PRIORIDAD)
- [ ] Canal de comunicación preferido
- [ ] Horarios de mejor contacto
- [ ] Histórico de emails/llamadas/visitas
- [ ] Respuesta rate

---

## 🔔 ALERTAS E INTEGRACIONES

### 🚧 Por Implementar (ALTA PRIORIDAD)

#### **Sistema de Alertas Avanzado**
- [ ] **Integración con Slack**
  - Alertas críticas a channels específicos
  - Menciones a usuarios relevantes
  - Configuración de umbrales personalizados

- [ ] **Pop-ups en Dashboard**
  - Alertas en tiempo real
  - Prioridad por severidad
  - Dismiss y snooze

- [ ] **Email/SMS Notifications**
  - Configurables por usuario
  - Digest diario/semanal
  - Alertas críticas instantáneas

#### **Alertas de Desvíos**
- [ ] Conversión < threshold
- [ ] Ventas vs target
- [ ] NPS en caída
- [ ] Inventario crítico
- [ ] Agente con performance bajo
- [ ] No-show rate alto

---

## 🔧 INTEGRACIONES TÉCNICAS

### 🚧 Por Implementar

#### **Autenticación** (ALTA PRIORIDAD)
- [ ] Google SSO
- [ ] Okta integration
- [ ] 2FA opcional
- [ ] Role management via admin panel

#### **Datos** (ALTA PRIORIDAD)
- [ ] Conexión a Snowflake
- [ ] Conexión a Databricks
- [ ] API para ingesta de datos en tiempo real
- [ ] Cache de datos con Redis
- [ ] Delta incremental updates

#### **Herramientas Operativas** (MEDIA PRIORIDAD)
- [ ] Integración con app operativa (@miguel navarrete)
- [ ] WhatsApp Business API
- [ ] Telephony system (para llamadas desde app)
- [ ] Calendar sync (Google Calendar, Outlook)

#### **BI Tools** (BAJA PRIORIDAD)
- [ ] Export a Tableau
- [ ] Export a Power BI
- [ ] Excel exports avanzados
- [ ] PDF reports automáticos

---

## 📱 MOBILE & UX

### 🚧 Por Implementar (MEDIA PRIORIDAD)

- [ ] Responsive design mejorado
- [ ] Mobile app para agentes (React Native / Flutter)
- [ ] Offline mode
- [ ] Push notifications
- [ ] Dark mode
- [ ] Multi-idioma (ES, PT, EN)

---

## 🤖 INTELIGENCIA ARTIFICIAL & ML

### 🚧 Por Implementar (BAJA PRIORIDAD - Futuro)

#### **Predictive Analytics**
- [ ] Lead scoring automático
- [ ] Churn prediction
- [ ] Next best action recommendation
- [ ] Optimal pricing suggestions

#### **NLP & Automation**
- [ ] Chatbot para FAQs
- [ ] Sentiment analysis en reviews
- [ ] Auto-categorización de cancelaciones
- [ ] Email/message auto-response

#### **Computer Vision**
- [ ] Vehicle damage detection
- [ ] Quality assessment de fotos

---

## 📈 ANALYTICS AVANZADO

### 🚧 Por Implementar (MEDIA PRIORIDAD)

- [ ] **Cohort Analysis**
  - Retención por cohorte
  - LTV por segmento
  - Repeat purchase rate

- [ ] **Attribution Modeling**
  - Marketing channel attribution
  - Multi-touch attribution
  - Campaign ROI

- [ ] **A/B Testing Framework**
  - Test de incentivos
  - Test de pricing
  - Test de mensajes

- [ ] **Custom Reports Builder**
  - Drag & drop report creator
  - Save & schedule reports
  - Share con equipo

---

## ❓ DUDAS / PREGUNTAS PARA RESOLVER

### Preguntas de Negocio

1. **¿Cuándo una reserva está activa?**
   - [ ] Definir estados de reserva
   - [ ] Timeouts de reserva
   - [ ] Renovación automática?

2. **¿De dónde se puede sacar el kavako que está gestionando el lead?**
   - [ ] Integración con CRM
   - [ ] Tabla de asignación en DB
   - [ ] API endpoint para consultar

3. **Asignación automática de agente**
   - [ ] Definir reglas de negocio
   - [ ] Criterios de asignación
   - [ ] Reasignación automática?
   - [ ] Override manual permitido?

---

## 🎯 PRIORIZACIÓN POR FASES

### **FASE 0: Contexto Celeste** (Dic 2024) ✅ COMPLETADO
**Objetivo:** Dar al agente acceso al contexto de Celeste

1. ✅ Brief Ejecutivo en perfil del cliente
2. ✅ Tab "Contexto Celeste" con historial completo
3. ✅ Citas Próximas con preview de contexto
4. ✅ Recomendaciones para el agente
5. ✅ Vehículos favoritos con ubicación en lote

### **FASE 1: Notificaciones y Preparación** (Q1 2025)
**Objetivo:** Asegurar que el agente esté preparado antes de cada cita

1. 🚧 Push notifications 15 min antes de cita
2. 🚧 WhatsApp al cliente con confirmación
3. 🚧 Checklist de conversación interactivo
4. 🚧 Dashboard "Mis Citas de Hoy"
5. 🚧 Métricas de adopción del contexto

### **FASE 2: Feedback Loop** (Q2 2025)
**Objetivo:** Celeste aprende de cada interacción en el hub

1. 🚧 Notas estructuradas post-visita
2. 🚧 Celeste incorpora notas a futuras conversaciones
3. 🚧 Encuesta de feedback post-visita
4. 🚧 Dashboard de satisfacción por agente
5. 🚧 Modelo de aprendizaje continuo

### **FASE 3: Co-Pilot en Tiempo Real** (Q3 2025)
**Objetivo:** Celeste asiste durante la conversación

1. 🚧 Panel de sugerencias dinámico
2. 🚧 Detección de contexto de conversación
3. 🚧 Tablet/Kiosko con Celeste en el hub
4. 🚧 División de roles Celeste/Agente

### **FASE 4: Data & Scale** (Q4 2025)
**Objetivo:** Conexión a datos reales y escalar

1. 🚧 Conexión a Snowflake/Databricks
2. 🚧 API de Celeste para historial real
3. 🚧 Mobile app para agentes
4. 🚧 Integración con WhatsApp Business
5. 🚧 Multi-idioma

---

## 💡 IDEAS ADICIONALES (Backlog)

### Performance
- [ ] Benchmarking vs industria
- [ ] Simulador de escenarios (what-if analysis)
- [ ] Capacity planning avanzado

### Experiencia
- [ ] Customer satisfaction predictor
- [ ] Win/loss analysis
- [ ] Voice of customer dashboard

### Operación
- [ ] Smart routing de leads
- [ ] Workforce optimization
- [ ] Shift planning automático

### Financiero
- [ ] Budget vs actual tracking
- [ ] Profitability por hub/agente
- [ ] Commission calculator

---

## 📝 CÓMO AGREGAR ITEMS AL ROADMAP

1. **Documentar la idea**
   - Descripción clara
   - Problema que resuelve
   - Beneficio esperado

2. **Clasificar**
   - Vista afectada (CEO / City Manager / Agente / Cliente)
   - Prioridad (Alta / Media / Baja)
   - Complejidad (1-5)

3. **Agregar a este documento**
   - En la sección correspondiente
   - Marcar como `[ ]` (pending)
   - Incluir en fase apropiada

4. **Revisión periódica**
   - Mensual: revisar prioridades
   - Trimestral: planificar siguiente fase

---

## 🔄 PROCESO DE DESARROLLO

### Workflow
1. Idea → Agregar a ROADMAP
2. Priorización → Asignar a Fase
3. Spec → Crear documento detallado en `docs/`
4. Desarrollo → Implementar feature
5. Testing → QA y validación
6. Deploy → Release
7. Marcar como ✅ en ROADMAP

### Criterios de Priorización
- **Impacto en negocio** (Alto / Medio / Bajo)
- **Complejidad técnica** (1-5)
- **Dependencias** (Bloqueantes?)
- **Recursos necesarios** (Dev hours)
- **ROI esperado**

---

**Última actualización:** Diciembre 2024
**Versión:** 2.0 - Celeste Co-Pilot Vision
**Mantenido por:** Equipo de Data & Analytics

---

## 📞 Contacto

Para sugerir nuevas features o discutir prioridades:
- Slack: #kavak-performance-app
- Email: data-analytics@kavak.com
