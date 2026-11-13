import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="AquaPou - Cuida el Agua",
    page_icon="💧",
    layout="centered"
)

# Estilos CSS personalizados (Tonos azul claro y blanco)
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(180deg, #E3F2FD 0%, #FFFFFF 100%);
        }
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
            color: #0277BD;
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

# Encabezado de la aplicación
st.markdown("""
    <div class="header-box">
        <h1 class="header-title">💧 AquaPou: ¡Alimenta la Gota!</h1>
        <p class="header-subtitle">Atrapa el agua limpia y esquiva las industrias contaminantes</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="legend-box">
        <b>¿Cómo jugar?</b> Mueve el cursor (o usa las flechas ⬅️ ➡️) sobre el área de juego.<br>
        ✅ <b>Atrapa (+10 pts):</b> Gotas de lluvia (💧) y botellas de agua (🧴).<br>
        ❌ <b>Esquiva (Pierdes):</b> Ropa/Fast Fashion (👕), Ganadería intensiva (🥩) e Industria petrolera (🛢️).
    </div>
""", unsafe_allow_html=True)

# Código del juego interactivo en HTML5 / Canvas / JS
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
    /* Pantalla de inicio y Game Over */
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

// Personaje tipo Pou (Gota de agua)
const pou = {
    x: canvas.width / 2,
    y: canvas.height - 65,
    radius: 38,
    speed: 8
};

// Controles
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

// Catálogo de objetos buenos y malos con sus datos educativos
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
    const isGood = Math.random() < 0.55; // 55% agua, 45% contaminantes
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

    // Cuerpo en forma de gotita tierna estilo Pou
    ctx.beginPath();
    ctx.moveTo(0, -pou.radius - 12);
    ctx.bezierCurveTo(pou.radius + 12, -5, pou.radius + 8, pou.radius, 0, pou.radius);
    ctx.bezierCurveTo(-pou.radius - 8, pou.radius, -pou.radius - 12, -5, 0, -pou.radius - 12);
    ctx.fillStyle = "#29B6F6";
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = "#0288D1";
    ctx.stroke();

    // Brillo de agua
    ctx.beginPath();
    ctx.ellipse(-14, -6, 5, 11, -0.3, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(255, 255, 255, 0.65)";
    ctx.fill();

    // Ojos grandes estilo Pou
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(-11, 4, 8, 0, Math.PI * 2);
    ctx.arc(11, 4, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#01579B";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Pupilas
    ctx.fillStyle = "#01579B";
    ctx.beginPath();
    ctx.arc(-10, 4, 4, 0, Math.PI * 2);
    ctx.arc(10, 4, 4, 0, Math.PI * 2);
    ctx.fill();

    // Boca (se abre cuando atrapa agua o se acerca un objeto)
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

    // Movimiento por teclado
    if (keys.ArrowLeft) pou.x = Math.max(pou.radius, pou.x - pou.speed);
    if (keys.ArrowRight) pou.x = Math.min(canvas.width - pou.radius, pou.x + pou.speed);

    if (mouthOpenTimer > 0) mouthOpenTimer--;

    // Generar nuevos objetos
    spawnTimer++;
    const spawnRate = Math.max(28, Math.floor(55 - score * 0.12));
    if (spawnTimer >= spawnRate) {
        spawnItem();
        spawnTimer = 0;
    }

    // Dibujar y actualizar objetos que caen
    ctx.font = "34px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    for (let i = items.length - 1; i >= 0; i--) {
        let it = items[i];
        it.y += it.speed;

        // Fondo sutil circular para distinguir mejor los ítems
        ctx.beginPath();
        ctx.arc(it.x, it.y, 22, 0, Math.PI * 2);
        ctx.fillStyle = it.isGood ? "rgba(255, 255, 255, 0.75)" : "rgba(255, 235, 238, 0.85)";
        ctx.fill();

        ctx.fillText(it.data.emoji, it.x, it.y + 2);

        // Detección de colisión con AquaPou
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

        // Eliminar si sale de la pantalla
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

# Renderizar el juego dentro de Streamlit
components.html(game_html, height=580)
