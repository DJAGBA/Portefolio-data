import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Projet 2 — Performances RH",
    layout="wide"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
* { font-family: 'Poppins', sans-serif; }
.main { background-color: #F0F4FF; }
.block-container { padding: 2rem 3rem !important; }

.dash-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1E3A8A;
    margin-bottom: 4px;
}
.dash-subtitle {
    font-size: 0.95rem;
    color: #64748B;
    margin-bottom: 30px;
}
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #BFDBFE;
    border-left: 4px solid ;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(37,99,235,0.08);
}
.kpi-number {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1E40AF;
}
.kpi-label {
    font-size: 0.78rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}
.insight-box {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-left: 4px solid;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 10px;
}
.insight-title {
    font-size: 1rem;
    font-weight: 600;
    color: #1E3A8A;
    margin-bottom: 10px;
}
.insight-text {
    font-size: 0.9rem;
    color: #374151;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

# ===================== CHARGEMENT =====================
@st.cache_data
def charger_donnees():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    chemin = os.path.join(BASE_DIR, "HRDataset_v14.csv")
    df = pd.read_csv(chemin)
    df = df.drop_duplicates(subset=['EmpID'], keep='first')
    df['DateofTermination'] = df['DateofTermination'].fillna("Actif")
    df['ManagerID'] = df['ManagerID'].fillna(-1)
    df['PerformanceScore'] = df['PerformanceScore'].astype(str).str.strip()
    return df

df = charger_donnees()

# Traduction des niveaux de performance
traduction_perf = {
    'Exceeds': 'Dépasse les attentes',
    'Fully Meets': 'Atteint les objectifs',
    'Needs Improvement': 'À améliorer',
    'PIP': 'Plan de redressement'
}
df['Performance'] = df['PerformanceScore'].map(traduction_perf)

# ===================== TITRE =====================
st.markdown("""
<div class="dash-title"> Tableau de Bord RH - Performances des Employés</div>
<div class="dash-subtitle">Analyse des distributions, détection des anomalies et facteurs de performance · Source : HRDataset v14</div>
""", unsafe_allow_html=True)

# ===================== FILTRES =====================
col1, col2, col3 = st.columns(3)
with col1:
    departements = ["Tous les départements"] + sorted(df['Department'].dropna().unique().tolist())
    dept_select = st.selectbox("Département", departements)
with col2:
    niveaux = ["Tous les niveaux"] + list(traduction_perf.values())
    perf_select = st.selectbox(" Niveau de performance", niveaux)
with col3:
    statuts = ["Tous", "Actif", "Parti"]
    statut_select = st.selectbox(" Statut de l'employé", statuts)

# Filtrage
df_f = df.copy()
if dept_select != "Tous les départements":
    df_f = df_f[df_f['Department'] == dept_select]
if perf_select != "Tous les niveaux":
    df_f = df_f[df_f['Performance'] == perf_select]
if statut_select == "Actif":
    df_f = df_f[df_f['DateofTermination'] == "Actif"]
elif statut_select == "Parti":
    df_f = df_f[df_f['DateofTermination'] != "Actif"]

st.divider()

# ===================== KPIs =====================
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-number">{len(df_f)}</div>
        <div class="kpi-label">Total Employés</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-number">${df_f['Salary'].mean():,.0f}</div>
        <div class="kpi-label">Salaire Moyen</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-number">{df_f['EngagementSurvey'].mean():.1f}/5</div>
        <div class="kpi-label">Engagement Moyen</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-number">{df_f['Absences'].mean():.1f}Jours</div>
        <div class="kpi-label">Absences Moyennes</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-number">{df_f['SpecialProjectsCount'].mean():.1f}</div>
        <div class="kpi-label">Projets Spéciaux</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ===================== GRAPHIQUE 1 + 2 =====================
c1, c2 = st.columns(2)

ordre_fr = ['Dépasse les attentes', 'Atteint les objectifs', 'À améliorer', 'Plan de redressement']
couleurs_bleu = ['#1E40AF', '#2563EB', '#60A5FA', '#BFDBFE']

with c1:
    counts = df_f['Performance'].value_counts().reindex(ordre_fr).fillna(0).reset_index()
    counts.columns = ['Niveau de Performance', 'Nombre']
    fig1 = px.bar(counts,
                  x='Niveau de Performance',
                  y='Nombre',
                  title="Répartition des Employés par Niveau de Performance",
                  color='Niveau de Performance',
                  color_discrete_sequence=couleurs_bleu,
                  text='Nombre')
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#F0F4FF',
        font_color='#1E3A8A',
        showlegend=False,
        title_font_size=13,
        title_font_color='#1E3A8A'
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    ordre_box = ['Plan de redressement', 'À améliorer', 'Atteint les objectifs', 'Dépasse les attentes']
    fig2 = px.box(df_f,
                  x='Performance',
                  y='Salary',
                  category_orders={'Performance': ordre_box},
                  title="Distribution des Salaires par Niveau de Performance",
                  color='Performance',
                  color_discrete_sequence=couleurs_bleu)
    fig2.update_layout(
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#F0F4FF',
        font_color='#1E3A8A',
        showlegend=False,
        title_font_size=13,
        title_font_color='#1E3A8A'
    )
    st.plotly_chart(fig2, use_container_width=True)

# ===================== GRAPHIQUE 3 + 4 =====================
c3, c4 = st.columns(2)

with c3:
    avg_proj = df_f.groupby('Performance')['SpecialProjectsCount'].mean().reindex(ordre_box).reset_index()
    avg_proj.columns = ['Performance', 'Moyenne']
    fig3 = px.bar(avg_proj,
                  x='Performance',
                  y='Moyenne',
                  title="Nombre Moyen de Projets Spéciaux par Performance",
                  color='Performance',
                  color_discrete_sequence=couleurs_bleu,
                  text=avg_proj['Moyenne'].round(2))
    fig3.update_traces(textposition='outside')
    fig3.update_layout(
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#F0F4FF',
        font_color='#1E3A8A',
        showlegend=False,
        title_font_size=13,
        title_font_color='#1E3A8A'
    )
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    avg_abs = df_f.groupby('Performance')['Absences'].mean().reindex(ordre_box).reset_index()
    avg_abs.columns = ['Performance', 'Moyenne']
    fig4 = px.bar(avg_abs,
                  x='Performance',
                  y='Moyenne',
                  title="Nombre Moyen d'Absences par Niveau de Performance",
                  color='Performance',
                  color_discrete_sequence=['#BFDBFE', '#60A5FA', '#2563EB', '#1E40AF'],
                  text=avg_abs['Moyenne'].round(2))
    fig4.update_traces(textposition='outside')
    fig4.update_layout(
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#F0F4FF',
        font_color='#1E3A8A',
        showlegend=False,
        title_font_size=13,
        title_font_color='#1E3A8A'
    )
    st.plotly_chart(fig4, use_container_width=True)

# ===================== GRAPHIQUE 5 + 6 =====================
c5, c6 = st.columns(2)

with c5:
    cols = ['PerfScoreID', 'SpecialProjectsCount', 'EngagementSurvey', 'Absences', 'Salary']
    noms_fr = {
        'PerfScoreID': 'Score Performance',
        'SpecialProjectsCount': 'Projets Spéciaux',
        'EngagementSurvey': 'Engagement',
        'Absences': 'Absences',
        'Salary': 'Salaire'
    }
    corr = df_f[cols].corr().round(2)
    corr.index = [noms_fr[c] for c in cols]
    corr.columns = [noms_fr[c] for c in cols]
    fig5 = px.imshow(corr,
                     text_auto=True,
                     color_continuous_scale='Blues',
                     title="Matrice de Corrélation — Performance et Facteurs RH")
    fig5.update_layout(
        paper_bgcolor='#F0F4FF',
        font_color='#1E3A8A',
        title_font_size=13,
        title_font_color='#1E3A8A'
    )
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    dept_proj = df_f.groupby('Department')['SpecialProjectsCount'].mean().reset_index()
    dept_proj.columns = ['Département', 'Moyenne']
    dept_proj = dept_proj.sort_values('Moyenne', ascending=True)
    fig6 = px.bar(dept_proj,
                  x='Moyenne',
                  y='Département',
                  orientation='h',
                  title="Charge de Travail par Département (Projets Spéciaux)",
                  color='Moyenne',
                  color_continuous_scale='Blues',
                  text=dept_proj['Moyenne'].round(2))
    fig6.update_traces(textposition='outside')
    fig6.update_layout(
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#F0F4FF',
        font_color='#1E3A8A',
        title_font_size=13,
        title_font_color='#1E3A8A',
        showlegend=False
    )
    st.plotly_chart(fig6, use_container_width=True)

# ===================== DÉTECTION ANOMALIES =====================
st.divider()
st.markdown("### Détection des Valeurs Aberrantes - Règle des 1,5 × IQR")

noms_variables = {
    'Salary': 'Salaire',
    'Absences': 'Absences',
    'SpecialProjectsCount': 'Projets Spéciaux',
    'EngagementSurvey': 'Engagement'
}
col_fr = st.selectbox("Choisir une variable à analyser", list(noms_variables.values()))
col_en = [k for k, v in noms_variables.items() if v == col_fr][0]

Q1 = df_f[col_en].quantile(0.25)
Q3 = df_f[col_en].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
anomalies = df_f[(df_f[col_en] < lower) | (df_f[col_en] > upper)]

oc1, oc2, oc3, oc4 = st.columns(4)
with oc1:
    st.metric("Premier Quartile (Q1)", f"{Q1:.2f}")
with oc2:
    st.metric("Troisième Quartile (Q3)", f"{Q3:.2f}")
with oc3:
    st.metric("Écart Interquartile (IQR)", f"{IQR:.2f}")
with oc4:
    st.metric("Valeurs aberrantes détectées", len(anomalies))

fig_out = px.box(df_f,
                 y=col_en,
                 title=f"Distribution et Valeurs Aberrantes — {col_fr}",
                 color_discrete_sequence=['#2563EB'])
fig_out.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#F0F4FF',
    font_color='#1E3A8A'
)
st.plotly_chart(fig_out, use_container_width=True)

if len(anomalies) > 0:
    with st.expander(f"📋 Voir les {len(anomalies)} valeurs aberrantes détectées"):
        st.dataframe(
            anomalies[['EmpID', 'Department', 'Performance', col_en]].reset_index(drop=True),
            use_container_width=True
        )

# ===================== MES CONCLUSIONS =====================
st.divider()
st.markdown("""
<div class="insight-box">
    <div class="insight-title"> Mes Observations et Conclusions</div>
    <div class="insight-text">
        • Les employés qui dépassent les attentes réalisent en moyenne plus de projets spéciaux que les autres.<br>
        • Un taux d'absence élevé est souvent associé aux niveaux de performance les plus faibles.<br>
        • Le score d'engagement est positivement corrélé avec la performance globale de l'employé.<br>
        • Certains départements présentent une charge de travail déséquilibrée qui mérite une attention particulière.<br>
        • Des valeurs aberrantes de salaire existent indépendamment du niveau de performance,ce qui suggère d'autres facteurs comme l'ancienneté.
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== FOOTER =====================
st.divider()
st.markdown("""
<div style="text-align:center; color:#94A3B8; font-size:0.85rem;">
    © 2026 <span style="color:#2563EB; font-weight:600;">DJAGBA Kuinambe Véronique</span> · 
    Projet 2 - Analyse des Performances RH · Data Analyst · Lomé, Togo
</div>
""", unsafe_allow_html=True)