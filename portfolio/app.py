import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Véronique DJAGBA — Data Analyst",
    page_icon="📊",
    layout="wide"
)

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

photo_base64 = get_image_base64("photo.jpeg")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');
* { font-family: 'Poppins', sans-serif; }
.main { background-color: #0F0A1E; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.hero {
    background: linear-gradient(135deg, #1A0A3E 0%, #2D1B69 50%, #1A0A3E 100%);
    border-bottom: 2px solid #7C3AED;
    display: flex;
    min-height: 100vh;
}
.hero-left {
    width: 40%;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
}
.hero-left img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top center;
    display: block;
    filter: brightness(0.9);
}
.hero-left-overlay {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: linear-gradient(to right, transparent 60%, #1A0A3E 100%);
}
.hero-right {
    width: 60%;
    padding: 80px 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.hero-name {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 8px;
    letter-spacing: 2px;
    line-height: 1.2;
}
.hero-name span { color: #A855F7; }
.hero-title {
    font-size: 1rem;
    color: #C4B5FD;
    font-weight: 300;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.hero-location { font-size: 0.9rem; color: #8B7FC7; margin-bottom: 24px; }
.hero-bio {
    font-size: 0.95rem;
    color: #DDD6FE;
    line-height: 1.8;
    font-weight: 300;
    margin-bottom: 40px;
    max-width: 500px;
}
.contact-links { display: flex; gap: 14px; flex-wrap: wrap; }
.contact-link {
    background: rgba(124,58,237,0.2);
    border: 1px solid #7C3AED;
    color: #C4B5FD !important;
    padding: 10px 22px;
    border-radius: 50px;
    text-decoration: none !important;
    font-size: 0.85rem;
}

.section { padding: 70px 60px; background: #0F0A1E; }
.section-alt { padding: 70px 60px; background: #130D24; }
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #A855F7;
    margin-bottom: 8px;
    font-weight: 700;
}
.section-divider {
    width: 60px; height: 3px;
    background: linear-gradient(90deg, #7C3AED, #A855F7);
    border-radius: 2px;
    margin-bottom: 40px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 40px;
}
.stat-card {
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 16px;
    padding: 30px 20px;
    text-align: center;
}
.stat-number { font-size: 2.5rem; font-weight: 700; color: #A855F7; margin-bottom: 4px; }
.stat-label { font-size: 0.85rem; color: #8B7FC7; text-transform: uppercase; letter-spacing: 1px; }

.project-card {
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 20px;
}
.project-title { font-size: 1.1rem; font-weight: 600; color: #E9D5FF; margin-bottom: 8px; }
.project-desc { font-size: 0.9rem; color: #8B7FC7; line-height: 1.7; margin-bottom: 12px; }
.project-tags { display: flex; gap: 8px; flex-wrap: wrap; }
.tag {
    background: rgba(124,58,237,0.2);
    color: #C4B5FD;
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 0.78rem;
    border: 1px solid rgba(124,58,237,0.4);
}

.coming-soon {
    background: rgba(124,58,237,0.08);
    border: 1px dashed #7C3AED;
    border-radius: 16px;
    padding: 60px 40px;
    text-align: center;
}
.coming-soon-icon { font-size: 3rem; margin-bottom: 16px; }
.coming-soon-title { font-size: 1.3rem; color: #C4B5FD; font-weight: 600; margin-bottom: 8px; }
.coming-soon-text { color: #6D5FA8; font-size: 0.95rem; line-height: 1.7; }
.coming-soon-date {
    display: inline-block;
    background: rgba(124,58,237,0.2);
    border: 1px solid #7C3AED;
    color: #A855F7;
    padding: 6px 20px;
    border-radius: 50px;
    font-size: 0.85rem;
    margin-top: 16px;
    font-weight: 500;
}

.info-card {
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 16px;
}
.info-card-title { font-size: 1rem; font-weight: 600; color: #E9D5FF; margin-bottom: 4px; }
.info-card-subtitle { font-size: 0.88rem; color: #A855F7; margin-bottom: 4px; }
.info-card-date { font-size: 0.82rem; color: #6D5FA8; }

.skill-badge {
    display: inline-block;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.4);
    color: #C4B5FD;
    padding: 8px 18px;
    border-radius: 50px;
    font-size: 0.88rem;
    margin: 6px;
}

.footer {
    background: #08051A;
    padding: 40px 60px;
    text-align: center;
    border-top: 1px solid rgba(124,58,237,0.2);
}
.footer-text { color: #4A3D7A; font-size: 0.85rem; }
.footer-name { color: #7C3AED; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ===================== HERO =====================
st.markdown(f"""
<div class="hero">
    <div class="hero-left">
        <img src="data:image/jpeg;base64,{photo_base64}" alt="Véronique DJAGBA"/>
        <div class="hero-left-overlay"></div>
    </div>
    <div class="hero-right">
        <div class="hero-name">DJAGBA Kuinambe<br><span>Véronique</span></div>
        <div class="hero-title">Data Analyst · Master IA & Big Data</div>
        <div class="hero-location">📍 Lomé, Togo</div>
        <div class="hero-bio">
            Étudiante en Master IA & Big Data, passionnée par l'analyse de données et les outils 
            d'intelligence artificielle. Curieuse et motivée, je souhaite mettre mes compétences 
            au service de projets qui transforment les données en décisions utiles.
        </div>
        <div class="contact-links">
            <a class="contact-link" href="mailto:veronique.djagba@gmail.com">✉ Email</a>
            <a class="contact-link" href="https://www.linkedin.com/in/véronique-djagba-31b86b2b6/" target="_blank">💼 LinkedIn</a>
            <a class="contact-link" href="https://github.com/DJAGBA/"> GitHub</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== STATS =====================
st.markdown("""
<div class="section">
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">4</div>
            <div class="stat-label">Stages réalisés</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">12</div>
            <div class="stat-label">Projets data prévus</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">Décembre.</div>
            <div class="stat-label">Portfolio complet 2026</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== COMPÉTENCES =====================
st.markdown("""
<div class="section-alt">
    <div class="section-title">Compétences</div>
    <div class="section-divider"></div>
    <div style="margin-bottom: 20px;">
        <p style="color: #8B7FC7; font-size: 0.9rem; margin-bottom: 16px;">Outils Data & Analyse</p>
        <span class="skill-badge">📊 Excel</span>
        <span class="skill-badge">🔄 Power Query</span>
        <span class="skill-badge">📈 Power BI</span>
        <span class="skill-badge">🗄️ SQL</span>
        <span class="skill-badge">🐍 Python</span>
    </div>
    <div style="margin-bottom: 20px;">
        <p style="color: #8B7FC7; font-size: 0.9rem; margin-bottom: 16px;">Développement</p>
        <span class="skill-badge">⚛️ React.js</span>
        <span class="skill-badge">🟨 JavaScript</span>
        <span class="skill-badge">🐘 PHP</span>
        <span class="skill-badge">🟢 Node.js</span>
        <span class="skill-badge">🔧 Git / GitHub</span>
    </div>
    <div>
        <p style="color: #8B7FC7; font-size: 0.9rem; margin-bottom: 16px;">En cours d'apprentissage</p>
        <span class="skill-badge">☁️ DevOps & Cloud AWS</span>
        <span class="skill-badge">🤖 IA Générative</span>
        <span class="skill-badge">📉 R</span>
        <span class="skill-badge">🧠 Machine learning</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== PROJETS =====================
st.markdown("""
<div class="section">
    <div class="section-title">Projets Data</div>
    <div class="section-divider"></div>
""", unsafe_allow_html=True)

# Projet 1
st.markdown("""
    <div class="project-card">
        <div class="project-title">📈 Projet 1 — Analyse des performances commerciales (Excel)</div>
        <div class="project-desc">
            Conception d'un tableau de bord interactif pour suivre les ventes par région et catégorie. 
            Analyse des KPIs clés : ventes totales 2 297 200 FCFA, marge 286 397 FCFA, taux de marge 12,47%. 
            Visualisation des tendances mensuelles et classement des 10 meilleurs produits.
        </div>
        <div class="project-tags">
            <span class="tag">Excel</span>
            <span class="tag">Power Query</span>
            <span class="tag">TCD</span>
            <span class="tag">KPIs</span>
            <span class="tag">Dashboard</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Bouton voir projet 1
with st.expander("📸 Voir le tableau de bord →"):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(BASE_DIR, "images", "projet1.png")
    if os.path.exists(img_path):
        st.image(img_path,
                 caption="Tableau de bord — Analyse des performances commerciales",
                 use_container_width=True)
    else:
        st.info("Image bientôt disponible...")

# Coming soon
st.markdown("""
    <div class="coming-soon">
        <div class="coming-soon-icon">🚀</div>
        <div class="coming-soon-title">10 projets data en cours de réalisation</div>
        <div class="coming-soon-text">
            Chaque semaine, un nouveau projet sera ajouté ici.<br>
            Suivez ma progression sur LinkedIn !
        </div>
        <div class="coming-soon-date">📅 Septembre — Novembre 2026</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== FORMATION =====================
st.markdown("""
<div class="section-alt">
    <div class="section-title">Formation</div>
    <div class="section-divider"></div>
    <div class="info-card">
        <div class="info-card-title">Master 1 — Intelligence Artificielle & Big Data</div>
        <div class="info-card-subtitle">ESGIS — École Supérieure de Gestion d'Informatique et des Sciences</div>
        <div class="info-card-date">📅 2025 — 2026 · Lomé, Togo</div>
    </div>
    <div class="info-card">
        <div class="info-card-title">Licence — Architecture des Logiciels</div>
        <div class="info-card-subtitle">ESGIS — École Supérieure de Gestion d'Informatique et des Sciences</div>
        <div class="info-card-date">📅 2024 — 2025 · Lomé, Togo</div>
    </div>
    <div class="info-card">
        <div class="info-card-title">Baccalauréat Série D</div>
        <div class="info-card-subtitle">Complexe Scolaire Ebenezer</div>
        <div class="info-card-date">📅 2022 · Lomé, Togo</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== EXPÉRIENCES =====================
st.markdown("""
<div class="section">
    <div class="section-title">Expériences</div>
    <div class="section-divider"></div>
    <div class="info-card">
        <div class="info-card-title">Stagiaire — Développement Web & Mobile</div>
        <div class="info-card-subtitle">Moon Togo</div>
        <div class="info-card-date">📅 Août — Novembre 2026 · Lomé, Togo</div>
    </div>
    <div class="info-card">
        <div class="info-card-title">Développeuse Fullstack (Stage)</div>
        <div class="info-card-subtitle">Yas-Togo</div>
        <div class="info-card-date">📅 Avril — Juin 2026 · Lomé, Togo</div>
    </div>
    <div class="info-card">
        <div class="info-card-title">Stagiaire — Direction des Systèmes d'Information</div>
        <div class="info-card-subtitle">CEET — Compagnie Énergie Électrique du Togo</div>
        <div class="info-card-date">📅 Juillet — Septembre 2025 · Lomé, Togo</div>
    </div>
    <div class="info-card">
        <div class="info-card-title">Stagiaire Développeuse</div>
        <div class="info-card-subtitle">Numerum DEV-Center</div>
        <div class="info-card-date">📅 Novembre 2024 — Mars 2025 · Lomé, Togo</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== CERTIFICATIONS =====================
st.markdown("""
<div class="section-alt">
    <div class="section-title">Certifications</div>
    <div class="section-divider"></div>
    <div class="coming-soon">
        <div class="coming-soon-icon">📜</div>
        <div class="coming-soon-title">Certifications en cours d'obtention</div>
        <div class="coming-soon-text">
            Google Cloud Skills Boost · Microsoft AI-900 · Kaggle Learn
        </div>
        <div class="coming-soon-date">📅 Mise à jour dès obtention</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== FOOTER =====================
st.markdown("""
<div class="footer">
    <div class="footer-text">
        © 2026 <span class="footer-name">DJAGBA Kuinambe Véronique</span> · 
        Data Analyst · Lomé, Togo 🇹🇬<br>
        <span style="color:#3D2E6B; font-size:0.8rem;">Portfolio en construction — mise à jour hebdomadaire</span>
    </div>
</div>
""", unsafe_allow_html=True)