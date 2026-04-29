"""
⚡ Torvix Energy — Solar Optimizer
Universidad de Costa Rica · Modelos de Optimización Industrial · I Ciclo 2026
David Alfredo Valdivia Williams - C4L974
Roger Alejandro Toruño Gutierrez - C4K365
"""
import streamlit as st
import pandas as pd
from modelo import resolver, analizar_viabilidad, HSP, VIDA_UTIL, DEGRADACION

st.set_page_config(
    page_title='Torvix Energy · Solar Optimizer',
    page_icon='⚡',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}

/* ── Background ── */
.stApp { background: #07070f; color: #cbd5e1; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1e1e2e; border-radius: 99px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0b0b16 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] label {
    color: #64748b !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}
[data-testid="stSidebar"] p { color: #334155 !important; font-size: 0.72rem !important; }
[data-testid="stSidebar"] input[type="number"] {
    background: #0f0f1c !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] input[type="number"]:focus {
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,0.15) !important;
}

/* ── Brand sidebar header ── */
.sidebar-brand {
    background: linear-gradient(135deg, #0f0a2e 0%, #150f3a 100%);
    border-bottom: 1px solid rgba(139,92,246,0.2);
    padding: 1.4rem 1.2rem 1.2rem;
    margin: -1rem -1rem 1.2rem -1rem;
}
.sidebar-brand .logo { font-size: 1.15rem; font-weight: 800; letter-spacing: -0.03em; color: #f1f5f9; }
.sidebar-brand .logo span { color: #8b5cf6; }
.sidebar-brand .tagline { font-size: 0.68rem; color: #475569; margin-top: 0.2rem; letter-spacing: 0.04em; text-transform: uppercase; }

/* ── Sidebar section labels ── */
.sb-section {
    font-size: 0.62rem; font-weight: 700; color: #2d3748;
    letter-spacing: 0.14em; text-transform: uppercase;
    margin: 1.4rem 0 0.5rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

/* ── Run button ── */
.stButton > button {
    background: linear-gradient(135deg, #6d28d9, #7c3aed) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: 0.88rem !important; padding: 0.7rem 1.5rem !important;
    width: 100% !important; letter-spacing: 0.02em !important;
    transition: all 0.15s !important;
    box-shadow: 0 4px 20px rgba(109,40,217,0.35) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #7c3aed, #8b5cf6) !important;
    box-shadow: 0 4px 28px rgba(109,40,217,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Hero header ── */
.hero {
    display: flex; align-items: flex-start; justify-content: space-between;
    padding: 2rem 0 1.8rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 2rem;
}
.hero-left .wordmark { font-size: 2rem; font-weight: 800; letter-spacing: -0.04em; color: #f8fafc; line-height: 1; }
.hero-left .wordmark span { color: #8b5cf6; }
.hero-left .subtitle { font-size: 0.78rem; color: #475569; margin-top: 0.4rem; }
.hero-right { display: flex; flex-direction: column; align-items: flex-end; gap: 0.3rem; }
.status-pill {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2);
    color: #4ade80; font-size: 0.7rem; font-weight: 600;
    padding: 0.25rem 0.75rem; border-radius: 99px; letter-spacing: 0.04em;
}
.status-pill::before {
    content: ''; width: 6px; height: 6px; background: #4ade80;
    border-radius: 50%; display: inline-block; animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }
.hero-meta { font-size: 0.68rem; color: #334155; letter-spacing: 0.02em; }

/* ── KPI cards ── */
.kpi {
    background: #0e0e1c; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 1.3rem 1.5rem;
    position: relative; overflow: hidden;
    transition: border-color 0.15s, transform 0.15s;
}
.kpi:hover { border-color: rgba(139,92,246,0.35); transform: translateY(-2px); }
.kpi::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.5), transparent);
    opacity: 0; transition: opacity 0.2s;
}
.kpi:hover::after { opacity: 1; }
.kpi .k-label { font-size: 0.65rem; font-weight: 600; color: #475569; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.55rem; }
.kpi .k-value { font-size: 1.7rem; font-weight: 700; color: #f1f5f9; line-height: 1; letter-spacing: -0.025em; }
.kpi .k-value.violet { color: #a78bfa; }
.kpi .k-value.green  { color: #4ade80; }
.kpi .k-value.amber  { color: #fbbf24; }
.kpi .k-value.red    { color: #f87171; }
.kpi .k-unit { font-size: 0.72rem; color: #334155; margin-top: 0.3rem; }

/* ── Card ── */
.card { background: #0e0e1c; border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 1.5rem 1.6rem; margin-bottom: 1rem; }
.card-title { font-size: 0.65rem; font-weight: 700; color: #334155; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 1.1rem; padding-bottom: 0.7rem; border-bottom: 1px solid rgba(255,255,255,0.04); }

/* ── Formula ── */
.formula { background: rgba(109,40,217,0.08); border-left: 2px solid #6d28d9; padding: 0.55rem 1rem; border-radius: 0 8px 8px 0; font-family: 'Courier New', monospace; font-size: 0.85rem; color: #c4b5fd; margin: 0.35rem 0; }

/* ── Restriction rows ── */
.rrow { display: flex; gap: 0.7rem; align-items: flex-start; padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.03); }
.rrow:last-child { border-bottom: none; }
.rlabel { background: rgba(109,40,217,0.1); color: #8b5cf6; border: 1px solid rgba(109,40,217,0.2); padding: 0.12rem 0.5rem; border-radius: 5px; font-size: 0.62rem; font-weight: 700; white-space: nowrap; letter-spacing: 0.05em; min-width: 80px; text-align: center; margin-top: 2px; }

/* ── Badges ── */
.badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.3rem 0.85rem; border-radius: 99px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.01em; }
.badge-ok   { background: rgba(34,197,94,0.08);   color: #4ade80; border: 1px solid rgba(34,197,94,0.2); }
.badge-warn { background: rgba(251,191,36,0.08);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.2); }
.badge-err  { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }

/* ── Info rows ── */
.info-row { display: flex; justify-content: space-between; align-items: center; padding: 0.55rem 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 0.82rem; }
.info-row:last-child { border-bottom: none; }
.info-key { color: #475569; }
.info-val { color: #e2e8f0; font-weight: 500; }

/* ── Progress bar ── */
.prog-wrap { background: rgba(255,255,255,0.04); border-radius: 99px; height: 6px; margin: 0.5rem 0 0.25rem; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #6d28d9, #8b5cf6); }
.prog-label { font-size: 0.68rem; color: #475569; display: flex; justify-content: space-between; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 0; background: transparent !important; border-bottom: 1px solid rgba(255,255,255,0.06) !important; padding: 0; }
.stTabs [data-baseweb="tab"] { font-size: 0.8rem !important; font-weight: 500 !important; color: #475569 !important; padding: 0.6rem 1.2rem !important; border-radius: 0 !important; background: transparent !important; border: none !important; }
.stTabs [aria-selected="true"] { color: #a78bfa !important; font-weight: 600 !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #7c3aed !important; height: 2px !important; }

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; font-size: 0.82rem !important; }

/* ── Misc ── */
hr { border-color: rgba(255,255,255,0.04) !important; margin: 1.5rem 0 !important; }
div[data-testid="stMetricValue"] { font-family: 'Inter', sans-serif !important; color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">Torv<span>ix</span> Energy</div>
        <div class="tagline">Solar Optimization Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Propiedad</div>', unsafe_allow_html=True)
    area = st.number_input("Área del techo disponible (m²)", min_value=10.0, max_value=1000.0, value=150.0, step=5.0, help="Área útil del techo donde se instalarán los paneles.")
    consumo_mensual = st.number_input("Consumo eléctrico mensual (kWh)", min_value=10.0, max_value=5000.0, value=280.0, step=10.0, help="Puedes consultarlo en tu factura del ICE.")

    st.markdown('<div class="sb-section">Tarifa eléctrica</div>', unsafe_allow_html=True)
    moneda = st.radio("Moneda", options=["Colones (₡/kWh)", "Dólares ($/kWh)"], horizontal=True)

    if moneda == "Colones (₡/kWh)":
        tarifa_crc = st.number_input("Tarifa (₡/kWh)", min_value=1.0, max_value=500.0, value=59.88, step=1.0, help="Tarifa ICE residencial aprox. ₡59.88/kWh (2025).")
        tipo_cambio = st.number_input("Tipo de cambio (₡ por $)", min_value=100.0, max_value=1500.0, value=520.0, step=5.0)
        tarifa_usd = tarifa_crc / tipo_cambio
        st.caption(f"Equivalente: **\${tarifa_usd:.4f} USD/kWh**")
    else:
        tarifa_usd = st.number_input("Tarifa ($/kWh)", min_value=0.01, max_value=1.0, value=0.115, step=0.005, format="%.4f")
        tipo_cambio = None

    st.markdown('<div class="sb-section">Opciones avanzadas</div>', unsafe_allow_html=True)
    limitar_inv = st.checkbox("Limitar inversión máxima")
    inversion_max = None
    if limitar_inv:
        inversion_max = st.number_input("Inversión máxima (USD)", min_value=100, max_value=100_000, value=3000, step=100)

    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("⚡ Ejecutar optimización")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.65rem;color:#1e293b;line-height:1.6">UCR · Modelos de Optimización Industrial · I Ciclo 2026<br>D. Valdivia C4L974 · R. Toruño C4K365</p>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATOS DERIVADOS + HELPERS
# ══════════════════════════════════════════════════════════════════════════════
consumo_diario = round(consumo_mensual / 30.44, 4)

def kpi(label, value, unit, color=""):
    cls = f"k-value {color}".strip()
    return f'<div class="kpi"><div class="k-label">{label}</div><div class="{cls}">{value}</div><div class="k-unit">{unit}</div></div>'

def irow(key, val):
    return f'<div class="info-row"><span class="info-key">{key}</span><span class="info-val">{val}</span></div>'


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-left">
    <div class="wordmark">Torv<span>ix</span> Energy</div>
    <div class="subtitle">Solar Optimization Platform &nbsp;·&nbsp; Programación Lineal Entera &nbsp;·&nbsp; {area} m² &nbsp;·&nbsp; {consumo_mensual} kWh/mes</div>
  </div>
  <div class="hero-right">
    <div class="status-pill">SISTEMA ACTIVO</div>
    <div class="hero-meta">UCR · Optimización Industrial · I Ciclo 2026</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TABS  (orden: Solución → Viabilidad → Modelo)
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "⚡  Solución Óptima",
    "📈  Viabilidad Financiera",
    "∑   Modelo Matemático",
])

# ── Variables compartidas entre tabs ─────────────────────────────────────────
res  = {}
viab = {}


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — SOLUCIÓN ÓPTIMA
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    if not run:
        st.info("Configura los parámetros en el panel izquierdo y presiona **⚡ Ejecutar optimización**.")
    else:
        res = resolver(area_disponible=area, demanda_diaria=consumo_diario, max_inversion=inversion_max)

        if not res['es_optimo']:
            st.error(f"No se encontró solución factible (status: **{res['status']}**). Intenta aumentar el área, reducir el consumo o ajustar el presupuesto.")
        else:
            total_paneles = res['xa'] + res['xb'] + res['xc']
            area_usada    = res['xa']*1.9 + res['xb']*2.1 + res['xc']*2.5
            pct_area      = area_usada / area * 100
            superavit     = res['superavit_diario']

            viab = analizar_viabilidad(inversion=res['inversion'], consumo_mensual_kwh=consumo_mensual, tarifa_kwh_usd=tarifa_usd)

            badge_html = (
                f'<span class="badge badge-ok">✅ Financieramente viable — recuperación en ~{viab["anio_recuperacion"]} años</span>'
                if viab['inversion_recuperada'] else
                '<span class="badge badge-warn">⚠️ No se recupera la inversión en 20 años</span>'
            )
            st.markdown(f'<div style="margin-bottom:1.2rem">Solución óptima encontrada &nbsp; {badge_html}</div>', unsafe_allow_html=True)

            # KPIs fila 1
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(kpi("Inversión mínima",  f"${res['inversion']:,.0f}", "USD", "violet"), unsafe_allow_html=True)
            c2.markdown(kpi("Paneles tipo A",     res['xa'], "unidades · 400 W"), unsafe_allow_html=True)
            c3.markdown(kpi("Paneles tipo B",     res['xb'], "unidades · 450 W"), unsafe_allow_html=True)
            c4.markdown(kpi("Paneles tipo C",     res['xc'], "unidades · 550 W"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # KPIs fila 2
            c5, c6, c7, c8 = st.columns(4)
            c5.markdown(kpi("Total paneles",      total_paneles, "unidades instaladas"), unsafe_allow_html=True)
            c6.markdown(kpi("Área utilizada",     f"{area_usada:.1f}", f"de {area} m² · {pct_area:.0f}%"), unsafe_allow_html=True)
            c7.markdown(kpi("Generación diaria",  f"{res['generacion_diaria']:.2f}", "kWh / día"), unsafe_allow_html=True)
            sup_color = "green" if superavit >= 0 else "red"
            c8.markdown(kpi("Superávit diario",   f"{superavit:+.2f}", "kWh / día", sup_color), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col_left, col_right = st.columns([1, 1], gap="large")

            with col_left:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Distribución de paneles instalados</div>', unsafe_allow_html=True)
                df_bar = pd.DataFrame({'Unidades': [res['xa'], res['xb'], res['xc']]}, index=['Panel A · 400W', 'Panel B · 450W', 'Panel C · 550W'])
                st.bar_chart(df_bar, color='#7c3aed', use_container_width=True, height=200)
                st.markdown(
                    f'<div class="prog-label"><span>Aprovechamiento del techo</span><span>{area_usada:.1f} / {area} m²</span></div>'
                    f'<div class="prog-wrap"><div class="prog-fill" style="width:{min(pct_area,100):.1f}%"></div></div>',
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with col_right:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Resumen técnico</div>', unsafe_allow_html=True)
                st.markdown(
                    irow("Inversión total",    f"USD ${res['inversion']:,.0f}") +
                    irow("Paneles A · 400W",   f"{res['xa']} ud. × $190 = ${res['xa']*190:,.0f}") +
                    irow("Paneles B · 450W",   f"{res['xb']} ud. × $205 = ${res['xb']*205:,.0f}") +
                    irow("Paneles C · 550W",   f"{res['xc']} ud. × $255 = ${res['xc']*255:,.0f}") +
                    irow("Generación diaria",  f"{res['generacion_diaria']:.2f} kWh") +
                    irow("Demanda diaria",     f"{res['demanda_diaria']:.2f} kWh") +
                    irow("Superávit",          f"{superavit:+.2f} kWh/día") +
                    irow("Área utilizada",     f"{area_usada:.1f} m² ({pct_area:.0f}%)") +
                    irow("Horas solares pico", f"{HSP} h/día") +
                    irow("Tarifa aplicada",    f"${tarifa_usd:.4f}/kWh"),
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Interpretación</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div style="font-size:0.82rem;color:#94a3b8;line-height:1.75">'
                    f'La configuración óptima instala <strong style="color:#e2e8f0">{total_paneles} paneles</strong> '
                    f'en <strong style="color:#e2e8f0">{area_usada:.1f} m²</strong>, minimizando la inversión a '
                    f'<strong style="color:#a78bfa">${res["inversion"]:,.0f} USD</strong>. '
                    f'El sistema cubre el 100% de la demanda con un '
                    f'{"<strong style=\'color:#4ade80\'>" if superavit>=0 else "<strong style=\'color:#f87171\'>"}'
                    f'{"superávit" if superavit>=0 else "déficit"} de {abs(superavit):.2f} kWh/día</strong>.'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — VIABILIDAD FINANCIERA
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    if not run:
        st.info("Primero ejecuta la optimización.")
    elif not res.get('es_optimo'):
        st.warning("No hay solución óptima que analizar financieramente.")
    else:
        viab = analizar_viabilidad(inversion=res['inversion'], consumo_mensual_kwh=consumo_mensual, tarifa_kwh_usd=tarifa_usd)
        rentab = viab['rentabilidad_neta']

        # KPIs financieros
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(kpi("Inversión inicial",        f"${res['inversion']:,.0f}", "USD"), unsafe_allow_html=True)
        c2.markdown(kpi("Ahorro mensual",            f"${viab['ahorro_mensual_inicial']:.2f}", "USD / mes"), unsafe_allow_html=True)
        c3.markdown(kpi("Ahorro acumulado · 20 años",f"${viab['ahorro_acumulado_20_anios']:,.0f}", "USD"), unsafe_allow_html=True)
        c4.markdown(kpi("Rentabilidad neta", f"{'+'if rentab>=0 else ''}${rentab:,.0f}", "USD en 20 años", "green" if rentab>=0 else "red"), unsafe_allow_html=True)

        # KPIs en colones si aplica
        if moneda == "Colones (₡/kWh)" and tipo_cambio:
            st.markdown("<br>", unsafe_allow_html=True)
            ce1, ce2, ce3, _ = st.columns(4)
            ce1.markdown(kpi("Ahorro mensual",           f"₡{viab['ahorro_mensual_inicial']*tipo_cambio:,.0f}", "colones / mes"), unsafe_allow_html=True)
            ce2.markdown(kpi("Ahorro acumulado · 20 años",f"₡{viab['ahorro_acumulado_20_anios']*tipo_cambio:,.0f}", "colones"), unsafe_allow_html=True)
            ce3.markdown(kpi("Rentabilidad neta", f"₡{rentab*tipo_cambio:,.0f}", "colones en 20 años", "green" if rentab>=0 else "red"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_g, col_d = st.columns([3, 2], gap="large")

        with col_g:
            años = list(range(0, VIDA_UTIL + 1))
            acum = [0.0]
            ahorro_anual_base = viab['ahorro_mensual_inicial'] * 12
            for a in range(1, VIDA_UTIL + 1):
                factor = (1 - DEGRADACION) ** (a - 1)
                acum.append(acum[-1] + ahorro_anual_base * factor)

            df_linea = pd.DataFrame({
                'Ahorro acumulado (USD)':  acum,
                'Inversión inicial (USD)': [res['inversion']] * len(años),
            }, index=años)
            df_linea.index.name = 'Año'

            st.markdown('<div class="card-title">Curva de recuperación de inversión (20 años)</div>', unsafe_allow_html=True)
            st.line_chart(df_linea, color=['#7c3aed', '#f59e0b'], use_container_width=True, height=300)

        with col_d:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Proyección por año (selección)</div>', unsafe_allow_html=True)
            rows_proj = []
            for a in range(2, VIDA_UTIL + 1, 2):
                rows_proj.append({
                    "Año": a,
                    "Ahorro anual (USD)": f"${ahorro_anual_base * (1-DEGRADACION)**(a-1):,.0f}",
                    "Acumulado (USD)":    f"${acum[a]:,.0f}",
                    "¿Pagado?":           "✅" if acum[a] >= res['inversion'] else "—",
                })
            st.dataframe(pd.DataFrame(rows_proj), hide_index=True, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Conclusión
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Conclusión financiera</div>', unsafe_allow_html=True)
        if viab['inversion_recuperada']:
            st.markdown('<span class="badge badge-ok" style="margin-bottom:0.8rem;display:inline-flex">✅ Proyecto financieramente viable</span>', unsafe_allow_html=True)
            st.markdown(
                f'<div style="font-size:0.83rem;color:#94a3b8;line-height:1.8">'
                f'Con una inversión de <strong style="color:#e2e8f0">${res["inversion"]:,.0f} USD</strong> '
                f'y un ahorro mensual de <strong style="color:#e2e8f0">${viab["ahorro_mensual_inicial"]:.2f} USD/mes</strong>, '
                f'el sistema se paga en <strong style="color:#a78bfa">~{viab["anio_recuperacion"]} años</strong>. '
                f'La rentabilidad neta al cabo de 20 años es <strong style="color:#4ade80">${viab["rentabilidad_neta"]:,.0f} USD</strong>.'
                f'</div>', unsafe_allow_html=True,
            )
        else:
            st.markdown('<span class="badge badge-warn" style="margin-bottom:0.8rem;display:inline-flex">⚠️ Inversión no recuperada en 20 años</span>', unsafe_allow_html=True)
            st.markdown(
                f'<div style="font-size:0.83rem;color:#94a3b8;line-height:1.8">'
                f'El ahorro acumulado proyectado <strong style="color:#e2e8f0">(${viab["ahorro_acumulado_20_anios"]:,.0f} USD)</strong> '
                f'no alcanza la inversión inicial <strong style="color:#e2e8f0">(${res["inversion"]:,.0f} USD)</strong>. '
                f'Considera revisar la tarifa eléctrica o aumentar el área disponible.'
                f'</div>', unsafe_allow_html=True,
            )
        st.markdown('<div style="margin-top:0.8rem;font-size:0.7rem;color:#334155">⚠ Este análisis no incluye VPN ni tasa de descuento. Se aplica degradación anual del 0.5%.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — MODELO MATEMÁTICO
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Variables de decisión</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Variable":    ["Xₐ", "X_b", "X_c"],
            "Descripción": ["Paneles tipo A · 400 W", "Paneles tipo B · 450 W", "Paneles tipo C · 550 W"],
            "Dominio":     ["ℤ ≥ 0", "ℤ ≥ 0", "ℤ ≥ 0"],
        }), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Catálogo de paneles</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Tipo":             ["A", "B", "C"],
            "Potencia (W)":     [400, 450, 550],
            "Área (m²)":        [1.9, 2.1, 2.5],
            "Costo (USD)":      [190, 205, 255],
            "W / m²":           [round(400/1.9,1), round(450/2.1,1), round(550/2.5,1)],
            "Gen. diaria (kWh)":[round(400*HSP/1000,2), round(450*HSP/1000,2), round(550*HSP/1000,2)],
        }), hide_index=True, use_container_width=True)
        st.caption(f"* Con {HSP} HSP diarias")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Parámetros de la instancia actual</div>', unsafe_allow_html=True)
        st.markdown(
            irow("Área disponible",    f"{area} m²") +
            irow("Consumo mensual",    f"{consumo_mensual} kWh/mes") +
            irow("Demanda diaria (D)", f"{consumo_diario} kWh/día") +
            irow("Tarifa eléctrica",   f"${tarifa_usd:.4f} USD/kWh") +
            irow("HSP",                f"{HSP} h/día") +
            irow("Vida útil",          f"{VIDA_UTIL} años") +
            irow("Degradación anual",  "0.5%"),
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Función objetivo</div>', unsafe_allow_html=True)
        st.markdown('<div class="formula">Min Z = 190·Xₐ + 205·X_b + 255·X_c</div>', unsafe_allow_html=True)
        st.caption("Minimizar la inversión inicial total en dólares (USD).")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Restricciones del modelo</div>', unsafe_allow_html=True)
        restr = [
            ("R1 · Energía",   f"(400·Xₐ + 450·X_b + 550·X_c)·{HSP}/1000  ≥  {consumo_diario}", f"Generación mínima diaria: {consumo_diario} kWh"),
            ("R2 · Área",      f"1.9·Xₐ + 2.1·X_b + 2.5·X_c  ≤  {area}",                       f"Área máxima: {area} m²"),
            ("R3 · Integridad", "Xₐ, X_b, X_c  ∈  ℤ",                                            "Solo paneles completos (PLE)"),
            ("R4 · No-neg.",   "Xₐ, X_b, X_c  ≥  0",                                             "Sin cantidades negativas"),
        ]
        if inversion_max:
            restr.append(("R5 · Presup.", f"190·Xₐ + 205·X_b + 255·X_c  ≤  {inversion_max}", f"Presupuesto máximo: ${inversion_max:,}"))
        for lbl, formula, desc in restr:
            st.markdown(
                f'<div class="rrow"><span class="rlabel">{lbl}</span>'
                f'<div><div class="formula" style="margin:0">{formula}</div>'
                f'<div style="color:#334155;font-size:0.7rem;margin-top:0.2rem">{desc}</div></div></div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Premisas del modelo</div>', unsafe_allow_html=True)
        for titulo, desc in [
            ("☀️ Radiación constante",  f"{HSP} HSP diarias fijas, sin variaciones estacionales."),
            ("🏠 Techo ideal",           "Área 100% aprovechable, sin obstáculos ni sombras."),
            ("⚡ Demanda estacionaria",  "Consumo diario constante durante toda la vida útil."),
            ("🔢 Programación entera",  "Variables enteras; no se instalan fracciones de paneles."),
            ("📉 Degradación",          "0.5% anual únicamente en el análisis financiero."),
        ]:
            st.markdown(
                f'<div style="margin-bottom:0.65rem">'
                f'<div style="font-size:0.77rem;font-weight:600;color:#64748b">{titulo}</div>'
                f'<div style="font-size:0.73rem;color:#334155;margin-top:0.1rem">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#1e293b;font-size:0.68rem;letter-spacing:0.04em">'
    'TORVIX ENERGY &nbsp;·&nbsp; Universidad de Costa Rica &nbsp;·&nbsp; '
    'Modelos de Optimización Industrial &nbsp;·&nbsp; I Ciclo 2026 &nbsp;·&nbsp; '
    'David Alfredo Valdivia Williams C4L974 &nbsp;·&nbsp; Roger Alejandro Toruño Gutiérrez C4K365'
    '</div>',
    unsafe_allow_html=True,
)
