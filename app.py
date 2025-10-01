import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# --- Configuración de la Página ---
st.set_page_config(
    page_title="ILLARI - Asistente Virtual",
    page_icon="👁️",
    layout="centered"
)

# --- Carga de la Clave API de Forma Segura ---
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not API_KEY:
    st.error("Falta GROQ_API_KEY en .env o en st.secrets.")
    st.stop()

client = Groq(api_key=API_KEY)


# --- (CAMBIO 1) Almacenar el conocimiento del proyecto en una variable ---
# Aquí guardamos toda la información que queremos que el chatbot sepa.
ILLARI_CONTEXT = """
El proyecto ILLARI es una iniciativa de innovación en tecnología médica y salud pública que nace en el Perú con el objetivo de resolver un problema crítico y desatendido: la falta de acceso al diagnóstico oftalmológico especializado en zonas rurales y remotas del país.

Su núcleo es el desarrollo de ILLARI, un topógrafo corneal portátil de bajo costo, integrado con una plataforma de telemedicina.

### Componentes Clave:

#### 1. El Problema: La Brecha de Diagnóstico en la Salud Ocular Peruana
- **Enfermedades corneales:** Afecciones como el queratocono deforman la córnea y distorsionan la visión. Si no se detectan a tiempo, pueden llevar a la necesidad de un trasplante de córnea.
- **Barrera Geográfica y Económica en Perú:** Cerca del 65% de las personas con ceguera viven en áreas rurales con escasez de oftalmólogos y equipos. Los topógrafos corneales estándar son costosos y se encuentran solo en grandes ciudades, obligando a los pacientes a realizar viajes largos y costosos. El proyecto ataca la ceguera evitable por falta de diagnóstico.

#### 2. La Solución Tecnológica: El Dispositivo ILLARI
- **¿Qué es un Topógrafo Corneal?:** Un instrumento que mapea la superficie de la córnea en 3D para detectar deformaciones.
- **Diferencias de ILLARI:**
  - **Portabilidad:** Ligero, robusto y fácil de transportar para llevarlo a campañas de salud en comunidades remotas.
  - **Bajo Costo:** Diseño y producción que reducen drásticamente el precio en comparación con equipos importados.
  - **Facilidad de Uso:** Interfaz diseñada para que personal de salud no especializado (técnicos, enfermeros) pueda capturar las imágenes.

#### 3. El Modelo de Servicio: La Integración con Telemedicina
- **Diagnóstico a Distancia:** El dispositivo captura las imágenes en la posta rural y las envía a una plataforma en la nube.
- **Conexión con Especialistas:** Un oftalmólogo en cualquier ciudad accede a las imágenes, emite un diagnóstico y lo envía de vuelta.
- **Impacto:** Este sistema de tele-oftalmología rompe la barrera geográfica, democratiza el acceso a la atención especializada, optimiza el tiempo de los oftalmólogos y reduce costos y tiempos de espera para el paciente.
"""

# --- (CAMBIO 2) Crear un prompt de sistema mucho más potente ---
# Le damos instrucciones claras y le entregamos todo el contexto que debe usar.
SYSTEM_PROMPT = f"""
Eres un asistente virtual experto y representante del proyecto ILLARI. Tu misión es responder a las preguntas de los usuarios de manera amable y precisa, basándote exclusivamente en el siguiente contexto que se te proporciona. No inventes información que no esté en este texto.

---
CONTEXTO DEL PROYECTO ILLARI:
{ILLARI_CONTEXT}
---

Si el usuario te pregunta algo que no está relacionado con el proyecto ILLARI, responde amablemente que tu función es solo proporcionar información sobre ILLARI.
"""

# --- Título y Logo ---
st.image('ojo.jpg', width=100)
st.title("Asistente Virtual del Proyecto ILLARI")

# --- Explicación del Proyecto en un Expansor (para el usuario humano) ---
with st.expander("Conoce más sobre el Proyecto ILLARI"):
    # Usamos la misma variable para no repetir texto
    st.markdown(ILLARI_CONTEXT, unsafe_allow_html=True)

# --- Configuración del Chatbot ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Renderizado del Historial de Chat ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Lógica del Chat ---
user_input = st.chat_input("Haz una pregunta sobre el proyecto ILLARI...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir mensajes para el modelo
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Añadimos solo el historial reciente para no sobrecargar el prompt
    for msg in st.session_state.chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Llamar a la API
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
        )
        respuesta_texto = response.choices[0].message.content
    except Exception as e:
        respuesta_texto = f"Lo siento, ocurrió un error al llamar a la API: `{e}`"

    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_texto})
    with st.chat_message("assistant"):
        st.markdown(respuesta_texto)

# PAra correr localmente usar: streamlit run app.py