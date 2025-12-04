"""
Celeste Copilot - AI Assistant for Kavak Agents
Interactive copilot that provides contextual insights, vehicle alternatives,
and actionable recommendations during customer interactions.
"""

import random
from datetime import datetime

import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# ═══════════════════════════════════════════════════════════════════════════════
# CELESTE COPILOT COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════


def render_celeste_copilot(customer_info=None, position="floating"):
    """
    Render the Celeste Copilot widget

    Args:
        customer_info: Dict with customer data for contextual responses
        position: "sidebar" (sidebar widget) or "floating" (bottom-right overlay)
    """
    if position == "sidebar":
        render_copilot_sidebar(customer_info)
    else:
        render_copilot_floating(customer_info)


def render_copilot_floating(customer_info):
    """
    Render Celeste Copilot as a floating chat widget on the RIGHT side

    Uses st.popover for the chat panel (native Streamlit floating element)
    with JavaScript to position it at bottom-right
    """
    # Initialize state
    if "copilot_open" not in st.session_state:
        st.session_state.copilot_open = False

    # Store customer context globally for the copilot
    if customer_info:
        st.session_state.copilot_customer_context = customer_info

    # Get current context
    context = st.session_state.get("copilot_customer_context", None)

    # ═══════════════════════════════════════════════════════════════════════════
    # CSS + JAVASCRIPT FOR FLOATING FAB
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown(
        """
        <style>
        /* ══════════════════════════════════════════════════════════════════
           CELESTE COPILOT - FLOATING FAB & POPOVER STYLES
        ══════════════════════════════════════════════════════════════════ */

        /* Style the popover trigger as a circular FAB */
        #celeste-fab-wrapper [data-testid="stPopover"] > div:first-child > button {
            width: 70px !important;
            height: 70px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%) !important;
            border: none !important;
            box-shadow: 0 4px 25px rgba(124, 58, 237, 0.5) !important;
            color: white !important;
            font-size: 1.6rem !important;
            padding: 0 !important;
            min-height: 70px !important;
            transition: all 0.3s ease !important;
        }

        #celeste-fab-wrapper [data-testid="stPopover"] > div:first-child > button:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 8px 35px rgba(124, 58, 237, 0.6) !important;
        }

        #celeste-fab-wrapper [data-testid="stPopover"] > div:first-child > button p {
            font-size: 1.6rem !important;
            margin: 0 !important;
        }

        /* Style the popover panel */
        [data-testid="stPopoverBody"] {
            width: 380px !important;
            max-height: 520px !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 50px rgba(0,0,0,0.25) !important;
            overflow-y: auto !important;
        }

        /* Floating FAB container */
        #celeste-fab-wrapper {
            position: fixed !important;
            bottom: 25px !important;
            right: 25px !important;
            z-index: 999999 !important;
        }

        /* Pulse animation - DISABLED for cleaner look */
        .celeste-pulse {
            display: none;
        }

        /* Online badge */
        .celeste-online {
            position: fixed;
            bottom: 80px;
            right: 27px;
            width: 18px;
            height: 18px;
            background: #10B981;
            border-radius: 50%;
            border: 3px solid white;
            z-index: 1000001;
            pointer-events: none;
        }
        </style>

        <!-- Online indicator -->
        <div class="celeste-online"></div>

        <script>
        // Move the Celeste FAB to fixed position after Streamlit renders
        const observer = new MutationObserver(() => {
            const fabWrapper = document.getElementById('celeste-fab-wrapper');
            if (fabWrapper && !fabWrapper.dataset.positioned) {
                fabWrapper.dataset.positioned = 'true';
                // Ensure it stays fixed
                fabWrapper.style.position = 'fixed';
                fabWrapper.style.bottom = '25px';
                fabWrapper.style.right = '25px';
                fabWrapper.style.zIndex = '999999';
            }
        });
        observer.observe(document.body, { childList: true, subtree: true });
        </script>
    """,
        unsafe_allow_html=True,
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # POPOVER FAB - Using native st.popover
    # ═══════════════════════════════════════════════════════════════════════════

    # Use popover - Streamlit's native floating element
    with st.popover("🤖", use_container_width=False):
        # Header
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
                padding: 16px 20px;
                margin: -1rem -1rem 1rem -1rem;
                color: white;
                display: flex;
                align-items: center;
                gap: 12px;
                border-radius: 12px 12px 0 0;
            ">
                <div style="
                    width: 45px;
                    height: 45px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.5rem;
                ">🤖</div>
                <div>
                    <div style="font-weight: 700; font-size: 1.1rem;">Celeste Copilot</div>
                    <div style="font-size: 0.75rem; opacity: 0.9; display: flex; align-items: center; gap: 6px;">
                        <span style="width: 8px; height: 8px; background: #10B981; border-radius: 50%; display: inline-block;"></span>
                        En línea • Tu asistente IA
                    </div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Quick actions
        st.markdown("**💡 Acciones rápidas:**")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚗 Autos", key="cel_alt", use_container_width=True):
                st.session_state.copilot_action = "alternatives"
        with c2:
            if st.button("💬 Tips", key="cel_tips", use_container_width=True):
                st.session_state.copilot_action = "tips"

        c3, c4 = st.columns(2)
        with c3:
            if st.button("📊 Análisis", key="cel_analysis", use_container_width=True):
                st.session_state.copilot_action = "analysis"
        with c4:
            if st.button("💰 Financ.", key="cel_fin", use_container_width=True):
                st.session_state.copilot_action = "financing"

        st.markdown("---")

        # Chat interface
        render_copilot_chat_compact(context)

    # ═══════════════════════════════════════════════════════════════════════════
    # JAVASCRIPT TO POSITION THE POPOVER AS FLOATING FAB
    # ═══════════════════════════════════════════════════════════════════════════

    # Use components.html to inject JavaScript that runs in an iframe
    # but can communicate with parent window
    components.html(
        """
        <script>
        // Function to position the popover trigger as a floating FAB
        function positionCelesteFAB() {
            // Access the parent Streamlit document
            const parent = window.parent.document;

            // Find all popovers and get the last one (ours)
            const popovers = parent.querySelectorAll('[data-testid="stPopover"]');

            if (popovers.length > 0) {
                const celeste = popovers[popovers.length - 1]; // Last popover

                // Get the popover trigger button container
                const triggerContainer = celeste.querySelector('div:first-child');

                if (triggerContainer && !triggerContainer.dataset.celestePositioned) {
                    triggerContainer.dataset.celestePositioned = 'true';

                    // Style it as floating FAB
                    celeste.style.cssText = `
                        position: fixed !important;
                        bottom: 25px !important;
                        right: 25px !important;
                        z-index: 999999 !important;
                        width: auto !important;
                    `;
                }
            }
        }

        // Run on load and observe for changes
        positionCelesteFAB();

        // Also run periodically in case Streamlit re-renders
        setInterval(positionCelesteFAB, 500);
        </script>
    """,
        height=0,
    )


def render_copilot_chat_compact(customer_info):
    """Render a compact chat interface for the floating panel"""
    # Initialize chat history
    if "copilot_messages" not in st.session_state:
        st.session_state.copilot_messages = []
        welcome_msg = get_welcome_message(customer_info)
        st.session_state.copilot_messages.append(
            {"role": "assistant", "content": welcome_msg, "timestamp": datetime.now()}
        )

    # Check for quick action triggers
    action = st.session_state.get("copilot_action", None)
    if action:
        handle_quick_action(action, customer_info)
        st.session_state.copilot_action = None

    # Display chat messages in a compact scrollable container
    chat_container = st.container(height=200)

    with chat_container:
        for msg in st.session_state.copilot_messages[-8:]:
            if msg["role"] == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("user", avatar="👤"):
                    st.write(msg["content"])

    # Input field
    user_input = st.chat_input("Pregunta a Celeste...", key="copilot_float_input")

    if user_input:
        st.session_state.copilot_messages.append(
            {"role": "user", "content": user_input, "timestamp": datetime.now()}
        )

        response = generate_copilot_response(user_input, customer_info)

        st.session_state.copilot_messages.append(
            {"role": "assistant", "content": response, "timestamp": datetime.now()}
        )

        st.rerun()


def render_copilot_sidebar(customer_info):
    """Render Celeste Copilot in the sidebar (alternative position)"""
    with st.sidebar:
        st.markdown("---")

        # Copilot header with avatar
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
                padding: 16px;
                border-radius: 12px;
                margin-bottom: 16px;
                text-align: center;
            ">
                <div style="font-size: 2.5rem;">🤖</div>
                <div style="color: white; font-weight: 700; font-size: 1.1rem;">Celeste Copilot</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem;">Tu asistente inteligente</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Status indicator
        st.markdown(
            """
            <div style="
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 12px;
            ">
                <div style="
                    width: 8px;
                    height: 8px;
                    background: #10B981;
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                "></div>
                <span style="color: #6B7280; font-size: 0.85rem;">En línea • Listo para ayudarte</span>
            </div>
            <style>
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # Quick action buttons
        st.markdown("**💡 Acciones rápidas:**")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "🚗 Alt. Autos", key="copilot_alt_autos", use_container_width=True
            ):
                st.session_state.copilot_action = "alternatives"

        with col2:
            if st.button("💬 Tips", key="copilot_tips", use_container_width=True):
                st.session_state.copilot_action = "tips"

        col3, col4 = st.columns(2)

        with col3:
            if st.button(
                "📊 Análisis", key="copilot_analysis", use_container_width=True
            ):
                st.session_state.copilot_action = "analysis"

        with col4:
            if st.button("❓ Preguntar", key="copilot_ask", use_container_width=True):
                st.session_state.copilot_action = "ask"

        st.markdown("---")

        # Chat interface
        render_copilot_chat(customer_info)


def render_copilot_chat(customer_info):
    """Render the chat interface for Celeste Copilot"""
    # Initialize chat history
    if "copilot_messages" not in st.session_state:
        st.session_state.copilot_messages = []
        # Add welcome message
        welcome_msg = get_welcome_message(customer_info)
        st.session_state.copilot_messages.append(
            {"role": "assistant", "content": welcome_msg, "timestamp": datetime.now()}
        )

    # Check for quick action triggers
    action = st.session_state.get("copilot_action", None)
    if action:
        handle_quick_action(action, customer_info)
        st.session_state.copilot_action = None

    # Display chat messages
    chat_container = st.container(height=300)

    with chat_container:
        for msg in st.session_state.copilot_messages[-10:]:  # Last 10 messages
            if msg["role"] == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("user", avatar="👤"):
                    st.write(msg["content"])

    # Input field
    user_input = st.chat_input("Pregunta a Celeste...", key="copilot_input")

    if user_input:
        # Add user message
        st.session_state.copilot_messages.append(
            {"role": "user", "content": user_input, "timestamp": datetime.now()}
        )

        # Generate response
        response = generate_copilot_response(user_input, customer_info)

        st.session_state.copilot_messages.append(
            {"role": "assistant", "content": response, "timestamp": datetime.now()}
        )

        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE GENERATION (Simulated AI Responses)
# ═══════════════════════════════════════════════════════════════════════════════


def get_welcome_message(customer_info):
    """Generate contextual welcome message"""
    if customer_info:
        name = customer_info.get("customer_name", "el cliente")
        score = customer_info.get("customer_score", 0)

        if score >= 70:
            return f"¡Hola! 👋 Estoy lista para ayudarte con **{name}**. Este cliente tiene un score alto ({score}/100), ¡excelente oportunidad! ¿Qué necesitas saber?"
        elif score >= 50:
            return f"¡Hola! 👋 Veo que estás con **{name}** (Score: {score}/100). Tengo insights que pueden ayudarte a cerrar. ¿En qué te apoyo?"
        else:
            return f"¡Hola! 👋 Con **{name}** (Score: {score}/100) vamos a necesitar trabajar las objeciones. Pregúntame cómo puedo ayudarte."
    else:
        return "¡Hola! 👋 Soy Celeste, tu copilot de ventas. Puedo ayudarte con alternativas de autos, tips de cierre, y análisis de clientes. ¿En qué te ayudo?"


def handle_quick_action(action, customer_info):
    """Handle quick action button clicks"""
    if action == "alternatives":
        response = generate_vehicle_alternatives(customer_info)
    elif action == "tips":
        response = generate_selling_tips(customer_info)
    elif action == "analysis":
        response = generate_customer_analysis(customer_info)
    elif action == "ask":
        response = "¿Qué te gustaría saber? Puedo ayudarte con:\n• Alternativas de vehículos\n• Tips de negociación\n• Análisis del cliente\n• Comparativas de modelos"
    else:
        response = "¿En qué puedo ayudarte?"

    st.session_state.copilot_messages.append(
        {"role": "assistant", "content": response, "timestamp": datetime.now()}
    )


def generate_copilot_response(user_input, customer_info):
    """Generate contextual response based on user input (simulated)"""
    input_lower = user_input.lower()

    # Detect intent and generate appropriate response
    if any(
        word in input_lower
        for word in ["alternativa", "otro", "similar", "parecido", "opcion", "opción"]
    ):
        return generate_vehicle_alternatives(customer_info)

    elif any(
        word in input_lower
        for word in ["tip", "consejo", "cerrar", "vender", "objeción", "objecion"]
    ):
        return generate_selling_tips(customer_info)

    elif any(
        word in input_lower
        for word in ["análisis", "analisis", "perfil", "score", "cliente"]
    ):
        return generate_customer_analysis(customer_info)

    elif any(
        word in input_lower
        for word in ["financ", "crédito", "credito", "pago", "mensual"]
    ):
        return generate_financing_info(customer_info)

    elif any(
        word in input_lower for word in ["precio", "descuento", "negociar", "rebaja"]
    ):
        return generate_pricing_tips(customer_info)

    elif any(
        word in input_lower for word in ["inventario", "stock", "disponible", "hay"]
    ):
        return generate_inventory_info(customer_info)

    elif any(
        word in input_lower
        for word in ["comparar", "diferencia", "versus", "vs", "mejor"]
    ):
        return generate_comparison(customer_info)

    else:
        return generate_generic_response(user_input, customer_info)


def generate_vehicle_alternatives(customer_info):
    """Generate vehicle alternatives based on customer preferences"""
    if not customer_info:
        return "Para darte alternativas específicas, necesito que selecciones un cliente primero."

    vehicles = customer_info.get("celeste_vehicles_shown", [])
    budget = customer_info.get("celeste_budget_range", "$200,000 - $350,000")

    if vehicles:
        fav = vehicles[0]
        brand = fav.get("brand", "Toyota")
        model = fav.get("model", "Corolla")
        price = fav.get("price", 250000)

        # Generate alternatives
        alternatives = [
            {
                "brand": "Honda",
                "model": "Civic",
                "year": 2022,
                "price": price * 0.95,
                "lote": "A-12",
            },
            {
                "brand": "Mazda",
                "model": "3",
                "year": 2022,
                "price": price * 1.02,
                "lote": "B-08",
            },
            {
                "brand": "Nissan",
                "model": "Sentra",
                "year": 2023,
                "price": price * 0.88,
                "lote": "C-15",
            },
        ]

        response = f"🚗 **Alternativas al {brand} {model}:**\n\n"

        for idx, alt in enumerate(alternatives, 1):
            response += f"**{idx}. {alt['brand']} {alt['model']} {alt['year']}**\n"
            response += f"   💰 ${alt['price']:,.0f} | 📍 Lote {alt['lote']}\n\n"

        response += f"\n💡 **Mi recomendación:** El **Mazda 3** tiene mejor equipamiento de serie y mayor valor de reventa. Ideal si el cliente valora tecnología."

        return response
    else:
        return f"📊 Basándome en el presupuesto ({budget}), te sugiero:\n\n1. **Toyota Corolla 2022** - Confiabilidad\n2. **Honda Civic 2022** - Deportividad\n3. **Mazda 3 2023** - Diseño y tecnología\n\n¿Quieres que busque disponibilidad de alguno?"


def generate_selling_tips(customer_info):
    """Generate contextual selling tips"""
    if not customer_info:
        return "**Tips generales de cierre:**\n\n1. 🎯 Identifica el pain point principal\n2. 🚗 Enfoca en beneficios, no características\n3. ⏰ Crea urgencia genuina\n4. 💰 Presenta el financiamiento como solución"

    objections = customer_info.get("celeste_main_objections", [])
    score = customer_info.get("customer_score", 50)
    financing = customer_info.get("celeste_financing_interest", {})

    tips = []

    if "precio" in str(objections).lower():
        tips.append(
            "💰 **Para objeción de precio:** Enfoca en el costo total de propiedad y el valor de reventa de Kavak. Menciona la garantía incluida."
        )

    if "pensar" in str(objections).lower() or "tiempo" in str(objections).lower():
        tips.append(
            "⏰ **Para 'lo voy a pensar':** Pregunta qué información adicional necesita para decidir hoy. Ofrece reservar el auto sin compromiso."
        )

    if financing and financing.get("interested"):
        tips.append(
            "📋 **Financiamiento:** Ya mostró interés. Prepara una cotización con 3 opciones de plazo para dar sensación de control."
        )

    if score >= 70:
        tips.append(
            "🔥 **Cliente caliente:** ¡Este cliente está listo! Presenta una oferta con fecha límite de 48hrs."
        )
    elif score < 50:
        tips.append(
            "🎯 **Cliente frío:** Enfócate en generar confianza primero. Comparte testimoniales y garantía Kavak."
        )

    if not tips:
        tips = [
            "🎯 Pregunta sobre su experiencia con el auto anterior",
            "💡 Menciona el programa de garantía extendida",
            "🚗 Ofrece test drive del vehículo favorito",
        ]

    return "**💡 Tips para este cliente:**\n\n" + "\n\n".join(tips)


def generate_customer_analysis(customer_info):
    """Generate detailed customer analysis"""
    if not customer_info:
        return "Selecciona un cliente para ver su análisis."

    name = customer_info.get("customer_name", "Cliente")
    score = customer_info.get("customer_score", 0)
    is_vip = customer_info.get("is_vip", False)
    num_sales = customer_info.get("num_sales", 0)
    budget = customer_info.get("celeste_budget_range", "No especificado")
    objections = customer_info.get("celeste_main_objections", [])

    # Score analysis
    if score >= 70:
        score_analysis = "🟢 **Alta probabilidad de compra.** Cliente enganchado, momento ideal para cerrar."
    elif score >= 50:
        score_analysis = (
            "🟡 **Probabilidad media.** Necesita más información o resolver objeciones."
        )
    else:
        score_analysis = "🔴 **Probabilidad baja.** Requiere más trabajo de nurturing."

    response = f"📊 **Análisis de {name}:**\n\n"
    response += f"**Sentinel Score:** {score}/100\n{score_analysis}\n\n"

    if is_vip:
        response += "⭐ **Cliente VIP** - Prioridad máxima\n\n"

    if num_sales > 0:
        response += f"🔄 **Cliente recurrente** con {num_sales} compras previas. ¡Conoce el proceso!\n\n"

    response += f"💰 **Presupuesto:** {budget}\n\n"

    if objections:
        response += "⚠️ **Objeciones a resolver:**\n"
        for obj in objections[:3]:
            response += f"   • {obj}\n"

    return response


def generate_financing_info(customer_info):
    """Generate financing information and suggestions"""
    if not customer_info:
        price = 250000
    else:
        vehicles = customer_info.get("celeste_vehicles_shown", [])
        price = vehicles[0].get("price", 250000) if vehicles else 250000

    # Calculate payment options
    options = [
        {"months": 12, "rate": 0.12, "down": 0.20},
        {"months": 24, "rate": 0.14, "down": 0.15},
        {"months": 36, "rate": 0.16, "down": 0.10},
    ]

    response = f"💰 **Opciones de financiamiento para ${price:,.0f}:**\n\n"

    for opt in options:
        down_payment = price * opt["down"]
        financed = price - down_payment
        monthly = (financed * (1 + opt["rate"])) / opt["months"]

        response += f"**{opt['months']} meses** (Enganche {opt['down']*100:.0f}%)\n"
        response += f"   • Enganche: ${down_payment:,.0f}\n"
        response += f"   • Mensualidad: ${monthly:,.0f}\n\n"

    response += "💡 **Tip:** El plan de 24 meses es el más popular - balancea mensualidad accesible con menos intereses totales."

    return response


def generate_pricing_tips(customer_info):
    """Generate pricing negotiation tips"""
    return """💰 **Tips para negociación de precio:**

1. **No bajes el precio primero** - Agrega valor con accesorios o servicios incluidos

2. **Usa el "Split the difference"** - Si pide $10k menos, ofrece $5k con condición de cierre hoy

3. **Trade-in como herramienta** - Si tiene un auto, ofrece mejor valuación en lugar de descuento

4. **Paquete financiero** - A veces una mejor tasa es más valioso que descuento

5. **Aprobación de gerente** - Usa la táctica del "voy a hablar con mi gerente" para dar sensación de esfuerzo

⚠️ **Recuerda:** El precio de lista ya tiene margen. Consulta límites con tu manager antes de negociar."""


def generate_inventory_info(customer_info):
    """Generate inventory availability info (simulated)"""
    if customer_info:
        vehicles = customer_info.get("celeste_vehicles_shown", [])
        if vehicles:
            fav = vehicles[0]
            return f"""📦 **Estado de inventario:**

**{fav.get('brand', 'Toyota')} {fav.get('model', 'Corolla')} {fav.get('year', 2022)}**
• 📍 Ubicación: Lote {fav.get('lote', 'A-1')}
• ✅ Estado: Disponible
• 🕐 Tiempo en inventario: 12 días
• 👀 Vistas esta semana: 8 clientes

⚠️ **Alerta:** Este modelo tiene alta demanda. Solo quedan 2 unidades similares en el hub.

💡 **Sugerencia:** Si el cliente está interesado, recomienda reservar hoy."""

    return (
        "Selecciona un cliente para ver la disponibilidad de sus vehículos de interés."
    )


def generate_comparison(customer_info):
    """Generate vehicle comparison"""
    return """📊 **Comparativa rápida SUVs Compactas:**

| Modelo | Precio Prom. | Confiabilidad | Reventa |
|--------|-------------|---------------|---------|
| Honda CR-V | $380k | ⭐⭐⭐⭐⭐ | Alta |
| Toyota RAV4 | $395k | ⭐⭐⭐⭐⭐ | Muy Alta |
| Mazda CX-5 | $360k | ⭐⭐⭐⭐ | Alta |
| Nissan X-Trail | $340k | ⭐⭐⭐ | Media |

💡 **Mi recomendación:**
- **Para familias:** RAV4 por espacio
- **Para parejas:** CX-5 por diseño
- **Mejor precio:** X-Trail

¿Quieres que profundice en alguno?"""


def generate_generic_response(user_input, customer_info):
    """Generate generic helpful response"""
    responses = [
        "Entiendo. ¿Podrías darme más contexto sobre lo que necesitas? Puedo ayudarte con alternativas de autos, tips de venta, o análisis del cliente.",
        "Interesante pregunta. Déjame pensar... ¿Te refieres a este cliente específico o en general?",
        "Claro, puedo ayudarte con eso. ¿Quieres que me enfoque en opciones de vehículos, financiamiento, o estrategia de cierre?",
        "Buena pregunta. Para darte la mejor respuesta, ¿me puedes decir más sobre la situación con el cliente?",
    ]
    return random.choice(responses)


# ═══════════════════════════════════════════════════════════════════════════════
# CELESTE INSIGHTS COMPONENT (Non-interactive summary)
# ═══════════════════════════════════════════════════════════════════════════════


def render_celeste_insights_card(customer_info):
    """Render a compact Celeste insights card (non-interactive summary)"""
    if not customer_info:
        return

    score = customer_info.get("customer_score", 0)
    objections = customer_info.get("celeste_main_objections", [])
    recommendations = customer_info.get("celeste_recommendations", [])

    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 1.5rem;">🤖</span>
                <span style="font-weight: 700; color: #7C3AED;">Celeste dice:</span>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Quick insight based on score
        if score >= 70:
            st.success(
                "🔥 **Cliente caliente** - Alta probabilidad de cierre. ¡Momento de actuar!"
            )
        elif score >= 50:
            st.info(
                "🎯 **Oportunidad activa** - Trabaja las objeciones y podrás cerrar."
            )
        else:
            st.warning(
                "📋 **En nurturing** - Necesita más información antes de decidir."
            )

        # Top objection
        if objections:
            st.caption(f"⚠️ Principal duda: *{objections[0]}*")

        # Top recommendation
        if recommendations:
            st.caption(f"💡 Tip: *{recommendations[0]}*")
