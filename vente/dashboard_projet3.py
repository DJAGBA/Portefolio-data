import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.stats as stats
import os

st.set_page_config(
    page_title="Projet 3 — Performances Commerciales",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.dash-header {
    background: linear-gradient(135deg, #14532D 0%, #16A34A 100%);
    padding: 28px 36px;
    border-radius: 16px;
    margin-bottom: 24px;
}
.dash-title { font-size: 1.5rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px; }
.dash-subtitle { font-size: 0.88rem; color: #BBF7D0; }

.kpi-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 16px 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(22,163,74,0.1);
    border-top: 3px solid #16A34A;
    height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-number {
    font-size: 1.4rem;
    font-weight: 700;
    color: #15803D;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.kpi-label {
    font-size: 0.7rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 500;
}

.stat-card {
    background: #FFFFFF;
    border: 1px solid #BBF7D0;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(22,163,74,0.08);
}
.stat-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #14532D;
    margin-bottom: 12px;
    border-bottom: 2px solid #BBF7D0;
    padding-bottom: 8px;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: #374151;
    padding: 4px 0;
}
.stat-value { font-weight: 600; color: #14532D; }
.stat-conclusion {
    margin-top: 10px;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 500;
}
.stat-oui { background: #DCFCE7; color: #14532D; }
.stat-non { background: #FEE2E2; color: #991B1B; }

.insight-box {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-left: 4px solid #16A34A;
    border-radius: 12px;
    padding: 20px 24px;
}
.insight-title { font-size: 1rem; font-weight: 600; color: #14532D; margin-bottom: 12px; }
.insight-item {
    font-size: 0.88rem;
    color: #374151;
    line-height: 1.8;
    padding: 6px 0;
    border-bottom: 1px solid #DCFCE7;
}
</style>
""", unsafe_allow_html=True)

# ===================== CHARGEMENT =====================
@st.cache_data
def charger_donnees():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    chemin = os.path.join(BASE_DIR, "Sample - Superstore.csv")
    df = pd.read_csv(chemin, encoding="latin-1")
    df = df.drop_duplicates()
    df = df.dropna()
    if 'Order Date' in df.columns:
        df['Year'] = pd.to_datetime(df['Order Date']).dt.year
    return df

df = charger_donnees()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("## Filtres")
    st.divider()

    regions = ["Toutes"] + sorted(df['Region'].dropna().unique().tolist())
    region_select = st.selectbox("Région", regions)

    categories = ["Toutes"] + sorted(df['Category'].dropna().unique().tolist())
    cat_select = st.selectbox("Catégorie", categories)

    if 'Year' in df.columns:
        annees = ["Toutes"] + sorted(df['Year'].unique().tolist())
        annee_select = st.selectbox("Année", annees)
    else:
        annee_select = "Toutes"

    st.divider()
    st.caption(" © 2023 - Projet 3")

# Filtrage
df_f = df.copy()
if region_select != "Toutes":
    df_f = df_f[df_f['Region'] == region_select]
if cat_select != "Toutes":
    df_f = df_f[df_f['Category'] == cat_select]
if annee_select != "Toutes" and 'Year' in df_f.columns:
    df_f = df_f[df_f['Year'] == annee_select]

# ===================== HEADER =====================
st.markdown("""
<div class="dash-header">
    <div class="dash-title"> Tableau de Bord — Performances Commerciales</div>
    <div class="dash-subtitle">Analyse des facteurs influençant les ventes · Marges · Remises · Stratégie régionale</div>
</div>
""", unsafe_allow_html=True)

# ===================== KPIs =====================
k1, k2, k3, k4, k5 = st.columns(5)

ventes = df_f['Sales'].sum()
profit = df_f['Profit'].sum()
taux = (profit / ventes * 100) if ventes != 0 else 0
remise = df_f['Discount'].mean() * 100

kpis = [
    (f"{len(df_f):,}", "Commandes"),
    (f"${ventes/1000:.1f}K", "Ventes Totales"),
    (f"${profit/1000:.1f}K", "Profit Total"),
    (f"{taux:.1f}%", "Taux de Marge"),
    (f"{remise:.1f}%", "Remise Moyenne"),
]
for col, (val, label) in zip([k1, k2, k3, k4, k5], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{val}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Paramètres graphiques
LP = dict(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#F8FAFC',
    font_color='#1E293B',
    font_family='Inter',
    title_font_size=13,
    title_font_color='#14532D',
    margin=dict(t=50, b=20, l=20, r=20)
)
VERTS = ['#14532D', '#16A34A', '#4ADE80', '#BBF7D0']

# ===================== ROW 1 =====================
c1, c2 = st.columns(2)

with c1:
    pr = df_f.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
    fig1 = px.bar(pr, x='Region', y=['Sales', 'Profit'],
                  title="Ventes et Profit par Région",
                  barmode='group',
                  color_discrete_sequence=['#16A34A', '#4ADE80'])
    fig1.update_layout(**LP)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.box(df_f, x='Region', y='Profit',
                  title="Distribution du Profit par Région",
                  color='Region',
                  color_discrete_sequence=VERTS)
    fig2.update_layout(**LP, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ===================== ROW 2 =====================
c3, c4 = st.columns(2)

with c3:
    ps = df_f.groupby('Sub-Category')['Profit'].mean().reset_index()
    ps.columns = ['Sous-Catégorie', 'Profit Moyen']
    ps = ps.sort_values('Profit Moyen', ascending=True)
    ps['Type'] = ps['Profit Moyen'].apply(lambda x: 'Déficitaire' if x < 0 else 'Rentable')
    fig3 = px.bar(ps, x='Profit Moyen', y='Sous-Catégorie',
                  orientation='h',
                  title="Profit Moyen par Sous-Catégorie",
                  color='Type',
                  color_discrete_map={'Déficitaire': '#EF4444', 'Rentable': '#16A34A'})
    fig3.update_layout(**LP)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = px.scatter(df_f, x='Discount', y='Profit',
                      color='Category',
                      title="Impact des Remises sur le Profit",
                      color_discrete_sequence=VERTS,
                      opacity=0.6,
                      labels={'Discount': 'Remise', 'Profit': 'Profit ($)'})
    fig4.add_hline(y=0, line_dash="dash", line_color="red",
                   annotation_text="Seuil de rentabilité")
    fig4.update_layout(**LP)
    st.plotly_chart(fig4, use_container_width=True)

# ===================== ROW 3 =====================
c5, c6 = st.columns(2)

with c5:
    cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    noms = {'Sales': 'Ventes', 'Quantity': 'Quantité', 'Discount': 'Remise', 'Profit': 'Profit'}
    corr = df_f[cols].corr().round(2)
    corr.index = [noms[c] for c in cols]
    corr.columns = [noms[c] for c in cols]
    fig5 = px.imshow(corr, text_auto=True,
                     color_continuous_scale='Greens',
                     title="Matrice de Corrélation")
    fig5.update_layout(**LP)
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    tc = pd.crosstab(df_f['Region'], df_f['Category'])
    fig6 = px.imshow(tc, text_auto=True,
                     color_continuous_scale='Greens',
                     title="Tableau Croisé — Région vs Catégorie")
    fig6.update_layout(**LP)
    st.plotly_chart(fig6, use_container_width=True)

# ===================== TESTS STATISTIQUES =====================
st.divider()
st.markdown("### Validation Statistique")
st.caption("Ces tests vérifient si les différences observées sont réelles ou dues au hasard")

s1, s2, s3 = st.columns(3)

# Test ANOVA
with s1:
    grps = [g['Profit'].values for _, g in df_f.groupby('Region')]
    if len(grps) >= 2:
        f_stat, p_val = stats.f_oneway(*grps)
        sig = p_val < 0.05
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">ANOVA — Profit par Région</div>
            <div class="stat-row"><span>Objectif</span><span class="stat-value">Comparer les régions</span></div>
            <div class="stat-row"><span>Statistique F</span><span class="stat-value">{f_stat:.2f}</span></div>
            <div class="stat-row"><span>p-value</span><span class="stat-value">{p_val:.4f}</span></div>
            <div class="stat-conclusion {'stat-oui' if sig else 'stat-non'}">
                {" Les régions ont des profits significativement différents" if sig else " Pas de différence significative entre les régions"}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Test Chi-2
with s2:
    ct = pd.crosstab(df_f['Region'], df_f['Category'])
    if ct.shape[0] >= 2 and ct.shape[1] >= 2:
        chi2, p_val2, dof, _ = stats.chi2_contingency(ct)
        sig2 = p_val2 < 0.05
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title"> Chi-2 — Région vs Catégorie</div>
            <div class="stat-row"><span>Objectif</span><span class="stat-value">Tester la dépendance</span></div>
            <div class="stat-row"><span>Statistique χ²</span><span class="stat-value">{chi2:.2f}</span></div>
            <div class="stat-row"><span>p-value</span><span class="stat-value">{p_val2:.4f}</span></div>
            <div class="stat-conclusion {'stat-oui' if sig2 else 'stat-non'}">
                {"Région et Catégorie sont liées statistiquement" if sig2 else " Région et Catégorie sont indépendantes"}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Test Pearson
with s3:
    r, p_val3 = stats.pearsonr(df_f['Discount'], df_f['Profit'])
    sig3 = p_val3 < 0.05
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-title">Pearson — Remise vs Profit</div>
        <div class="stat-row"><span>Objectif</span><span class="stat-value">Mesurer la corrélation</span></div>
        <div class="stat-row"><span>Coefficient r</span><span class="stat-value">{r:.4f}</span></div>
        <div class="stat-row"><span>p-value</span><span class="stat-value">{p_val3:.4f}</span></div>
        <div class="stat-conclusion {'stat-oui' if sig3 else 'stat-non'}">
            {" La remise a un impact négatif significatif sur le profit" if sig3 else " Pas d'impact significatif"}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== RECOMMANDATIONS =====================
st.divider()
st.markdown("""
<div class="insight-box">
    <div class="insight-title"> Recommandations Stratégiques</div>
    <div class="insight-item"> <strong>Politique de Remises</strong> — Plafonner les remises à 20% car au-delà, la majorité des ventes génèrent un profit négatif.</div>
    <div class="insight-item"> <strong>Rationalisation du Catalogue</strong> — Réévaluer les sous-catégories déficitaires (Tables, Bookcases) et revoir leur stratégie de prix.</div>
    <div class="insight-item"><strong>Stratégie Régionale</strong> — Concentrer les efforts d'optimisation dans les régions avec de faibles marges malgré un volume de vente élevé.</div>
</div>
""", unsafe_allow_html=True)

# ===================== FOOTER =====================
st.divider()
st.markdown("""
<div style="text-align:center; color:#94A3B8; font-size:0.82rem; padding:10px 0;">
    © 2026 <span style="color:#16A34A; font-weight:600;">DJAGBA Kuinambe Véronique</span> · 
    Projet 3-Performances Commerciales
</div>
""", unsafe_allow_html=True)