# 🔐 Sistema de Autenticación y Roles

## ✅ Estado: Implementado (MVP con datos dummy)

---

## 🎯 Objetivo

Implementar un sistema de autenticación y autorización basado en roles que controle:
- **Quién** puede acceder a la aplicación
- **Qué** vistas puede ver cada usuario
- **Qué datos** puede acceder según su rol y ubicación

---

## 📋 Arquitectura del Sistema

### Componentes Principales

1. **`utils/auth.py`** - Sistema de autenticación y autorización
2. **`views/login.py`** - Vista de login
3. **`app.py`** - Aplicación principal (modificada para verificar autenticación)

---

## 👥 Roles Implementados

### 1. CEO
**Acceso:** Total
**Permisos:**
- ✅ Ve todos los países y todos los hubs
- ✅ Acceso a las 3 vistas (Executive, City Manager, Kavako)
- ✅ Puede hacer drill-down a agentes y clientes
- ✅ Sin restricciones de datos

**Usuario Demo:**
```
Email: ceo@kavak.com
Contraseña: ceo123
```

**Caso de uso:**
El CEO puede ver performance global, comparar países y hubs, y hacer drill-down hasta el nivel de agente individual.

---

### 2. Director Regional
**Acceso:** Por país
**Permisos:**
- ✅ Ve solo su país asignado (ej: México)
- ✅ Ve todos los hubs de su país
- ✅ Acceso a Executive Dashboard y City Manager
- ✅ Puede hacer drill-down a agentes
- ❌ No ve datos de otros países

**Usuario Demo:**
```
Email: director.mexico@kavak.com
Contraseña: dir123
País: México
```

**Caso de uso:**
El Director de México solo ve hubs y agentes de México. No puede ver Brasil, Argentina o Chile.

---

### 3. City Manager
**Acceso:** Por hub
**Permisos:**
- ✅ Ve solo su hub asignado (ej: CDMX Norte)
- ✅ Acceso solo a City Manager Dashboard
- ✅ Puede hacer drill-down a sus agentes
- ✅ Ve clientes asignados a su hub
- ❌ No ve otros hubs

**Usuario Demo:**
```
Email: manager.cdmx@kavak.com
Contraseña: mgr123
Hub: CDMX Norte, México
```

**Caso de uso:**
El City Manager de CDMX Norte solo ve performance de su hub y sus agentes. No ve CDMX Sur ni Guadalajara.

---

### 4. Kavako (Agente)
**Acceso:** Personal
**Permisos:**
- ✅ Ve solo su información personal
- ✅ Acceso solo a "Mi Dashboard"
- ✅ Ve su cartera y agenda
- ✅ Puede ver perfiles de sus clientes
- ❌ No puede hacer drill-down
- ❌ No ve información de otros agentes

**Usuarios Demo:**
```
Email: agente1@kavak.com
Contraseña: agt123
Hub: CDMX Norte
```

```
Email: agente2@kavak.com
Contraseña: agt123
Hub: Guadalajara
```

**Caso de uso:**
El agente solo ve su dashboard personal con su cartera, citas, métricas y clientes asignados.

---

## 🔐 Sistema de Autenticación

### MVP: Datos Dummy

Actualmente usa un diccionario hardcodeado en `utils/auth.py`:

```python
DUMMY_USERS = {
    "email@kavak.com": {
        "password": "password",
        "name": "Nombre Completo",
        "role": "CEO",
        "country": "México",
        "hub": "CDMX Norte",
        "permissions": ["executive_dashboard", ...]
    }
}
```

### Flujo de Login

1. Usuario ingresa email y contraseña
2. Sistema verifica credenciales contra `DUMMY_USERS`
3. Si es válido:
   - Crea sesión (st.session_state)
   - Guarda info del usuario
   - Redirige a dashboard
4. Si es inválido:
   - Muestra error
   - Mantiene en pantalla de login

### Session State

Cuando el usuario hace login, se guarda en `session_state`:

```python
{
    'authenticated': True,
    'user_email': 'ceo@kavak.com',
    'user_info': {
        'name': 'Carlos Mendoza',
        'role': 'CEO',
        'country': 'Todos',
        'hub': 'Todos',
        'permissions': [...]
    },
    'login_time': datetime.now()
}
```

---

## 🛡️ Control de Acceso

### 1. Control de Vistas (Tabs)

Cada rol tiene tabs específicos:

```python
ROLE_CAPABILITIES = {
    "CEO": {
        "tabs_visible": [
            "Executive Dashboard (CEO)",
            "Team Performance (City Manager)",
            "Mi Dashboard (Kavako/Agente)"
        ]
    },
    "Director Regional": {
        "tabs_visible": [
            "Executive Dashboard (CEO)",
            "Team Performance (City Manager)"
        ]
    },
    "City Manager": {
        "tabs_visible": ["Team Performance (City Manager)"]
    },
    "Kavako": {
        "tabs_visible": ["Mi Dashboard (Kavako/Agente)"]
    }
}
```

**Implementación:**
```python
accessible_tabs = get_accessible_tabs()
# Solo muestra tabs que el usuario puede ver
```

---

### 2. Filtrado de Datos

Los datos se filtran automáticamente según el rol:

**CEO:**
```python
# Ve todos los datos sin filtrar
data = get_filtered_data_for_user(data)  # Sin filtros
```

**Director Regional (México):**
```python
# Solo datos de México
data = data[data['country'] == 'México']
```

**City Manager (CDMX Norte):**
```python
# Solo datos de CDMX Norte
data = data[
    (data['country'] == 'México') &
    (data['hub'] == 'CDMX Norte')
]
```

**Kavako:**
```python
# Solo sus propios datos
data = data[data['agent_id'] == user.agent_id]
```

---

### 3. Control de Drill-Down

Algunos roles pueden navegar a vistas detalladas:

| Rol | Puede ver perfil de agente | Puede ver perfil de cliente |
|-----|---------------------------|----------------------------|
| CEO | ✅ Sí | ✅ Sí |
| Director Regional | ✅ Sí | ✅ Sí |
| City Manager | ✅ Sí (de su hub) | ✅ Sí (de su hub) |
| Kavako | ❌ No | ✅ Sí (sus clientes) |

---

## 🖥️ Vista de Login

### Características

1. **Formulario Limpio**
   - Email corporativo
   - Contraseña
   - Botón de login

2. **Usuarios Demo**
   - Expandible con lista de usuarios
   - Muestra credenciales para testing
   - Explica permisos de cada rol

3. **Mensajes Claros**
   - Error: "Usuario no encontrado"
   - Error: "Contraseña incorrecta"
   - Éxito: "Login exitoso! Redirigiendo..."

4. **Info de SSO**
   - Mensaje sobre integración futura con Google SSO

---

## 🔄 Flujo de la Aplicación

### 1. Inicio de Aplicación

```
Usuario abre app.py
     ↓
¿Está autenticado?
     ├─ NO → Mostrar login.py
     │        ↓
     │   Usuario ingresa credenciales
     │        ↓
     │   ¿Credenciales válidas?
     │        ├─ SÍ → Crear sesión → (volver arriba)
     │        └─ NO → Mostrar error → Quedarse en login
     │
     └─ SÍ → Obtener user_info
              ↓
         Filtrar datos según rol
              ↓
         Mostrar tabs disponibles
              ↓
         Usuario navega en app
```

### 2. Durante la Sesión

```
Usuario autenticado
     ↓
Cada vista/acción verifica permisos
     ├─ ¿Puede ver estos datos? → Filtrar según país/hub
     ├─ ¿Puede ver esta vista? → Mostrar/Ocultar tabs
     └─ ¿Puede hacer drill-down? → Habilitar/Deshabilitar botones
```

### 3. Cierre de Sesión

```
Usuario hace clic en "Cerrar Sesión"
     ↓
Ejecuta logout_user()
     ↓
Limpia session_state
     ↓
Redirige a login
```

---

## 📱 Experiencia por Rol

### CEO (Carlos Mendoza)

**Login:**
```
ceo@kavak.com / ceo123
```

**Ve:**
- ✅ 3 tabs: Executive, City Manager, Kavako
- ✅ Selector de país: Todos los países
- ✅ Selector de hub: Todos los hubs
- ✅ Comparación entre hubs
- ✅ Puede hacer clic en cualquier agente → Ver perfil
- ✅ Puede hacer clic en cualquier cliente → Ver perfil

**Workflow típico:**
1. Ve Executive Dashboard global
2. Filtra por México
3. Compara hubs de México
4. Hace drill-down a CDMX Norte
5. Ve ranking de agentes
6. Hace clic en agente → Ve perfil completo
7. Ve agenda del agente
8. Hace clic en cliente → Ve historial completo

---

### City Manager (Juan Pérez - CDMX Norte)

**Login:**
```
manager.cdmx@kavak.com / mgr123
```

**Ve:**
- ✅ 1 tab: City Manager
- ❌ Solo ve datos de CDMX Norte (sin selector)
- ✅ Ranking de agentes de su hub
- ✅ Puede hacer clic en agente → Ver perfil
- ✅ Ve clientes de su hub

**Workflow típico:**
1. Ve performance de CDMX Norte
2. Ve ranking de sus agentes
3. Hace clic en agente con baja conversión
4. Ve su cartera activa
5. Identifica problema
6. Ve clientes del agente
7. Hace seguimiento

---

### Kavako (Ana Martínez)

**Login:**
```
agente1@kavak.com / agt123
```

**Ve:**
- ✅ 1 tab: Mi Dashboard
- ✅ Solo su información personal
- ✅ Su cartera de leads
- ✅ Su agenda de citas
- ✅ Sus métricas y objetivos
- ✅ Puede ver sus clientes

**Workflow típico:**
1. Inicia sesión
2. Ve su dashboard personal
3. Revisa citas del día
4. Ve cartera con leads prioritarios
5. Hace clic en cliente → Ve historial
6. Planifica seguimiento

---

## 🚀 Migración a Google SSO

### Futuro: Integración con Google SSO

**Cambios necesarios:**

1. **Agregar dependencias:**
```bash
pip install streamlit-google-auth
```

2. **Configurar Google OAuth:**
```python
from streamlit_google_auth import Authenticate

authenticator = Authenticate(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8501"
)
```

3. **Reemplazar login form:**
```python
if st.button("Login with Google"):
    user_info = authenticator.login()
    # Obtener role desde base de datos
```

4. **Base de datos de usuarios:**
```sql
CREATE TABLE users (
    email VARCHAR PRIMARY KEY,
    name VARCHAR,
    role VARCHAR,
    country VARCHAR,
    hub VARCHAR,
    active BOOLEAN
);
```

---

## 🔒 Seguridad

### MVP (Actual)

- ⚠️ Contraseñas en texto plano (solo para demo)
- ⚠️ Sin encriptación de sesión
- ✅ Control de acceso funcional
- ✅ Filtrado de datos por rol

### Producción (Futuro)

- ✅ Google SSO (sin contraseñas)
- ✅ Tokens JWT
- ✅ HTTPS obligatorio
- ✅ Sesiones con timeout
- ✅ Logs de acceso
- ✅ 2FA opcional

---

## 📊 Matriz de Permisos

| Vista/Acción | CEO | Director | Manager | Kavako |
|--------------|-----|----------|---------|--------|
| **Executive Dashboard** | ✅ | ✅ | ❌ | ❌ |
| **City Manager Dashboard** | ✅ | ✅ | ✅ | ❌ |
| **Kavako Dashboard** | ✅ | ❌ | ❌ | ✅ |
| **Ver todos los países** | ✅ | ❌ | ❌ | ❌ |
| **Ver todos los hubs** | ✅ | ✅* | ❌ | ❌ |
| **Ver perfil de agente** | ✅ | ✅ | ✅ | ❌ |
| **Ver perfil de cliente** | ✅ | ✅ | ✅ | ✅** |
| **Exportar reportes** | ✅ | ✅ | ✅ | ❌ |
| **Admin settings** | ✅ | ❌ | ❌ | ❌ |

\* Solo de su país
\** Solo sus clientes asignados

---

## 🧪 Testing

### Cómo Probar

1. **Login como CEO:**
   ```
   ceo@kavak.com / ceo123
   → Debería ver 3 tabs
   → Debería ver todos los países
   ```

2. **Login como Director:**
   ```
   director.mexico@kavak.com / dir123
   → Debería ver 2 tabs
   → Debería ver solo México
   ```

3. **Login como Manager:**
   ```
   manager.cdmx@kavak.com / mgr123
   → Debería ver 1 tab (City Manager)
   → Debería ver solo CDMX Norte
   ```

4. **Login como Agente:**
   ```
   agente1@kavak.com / agt123
   → Debería ver 1 tab (Mi Dashboard)
   → Debería ver solo su info
   ```

5. **Intentar login inválido:**
   ```
   ceo@kavak.com / wrong_password
   → Debería rechazar
   → Debería mostrar error
   ```

---

## 📝 Archivos Modificados

### Nuevos Archivos:
- ✅ `utils/auth.py` - Sistema de autenticación
- ✅ `views/login.py` - Vista de login
- ✅ `views/customer_profile.py` - Perfil de cliente
- ✅ `views/agent_profile_detail.py` - Perfil de agente

### Archivos Modificados:
- ✅ `app.py` - Verificación de autenticación y control de acceso
- ✅ `views/__init__.py` - Exports actualizados
- ✅ `utils/data_generator.py` - Agregado generate_customer_data()
- ✅ `views/city_manager_dashboard.py` - Agregados botones de drill-down

---

## ✅ Checklist de Implementación

- [x] Sistema de autenticación básico
- [x] Vista de login
- [x] 4 roles definidos
- [x] 5 usuarios dummy
- [x] Control de acceso a tabs
- [x] Filtrado de datos por rol
- [x] Drill-down a perfil de agente
- [x] Drill-down a perfil de cliente
- [x] Breadcrumb navigation
- [x] Info de usuario en sidebar
- [x] Botón de logout
- [x] Tests passing
- [ ] Integración Google SSO (futuro)
- [ ] Base de datos de usuarios (futuro)
- [ ] 2FA (futuro)

---

**Última actualización:** Noviembre 2025
**Versión:** 4.0.0 - Authentication System
**Estado:** ✅ MVP Completo con datos dummy
