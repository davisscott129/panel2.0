"""
☀️  Optimizador de Paneles Solares — UCR Modelos de Optimización Industrial
David Alfredo Valdivia Williams - C4L974
Roger Alejandro Toruño Gutierrez - C4K365
"""
import streamlit as st
import pandas as pd
from modelo import resolver, analizar_viabilidad, PANELES, HSP, VIDA_UTIL, DEGRADACION

# ─── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title='Solar Optimizer · UCR',
    page_icon='☀️',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ─── CSS minimalista ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Fondo */
.stApp {
    background: #0a0a0f;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #64748b;
    font-size: 0.75rem;
}

/* Header */
.hero {
    padding: 2rem 0 1.5rem 0;
    margin-bottom: 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.hero h1 {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
    letter-spacing: -0.03em;
    margin: 0 0 0.25rem 0 !important;
}
.hero p {
    color: #475569;
    font-size: 0.82rem;
    margin: 0;
}
.hero .dot { color: #334155; margin: 0 0.4rem; }

/* Metric cards */
.metric-card {
    background: #13131f;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.25rem 1.4rem;
    transition: border-color 0.15s;
}
.metric-card:hover { border-color: rgba(99,102,241,0.4); }
.metric-card .label {
    font-size: 0.7rem;
    color: #64748b;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.metric-card .value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1;
    letter-spacing: -0.02em;
}
.metric-card .unit {
    font-size: 0.75rem;
    color: #475569;
    margin-top: 0.3rem;
}
.metric-card .accent { color: #818cf8; }

/* Badges */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.9rem;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.01em;
}
.badge-ok   { background: rgba(34,197,94,0.1);  color: #4ade80; border: 1px solid rgba(34,197,94,0.25); }
.badge-warn { background: rgba(234,179,8,0.1);  color: #facc15; border: 1px solid rgba(234,179,8,0.25); }
.badge-err  { background: rgba(239,68,68,0.1);  color: #f87171; border: 1px solid rgba(239,68,68,0.25); }

/* Section block */
.block {
    background: #13131f;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.block-title {
    font-size: 0.72rem;
    font-weight: 600;
    color: #64748b;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* Formula */
.formula {
    background: rgba(99,102,241,0.07);
    border-left: 2px solid #4f46e5;
    padding: 0.6rem 1rem;
    border-radius: 0 8px 8px 0;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    color: #c7d2fe;
    margin: 0.4rem 0;
}

/* Restrict rows */
.rrow {
    display: flex;
    gap: 0.7rem;
    align-items: flex-start;
    padding: 0.65rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.rlabel {
    background: rgba(99,102,241,0.1);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.2);
    padding: 0.15rem 0.55rem;
    border-radius: 6px;
    font-size: 0.68rem;
    font-weight: 700;
    white-space: nowrap;
    letter-spacing: 0.03em;
}

/* Main button */
.stButton>button {
    background: #4f46e5 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    letter-spacing: 0.01em;
    transition: opacity 0.15s !important;
}
.stButton>button:hover { opacity: 0.85 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    padding: 0.5rem 1rem !important;
    border-radius: 6px 6px 0 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #818cf8 !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background-color: #4f46e5 !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.05) !important; }

/* Alerts */
.stAlert { border-radius: 10px !important; }

/* Sidebar section title */
.sidebar-section {
    font-size: 0.68rem;
    font-weight: 700;
    color: #334155;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 1.2rem 0 0.6rem 0;
}

div[data-testid="stMetricValue"] {
    font-family: 'Inter', sans-serif !important;
    color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>☀️ Optimizador de Paneles Solares</h1>
  <p>
    Universidad de Costa Rica
    <span class="dot">·</span>
    Modelos de Optimización Industrial
    <span class="dot">·</span>
    I Ciclo 2026
    <span class="dot">·</span>
    David A. Valdivia Williams C4L974
    <span class="dot">·</span>
    Roger A. Toruño Gutiérrez C4K365
  </p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR — Entrada libre de parámetros
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## Parámetros")
    st.markdown("Ingresa los datos de tu propiedad.")

    # ── Geometría y consumo ───────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Propiedad</div>', unsafe_allow_html=True)

    area = st.number_input(
        "Área del techo disponible (m²)",
        min_value=10.0, max_value=1000.0,
        value=150.0, step=5.0,
        help="Área útil del techo donde se instalarán los paneles.",
    )

    consumo_mensual = st.number_input(
        "Consumo eléctrico mensual (kWh)",
        min_value=10.0, max_value=5000.0,
        value=280.0, step=10.0,
        help="Puedes consultar tu factura del ICE.",
    )

    # ── Tarifa eléctrica ─────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Tarifa eléctrica</div>', unsafe_allow_html=True)

    moneda = st.radio(
        "Moneda de la tarifa",
        options=["Colones (₡/kWh)", "Dólares ($/kWh)"],
        horizontal=True,
    )

    if moneda == "Colones (₡/kWh)":
        tarifa_crc = st.number_input(
            "Tarifa (₡/kWh)",
            min_value=1.0, max_value=500.0,
            value=59.88, step=1.0,
            help="Tarifa ICE residencial aprox. ₡59.88/kWh (2025).",
        )
        tipo_cambio = st.number_input(
            "Tipo de cambio (₡ por $)",
            min_value=100.0, max_value=1500.0,
            value=520.0, step=5.0,
        )
        tarifa_usd = tarifa_crc / tipo_cambio
        st.caption(f"Equivalente: **${tarifa_usd:.4f} / kWh**")
    else:
        tarifa_usd = st.number_input(
            "Tarifa ($/kWh)",
            min_value=0.01, max_value=1.0,
            value=0.115, step=0.005, format="%.4f",
        )
        tipo_cambio = None

    # ── Restricción de inversión ─────────────────────────────────────────
    st.markdown('<div class="sidebar-section">Opciones avanzadas</div>', unsafe_allow_html=True)

    limitar_inv = st.checkbox("Limitar inversión máxima")
    inversion_max = None
    if limitar_inv:
        inversion_max = st.number_input(
            "Inversión máxima (USD)",
            min_value=100, max_value=100_000,
            value=3000, step=100,
        )

    st.markdown("")
    run = st.button("Optimizar →")

# ─── Datos derivados ─────────────────────────────────────────────────────────
consumo_diario = round(consumo_mensual / 30.44, 4)

# Helper: render metric card
def mc(label, value, unit, accent=False):
    v_class = 'value accent' if accent else 'value'
    return (
        f'<div class="metric-card">'
        f'<div class="label">{label}</div>'
        f'<div class="{v_class}">{value}</div>'
        f'<div class="unit">{unit}</div>'
        f'</div>'
    )

# ─── Tabs ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Modelo Matemático",
    "Solución Óptima",
    "Viabilidad Financiera",
])


# ═══════════════════════════════════════════════════════════════════════════
# TAB 1 — MODELO MATEMÁTICO
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        # Variables de decisión
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">Variables de decisión</div>', unsafe_allow_html=True)
        vd = pd.DataFrame({
            "Variable": ["Xₐ", "X_b", "X_c"],
            "Descripción": [
                "Paneles tipo A — 400 W",
                "Paneles tipo B — 450 W",
                "Paneles tipo C — 550 W",
            ],
            "Dominio": ["ℤ ≥ 0", "ℤ ≥ 0", "ℤ ≥ 0"],
        })
        st.dataframe(vd, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Características de paneles
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">Características de paneles</div>', unsafe_allow_html=True)
        dp = pd.DataFrame({
            "Tipo": ["A", "B", "C"],
            "Potencia (W)": [400, 450, 550],
            "Área (m²)": [1.9, 2.1, 2.5],
            "Costo (USD)": [190, 205, 255],
            "Gen. diaria (kWh)*": [
                round(400 * HSP / 1000, 2),
                round(450 * HSP / 1000, 2),
                round(550 * HSP / 1000, 2),
            ],
        })
        st.dataframe(dp, hide_index=True, use_container_width=True)
        st.caption(f"* Con {HSP} HSP (Horas Solares Pico diarias)")
        st.markdown('</div>', unsafe_allow_html=True)

        # Parámetros actuales
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">Parámetros actuales</div>', unsafe_allow_html=True)
        params_df = pd.DataFrame({
            "Parámetro": ["Área disponible", "Demanda diaria", "Consumo mensual", "Tarifa eléctrica", "HSP", "Vida útil"],
            "Valor": [
                f"{area} m²",
                f"{consumo_diario} kWh/día",
                f"{consumo_mensual} kWh/mes",
                f"${tarifa_usd:.4f}/kWh",
                f"{HSP} h",
                f"{VIDA_UTIL} años",
            ],
        })
        st.dataframe(params_df, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        # Función objetivo
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">Función objetivo</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="formula">Min Z = 190·Xₐ + 205·X_b + 255·X_c</div>',
            unsafe_allow_html=True,
        )
        st.caption("Minimizar la inversión inicial total en dólares (USD).")
        st.markdown('</div>', unsafe_allow_html=True)

        # Restricciones
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">Restricciones</div>', unsafe_allow_html=True)

        restr = [
            ("R1 Energía",
             f"(400·Xₐ + 450·X_b + 550·X_c) · {HSP}/1000  ≥  {consumo_diario}",
             f"Generación mínima diaria: {consumo_diario} kWh/día"),
            ("R2 Área",
             f"1.9·Xₐ + 2.1·X_b + 2.5·X_c  ≤  {area}",
             f"Área máxima disponible: {area} m²"),
            ("R3 Integridad",
             "Xₐ, X_b, X_c  ∈  ℤ",
             "Solo se instalan paneles completos"),
            ("R4 No-neg.",
             "Xₐ, X_b, X_c  ≥  0",
             "No se permiten cantidades negativas"),
        ]
        if inversion_max:
            restr.append(("R5 Inversión",
                          f"190·Xₐ + 205·X_b + 255·X_c  ≤  {inversion_max}",
                          f"Presupuesto máximo: USD {inversion_max:,}"))

        for lbl, formula, desc in restr:
            st.markdown(
                f'<div class="rrow">'
                f'<span class="rlabel">{lbl}</span>'
                f'<div><div class="formula" style="margin:0">{formula}</div>'
                f'<div style="color:#475569;font-size:0.75rem;margin-top:0.25rem">{desc}</div></div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Premisas
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">Premisas del modelo</div>', unsafe_allow_html=True)
        premisas = [
            ("☀️ Radiación constante", f"{HSP} HSP fijas, sin variaciones estacionales."),
            ("🏠 Techo ideal", "Área totalmente aprovechable, sin obstáculos ni sombras."),
            ("⚡ Demanda estacionaria", "Consumo diario constante en todo el período."),
            ("📉 Degradación", "0.5% anual aplicado al análisis financiero."),
        ]
        for titulo, desc in premisas:
            st.markdown(
                f'<div style="margin-bottom:0.6rem">'
                f'<span style="font-size:0.78rem;font-weight:600;color:#94a3b8">{titulo}</span>'
                f'<div style="font-size:0.75rem;color:#475569;margin-top:0.15rem">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 2 — SOLUCIÓN ÓPTIMA
# ═══════════════════════════════════════════════════════════════════════════
with tab2:
    if not run:
        st.info("👈 Ajusta los parámetros en el panel izquierdo y presiona **Optimizar →**")
    else:
        res = resolver(
            area_disponible=area,
            demanda_diaria=consumo_diario,
            max_inversion=inversion_max,
        )

        if not res['es_optimo']:
            st.error(
                f"⚠️ No se encontró solución óptima (status: {res['status']}). "
                "Intenta aumentar el área, reducir el consumo o ajustar el presupuesto."
            )
        else:
            st.success(f"✅ Solución óptima encontrada — Status: {res['status']}")

            # KPIs — fila 1
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(mc("Inversión mínima", f"${res['inversion']:,.0f}", "USD", accent=True), unsafe_allow_html=True)
            c2.markdown(mc("Paneles tipo A", res['xa'], "unidades × 400 W"), unsafe_allow_html=True)
            c3.markdown(mc("Paneles tipo B", res['xb'], "unidades × 450 W"), unsafe_allow_html=True)
            c4.markdown(mc("Paneles tipo C", res['xc'], "unidades × 550 W"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # KPIs — fila 2
            c5, c6, c7, c8 = st.columns(4)
            total_paneles = res['xa'] + res['xb'] + res['xc']
            area_usada    = res['xa']*1.9 + res['xb']*2.1 + res['xc']*2.5
            superavit     = res['superavit_diario']

            c5.markdown(mc("Total paneles", total_paneles, "unidades"), unsafe_allow_html=True)
            c6.markdown(mc("Área utilizada", f"{area_usada:.1f}", f"de {area} m²"), unsafe_allow_html=True)
            c7.markdown(mc("Generación diaria", f"{res['generacion_diaria']:.2f}", "kWh/día"), unsafe_allow_html=True)
            c8.markdown(mc("Superávit diario", f"{superavit:+.2f}", "kWh/día"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col_chart, col_interp = st.columns([1, 1], gap="large")

            with col_chart:
                st.markdown('<div class="block-title">Distribución de paneles</div>', unsafe_allow_html=True)
                df_bar = pd.DataFrame(
                    {'Unidades': [res['xa'], res['xb'], res['xc']]},
                    index=['Panel A (400W)', 'Panel B (450W)', 'Panel C (550W)'],
                )
                st.bar_chart(df_bar, color='#4f46e5', use_container_width=True)

            with col_interp:
                st.markdown('<div class="block">', unsafe_allow_html=True)
                st.markdown('<div class="block-title">Interpretación</div>', unsafe_allow_html=True)

                st.markdown(f"""
La solución óptima asigna **{res['xa']} paneles A**, **{res['xb']} paneles B** y **{res['xc']} paneles C**,
con una inversión mínima de **USD ${res['inversion']:,.0f}**.

El sistema genera **{res['generacion_diaria']:.2f} kWh/día**, cubriendo la demanda de
**{res['demanda_diaria']:.2f} kWh/día** con un
{"superávit" if superavit >= 0 else "déficit"} de **{abs(superavit):.2f} kWh/día**.

Se utilizan **{area_usada:.1f} m²** de los **{area} m²** disponibles
({(area_usada/area*100):.1f}% de aprovechamiento).
                """)

                viab = analizar_viabilidad(
                    inversion=res['inversion'],
                    consumo_mensual_kwh=consumo_mensual,
                    tarifa_kwh_usd=tarifa_usd,
                )
                if viab['inversion_recuperada']:
                    st.markdown(
                        f'<span class="badge badge-ok">✅ Viable — recuperación en ~{viab["anio_recuperacion"]} años</span>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        '<span class="badge badge-warn">⚠️ No se recupera la inversión en 20 años</span>',
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 3 — VIABILIDAD FINANCIERA
# ═══════════════════════════════════════════════════════════════════════════
with tab3:
    if not run:
        st.info("👈 Primero ejecuta la optimización.")
    else:
        if not res.get('es_optimo'):
            st.warning("No hay solución óptima que analizar.")
        else:
            viab = analizar_viabilidad(
                inversion=res['inversion'],
                consumo_mensual_kwh=consumo_mensual,
                tarifa_kwh_usd=tarifa_usd,
            )

            # KPIs financieros
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(mc("Inversión inicial", f"${res['inversion']:,.0f}", "USD"), unsafe_allow_html=True)
            c2.markdown(mc("Ahorro mensual", f"${viab['ahorro_mensual_inicial']:.2f}", "USD/mes"), unsafe_allow_html=True)
            c3.markdown(mc("Ahorro acumulado 20 años", f"${viab['ahorro_acumulado_20_anios']:,.0f}", "USD"), unsafe_allow_html=True)
            rentab = viab['rentabilidad_neta']
            c4.markdown(
                mc("Rentabilidad neta", f"{'+'if rentab>=0 else ''}${rentab:,.0f}", "USD en 20 años", accent=rentab>=0),
                unsafe_allow_html=True,
            )

            # Si la tarifa es en colones, mostrar equivalencias
            if moneda == "Colones (₡/kWh)":
                st.markdown("<br>", unsafe_allow_html=True)
                ce1, ce2, ce3 = st.columns(3)
                ce1.markdown(mc("Ahorro mensual", f"₡{viab['ahorro_mensual_inicial']*tipo_cambio:,.0f}", "colones/mes"), unsafe_allow_html=True)
                ce2.markdown(mc("Ahorro acumulado 20 años", f"₡{viab['ahorro_acumulado_20_anios']*tipo_cambio:,.0f}", "colones"), unsafe_allow_html=True)
                ce3.markdown(mc("Rentabilidad neta", f"₡{rentab*tipo_cambio:,.0f}", "colones en 20 años", accent=rentab>=0), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Gráfico de recuperación
            años = list(range(0, VIDA_UTIL + 1))
            acum = [0.0]
            ahorro_inicial = viab['ahorro_mensual_inicial'] * 12
            for a in range(1, VIDA_UTIL + 1):
                factor = (1 - DEGRADACION) ** (a - 1)
                acum.append(acum[-1] + ahorro_inicial * factor)

            inv_line = [res['inversion']] * len(años)
            df_linea = pd.DataFrame({
                'Ahorro acumulado (USD)': acum,
                'Inversión inicial (USD)': inv_line,
            }, index=años)
            df_linea.index.name = 'Año'

            st.markdown('<div class="block-title">Ahorro acumulado vs. inversión (20 años)</div>', unsafe_allow_html=True)
            st.line_chart(df_linea, color=['#4f46e5', '#f59e0b'], use_container_width=True)

            # Conclusión
            st.markdown('<div class="block">', unsafe_allow_html=True)
            st.markdown('<div class="block-title">Conclusión</div>', unsafe_allow_html=True)

            if viab['inversion_recuperada']:
                st.markdown(f"""
**✅ El proyecto es financieramente viable.**

Con una inversión de **USD ${res['inversion']:,.0f}** y un ahorro mensual de **USD ${viab['ahorro_mensual_inicial']:.2f}**,
el sistema se paga en aproximadamente **{viab['anio_recuperacion']} años**,
generando una rentabilidad neta de **USD ${viab['rentabilidad_neta']:,.0f}** al final de la vida útil (20 años).
                """)
            else:
                st.markdown(f"""
**⚠️ El proyecto no recupera la inversión en el horizonte de 20 años.**

El ahorro acumulado proyectado (**USD ${viab['ahorro_acumulado_20_anios']:,.0f}**) es menor
que la inversión inicial (**USD ${res['inversion']:,.0f}**).
Considera aumentar la tarifa de referencia, reducir el área o ajustar el consumo.
                """)

            st.caption(
                "Nota: este análisis no incluye VPN, tasa de descuento ni flujos descontados. "
                "Se aplica únicamente degradación anual del 0.5% en la generación."
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#1e293b;font-size:0.72rem">'
    'Universidad de Costa Rica · Modelos de Optimización Industrial · I Ciclo 2026 · '
    'David Alfredo Valdivia Williams C4L974 · Roger Alejandro Toruño Gutiérrez C4K365'
    '</div>',
    unsafe_allow_html=True,
)
