import streamlit as st

# Configuración inicial para un diseño optimizado y profesional
st.set_page_config(
    page_title="SokoNews - Recomendador de Noticias",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo global con CSS avanzado para un diseño inspirado en Microsoft Fluent Design
st.markdown("""
    <style>
        /* Estilo general */
        body {
            background-color: #f5f5f5 !important;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #2e2e2e;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Encabezado */
        .header-container {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px 0;
            border-bottom: 2px solid #00A4EF;
        }
        .main-title {
            color: #00A4EF;
            font-size: 2.8em;
            font-weight: 700;
            margin: 0;
        }
        .subtitle {
            color: #737373;
            font-size: 1.1em;
            font-weight: 400;
            margin-top: 5px;
        }

        /* Sección de controles */
        .control-section {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
            display: flex;
            gap: 20px;
            align-items: center;
        }
        .stSelectbox > div > div > div {
            background-color: #f9f9f9;
            border: 1px solid #00A4EF;
            border-radius: 5px;
            padding: 5px;
            font-size: 1em;
        }
        .stSlider > div > div > div > div {
            background-color: #00A4EF;
        }
        .control-label {
            color: #00A4EF;
            font-size: 1em;
            font-weight: 500;
            margin-bottom: 5px;
        }

        /* Pestañas */
        .stTabs {
            margin-top: 20px;
        }
        .stTabs [role="tab"] {
            background-color: #e6f7ff;
            color: #00A4EF;
            border-radius: 10px 10px 0 0;
            padding: 12px 25px;
            font-weight: 500;
            font-size: 1em;
            transition: background-color 0.3s, color 0.3s;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: #ffffff;
            color: #F25022;
            border-bottom: 3px solid #F25022;
        }
        .stTabs [role="tab"]:hover {
            background-color: #d0eaff;
        }
        .tab-content {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 0 10px 10px 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }

        /* Tarjetas de artículos */
        .article-card {
            background-color: #e6f7ff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid #00A4EF;
        }
        .article-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        }
        .article-title {
            color: #00A4EF;
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .article-summary {
            color: #737373;
            font-size: 1em;
            line-height: 1.5;
        }
        .description-text {
            color: #737373;
            font-size: 1em;
            font-style: italic;
            margin-bottom: 25px;
            line-height: 1.6;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #737373;
            font-size: 0.9em;
            margin-top: 40px;
            padding: 20px 0;
            border-top: 1px solid #00A4EF;
        }
        .footer a {
            color: #00A4EF;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Encabezado con logo y título
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image("logo.png", width=80)
    except:
        st.markdown("🖼️")
with col2:
    st.markdown('<h1 class="main-title">SokoNews</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Descubre noticias personalizadas con tecnología de Microsoft</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sección de controles para selección de perfil y número de recomendaciones
st.markdown('<div class="control-section">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown('<p class="control-label">👤 Perfil de usuario</p>', unsafe_allow_html=True)
    user_profiles = ["Amante de la tecnología", "Fanático del deporte", "Entusiasta de política", "Aficionado al cine"]
    selected_profile = st.selectbox("", user_profiles, help="Elige un perfil para personalizar tus recomendaciones.")
with col2:
    st.markdown('<p class="control-label">📏 Número de recomendaciones</p>', unsafe_allow_html=True)
    num_recommendations = st.slider("", 1, 20, 5, help="Ajusta cuántas noticias deseas ver.")
with col3:
    st.markdown('<p class="control-label">🔄 Actualizar</p>', unsafe_allow_html=True)
    if st.button("Refrescar"):
        st.experimental_rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Datos dummy para las recomendaciones (serán reemplazados por datos reales más adelante)
collab_recommendations = {
    "Amante de la tecnología": [
        ("La IA revoluciona el mundo", "Un nuevo avance en inteligencia artificial está cambiando cómo interactuamos con la tecnología diaria."),
        ("El futuro de los smartphones", "Innovaciones que cambiarán el mercado móvil en 2025 y más allá."),
        ("5G y más allá", "Cómo la tecnología 5G está transformando las comunicaciones globales."),
        ("El auge de la realidad virtual", "Nuevos dispositivos VR que están llevando la inmersión al siguiente nivel."),
        ("Ciberseguridad en 2025", "Tendencias y amenazas emergentes que debes conocer para proteger tus datos."),
        ("El impacto de la nube", "Cómo la nube está transformando las empresas modernas."),
        ("Avances en robótica", "Robots que cambiarán nuestras vidas en la próxima década."),
        ("El futuro del trabajo remoto", "Tecnologías que están redefiniendo el teletrabajo."),
        ("Blockchain más allá de las criptos", "Aplicaciones innovadoras que están revolucionando industrias."),
        ("Seguridad en IoT", "Cómo proteger tus dispositivos conectados en un mundo hiperconectado."),
    ],
    "Fanático del deporte": [
        ("Final de la Champions 2025", "Resumen del partido de la década con momentos clave y análisis."),
        ("Atletas que rompen récords", "Historias inspiradoras de deportistas que están haciendo historia en 2025."),
        ("NBA: Lo que viene", "Predicciones para la temporada 2025-2026 y jugadores a seguir."),
        ("El regreso de las Olimpiadas", "Preparativos para el próximo evento mundial que no te puedes perder."),
        ("Fútbol y tecnología", "Cómo la IA está cambiando las estrategias y el análisis del juego."),
        ("Entrenamiento con tecnología", "Gadgets que están ayudando a los atletas a mejorar su rendimiento."),
        ("Lesiones deportivas: Prevención", "Consejos prácticos para evitar lesiones comunes en deportistas."),
        ("Fórmula 1: Temporada 2025", "Lo que viene en el automovilismo y los equipos favoritos."),
        ("Deportes extremos", "Nuevas tendencias y destinos para los amantes de la adrenalina."),
        ("Historias de superación", "Atletas que vencieron la adversidad para alcanzar la gloria."),
    ],
    "Entusiasta de política": [
        ("Elecciones 2025: Lo que debes saber", "Un análisis profundo de los candidatos y sus propuestas clave."),
        ("Políticas climáticas globales", "Nuevas medidas para combatir el cambio climático a nivel internacional."),
        ("Tensiones geopolíticas", "Lo último en relaciones internacionales y conflictos emergentes."),
        ("Reformas económicas", "Impacto de las nuevas leyes fiscales en la economía global."),
        ("Derechos humanos en foco", "Avances y desafíos actuales en la lucha por los derechos humanos."),
        ("La política en la era digital", "Cómo las redes sociales están influyendo en las decisiones políticas."),
        ("Cambio climático y acción política", "Decisiones clave que están moldeando el futuro del planeta."),
        ("El futuro de la democracia", "Tendencias globales que están redefiniendo los sistemas democráticos."),
        ("Economía post-pandemia", "Lecciones aprendidas y nuevas estrategias económicas."),
        ("Liderazgo femenino", "Mujeres que están cambiando el panorama político mundial."),
    ],
    "Aficionado al cine": [
        ("Estrenos de marzo 2025", "Las películas más esperadas del mes que no te puedes perder."),
        ("El renacer de los clásicos", "Remakes que están trayendo de vuelta historias icónicas con un toque moderno."),
        ("Oscars 2025: Predicciones", "Quiénes lideran las nominaciones y qué películas podrían ganar."),
        ("Cine independiente en auge", "Festivales que están destacando este año y películas imperdibles."),
        ("Tecnología en el cine", "Cómo los efectos visuales están evolucionando para crear experiencias únicas."),
        ("Directores emergentes", "Nuevos talentos que están dejando su marca en la industria cinematográfica."),
        ("El impacto del streaming", "Cómo las plataformas están cambiando la forma en que consumimos cine."),
        ("Cine de ciencia ficción", "Películas que predicen el futuro con un toque de creatividad."),
        ("Documentales imprescindibles", "Historias reales que inspiran y educan a la audiencia."),
        ("El arte de la cinematografía", "Técnicas detrás de las grandes películas que han marcado historia."),
    ],
}

content_based_recommendations = {
    "Amante de la tecnología": [
        ("Nuevos gadgets de 2025", "Lo último en tecnología portátil que está revolucionando el mercado."),
        ("El impacto de la nube", "Cómo la nube está transformando las operaciones empresariales modernas."),
        ("Avances en robótica", "Robots que cambiarán nuestras vidas en la próxima década con aplicaciones innovadoras."),
        ("El futuro del trabajo remoto", "Tecnologías que están redefiniendo el teletrabajo y la colaboración."),
        ("Blockchain más allá de las criptos", "Aplicaciones innovadoras que están revolucionando industrias como la salud y la logística."),
        ("IA y ética: Un debate", "Explorando los límites de la inteligencia artificial y sus implicaciones."),
        ("Tendencias tecnológicas 2025", "Qué esperar este año en el mundo de la tecnología y la innovación."),
        ("El auge de los drones", "Aplicaciones civiles y comerciales que están expandiendo el uso de drones."),
        ("Seguridad en IoT", "Cómo proteger tus dispositivos conectados en un mundo hiperconectado."),
        ("El futuro de la educación", "Tecnología que está transformando el aula y el aprendizaje."),
    ],
    "Fanático del deporte": [
        ("Entrenamiento con tecnología", "Gadgets que están ayudando a los atletas a mejorar su rendimiento físico."),
        ("Lesiones deportivas: Prevención", "Consejos prácticos para evitar lesiones comunes en deportistas de alto rendimiento."),
        ("Fórmula 1: Temporada 2025", "Lo que viene en el automovilismo y los equipos favoritos para ganar."),
        ("Deportes extremos", "Nuevas tendencias y destinos para los amantes de la adrenalina y la aventura."),
        ("Historias de superación", "Atletas que vencieron la adversidad para alcanzar la gloria deportiva."),
        ("Tecnología en el fútbol", "El VAR y otras innovaciones que están cambiando las reglas del juego."),
        ("Maratones más populares", "Eventos que no te puedes perder si eres un corredor apasionado."),
        ("Nutrición para atletas", "Consejos de expertos para optimizar tu dieta y rendimiento."),
        ("Deportes acuáticos", "Tendencias y competiciones que están marcando el 2025."),
        ("El impacto de los fans", "Cómo los seguidores están influyendo en los eventos deportivos modernos."),
    ],
    "Entusiasta de política": [
        ("La política en la era digital", "Cómo las redes sociales están influyendo en las decisiones políticas globales."),
        ("Cambio climático y acción política", "Decisiones clave que están moldeando el futuro del planeta en 2025."),
        ("El futuro de la democracia", "Tendencias globales que están redefiniendo los sistemas democráticos modernos."),
        ("Economía post-pandemia", "Lecciones aprendidas y nuevas estrategias económicas para un mundo en recuperación."),
        ("Liderazgo femenino", "Mujeres que están cambiando el panorama político mundial con sus iniciativas."),
        ("Tecnología y elecciones", "El papel de los datos y la IA en las campañas electorales modernas."),
        ("Políticas de IA", "Regulaciones que están emergiendo para controlar el uso de la inteligencia artificial."),
        ("Sostenibilidad global", "Acuerdos internacionales que están marcando el camino hacia un futuro sostenible."),
        ("Derechos digitales", "Privacidad y seguridad en la era digital: un debate en curso."),
        ("El futuro del trabajo", "Políticas laborales emergentes para adaptarse a un mundo cambiante."),
    ],
    "Aficionado al cine": [
        ("Directores emergentes", "Nuevos talentos que están dejando su marca en la industria cinematográfica global."),
        ("El impacto del streaming", "Cómo las plataformas están cambiando la forma en que consumimos cine y series."),
        ("Cine de ciencia ficción", "Películas que predicen el futuro con un toque de creatividad e innovación visual."),
        ("Documentales imprescindibles", "Historias reales que inspiran y educan a la audiencia sobre temas clave."),
        ("El arte de la cinematografía", "Técnicas detrás de las grandes películas que han marcado historia en el cine."),
        ("Cine y tecnología", "Cómo la IA está creando nuevas experiencias cinematográficas inmersivas."),
        ("Festivales de cine 2025", "Eventos imperdibles para los amantes del cine independiente y comercial."),
        ("El legado de los clásicos", "Películas que definieron una era y siguen siendo relevantes hoy."),
        ("Nuevos géneros cinematográficos", "Tendencias emergentes que están redefiniendo el cine moderno."),
        ("Cine y realidad aumentada", "Experiencias inmersivas que están llevando el cine al siguiente nivel."),
    ],
}

hybrid_recommendations = {
    "Amante de la tecnología": [
        ("IA y ética: Un debate", "Explorando los límites de la inteligencia artificial y sus implicaciones éticas."),
        ("Tendencias tecnológicas 2025", "Qué esperar este año en el mundo de la tecnología y la innovación global."),
        ("El auge de los drones", "Aplicaciones civiles y comerciales que están expandiendo el uso de drones en 2025."),
        ("Seguridad en IoT", "Cómo proteger tus dispositivos conectados en un mundo hiperconectado e interdependiente."),
        ("El futuro de la educación", "Tecnología que está transformando el aula y el aprendizaje a nivel global."),
        ("Nuevos gadgets de 2025", "Lo último en tecnología portátil que está revolucionando el mercado actual."),
        ("El impacto de la nube", "Cómo la nube está transformando las operaciones empresariales modernas y eficientes."),
        ("Avances en robótica", "Robots que cambiarán nuestras vidas en la próxima década con aplicaciones innovadoras."),
        ("El futuro del trabajo remoto", "Tecnologías que están redefiniendo el teletrabajo y la colaboración digital."),
        ("Blockchain más allá de las criptos", "Aplicaciones innovadoras que están revolucionando industrias como la salud y la logística."),
    ],
    "Fanático del deporte": [
        ("Tecnología en el fútbol", "El VAR y otras innovaciones que están cambiando las reglas del juego moderno."),
        ("Maratones más populares", "Eventos que no te puedes perder si eres un corredor apasionado y competitivo."),
        ("Nutrición para atletas", "Consejos de expertos para optimizar tu dieta y rendimiento físico."),
        ("Deportes acuáticos", "Tendencias y competiciones que están marcando el 2025 en el mundo deportivo."),
        ("El impacto de los fans", "Cómo los seguidores están influyendo en los eventos deportivos modernos y globales."),
        ("Final de la Champions 2025", "Resumen del partido de la década con momentos clave y análisis detallado."),
        ("Atletas que rompen récords", "Historias inspiradoras de deportistas que están haciendo historia en 2025."),
        ("NBA: Lo que viene", "Predicciones para la temporada 2025-2026 y jugadores a seguir de cerca."),
        ("El regreso de las Olimpiadas", "Preparativos para el próximo evento mundial que no te puedes perder."),
        ("Fórmula 1: Temporada 2025", "Lo que viene en el automovilismo y los equipos favoritos para ganar."),
    ],
    "Entusiasta de política": [
        ("Tecnología y elecciones", "El papel de los datos y la IA en las campañas electorales modernas y digitales."),
        ("Políticas de IA", "Regulaciones que están emergiendo para controlar el uso de la inteligencia artificial."),
        ("Sostenibilidad global", "Acuerdos internacionales que están marcando el camino hacia un futuro sostenible."),
        ("Derechos digitales", "Privacidad y seguridad en la era digital: un debate en curso a nivel global."),
        ("El futuro del trabajo", "Políticas laborales emergentes para adaptarse a un mundo cambiante y tecnológico."),
        ("Elecciones 2025: Lo que debes saber", "Un análisis profundo de los candidatos y sus propuestas clave para el futuro."),
        ("Políticas climáticas globales", "Nuevas medidas para combatir el cambio climático a nivel internacional y local."),
        ("Tensiones geopolíticas", "Lo último en relaciones internacionales y conflictos emergentes en 2025."),
        ("Reformas económicas", "Impacto de las nuevas leyes fiscales en la economía global y local."),
        ("Liderazgo femenino", "Mujeres que están cambiando el panorama político mundial con sus iniciativas."),
    ],
    "Aficionado al cine": [
        ("Cine y tecnología", "Cómo la IA está creando nuevas experiencias cinematográficas inmersivas y únicas."),
        ("Festivales de cine 2025", "Eventos imperdibles para los amantes del cine independiente y comercial este año."),
        ("El legado de los clásicos", "Películas que definieron una era y siguen siendo relevantes hoy en día."),
        ("Nuevos géneros cinematográficos", "Tendencias emergentes que están redefiniendo el cine moderno y global."),
        ("Cine y realidad aumentada", "Experiencias inmersivas que están llevando el cine al siguiente nivel de innovación."),
        ("Estrenos de marzo 2025", "Las películas más esperadas del mes que no te puedes perder en cines."),
        ("El renacer de los clásicos", "Remakes que están trayendo de vuelta historias icónicas con un toque moderno."),
        ("Oscars 2025: Predicciones", "Quiénes lideran las nominaciones y qué películas podrían ganar este año."),
        ("Cine independiente en auge", "Festivales que están destacando este año y películas imperdibles para ver."),
        ("Tecnología en el cine", "Cómo los efectos visuales están evolucionando para crear experiencias únicas."),
    ],
}

# Función para obtener recomendaciones
def get_recommendations(profile, recommender_type):
    if recommender_type == "Filtrado Colaborativo":
        return collab_recommendations.get(profile, [])[:num_recommendations]
    elif recommender_type == "Basado en Contenido":
        return content_based_recommendations.get(profile, [])[:num_recommendations]
    elif recommender_type == "Híbrido":
        return hybrid_recommendations.get(profile, [])[:num_recommendations]
    return []

# Pestañas para cada tipo de recomendador con un diseño interactivo y moderno
tab1, tab2, tab3 = st.tabs(["Filtrado Colaborativo", "Basado en Contenido", "Híbrido"])

with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Filtrado Colaborativo</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">Este método analiza el comportamiento de usuarios con intereses similares a los tuyos para recomendarte noticias relevantes.</p>', unsafe_allow_html=True)
    recommendations = get_recommendations(selected_profile, "Filtrado Colaborativo")
    if recommendations:
        for title, summary in recommendations:
            st.markdown(
                f"""
                <div class="article-card">
                    <h3 class="article-title">{title}</h3>
                    <p class="article-summary">{summary}</p>
                </div>
                """, unsafe_allow_html=True
            )
    else:
        st.markdown('<p class="description-text">No hay recomendaciones disponibles para este perfil en este momento.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Basado en Contenido</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">Este método recomienda noticias basándose en el contenido de los artículos que has leído anteriormente, identificando patrones en tus preferencias.</p>', unsafe_allow_html=True)
    recommendations = get_recommendations(selected_profile, "Basado en Contenido")
    if recommendations:
        for title, summary in recommendations:
            st.markdown(
                f"""
                <div class="article-card">
                    <h3 class="article-title">{title}</h3>
                    <p class="article-summary">{summary}</p>
                </div>
                """, unsafe_allow_html=True
            )
    else:
        st.markdown('<p class="description-text">No hay recomendaciones disponibles para este perfil en este momento.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Híbrido</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">Este método combina lo mejor del filtrado colaborativo y basado en contenido para ofrecerte recomendaciones más precisas y personalizadas.</p>', unsafe_allow_html=True)
    recommendations = get_recommendations(selected_profile, "Híbrido")
    if recommendations:
        for title, summary in recommendations:
            st.markdown(
                f"""
                <div class="article-card">
                    <h3 class="article-title">{title}</h3>
                    <p class="article-summary">{summary}</p>
                </div>
                """, unsafe_allow_html=True
            )
    else:
        st.markdown('<p class="description-text">No hay recomendaciones disponibles para este perfil en este momento.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer con información adicional y enlaces
st.markdown(
    """
    <div class="footer">
        <p>© 2025 SokoNews - Desarrollado para Microsoft Capstone Project</p>
        <p>Explora el poder de la recomendación de noticias con el <a href="https://www.kaggle.com/datasets/arashnic/mind-news-dataset" target="_blank">dataset MIND</a>.</p>
    </div>
    """, unsafe_allow_html=True
)
