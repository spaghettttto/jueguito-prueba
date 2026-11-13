import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="El agua en México: Disponibilidad y Desperdicio 💧",
    page_icon="💧",
    layout="centered"
)

st.markdown("""
<style>
.main {
    background-color: #F4F8FB;
}
h1 {
    color: #1B4965;
    text-align: center;
}
h3 {
    color: #62B6CB;
}
/* Estilos para AquaPou */
.header-box {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 18px;
    border: 2px solid #90CAF9;
    text-align: center;
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.12);
    margin-bottom: 15px;
}
.header-title {
    color: #0277BD !important;
    font-size: 2.1rem;
    font-weight: 800;
    margin: 0;
}
.header-subtitle {
    color: #4FC3F7;
    font-size: 1.05rem;
    font-weight: 600;
    margin-top: 5px;
}
.legend-box {
    background-color: #F0F8FF;
    border-left: 5px solid #29B6F6;
    padding: 12px 18px;
    border-radius: 10px;
    color: #01579B;
    font-size: 0.95rem;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("💧 El agua en México: disponibilidad, calidad y desperdicio")

st.write(
    "Aplicación interactiva desarrollada para analizar la situación "
    "hídrica por estados, comprender los indicadores oficiales y "
    "concientizar sobre el consumo en actividades cotidianas."
)

# =====================================================
# 1. DATOS DE LOS ESTADOS
# =====================================================

estados_mexico = sorted([
    "Aguascalientes", "Baja California", "Baja California Sur",
    "Campeche", "Chiapas", "Chihuahua", "Ciudad de México",
    "Coahuila", "Colima", "Durango", "Estado de México",
    "Guanajuato", "Guerrero", "Hidalgo", "Jalisco",
    "Michoacán", "Morelos", "Nayarit", "Nuevo León",
    "Oaxaca", "Puebla", "Querétaro", "Quintana Roo",
    "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco",
    "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán",
    "Zacatecas"
])

periodos = [
    "2006-2010",
    "2011-2015",
    "2016-2020",
    "2021-2025",
    "2026-2030",
    "Dato más reciente disponible"
]

# =====================================================
# 2. DISPONIBILIDAD DE AGUA
# =====================================================

datos_disponibilidad = {
    "Aguascalientes": [420, 390, 360, 340],
    "Baja California": [980, 920, 870, 810],
    "Baja California Sur": [780, 730, 690, 650],
    "Campeche": [18500, 18000, 17500, 16900],
    "Chiapas": [24000, 23200, 22500, 21800],
    "Chihuahua": [1850, 1720, 1610, 1540],
    "Ciudad de México": [160, 150, 140, 130],
    "Coahuila": [1450, 1380, 1310, 1250],
    "Colima": [3200, 3050, 2900, 2780],
    "Durango": [3100, 2950, 2800, 2680],
    "Estado de México": [260, 240, 220, 210],
    "Guanajuato": [680, 630, 590, 550],
    "Guerrero": [5800, 5500, 5200, 4950],
    "Hidalgo": [1950, 1850, 1750, 1680],
    "Jalisco": [1550, 1470, 1390, 1320],
    "Michoacán": [2900, 2750, 2600, 2480],
    "Morelos": [1150, 1080, 1020, 970],
    "Nayarit": [7800, 7400, 7000, 6650],
    "Nuevo León": [1300, 1200, 1100, 1020],
    "Oaxaca": [8500, 8100, 7700, 7300],
    "Puebla": [950, 890, 840, 790],
    "Querétaro": [820, 770, 720, 680],
    "Quintana Roo": [12500, 11800, 11100, 10500],
    "San Luis Potosí": [1650, 1560, 1480, 1400],
    "Sinaloa": [5200, 4900, 4600, 4350],
    "Sonora": [2800, 2650, 2500, 2380],
    "Tabasco": [22000, 21500, 20800, 19900],
    "Tamaulipas": [2100, 1980, 1870, 1780],
    "Tlaxcala": [510, 480, 450, 420],
    "Veracruz": [11500, 10900, 10300, 9800],
    "Yucatán": [9200, 8700, 8200, 7800],
    "Zacatecas": [1250, 1180, 1110, 1050]
}

# =====================================================
# 3. COBERTURA Y POTABILIDAD
# =====================================================

datos_cobertura_potable = {
    "Aguascalientes": (98.8, "Buena (Tratamiento constante)"),
    "Baja California": (97.5, "Aceptable / Alta salinidad en zonas"),
    "Baja California Sur": (95.2, "Moderada (Presencia de minerales)"),
    "Campeche": (89.4, "Aceptable"),
    "Chiapas": (88.8, "Baja en zonas rurales (Riesgo biológico)"),
    "Chihuahua": (98.1, "Buena (Monitoreo continuo de arsénico)"),
    "Ciudad de México": (98.6, "Variable según alcaldía / Red antigua"),
    "Coahuila": (98.4, "Aceptable"),
    "Colima": (99.0, "Buena"),
    "Durango": (96.5, "Moderada (Presencia de flúor en acuíferos)"),
    "Estado de México": (96.2, "Variable / Presión intermitente"),
    "Guanajuato": (96.8, "Moderada (Tratamiento por metales en pozos)"),
    "Guerrero": (87.1, "Baja (Deficiencia en cloración municipal)"),
    "Hidalgo": (94.3, "Aceptable"),
    "Jalisco": (97.8, "Buena en ZMM / Variable en zonas agrícolas"),
    "Michoacán": (94.6, "Aceptable"),
    "Morelos": (96.9, "Buena"),
    "Nayarit": (95.1, "Aceptable"),
    "Nuevo León": (98.9, "Alta (Red automatizada y potabilizada)"),
    "Oaxaca": (85.5, "Baja en zonas rurales (Falta de potabilizadoras)"),
    "Puebla": (94.8, "Aceptable / Vulnerable en cuencas urbanas"),
    "Querétaro": (97.3, "Buena"),
    "Quintana Roo": (97.1, "Aceptable (Monitoreo de dureza y karst)"),
    "San Luis Potosí": (94.2, "Moderada"),
    "Sinaloa": (96.7, "Aceptable"),
    "Sonora": (97.6, "Moderada (Tratamiento en acuíferos del norte)"),
    "Tabasco": (88.2, "Moderada (Alta turbiedad en ríos)"),
    "Tamaulipas": (96.1, "Aceptable"),
    "Tlaxcala": (97.9, "Aceptable"),
    "Veracruz": (89.7, "Variable (Vulnerable a eventos meteorológicos)"),
    "Yucatán": (96.8, "Moderada (Agua dura / Acuífero somero)"),
    "Zacatecas": (96.3, "Moderada")
}

datos_consumo_agua = {
    "Aguascalientes": 680, "Baja California": 2950, "Baja California Sur": 480,
    "Campeche": 510, "Chiapas": 2400, "Chihuahua": 5150,
    "Ciudad de México": 1150, "Coahuila": 2350, "Colima": 1520,
    "Durango": 2100, "Estado de México": 2450, "Guanajuato": 4450,
    "Guerrero": 1350, "Hidalgo": 2650, "Jalisco": 4850,
    "Michoacán": 5400, "Morelos": 1320, "Nayarit": 1680,
    "Nuevo León": 2150, "Oaxaca": 1580, "Puebla": 2250,
    "Querétaro": 1050, "Quintana Roo": 790, "San Luis Potosí": 1540,
    "Sinaloa": 9850, "Sonora": 7200, "Tabasco": 690,
    "Tamaulipas": 4300, "Tlaxcala": 360, "Veracruz": 5600,
    "Yucatán": 1480, "Zacatecas": 1750
}

# =====================================================
# PESTAÑAS PRINCIPALES
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Situación por Estado",
    "🚿 Simulador y Ahorro",
    "🎮 Interactivos",
    "📚 Fuentes"
])

# =====================================================
# TAB 1: CONSULTA POR ESTADO Y MAPA
# =====================================================
with tab1:
    st.subheader("1. Consulta por Estado y Periodo")

    col1, col2 = st.columns(2)

    with col1:
        estado_seleccionado = st.selectbox(
            "Selecciona un estado de México:",
            estados_mexico,
            index=estados_mexico.index("Chihuahua")
        )

    with col2:
        periodo_seleccionado = st.selectbox(
            "Selecciona el periodo:",
            periodos,
            index=3
        )

    st.subheader("2. Indicadores Hídricos y Potabilidad")

    indice_periodo = periodos.index(periodo_seleccionado)

    if indice_periodo < 4:
        disp_valor = datos_disponibilidad[estado_seleccionado][indice_periodo]
    elif indice_periodo == 5:
        disp_valor = datos_disponibilidad[estado_seleccionado][3]
    else:
        disp_valor = "Sin datos disponibles"

    cobertura, potabilidad = datos_cobertura_potable[estado_seleccionado]

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        if isinstance(disp_valor, (int, float)):
            st.metric(
                f"Disponibilidad per cápita ({periodo_seleccionado})",
                f"{disp_valor:,.0f} m³/hab/año"
            )
        else:
            st.metric("Disponibilidad per cápita", disp_valor)

    with col_m2:
        st.metric("Cobertura de Agua Entubada", f"{cobertura}%")

    with col_m3:
        st.metric("Calidad / Potabilidad General", potabilidad)

    st.info("""
    💡 **¿Qué significan estos indicadores?**

    - **Disponibilidad:** Mide el agua renovable total del estado dividida entre su población.
    - **Cobertura:** Porcentaje de hogares conectados a la red pública de agua entubada.
    - **Potabilidad:** Diagnóstico regional sobre la aptitud del agua para uso doméstico y los retos de tratamiento local.
    """)

    st.markdown("---")
    st.subheader("🗺️ Mapa de Consumo Total de Agua por Estado")

    st.write(
        "Visualización geográfica del volumen anual de agua concesionada/consumida "
        "(incluye uso agrícola, público e industrial en millones de m³)."
    )

    df_mapa = pd.DataFrame({
        "Estado": list(datos_consumo_agua.keys()),
        "Consumo_Mm3": list(datos_consumo_agua.values())
    })

    url_geojson = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
    mapa_mexico = alt.Data(
        url=url_geojson,
        format=alt.DataFormat(property="features", type="json")
    )

    fig_mapa = alt.Chart(mapa_mexico).mark_geoshape(
        stroke="white",
        strokeWidth=0.8
    ).encode(
        color=alt.Color(
            "Consumo_Mm3:Q",
            scale=alt.Scale(scheme="blues"),
            title="Consumo (Mm³/año)"
        ),
        tooltip=[
            alt.Tooltip("properties.name:N", title="Estado"),
            alt.Tooltip("Consumo_Mm3:Q", title="Consumo (Mm³/año)", format=",.0f")
        ]
    ).transform_lookup(
        lookup="properties.name",
        from_=alt.LookupData(df_mapa, "Estado", ["Consumo_Mm3"])
    ).project(
        type="mercator"
    ).properties(
        width=650,
        height=420
    ).configure_view(
        strokeWidth=0
    ).configure(
        background="#F4F8FB"
    )

    st.altair_chart(fig_mapa, use_container_width=True)

    estado_max = df_mapa.loc[df_mapa["Consumo_Mm3"].idxmax()]
    consumo_sel = datos_consumo_agua.get(estado_seleccionado, 0)

    st.warning(
        f"📊 **Mayor consumidor a nivel nacional:** **{estado_max['Estado']}** con aproximadamente "
        f"**{estado_max['Consumo_Mm3']:,.0f} millones de m³ al año** (impulsado principalmente por su alta actividad agrícola).\n\n"
        f"📍 **Estado seleccionado ({estado_seleccionado}):** Consume aproximadamente **{consumo_sel:,.0f} millones de m³ al año**."
    )

# =====================================================
# TAB 2: SIMULADOR DE DESPERDICIO Y RETO DE AHORRO
# =====================================================
with tab2:
    st.subheader("3. Simulador de desperdicio en botellas de agua (500 ml)")

    st.write(
        "Calcula cuántas botellas de 500 ml y cuánto dinero equivaldría "
        "el agua que se desperdicia mientras esperas a que salga caliente "
        "en la regadera."
    )

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    with col_s1:
        minutos_espera = st.slider("Minutos de espera:", 0, 10, 3)

    with col_s2:
        caudal_regadera = st.slider("Caudal (Litros/min):", 2, 15, 8)

    with col_s3:
        frecuencia_semanal = st.slider("Duchas por semana:", 1, 14, 7)

    with col_s4:
        costo_botella = st.number_input(
            "Precio por botella de 500 ml ($ MXN):",
            value=15.0,
            step=1.0
        )

    litros_ducha = minutos_espera * caudal_regadera
    litros_semana = litros_ducha * frecuencia_semanal
    litros_mes = litros_semana * 4.33
    litros_anio = litros_semana * 52

    botellas_ducha = litros_ducha * 2
    botellas_semana = litros_semana * 2
    botellas_mes = litros_mes * 2
    botellas_anio = litros_anio * 2

    costo_ducha = botellas_ducha * costo_botella
    costo_semana = botellas_semana * costo_botella
    costo_mes = botellas_mes * costo_botella
    costo_anio = botellas_anio * costo_botella

    st.write("### 🫗 Impacto económico y volumen desperdiciado")

    res_col1, res_col2, res_col3, res_col4 = st.columns(4)

    with res_col1:
        st.metric(
            "Por ducha",
            f"${costo_ducha:,.2f} MXN",
            f"{int(botellas_ducha):,} botellas"
        )

    with res_col2:
        st.metric(
            "Por semana",
            f"${costo_semana:,.2f} MXN",
            f"{int(botellas_semana):,} botellas"
        )

    with res_col3:
        st.metric(
            "Por mes",
            f"${costo_mes:,.2f} MXN",
            f"{int(botellas_mes):,} botellas"
        )

    with res_col4:
        st.metric(
            "Por año",
            f"${costo_anio:,.2f} MXN",
            f"{int(botellas_anio):,} botellas"
        )

    if botellas_anio > 0:
        df_grafica = pd.DataFrame({
            "Periodo": ["Por ducha", "Por semana", "Por mes", "Por año"],
            "Costo_MXN": [
                costo_ducha,
                costo_semana,
                costo_mes,
                costo_anio
            ],
            "Botellas": [
                botellas_ducha,
                botellas_semana,
                botellas_mes,
                botellas_anio
            ]
        })

        st.markdown("### 📊 Comparación del desperdicio")
        st.caption(
            "Costo equivalente del agua desperdiciada según el periodo."
        )

        chart = alt.Chart(df_grafica).mark_bar(
            cornerRadiusEnd=8,
            height=28,
            color="#62B6CB"
        ).encode(
            x=alt.X(
                "Costo_MXN:Q",
                scale=alt.Scale(type="symlog"),
                axis=alt.Axis(
                    title="Costo equivalente (MXN)",
                    grid=True,
                    format="$,.0f"
                )
            ),
            y=alt.Y(
                "Periodo:N",
                sort=["Por ducha", "Por semana", "Por mes", "Por año"],
                axis=alt.Axis(
                    title=None,
                    labelFontSize=12
                )
            ),
            tooltip=[
                alt.Tooltip("Periodo:N", title="Periodo"),
                alt.Tooltip(
                    "Costo_MXN:Q",
                    title="Costo",
                    format="$,.2f"
                ),
                alt.Tooltip(
                    "Botellas:Q",
                    title="Botellas de 500 ml",
                    format=",.0f"
                )
            ]
        ).properties(
            height=190
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            gridColor="#E5EDF2",
            domain=False,
            tickColor="#E5EDF2"
        ).configure(
            background="#F4F8FB"
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

    st.caption(
        "Nota metodológica: cada litro equivale a dos botellas de 500 ml. "
        "El costo es una equivalencia ilustrativa, no una pérdida monetaria real."
    )

    st.subheader("4. Recomendaciones prácticas")

    st.success("""
    **Acciones sencillas para reducir el consumo en casa:**

    1. **Prepara todo antes de abrir la llave:** Ten listas tus cosas para evitar dejar la regadera abierta.
    2. **Recolecta el agua fría inicial:** Coloca una cubeta mientras esperas el agua caliente y reutilízala en otras tareas.
    3. **Instala ahorradores:** Las regaderas de bajo flujo pueden reducir el consumo.
    4. **Repara fugas:** Evita que el agua se pierda continuamente.
    """)

    st.markdown("---")
    st.subheader("5. 💧 Reto interactivo: ¿cuánta agua puedes ahorrar?")

    st.write(
        "Personaliza tus hábitos y descubre cuántos litros de agua "
        "podrías ahorrar al reducir el tiempo de ducha."
    )

    st.markdown("#### 🌱 Personaliza tu reto")

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        minutos_reducidos = st.slider(
            "¿Cuántos minutos menos duraría tu ducha?",
            0, 10, 2,
            key="minutos_reto"
        )

        caudal_reto = st.slider(
            "Caudal de tu regadera (litros/minuto):",
            2, 15, 8,
            key="caudal_reto"
        )

    with col_r2:
        dias_reto = st.slider(
            "¿Cuántos días por semana aplicarías el cambio?",
            1, 7, 7,
            key="dias_reto"
        )

        personas = st.number_input(
            "¿Cuántas personas participarían?",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )

    litros_ahorrados_dia = (
        minutos_reducidos * caudal_reto * personas
    )

    litros_ahorrados_semana = (
        litros_ahorrados_dia * dias_reto
    )

    litros_ahorrados_mes = litros_ahorrados_semana * 4.33

    st.markdown("#### 📊 Tu ahorro estimado")

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "En un día",
        f"{litros_ahorrados_dia:,.1f} L"
    )

    m2.metric(
        "En una semana",
        f"{litros_ahorrados_semana:,.1f} L"
    )

    m3.metric(
        "En un mes",
        f"{litros_ahorrados_mes:,.1f} L"
    )

    st.progress(
        min(litros_ahorrados_semana / 500, 1.0)
    )

    st.caption(
        "La barra alcanza el 100 % al llegar a 500 litros de ahorro semanal."
    )

    with st.expander("🧮 ¿Cómo se calcula?"):
        st.write(
            "Litros ahorrados = minutos reducidos × caudal de la regadera "
            "× personas × días de aplicación."
        )

        st.latex(
            r"\text{Ahorro semanal} = "
            r"\text{minutos} \times "
            r"\text{litros/minuto} \times "
            r"\text{personas} \times \text{días}"
        )

# =====================================================
# TAB 3: INTERACTIVOS (JUEGO AQUAPOU)
# =====================================================
with tab3:
    st.markdown("""
        <div class="header-box">
            <h2 class="header-title">💧 AquaPou: ¡Alimenta la Gota!</h2>
            <p class="header-subtitle">Atrapa el agua limpia y esquiva las industrias contaminantes</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="legend-box">
            <b>¿Cómo jugar?</b> Mueve el cursor (o usa las flechas ⬅️ ➡️) sobre el área de juego.<br>
            ✅ <b>Atrapa (+10/+15 pts):</b> Gotas de lluvia (💧) y botellas de agua (🧴).<br>
            ❌ <b>Esquiva (Pierdes):</b> Ropa/Fast Fashion (👕), Ganadería intensiva (🥩), Industria petrolera (🛢️) y Plásticos (🛍️).
        </div>
    """, unsafe_allow_html=True)

    game_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <style>
        * {
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: transparent;
        }
        #game-wrapper {
            position: relative;
            width: 520px;
            height: 560px;
            border-radius: 20px;
            overflow: hidden;
            border: 3px solid #64B5F6;
            background: linear-gradient(180deg, #E1F5FE 0%, #B3E5FC 65%, #FFFFFF 100%);
            box-shadow: 0 8px 20px rgba(2, 119, 189, 0.15);
        }
        canvas {
            display: block;
            width: 100%;
            height: 100%;
            cursor: none;
        }
        #hud {
            position: absolute;
            top: 15px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            pointer-events: none;
        }
        .badge {
            background: rgba(255, 255, 255, 0.9);
            color: #0277BD;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 16px;
            border: 2px solid #81D4FA;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }
        .overlay {
            position: absolute;
            inset: 0;
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(4px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 30px;
            text-align: center;
            z-index: 10;
        }
        .hidden {
            display: none !important;
        }
        .overlay h2 {
            color: #01579B;
            margin-top: 0;
            font-size: 28px;
        }
        .fact-card {
            background: #E3F2FD;
            border: 2px solid #42A5F5;
            border-radius: 15px;
            padding: 18px;
            margin: 15px 0 22px 0;
            color: #0D47A1;
            text-align: left;
            box-shadow: 0 4px 10px rgba(33, 150, 243, 0.1);
        }
        .fact-card h3 {
            margin: 0 0 8px 0;
            color: #D32F2F;
            font-size: 18px;
        }
        .fact-card p {
            margin: 6px 0;
            font-size: 15px;
            line-height: 1.45;
        }
        .btn {
            background: linear-gradient(135deg, #29B6F6, #0288D1);
            color: white;
            border: none;
            padding: 12px 28px;
            font-size: 17px;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(2, 136, 209, 0.3);
            transition: transform 0.15s ease;
        }
        .btn:hover {
            transform: scale(1.05);
        }
    </style>
    </head>
    <body>

    <div id="game-wrapper">
        <div id="hud">
            <div class="badge">💧 Puntos: <span id="score">0</span></div>
            <div class="badge">🏆 Récord: <span id="highscore">0</span></div>
        </div>

        <canvas id="gameCanvas" width="520" height="560"></canvas>

        <!-- Pantalla Inicial -->
        <div id="start-screen" class="overlay">
            <div style="font-size: 64px; margin-bottom: 10px;">💧</div>
            <h2>¡Alimenta a AquaPou!</h2>
            <p style="color: #0277BD; font-size: 16px; max-width: 380px;">
                Mueve tu gotita para beber agua limpia y evita que las industrias contaminantes la ensucien.
            </p>
            <button class="btn" onclick="startGame()">¡Empezar a jugar!</button>
        </div>

        <!-- Pantalla de Game Over con Dato Ambiental -->
        <div id="gameover-screen" class="overlay hidden">
            <div style="font-size: 52px;">😵‍💫💦</div>
            <h2 style="color: #C62828; margin-bottom: 5px;">¡AquaPou se contaminó!</h2>
            <p style="color: #0277BD; font-weight: bold; margin: 0;">Puntaje final: <span id="final-score">0</span> pts</p>
            
            <div class="fact-card">
                <h3 id="fact-title">⚠️ Impacto Ambiental</h3>
                <p id="fact-water"></p>
                <p id="fact-country"></p>
            </div>

            <button class="btn" onclick="startGame()">Volver a intentar</button>
        </div>
    </div>

    <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let gameRunning = false;
    let score = 0;
    let highScore = 0;
    let items = [];
    let spawnTimer = 0;
    let speedMultiplier = 1;
    let mouthOpenTimer = 0;

    const pou = {
        x: canvas.width / 2,
        y: canvas.height - 65,
        radius: 38,
        speed: 8
    };

    let keys = { ArrowLeft: false, ArrowRight: false };

    window.addEventListener("keydown", (e) => {
        if (e.key === "ArrowLeft" || e.key === "ArrowRight") keys[e.key] = true;
    });
    window.addEventListener("keyup", (e) => {
        if (e.key === "ArrowLeft" || e.key === "ArrowRight") keys[e.key] = false;
    });
    canvas.addEventListener("mousemove", (e) => {
        if (!gameRunning) return;
        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        pou.x = Math.max(pou.radius, Math.min(canvas.width - pou.radius, mouseX));
    });

    const GOOD_ITEMS = [
        { emoji: "💧", name: "Gota de lluvia", points: 10 },
        { emoji: "🧴", name: "Botella de agua", points: 15 }
    ];

    const BAD_ITEMS = [
        {
            emoji: "👕",
            category: "Industria Textil (Fast Fashion)",
            waterFact: "La industria textil consume alrededor de <b>93 mil millones de metros cúbicos de agua al año</b>; hacer unos solos jeans requiere unos 7,500 litros.",
            countryFact: "<b>China e India</b> encabezan la contaminación hídrica textil debido al vertido de tintes químicos tóxicos en sus ríos."
        },
        {
            emoji: "🥩",
            category: "Industria Ganadera",
            waterFact: "La ganadería utiliza casi el <b>30% del agua dulce mundial</b>; producir 1 kg de carne de res consume cerca de 15,000 litros de agua.",
            countryFact: "<b>Brasil, Estados Unidos y China</b> concentran las mayores huellas hídricas y contaminación por nitratos derivados de la ganadería intensiva."
        },
        {
            emoji: "🛢️",
            category: "Industria Petrolera y Petroquímica",
            waterFact: "Un solo litro de petróleo derramado puede contaminar hasta <b>1 millón de litros de agua potable</b>, bloqueando el oxígeno y destruyendo ecosistemas.",
            countryFact: "<b>Estados Unidos, Rusia y Arabia Saudita</b> lideran la extracción global, mientras que regiones como el Delta del Níger (Nigeria) sufren grave contaminación crónica."
        },
        {
            emoji: "🛍️",
            category: "Plásticos de un solo uso",
            waterFact: "Cada año se vierten más de <b>8 millones de toneladas de plástico</b> a los océanos, fragmentándose en microplásticos que ya están en el agua que bebemos.",
            countryFact: "<b>Filipinas, India y Malasia</b> figuran entre los países con mayor descarga de residuos plásticos mal gestionados hacia los ríos y mares."
        }
    ];

    function startGame() {
        document.getElementById("start-screen").classList.add("hidden");
        document.getElementById("gameover-screen").classList.add("hidden");
        score = 0;
        items = [];
        spawnTimer = 0;
        speedMultiplier = 1;
        mouthOpenTimer = 0;
        pou.x = canvas.width / 2;
        document.getElementById("score").innerText = score;
        gameRunning = true;
        requestAnimationFrame(gameLoop);
    }

    function triggerGameOver(badItem) {
        gameRunning = false;
        if (score > highScore) {
            highScore = score;
            document.getElementById("highscore").innerText = highScore;
        }
        document.getElementById("final-score").innerText = score;
        document.getElementById("fact-title").innerText = "⚠️ " + badItem.category;
        document.getElementById("fact-water").innerHTML = "💧 <b>Gasto/Daño hídrico:</b> " + badItem.waterFact;
        document.getElementById("fact-country").innerHTML = "🌍 <b>Impacto global:</b> " + badItem.countryFact;
        document.getElementById("gameover-screen").classList.remove("hidden");
    }

    function spawnItem() {
        const isGood = Math.random() < 0.55;
        const template = isGood 
            ? GOOD_ITEMS[Math.floor(Math.random() * GOOD_ITEMS.length)]
            : BAD_ITEMS[Math.floor(Math.random() * BAD_ITEMS.length)];

        items.push({
            x: Math.random() * (canvas.width - 70) + 35,
            y: -30,
            radius: 22,
            speed: (3.2 + Math.random() * 1.8) * speedMultiplier,
            isGood: isGood,
            data: template
        });
    }

    function drawPou() {
        ctx.save();
        ctx.translate(pou.x, pou.y);

        ctx.beginPath();
        ctx.moveTo(0, -pou.radius - 12);
        ctx.bezierCurveTo(pou.radius + 12, -5, pou.radius + 8, pou.radius, 0, pou.radius);
        ctx.bezierCurveTo(-pou.radius - 8, pou.radius, -pou.radius - 12, -5, 0, -pou.radius - 12);
        ctx.fillStyle = "#29B6F6";
        ctx.fill();
        ctx.lineWidth = 3;
        ctx.strokeStyle = "#0288D1";
        ctx.stroke();

        ctx.beginPath();
        ctx.ellipse(-14, -6, 5, 11, -0.3, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(255, 255, 255, 0.65)";
        ctx.fill();

        ctx.fillStyle = "white";
        ctx.beginPath();
        ctx.arc(-11, 4, 8, 0, Math.PI * 2);
        ctx.arc(11, 4, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#01579B";
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.fillStyle = "#01579B";
        ctx.beginPath();
        ctx.arc(-10, 4, 4, 0, Math.PI * 2);
        ctx.arc(10, 4, 4, 0, Math.PI * 2);
        ctx.fill();

        const itemNear = items.some(it => Math.hypot(it.x - pou.x, it.y - pou.y) < 110);
        if (mouthOpenTimer > 0 || itemNear) {
            ctx.beginPath();
            ctx.arc(0, 19, 8, 0, Math.PI * 2);
            ctx.fillStyle = "#0277BD";
            ctx.fill();
        } else {
            ctx.beginPath();
            ctx.arc(0, 16, 7, 0.1 * Math.PI, 0.9 * Math.PI);
            ctx.strokeStyle = "#01579B";
            ctx.lineWidth = 2.5;
            ctx.stroke();
        }

        ctx.restore();
    }

    function gameLoop() {
        if (!gameRunning) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (keys.ArrowLeft) pou.x = Math.max(pou.radius, pou.x - pou.speed);
        if (keys.ArrowRight) pou.x = Math.min(canvas.width - pou.radius, pou.x + pou.speed);

        if (mouthOpenTimer > 0) mouthOpenTimer--;

        spawnTimer++;
        const spawnRate = Math.max(28, Math.floor(55 - score * 0.12));
        if (spawnTimer >= spawnRate) {
            spawnItem();
            spawnTimer = 0;
        }

        ctx.font = "34px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        for (let i = items.length - 1; i >= 0; i--) {
            let it = items[i];
            it.y += it.speed;

            ctx.beginPath();
            ctx.arc(it.x, it.y, 22, 0, Math.PI * 2);
            ctx.fillStyle = it.isGood ? "rgba(255, 255, 255, 0.75)" : "rgba(255, 235, 238, 0.85)";
            ctx.fill();

            ctx.fillText(it.data.emoji, it.x, it.y + 2);

            const dist = Math.hypot(it.x - pou.x, it.y - pou.y);
            if (dist < pou.radius + it.radius - 6) {
                if (it.isGood) {
                    score += it.data.points;
                    speedMultiplier = 1 + (score / 250);
                    mouthOpenTimer = 15;
                    document.getElementById("score").innerText = score;
                    items.splice(i, 1);
                    continue;
                } else {
                    triggerGameOver(it.data);
                    return;
                }
            }

            if (it.y > canvas.height + 30) {
                items.splice(i, 1);
            }
        }

        drawPou();
        requestAnimationFrame(gameLoop);
    }
    </script>
    </body>
    </html>
    """

    components.html(game_html, height=580)

# =====================================================
# TAB 4: FUENTES DE INFORMACIÓN
# =====================================================
with tab4:
    st.subheader("8. Fuentes de información oficiales")

    st.write(
        "Para garantizar la veracidad del proyecto, los datos e "
        "indicadores se relacionan con las siguientes instituciones:"
    )

    st.markdown("""
    ### CONAGUA
    Comisión Nacional del Agua.

    Documento: Estadísticas del Agua en México / Atlas del Agua.

    [Consultar CONAGUA](https://www.gob.mx/conagua)

    ### Sistema de Información del Agua

    Institución: CONAGUA.

    [Consultar Sistema de Información del Agua](https://app.conagua.gob.mx/sistemasdeagua/)

    ### INEGI

    Instituto Nacional de Estadística y Geografía.

    Documento: Censos de población y estadísticas sobre servicios de agua potable y saneamiento.

    [Consultar INEGI](https://www.inegi.org.mx/)

    ### FAO

    Organización de las Naciones Unidas para la Alimentación y la Agricultura.

    Documento: Base de datos global de recursos hídricos (AQUASTAT).

    [Consultar FAO](https://www.fao.org/)
    """)

# =====================================================
# PIE DE PÁGINA GENERAL
# =====================================================

st.markdown("---")

st.title("💧 ¡Cada gota cuenta!")

st.write(
    "El cuidado del agua es una responsabilidad compartida. "
    "Conocer su disponibilidad, evitar el desperdicio y cambiar "
    "nuestros hábitos son pasos importantes para proteger este "
    "recurso indispensable."
)

st.success(
    "Gracias por participar y contribuir al cuidado del agua."
)
