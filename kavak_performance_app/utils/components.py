"""
Reusable UI components for Streamlit
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from config import COLORS, THRESHOLDS


def apply_custom_styles():
    """Apply custom CSS styling - Kavak Brand Identity (Enhanced UX)"""
    st.markdown(
        """
        <style>
        /* ═══════════════════════════════════════════════════════════════════
           KAVAK BRAND STYLES - Enhanced UX Version
           Typography: Outfit (distinctive, modern)
           Colors: Kavak Blue with semantic accents
        ═══════════════════════════════════════════════════════════════════ */

        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

        /* Apply font to text elements only, not icons */
        body, p, span, div, h1, h2, h3, h4, h5, h6, label, input, button, textarea, select, option, a {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Preserve Material Icons font */
        .material-symbols-rounded, .material-icons, [class*="icon"] {
            font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        }

        /* ═══════════════════════════════════════════════════════════════════
           LAYOUT & BACKGROUNDS
        ═══════════════════════════════════════════════════════════════════ */

        .main {
            background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%);
        }

        .block-container {
            padding-top: 2rem;
            max-width: 1400px;
        }

        /* ═══════════════════════════════════════════════════════════════════
           TYPOGRAPHY
        ═══════════════════════════════════════════════════════════════════ */

        h1 {
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            color: #0F172A !important;
            letter-spacing: -0.02em;
        }

        h2 {
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            color: #1E293B !important;
            margin-top: 1.5rem !important;
        }

        h3 {
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            color: #334155 !important;
            letter-spacing: -0.01em;
        }

        /* ═══════════════════════════════════════════════════════════════════
           METRICS - Modern card style
        ═══════════════════════════════════════════════════════════════════ */

        [data-testid="stMetricValue"] {
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            color: #64748B !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        [data-testid="stMetricDelta"] {
            font-size: 0.875rem !important;
            font-weight: 600 !important;
        }

        /* ═══════════════════════════════════════════════════════════════════
           TABS - Pill style navigation
        ═══════════════════════════════════════════════════════════════════ */

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #F1F5F9;
            padding: 6px;
            border-radius: 12px;
            border: none;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            background-color: transparent;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.875rem;
            color: #64748B;
            border: none;
            transition: all 0.2s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: white;
            color: #0B4FD6;
        }

        .stTabs [aria-selected="true"] {
            background-color: white !important;
            color: #0B4FD6 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        /* ═══════════════════════════════════════════════════════════════════
           BUTTONS - Primary action style
        ═══════════════════════════════════════════════════════════════════ */

        .stButton > button {
            background: linear-gradient(135deg, #0B4FD6 0%, #003DAC 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(11,79,214,0.2);
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(11,79,214,0.3);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* Secondary buttons (in expanders, etc) */
        [data-testid="stExpander"] .stButton > button {
            background: white;
            color: #0B4FD6;
            border: 1px solid #E2E8F0;
            box-shadow: none;
        }

        [data-testid="stExpander"] .stButton > button:hover {
            background: #F8FAFC;
            border-color: #0B4FD6;
        }

        /* ═══════════════════════════════════════════════════════════════════
           RADIO BUTTONS - Navigation pills
        ═══════════════════════════════════════════════════════════════════ */

        .stRadio > div {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .stRadio [role="radiogroup"] {
            gap: 8px;
        }

        .stRadio label {
            background: #F1F5F9;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 500;
            font-size: 0.875rem;
            color: #64748B;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 2px solid transparent;
        }

        .stRadio label:hover {
            background: #E2E8F0;
            color: #0B4FD6;
        }

        .stRadio [data-checked="true"] label,
        .stRadio input:checked + div {
            background: #0B4FD6 !important;
            color: white !important;
        }

        /* ═══════════════════════════════════════════════════════════════════
           ALERTS - Semantic colors
        ═══════════════════════════════════════════════════════════════════ */

        .alert-critical {
            background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
            border-left: 4px solid #EF4444;
            padding: 16px 20px;
            border-radius: 8px;
            margin: 12px 0;
        }

        .alert-warning {
            background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
            border-left: 4px solid #F59E0B;
            padding: 16px 20px;
            border-radius: 8px;
            margin: 12px 0;
        }

        .alert-info {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-left: 4px solid #0B4FD6;
            padding: 16px 20px;
            border-radius: 8px;
            margin: 12px 0;
        }

        /* ═══════════════════════════════════════════════════════════════════
           EXPANDERS - Clean card style
        ═══════════════════════════════════════════════════════════════════ */

        .streamlit-expanderHeader {
            background-color: white;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            font-weight: 600;
            color: #1E293B;
            padding: 12px 16px;
        }

        .streamlit-expanderHeader:hover {
            border-color: #0B4FD6;
            background-color: #F8FAFC;
        }

        [data-testid="stExpander"] {
            border: none;
            background: transparent;
        }

        /* ═══════════════════════════════════════════════════════════════════
           INPUTS - Modern form controls
        ═══════════════════════════════════════════════════════════════════ */

        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #E2E8F0;
            padding: 12px 16px;
            font-size: 0.9375rem;
            transition: all 0.2s ease;
        }

        .stTextInput > div > div > input:focus {
            border-color: #0B4FD6;
            box-shadow: 0 0 0 4px rgba(11,79,214,0.1);
        }

        .stSelectbox > div > div {
            border-radius: 10px;
        }

        /* ═══════════════════════════════════════════════════════════════════
           PROGRESS BARS
        ═══════════════════════════════════════════════════════════════════ */

        .stProgress > div > div > div {
            background: linear-gradient(90deg, #0B4FD6, #3B82F6);
            border-radius: 4px;
        }

        .stProgress > div > div {
            background: #E2E8F0;
            border-radius: 4px;
        }

        /* ═══════════════════════════════════════════════════════════════════
           SIDEBAR
        ═══════════════════════════════════════════════════════════════════ */

        [data-testid="stSidebar"] {
            background: white;
            border-right: 1px solid #E2E8F0;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }

        /* ═══════════════════════════════════════════════════════════════════
           DATAFRAMES
        ═══════════════════════════════════════════════════════════════════ */

        .dataframe {
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            overflow: hidden;
        }

        .dataframe th {
            background: #F8FAFC !important;
            color: #475569 !important;
            font-weight: 600 !important;
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 12px 16px !important;
        }

        .dataframe td {
            padding: 10px 16px !important;
            font-size: 0.875rem;
        }

        /* ═══════════════════════════════════════════════════════════════════
           DIVIDERS
        ═══════════════════════════════════════════════════════════════════ */

        hr {
            border: none;
            border-top: 1px solid #E2E8F0;
            margin: 1.5rem 0;
        }

        /* ═══════════════════════════════════════════════════════════════════
           SUCCESS/INFO/WARNING/ERROR BOXES
        ═══════════════════════════════════════════════════════════════════ */

        .stSuccess {
            background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
            border-radius: 10px;
            border-left: 4px solid #10B981;
        }

        .stInfo {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-radius: 10px;
            border-left: 4px solid #0B4FD6;
        }

        .stWarning {
            background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
            border-radius: 10px;
            border-left: 4px solid #F59E0B;
        }

        .stError {
            background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
            border-radius: 10px;
            border-left: 4px solid #EF4444;
        }

        /* ═══════════════════════════════════════════════════════════════════
           ANIMATIONS
        ═══════════════════════════════════════════════════════════════════ */

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .element-container {
            animation: fadeIn 0.3s ease-out;
        }

        </style>
    """,
        unsafe_allow_html=True,
    )


def format_currency_compact(value):
    """Format large currency values compactly (e.g. $1.5M, $899K)"""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.0f}K"
    else:
        return f"${value:.0f}"


def render_kpi_card(label, value, delta=None, delta_color="normal", format_str=None):
    """
    Render a KPI metric card

    Args:
        label: KPI label
        value: Main value to display
        delta: Optional delta value
        delta_color: Color for delta (normal, inverse, off)
        format_str: Optional format string (e.g., "%.1f%%", "$%.0f")
    """
    if format_str:
        if isinstance(value, (int, float)):
            formatted_value = format_str % value
        else:
            formatted_value = str(value)
    else:
        formatted_value = value

    st.metric(label=label, value=formatted_value, delta=delta, delta_color=delta_color)


def render_metric_comparison(
    label, hub_value, avg_value, format_str="%.1f", suffix="", country_name="país"
):
    """
    Render a comparison metric showing only country average and gap
    (hub value is already shown in the main KPIs section above)

    Args:
        label: Metric label
        hub_value: Value for the selected hub/region
        avg_value: Average value for the country
        format_str: Format string for values
        suffix: Suffix to add (e.g., "%")
        country_name: Name of the country to display in labels
    """
    delta = hub_value - avg_value
    delta_pct = (delta / avg_value * 100) if avg_value != 0 else 0

    # Display label
    st.markdown(f"**{label.upper()}**")

    # Show country average and gap in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"Promedio {country_name}")
        st.markdown(f"### {format_str % avg_value}{suffix}")
    with col2:
        st.caption(f"Gap vs {country_name}")
        if delta_pct >= 0:
            st.markdown(f"### :green[↑ {delta_pct:+.1f}%]")
        else:
            st.markdown(f"### :red[↓ {delta_pct:.1f}%]")


def render_alert_box(alert_type, title, description, timestamp=None):
    """
    Render an alert box with styling

    Args:
        alert_type: 'critical', 'warning', or 'info'
        title: Alert title
        description: Alert description
        timestamp: Optional timestamp
    """
    icons = {"critical": "🚨", "warning": "⚠️", "info": "ℹ️"}

    icon = icons.get(alert_type, "ℹ️")
    timestamp_str = f" - {timestamp.strftime('%H:%M')}" if timestamp else ""

    st.markdown(
        f"""
        <div class="alert-{alert_type}">
            <strong>{icon} {title}</strong>{timestamp_str}<br>
            {description}
        </div>
    """,
        unsafe_allow_html=True,
    )


def render_funnel_chart(stages, values, title="Funnel de Conversión"):
    """
    Render a funnel chart

    Args:
        stages: List of stage names
        values: List of values for each stage
        title: Chart title
    """
    fig = go.Figure(
        go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker={
                "color": [
                    COLORS["info"],
                    COLORS["primary"],
                    COLORS["warning"],
                    COLORS["success"],
                ]
            },
        )
    )

    fig.update_layout(title=title, height=400)

    st.plotly_chart(fig, use_container_width=True)


def render_trend_chart(df, x_col, y_col, title, color=None, height=350):
    """
    Render a line/area trend chart

    Args:
        df: DataFrame with data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        color: Optional color
        height: Chart height (default 350)
    """
    fig = px.line(df, x=x_col, y=y_col, title=title, markers=True)

    if color:
        fig.update_traces(line_color=color, fill="tozeroy")

    fig.update_layout(height=height, xaxis_title="", yaxis_title="")

    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(df, x_col, y_col, title, color=None, orientation="v"):
    """
    Render a bar chart
    """
    fig = px.bar(
        df,
        x=x_col if orientation == "v" else y_col,
        y=y_col if orientation == "v" else x_col,
        title=title,
        orientation=orientation,
        color_discrete_sequence=[color or COLORS["primary"]],
    )

    fig.update_layout(height=400, xaxis_title="", yaxis_title="")

    st.plotly_chart(fig, use_container_width=True)


def render_agent_status_badge(conversion, nps):
    """
    Determine and render agent status badge

    Returns:
        Status emoji and text
    """
    if conversion >= THRESHOLDS["conversion_good"] and nps >= THRESHOLDS["nps_good"]:
        return "🔥 Excelente"
    elif (
        conversion >= THRESHOLDS["conversion_warning"]
        and nps >= THRESHOLDS["nps_warning"]
    ):
        return "⭐ Bueno"
    elif (
        conversion < THRESHOLDS["conversion_warning"] or nps < THRESHOLDS["nps_warning"]
    ):
        return "⚠️ Atención"
    else:
        return "✅ Regular"


def render_ranking_table(df, title="Ranking"):
    """
    Render a styled ranking table
    """
    st.subheader(title)

    # Style the dataframe
    styled_df = df.style.background_gradient(
        subset=["conversion", "nps"], cmap="RdYlGn", vmin=0, vmax=100
    ).format(
        {"conversion": "{:.1%}", "nps": "{:.0f}", "noshow": "{:.1%}", "sales": "{:.0f}"}
    )

    st.dataframe(styled_df, use_container_width=True, height=400)


def render_kpi_grid(kpis, columns=4):
    """
    Render a grid of KPI cards

    Args:
        kpis: List of dicts with 'label', 'value', 'delta', 'format'
        columns: Number of columns in grid
    """
    cols = st.columns(columns)

    for idx, kpi in enumerate(kpis):
        with cols[idx % columns]:
            render_kpi_card(
                label=kpi.get("label"),
                value=kpi.get("value"),
                delta=kpi.get("delta"),
                delta_color=kpi.get("delta_color", "normal"),
                format_str=kpi.get("format"),
            )


def render_global_filters():
    """
    Render unified sidebar filters for all management views.
    Uses 'global_' prefix for session state keys to share context.
    """
    from config import COUNTRIES, PERIOD_OPTIONS, REGIONS_HUBS

    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📊 Filtros Globales")

        # 1. Country Selection
        # Set default if not exists
        if "global_country" not in st.session_state:
            st.session_state.global_country = "Todos"

        country_options = ["Todos"] + COUNTRIES
        try:
            country_index = country_options.index(st.session_state.global_country)
        except ValueError:
            country_index = 0

        country = st.selectbox(
            "País", country_options, index=country_index, key="global_country"
        )

        # 2. Region Selection
        region_options = ["Todos"]
        if country != "Todos":
            region_list = list(REGIONS_HUBS.get(country, {}).keys())
            region_options += region_list

        # Ensure selected region is valid
        if (
            "global_region" not in st.session_state
            or st.session_state.global_region not in region_options
        ):
            st.session_state.global_region = "Todos"

        try:
            region_index = region_options.index(st.session_state.global_region)
        except ValueError:
            region_index = 0

        region = st.selectbox(
            "Región", region_options, index=region_index, key="global_region"
        )

        # 3. Hub Selection
        hub_options = ["Todos los Hubs"]
        if country != "Todos" and region != "Todos":
            if region in REGIONS_HUBS.get(country, {}):
                hub_options += REGIONS_HUBS[country][region]

        # Ensure selected hub is valid
        if (
            "global_hub" not in st.session_state
            or st.session_state.global_hub not in hub_options
        ):
            st.session_state.global_hub = "Todos los Hubs"

        try:
            hub_index = hub_options.index(st.session_state.global_hub)
        except ValueError:
            hub_index = 0

        hub = st.selectbox("Hub", hub_options, index=hub_index, key="global_hub")

        # 4. Period Selection
        period_options = list(PERIOD_OPTIONS.keys())
        if "global_period" not in st.session_state:
            st.session_state.global_period = "Últimos 30 días"

        try:
            period_index = period_options.index(st.session_state.global_period)
        except ValueError:
            period_index = 0

        period = st.selectbox(
            "Periodo", period_options, index=period_index, key="global_period"
        )

        st.markdown("---")
        if st.button("🔄 Actualizar Todo", type="primary", use_container_width=True):
            st.rerun()
