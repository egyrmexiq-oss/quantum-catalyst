import streamlit as st
import google.generativeai as genai
import pandas as pd
import utils_voz as voz # Módulo de voz modular
import time
from datetime import datetime

# ==========================================
# ⚙️ 1. CONFIGURACIÓN Y ESTILOS (LABORATORIO CIENTÍFICO)
# ==========================================
st.set_page_config(page_title="Quantum Catalyst", page_icon="⚛️", layout="wide")
voz.inyectar_css_footer() # Inyectar estilos del micrófono

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    /* Estilos del Contador */
    .counter-box {
        padding: 15px; border-radius: 10px;
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        text-align: center; border: 1px solid #4facfe;
        margin-bottom: 20px;
    }
    .counter-number { font-size: 2.5em; font-weight: bold; color: #fff; }
    .counter-label { font-size: 0.9em; color: #ddd; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Alerta de Créditos Bajos */
    .low-credits { border: 2px solid #ff4b1f; animation: pulse 2s infinite; }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 75, 31, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 75, 31, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 75, 31, 0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECRETOS Y CONFIGURACIÓN ---
try:
    API_KEY = st.secrets.get("GOOGLE_API_KEY")
    # URL de tu Hoja de Cálculo (Publicada como CSV)
    # ¡OJO! Reemplaza esto con TU LINK real de la hoja nueva
    URL_SHEET_CATALYST = st.secrets["URL_SHEET_CATALYST"]
except:
    st.error("⚠️ Error en Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash') # Usamos Flash para rapidez en chat

# Inicializar Estado
if "mensajes" not in st.session_state: st.session_state.mensajes = []
if "usuario_data" not in st.session_state: st.session_state.usuario_data = None
if "creditos_sesion" not in st.session_state: st.session_state.creditos_sesion = 0
if "modo_investigacion" not in st.session_state: st.session_state.modo_investigacion = "Exploración Rápida"

# ==========================================
# 📊 2. GESTIÓN DE DATOS (GOOGLE SHEETS)
# ==========================================
# Así debe quedar tu función COMPLETA (Reemplaza desde la línea 62 hasta el return)

@st.cache_data(ttl=60)
def cargar_usuarios():
    try:
        # LÍNEA 65: Usamos la variable (Más limpio)
        df = pd.read_csv(URL_SHEET_CATALYST)
        
        # Normalizamos nombres de columnas
        df.columns = [c.strip().lower() for c in df.columns]
        
        # 👇 ESTO ES LO QUE TE FALTA EN TU IMAGEN 👇
        # Limpieza de espacios invisibles en las claves
        if 'clave' in df.columns:
            df['clave'] = df['clave'].astype(str).str.strip()
            
        return df
    except Exception as e:
        return None

def registrar_interaccion(usuario):
    """
    Simulación de escritura. 
    Nota para el CEO: Para escribir en la hoja real desde aquí, 
    necesitaríamos configurar la API de Google Sheets (Service Account).
    Por ahora, controlamos la sesión localmente.
    """
    # Aquí iría el código de escritura a la nube.
    pass

# ==========================================
# 🔐 3. LOGIN (ESTILO QUANTUM)
# ==========================================
if not st.session_state.usuario_data:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## ⚛️ Quantum Catalyst")
        st.caption("Acelerador de Ideas Científicas & Tecnológicas")
        
        # Animación Spline (Onda Senoidal / Átomo)
        try: 
            import streamlit.components.v1 as components
            components.iframe("https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/", height=300)
        except: pass
        
        # Audio Ambiental (Frecuencia para pensar)
        st.audio("https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3", start_time=0, autoplay=True)
        
        with st.form("login_form"):
            clave_input = st.text_input("Clave de Acceso (DEMO / VIP):", type="password")
            submit = st.form_submit_button("Inicializar Sistema")
            
            if submit:
                df_usuarios = cargar_usuarios()
                
                # Búsqueda de usuario (Si no hay hoja real, usamos un dict de respaldo para pruebas)
                usuario_encontrado = None
                
                if df_usuarios is not None:
                    # Buscar en CSV
                    filtro = df_usuarios[df_usuarios['clave'].astype(str) == clave_input]
                    if not filtro.empty:
                        usuario_encontrado = filtro.iloc[0].to_dict()
                else:
                    # RESPALDO LOCAL (Para que pruebes YA sin configurar la hoja)
                    if clave_input == "DEMO":
                        usuario_encontrado = {"clave": "DEMO", "tipo": "DEMO", "limite": 5, "usados": 0, "discapacidad": ""}
                    elif clave_input == "VIP":
                        usuario_encontrado = {"clave": "VIP", "tipo": "VIP", "limite": 60, "usados": 0, "discapacidad": ""}

                if usuario_encontrado:
                    # Cargar datos a sesión
                    st.session_state.usuario_data = usuario_encontrado
                    
                    # Calcular créditos restantes
                    limite = int(usuario_encontrado['limite'])
                    usados = int(usuario_encontrado['usados'])
                    restantes = limite - usados
                    st.session_state.creditos_sesion = restantes
                    
                    if restantes <= 0:
                        st.error("⛔ Tu periodo de investigación ha finalizado. Contacta al Administrador.")
                        st.session_state.usuario_data = None
                    else:
                        st.success(f"Bienvenido. Nivel: {usuario_encontrado['tipo']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("⛔ Clave no válida en la Base de Datos.")
    st.stop()

# ==========================================
# 🏠 4. INTERFAZ CIENTÍFICA (DASHBOARD)
# ==========================================

# --- BARRA LATERAL (CONTROLES) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2021/2021646.png", width=50) # Icono Átomo
    st.title("Panel de Control")
    
    # 1. EL CONTADOR (GRANDE Y VISIBLE)
    restantes = st.session_state.creditos_sesion
    clase_alerta = "low-credits" if restantes <= 3 else ""
    
    st.markdown(f"""
        <div class="counter-box {clase_alerta}">
            <div class="counter-number">{restantes}</div>
            <div class="counter-label">Interacciones Restantes</div>
        </div>
    """, unsafe_allow_html=True)
    
    if restantes <= 3:
        st.warning("⚠️ Energía baja. Tus créditos están por agotarse.")
    
    st.markdown("---")
    
    # 2. MODO DE INVESTIGACIÓN
    st.markdown("### 🔬 Profundidad")
    modo = st.radio("Nivel de Análisis:", ["Exploración Rápida", "Investigación Profunda"], 
                    help="Rápida: Ideas y conceptos generales. Profunda: Citas, papers y análisis crítico.")
    st.session_state.modo_investigacion = modo

    # 3. ACCESIBILIDAD Y FEEDBACK
    with st.expander("♿ Accesibilidad"):
        # Leemos si ya tiene discapacidad registrada
        disc_actual = st.session_state.usuario_data.get('discapacidad', '')
        nueva_disc = st.text_input("¿Tienes alguna discapacidad visual/auditiva?", value=disc_actual)
        if nueva_disc != disc_actual:
            st.info("Preferencia guardada localmente para esta sesión.")
            # Aquí mandaríamos el update a la hoja de cálculo
    
    st.markdown("---")
    st.caption(f"ID Sesión: {st.session_state.usuario_data['clave']}")
    
    if st.button("💾 Guardar y Salir"):
        st.session_state.usuario_data = None
        st.rerun()

# --- ÁREA PRINCIPAL ---
st.title("Quantum Catalyst 🧪")
st.caption(f"Modo: **{st.session_state.modo_investigacion}** | Catalizando ideas nuevas...")

# Historial
for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "audio" in msg: st.audio(msg["audio"], format="audio/mp3")

# ==========================================
# 🎤 5. INPUT MODULAR (FULL WIDTH)
# ==========================================

# VALIDACIÓN DE CRÉDITOS ANTES DE MOSTRAR INPUT
if st.session_state.creditos_sesion <= 0:
    st.error("⛔ Has alcanzado el límite de tu plan. Para continuar catalizando ideas, por favor solicita una recarga de créditos.")
    st.info("Contacta al administrador para desbloquear niveles superiores.")
    st.stop()

# Si tiene créditos, mostramos el input
if "mic_key_counter" not in st.session_state: st.session_state.mic_key_counter = 0

st.markdown("---")
mic_key = f"audio_cat_{st.session_state.mic_key_counter}"
audio_blob = st.audio_input("🎙️ Grabar Hipótesis / Idea", key=mic_key)
texto_chat = st.chat_input("Escribe tu planteamiento científico...")

# LÓGICA
prompt_usuario = None
usar_voz = False

if texto_chat:
    prompt_usuario = texto_chat
elif audio_blob:
    transcripcion = voz.escuchar_usuario(audio_blob)
    if transcripcion:
        prompt_usuario = transcripcion
        usar_voz = True
        st.session_state.mic_key_counter += 1

if prompt_usuario:
    # 1. Descontar Crédito
    st.session_state.creditos_sesion -= 1
    # (Aquí llamaríamos a la función para actualizar la hoja en la nube)
    
    # 2. Mostrar Usuario
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
    st.session_state.mensajes.append({"role": "user", "content": prompt_usuario})

    # 3. CONSTRUCCIÓN DEL PROMPT CIENTÍFICO (EL ALMA)
    tipo_usuario = st.session_state.usuario_data['tipo'] # DEMO o VIP
    nivel_analisis = st.session_state.modo_investigacion
    
    # Restricciones según tipo
    profundidad = "Baja. Sé breve y general." if tipo_usuario == "DEMO" else "Alta. Sé riguroso y exhaustivo."
    
    # Instrucciones base
    system_prompt = f"""
    Actúa como Quantum Catalyst, un asistente de I+D científica avanzada.
    
    TUS REGLAS DE ORO:
    1. PROACTIVIDAD: No solo respondas, propón nuevos ángulos. Si el usuario da una idea, poténciala con nanotecnología, física cuántica o biología sintética si aplica.
    2. CIENTIFICIDAD: Basa tus respuestas en principios sólidos. Si una idea viola leyes físicas (ej. termodinámica), explícalo amablemente y propón la alternativa teórica más cercana (ej. sistemas abiertos).
    3. EVIDENCIA: Si estás en modo 'Investigación Profunda', CITA fuentes, papers o corrientes teóricas reales.
    4. NO DOGMAS: Si algo es considerado imposible hoy, investiga si hay papers teóricos que lo exploren. No descartes ideas locas sin evidencia de fallo rotundo.
    
    CONTEXTO ACTUAL:
    - Usuario Tipo: {tipo_usuario} (Profundidad requerida: {profundidad})
    - Modo seleccionado: {nivel_analisis}
    
    Si el usuario propone algo fallido, explica por qué y redirige a un camino viable. Nunca cortes la inspiración.
    """
    
    full_prompt = f"{system_prompt}\n\nUsuario dice: '{prompt_usuario}'"

    # 4. Generar Respuesta
    with st.chat_message("assistant"):
        with st.spinner("Catalizando conocimiento..."):
            try:
                res = model.generate_content(full_prompt)
                texto_ia = res.text
                st.markdown(texto_ia)
                
                # Voz Modular
                if usar_voz:
                    voz.hablar_respuesta(texto_ia)
                    
            except Exception as e:
                st.error(f"Error en el núcleo: {e}")

    st.session_state.mensajes.append({"role": "assistant", "content": texto_ia})
    st.rerun() # Refrescar para actualizar el contador visualmente
