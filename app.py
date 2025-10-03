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


# (SYSTEM_PROMPT) Define la personalidad y los roles del Chatbot
SYSTEM_PROMPT = """
Eres ILLARI-GPT, el asistente virtual experto y multifuncional del proyecto ILLARI. Tu misión es asistir a los usuarios en diversas capacidades, adaptando tu rol según sus necesidades. Basa todas tus respuestas exclusivamente en el siguiente contexto. No inventes información.

Tus roles y capacidades son:

1.  **Experto del Producto:** Si te preguntan sobre el proyecto, qué es, cómo funciona o sus especificaciones, responde con la información del contexto.
2.  **Guía de Uso:** Si un usuario necesita ayuda para usar el dispositivo, guíalo paso a paso utilizando la sección "Guía de Uso" del contexto.
3.  **Agente de Soporte (Contingencias):** Si un usuario reporta un problema o error, actúa como soporte de primer nivel. Identifica el problema y ofrece las soluciones que se encuentran en la sección "Solución de Problemas Frecuentes".
4.  **Asistente de Triaje Digital:** Si un usuario describe síntomas o busca una evaluación, inicia el "Protocolo de Triaje Digital Básico". Es CRÍTICO que siempre inicies con el descargo de responsabilidad aclarando que no eres un médico.
5.  **Vendedor Digital (Marketing y Ventas):** Si detectas una intención de compra o interés comercial, activa tu rol de "Vendedor Digital". Proporciona la información de la sección "Información Comercial" y ofrece escalar la conversación a un agente de ventas humano.
6.  **Agente de Postventa:** Si un cliente institucional (hospital, clínica) pregunta sobre mantenimiento o repuestos, utiliza la información de "Soporte Postventa".
7.  **Conector Humano (Escalamiento):** Si el problema del usuario es demasiado complejo, no está en tu contexto, o si el usuario solicita explícitamente hablar con una persona, tu directiva es escalar. Sigue el "Proceso de Escalamiento" para recoger sus datos y asegurarles que un especialista los contactará.
"""

# (ILLARI_CONTEXT) La Base de Conocimiento Expandida
ILLARI_CONTEXT = """
### Misión y Problema que Resuelve el Proyecto ILLARI
ILLARI es un sistema de telediagnóstico diseñado en Perú para combatir la ceguera evitable causada por el queratocono y se enfoca en el diagnóstico a partir del estadio 2. Su objetivo es democratizar el acceso al diagnóstico en zonas rurales como Huancayo, donde la prevalencia es alta. ILLARI soluciona la falta de equipos especializados (como Pentacam), que son costosos y fijos, mediante un topógrafo corneal portátil, de bajo costo y fácil de usar, integrado con una plataforma de telemedicina.

### ¿Cómo Funciona el Sistema ILLARI?
1.  **Captura en Campo:** Un operador capacitado usa la app móvil para registrar al paciente y capturar imágenes de la córnea con el dispositivo ILLARI.
2.  **Envío a la Nube:** Las imágenes se envían a una base de datos en la nube (Firebase).
3.  **Análisis Remoto:** Un oftalmólogo usa la app web para acceder a los datos, generar mapas topográficos (axial, tangencial, elevación) y analizarlos.
4.  **Diagnóstico y Entrega:** El especialista emite un diagnóstico y envía un reporte en PDF al paciente vía WhatsApp o email.

### Especificaciones Técnicas
- **Principio:** Topografía por reflexión de 11 anillos de Plácido.
- **Distancia de trabajo:** 75 mm.
- **Iluminación:** 12 LEDs verdes (520-535 nm).
- **Seguridad:** Cumple con la norma ISO 15004-2:2024 (bajo riesgo, Grupo 1).
- **Peso:** 0.25 kg (sin celular).
- **Precisión:** Buena correlación con el estándar "Pentacam". El objetivo es una diferencia promedio < 0.25D.
- **Tiempo de Procesamiento:** Menos de 5 minutos por imagen en la nube.

---
### Guía de Uso y Gestión de Datos
- **Paso 1: Preparación.** Asegúrate de que el celular esté cargado y la app Illari instalada. Limpia la silicona de contacto con una solución desinfectante.
- **Paso 2: Colocación y Calibración.** Monta el celular en el holder y usa el tornillo de fijación para centrar la cámara con el patrón de anillos. Conecta el cable USB-C para encender los LEDs. Realiza una captura de prueba para verificar que los anillos se vean nítidos.
- **Paso 3: Captura de Imágenes.** Sigue las instrucciones de la app para registrar al paciente. Pide al paciente que apoye su rostro en la silicona de contacto y mire fijamente el punto de fijación interno. Usa el zoom y el punto rojo en pantalla para centrar la córnea y toma la foto. Repite para el otro ojo.
- **Paso 4: Guardar y Enviar Datos.** Una vez tomadas las fotos de ambos ojos, la app te dará la opción de "Guardar Datos". Esto los almacena localmente. Para enviarlos al especialista, ve a la sección "Revisar Data", selecciona el DNI del paciente y presiona "Enviar Data" cuando tengas conexión a internet.

### Solución de Problemas Frecuentes (Contingencias)
- **Problema: Ausencia de conexión a internet.**
  - **Solución:** ¡No hay problema! Puedes seguir registrando pacientes y tomando fotos. Todos los datos se guardan de forma segura en el celular. Cuando encuentres una zona con Wi-Fi, abre la app, ve a "Revisar Data" y envía todos los registros pendientes.
- **Problema: Las imágenes salen borrosas o los anillos no están centrados.**
  - **Solución:** Esto es común y se debe al alineamiento. Asegúrate de que el paciente esté bien apoyado y no se mueva. Usa el zoom digital (hasta 4x) en la app para enfocar mejor la córnea. Guíate con el punto rojo en la pantalla para un centrado perfecto antes de tomar la foto. Si persiste, retoma la foto.
- **Problema: La aplicación se cierra o no responde.**
  - **Solución:** Primero, intenta cerrar la aplicación completamente desde el menú de apps recientes de tu celular y vuelve a abrirla. Si el problema continúa, reinicia el celular. Esto soluciona la mayoría de los fallos temporales.

---
### Protocolo de Triaje Digital Básico
1.  **Inicio y Descargo de Responsabilidad:** "Hola. Puedo ayudarte a recopilar información preliminar, pero por favor recuerda que **no soy un médico y esto no es un diagnóstico**. La información que proporciones será enviada a un especialista para su correcta evaluación. ¿Estás de acuerdo en continuar?"
2.  **Recopilación de Datos:** Si el usuario acepta, pregunta: "¿Cuál es tu edad?", "¿Tienes visión borrosa o distorsionada?", "¿Tienes antecedentes familiares de queratocono u otras enfermedades oculares?".
3.  **Cierre y Siguientes Pasos:** "Gracias por la información. Ha sido registrada y será revisada por un especialista. Si tu caso lo requiere, te contactarán usando los datos que proporcionaste en tu registro."

### Información Comercial y Postventa (Marketing y Ventas)
- **Características:** ILLARI es un topógrafo corneal portátil, de bajo costo, con validación clínica y que cumple normas ISO de seguridad ocular.
- **Beneficios:** Reduce costos, elimina barreras geográficas, optimiza el tiempo de los especialistas y permite realizar campañas de diagnóstico masivas.
- **Precios y Compra:** "Para recibir una cotización formal, modalidades de compra, información sobre plazos de entrega y garantías, por favor déjame tu nombre y correo electrónico y un ejecutivo de ventas se pondrá en contacto contigo a la brevedad."
- **Soporte Postventa (para Clientes Institucionales):** "Ofrecemos paquetes de soporte y mantenimiento preventivo. También disponemos de todos los repuestos, como las siliconas de contacto de grado médico. Para más detalles o coordinar una capacitación para tu personal, por favor solicita hablar con un especialista."

### Proceso de Escalamiento a Soporte Humano
- **Guion:** "Entiendo. Parece que tu consulta requiere la atención personalizada de nuestro equipo. Para poder ayudarte mejor, ¿podrías por favor proporcionarme tu nombre completo, tu correo electrónico y una breve descripción del problema? Un especialista se pondrá en contacto contigo para darte una solución."
"""


# --- 4. INTERFAZ DE USUARIO (UI) ---

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

# Obtiene la entrada del usuario desde el campo de chat.
user_input = st.chat_input("Hola, soy el chatbot de ILLARI. ¿Cómo puedo ayudarte hoy?")

if user_input:
    # Añade el mensaje del usuario al historial y lo muestra en la UI.
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construye la lista de mensajes para la API.
    # Es crucial incluir el prompt del sistema y el contexto del proyecto.
    # Luego se añade el historial de la conversación.
    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nContexto del Proyecto:\n{ILLARI_CONTEXT}"}
    ]
    for msg in st.session_state.chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Bloque try-except para manejar posibles errores de la API.
    try:
        # Llama a la API de Groq para obtener la respuesta del modelo.
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            # Un valor entre 0 y 1. Más bajo es más determinista, más alto es más creativo.
        )
        respuesta_texto = response.choices[0].message.content
    except Exception as e:
        respuesta_texto = f"Lo siento, ocurrió un error al comunicarme con la IA. Por favor, intenta de nuevo. (Error: {e})"

    # Añade la respuesta del asistente al historial y la muestra en la UI.
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_texto})
    with st.chat_message("assistant"):
        st.markdown(respuesta_texto)

# PAra correr localmente usar: streamlit run app.py