import streamlit as st

# ─── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title="Conversor de Temperaturas",
    page_icon="🌡️",
    layout="centered",
)

# ─── Estilos personalizados ─────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stApp { max-width: 700px; margin: auto; }
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
        text-align: center;
        color: white;
    }
    .result-value {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .result-label {
        font-size: 1rem;
        opacity: 0.85;
        margin-top: 4px;
    }
    .conversion-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
        border-left: 5px solid;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .celsius-card   { border-color: #e74c3c; }
    .fahrenheit-card{ border-color: #f39c12; }
    .kelvin-card    { border-color: #3498db; }
    .formula-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 14px 18px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: #555;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Funciones de conversión ─────────────────────────────────────────────────
def celsius_to_fahrenheit(c):    return c * 9/5 + 32
def celsius_to_kelvin(c):        return c + 273.15
def fahrenheit_to_celsius(f):    return (f - 32) * 5/9
def fahrenheit_to_kelvin(f):     return fahrenheit_to_celsius(f) + 273.15
def kelvin_to_celsius(k):        return k - 273.15
def kelvin_to_fahrenheit(k):     return kelvin_to_celsius(k) * 9/5 + 32

FORMULAS = {
    "Celsius": {
        "Fahrenheit": "°F = (°C × 9/5) + 32",
        "Kelvin":     "K  = °C + 273.15",
    },
    "Fahrenheit": {
        "Celsius": "°C = (°F − 32) × 5/9",
        "Kelvin":  "K  = (°F − 32) × 5/9 + 273.15",
    },
    "Kelvin": {
        "Celsius":     "°C = K − 273.15",
        "Fahrenheit":  "°F = (K − 273.15) × 9/5 + 32",
    },
}

SYMBOLS = {"Celsius": "°C", "Fahrenheit": "°F", "Kelvin": "K"}
CARD_CLASS = {"Celsius": "celsius-card", "Fahrenheit": "fahrenheit-card", "Kelvin": "kelvin-card"}
EMOJI = {"Celsius": "🔴", "Fahrenheit": "🟠", "Kelvin": "🔵"}

# ─── Encabezado ──────────────────────────────────────────────────────────────
st.title("🌡️ Conversor de Temperaturas")
st.markdown("Convierte entre **Celsius**, **Fahrenheit** y **Kelvin** de forma instantánea.")
st.divider()

# ─── Controles ───────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    unidad_origen = st.selectbox(
        "Unidad de origen",
        ["Celsius", "Fahrenheit", "Kelvin"],
        index=0,
    )
with col2:
    valor = st.number_input(
        f"Valor en {SYMBOLS[unidad_origen]}",
        value=0.0,
        step=0.1,
        format="%.4f",
    )

# Validación de Kelvin
if unidad_origen == "Kelvin" and valor < 0:
    st.error("⚠️ El Kelvin no puede ser negativo (cero absoluto = 0 K).")
    st.stop()

# ─── Cálculos ────────────────────────────────────────────────────────────────
conversiones = {}
if unidad_origen == "Celsius":
    conversiones = {
        "Fahrenheit": celsius_to_fahrenheit(valor),
        "Kelvin":     celsius_to_kelvin(valor),
    }
elif unidad_origen == "Fahrenheit":
    conversiones = {
        "Celsius": fahrenheit_to_celsius(valor),
        "Kelvin":  fahrenheit_to_kelvin(valor),
    }
else:
    conversiones = {
        "Celsius":     kelvin_to_celsius(valor),
        "Fahrenheit":  kelvin_to_fahrenheit(valor),
    }

# ─── Resultados ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="result-box">
    <div class="result-label">Valor ingresado</div>
    <div class="result-value">{valor:.4f} {SYMBOLS[unidad_origen]}</div>
    <div class="result-label">{unidad_origen}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("### Resultados de conversión")

for unidad_destino, resultado in conversiones.items():
    card = CARD_CLASS[unidad_destino]
    sym  = SYMBOLS[unidad_destino]
    formula = FORMULAS[unidad_origen][unidad_destino]
    emoji = EMOJI[unidad_destino]

    st.markdown(f"""
    <div class="conversion-card {card}">
        <strong>{emoji} {unidad_destino}</strong><br>
        <span style="font-size:1.8rem; font-weight:700;">{resultado:.4f} {sym}</span>
        <div class="formula-box">📐 {formula}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Tabla de referencia rápida ──────────────────────────────────────────────
with st.expander("📊 Tabla de referencia rápida"):
    referencias = {
        "Punto de referencia": [
            "Cero absoluto", "Congelación del agua",
            "Temperatura corporal", "Ebullición del agua",
        ],
        "°C":  [-273.15, 0,    37,    100],
        "°F":  [-459.67, 32,   98.6,  212],
        "K":   [0,       273.15, 310.15, 373.15],
    }
    st.table(referencias)

# ─── Pie de página ───────────────────────────────────────────────────────────
st.divider()
st.caption("Desarrollado con ❤️ usando Python + Streamlit · Cristina López")
