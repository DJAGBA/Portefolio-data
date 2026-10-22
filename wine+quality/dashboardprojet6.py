import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

# ===================== CHARGEMENT =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df_red = pd.read_csv(os.path.join(BASE_DIR, "winequality-red.csv"), sep=';')
df_white = pd.read_csv(os.path.join(BASE_DIR, "winequality-white.csv"), sep=';')

df_red['type'] = 'Rouge'
df_white['type'] = 'Blanc'
df = pd.concat([df_red, df_white], ignore_index=True)
df = df.drop_duplicates().reset_index(drop=True)

# ===================== ACP =====================
X_full = df.drop(columns=['quality', 'type'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_full)

pca = PCA()
X_pca = pca.fit_transform(X_scaled)
var_exp = pca.explained_variance_ratio_ * 100

df_pca = pd.DataFrame(X_pca[:, :2], columns=['CP1', 'CP2'])
df_pca['type'] = df['type'].values
df_pca['qualite'] = df['quality'].values

# ===================== COULEURS =====================
BORDEAUX = "#722F37"
BORDEAUX_LIGHT = "#F5E8EA"
BORDEAUX_DARK = "#4A1A20"
FOND = "#FAFAFA"
BLANC = "#FFFFFF"
TEXTE = "#000000"
GRIS = "#333333"

# ===================== GRAPHIQUES =====================
LP = dict(
    plot_bgcolor=BLANC,
    paper_bgcolor=FOND,
    font_color=TEXTE,
    title_font_color=TEXTE,
    margin=dict(t=50, b=40, l=20, r=20)
)

# Heatmap corrélation
X_chem = df.drop(columns=['quality', 'type'])
corr = X_chem.corr().round(2)
fig_corr = px.imshow(corr, text_auto=True,
                     color_continuous_scale='RdBu_r',
                     title="Matrice de Corrélation des Propriétés Chimiques")
fig_corr.update_layout(**LP)

# Nuage de points ACP
fig_pca = px.scatter(df_pca, x='CP1', y='CP2',
                     color='type',
                     color_discrete_map={'Rouge': BORDEAUX, 'Blanc': '#C4A35A'},
                     opacity=0.5,
                     title=f"Nuage de Points ACP (CP1 vs CP2) — Variance expliquée : {var_exp[0]+var_exp[1]:.2f}%",
                     labels={'CP1': f'CP1 ({var_exp[0]:.2f}%)', 'CP2': f'CP2 ({var_exp[1]:.2f}%)'})
fig_pca.add_hline(y=0, line_dash="dash", line_color="grey", line_width=0.8)
fig_pca.add_vline(x=0, line_dash="dash", line_color="grey", line_width=0.8)
fig_pca.update_layout(**LP)

# Variance expliquée cumulée
fig_var = go.Figure()
fig_var.add_trace(go.Bar(
    x=[f'CP{i+1}' for i in range(len(var_exp))],
    y=var_exp,
    name='Variance par composante',
    marker_color=BORDEAUX,
    opacity=0.8
))
fig_var.add_trace(go.Scatter(
    x=[f'CP{i+1}' for i in range(len(var_exp))],
    y=np.cumsum(var_exp),
    name='Variance cumulée',
    mode='lines+markers',
    line=dict(color='#C4A35A', width=2),
    marker=dict(size=6)
))
fig_var.update_layout(
    title="Variance Expliquée par Composante Principale",
    xaxis_title="Composantes Principales",
    yaxis_title="Variance Expliquée (%)",
    **LP
)

# Cercle des corrélations
loadings = pca.components_[:2, :].T * np.sqrt(pca.explained_variance_[:2])
features = X_full.columns.tolist()

fig_cercle = go.Figure()
theta = np.linspace(0, 2 * np.pi, 100)
fig_cercle.add_trace(go.Scatter(
    x=np.cos(theta), y=np.sin(theta),
    mode='lines',
    line=dict(color='grey', dash='dash', width=1),
    showlegend=False
))
for i, feat in enumerate(features):
    fig_cercle.add_annotation(
        x=loadings[i, 0] * 1.15, y=loadings[i, 1] * 1.15,
        text=feat, showarrow=False,
        font=dict(size=9, color=BORDEAUX_DARK)
    )
    fig_cercle.add_shape(
        type='line', x0=0, y0=0,
        x1=loadings[i, 0], y1=loadings[i, 1],
        line=dict(color=BORDEAUX, width=1.5),
    )
fig_cercle.update_layout(
    title="Cercle des Corrélations",
    xaxis=dict(range=[-1.3, 1.3], zeroline=True, zerolinecolor='grey', zerolinewidth=0.8),
    yaxis=dict(range=[-1.3, 1.3], zeroline=True, zerolinecolor='grey', zerolinewidth=0.8),
    xaxis_title=f'CP1 ({var_exp[0]:.2f}%)',
    yaxis_title=f'CP2 ({var_exp[1]:.2f}%)',
    **LP
)

# Distribution qualité
fig_qual = px.histogram(df, x='quality', color='type',
                        color_discrete_map={'Rouge': BORDEAUX, 'Blanc': '#C4A35A'},
                        barmode='group',
                        title="Distribution de la Qualité par Type de Vin",
                        labels={'quality': 'Score de Qualité', 'count': 'Nombre de Bouteilles'})
fig_qual.update_layout(**LP)

# Boxplot propriétés chimiques
fig_box = px.box(df, x='type', y='alcohol',
                 color='type',
                 color_discrete_map={'Rouge': BORDEAUX, 'Blanc': '#C4A35A'},
                 title="Distribution du Taux d'Alcool par Type de Vin",
                 labels={'alcohol': "Taux d'Alcool (%)", 'type': 'Type de Vin'})
fig_box.update_layout(**LP, showlegend=False)

# ===================== COMPOSANTS =====================
def kpi_card(valeur, label):
    return html.Div([
        html.Div(valeur, style={'fontSize': '1.5rem', 'fontWeight': '700',
                                'color': BORDEAUX, 'marginBottom': '4px'}),
        html.Div(label, style={'fontSize': '0.7rem', 'color': GRIS,
                               'textTransform': 'uppercase', 'letterSpacing': '1px'})
    ], style={'background': BLANC, 'borderRadius': '12px', 'padding': '16px',
              'textAlign': 'center', 'boxShadow': '0 1px 4px rgba(0,0,0,0.08)',
              'border': f'1px solid {BORDEAUX_LIGHT}', 'flex': '1'})

def info_card(titre, contenu):
    return html.Div([
        html.Div(titre, style={'fontSize': '0.88rem', 'fontWeight': '600',
                               'color': '#000000', 'marginBottom': '10px',
                               'paddingBottom': '8px',
                               'borderBottom': f'2px solid {BORDEAUX_LIGHT}'}),
        html.Div(contenu, style={'fontSize': '0.82rem', 'color': '#000000', 'lineHeight': '1.7'})
    ], style={'background': BLANC, 'border': f'1px solid {BORDEAUX_LIGHT}',
              'borderRadius': '12px', 'padding': '20px',
              'boxShadow': '0 1px 4px rgba(0,0,0,0.08)', 'flex': '1'})

# ===================== APP =====================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    # HEADER
    html.Div([
        html.H1("🍷 Tableau de Bord - Analyse & ACP des Vins",
                style={'color': '#000000', 'fontSize': '1.4rem', 'fontWeight': '700', 'marginBottom': '4px'}),
        html.P("Analyse exploratoire · Propriétés chimiques · Réduction de dimensionnalité (ACP) · Wine Quality Dataset",
               style={'color': '#333333', 'fontSize': '0.88rem', 'margin': '0'})
    ], style={'background': BLANC, 'border': f'1px solid {BORDEAUX_LIGHT}',
              'borderLeft': f'5px solid {BORDEAUX}', 'padding': '24px 32px',
              'borderRadius': '12px', 'marginBottom': '24px',
              'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),

    # KPIs
    html.Div([
        kpi_card(f"{len(df):,}", "Total Bouteilles"),
        kpi_card(f"{len(df[df['type']=='Rouge']):,}", "Vins Rouges"),
        kpi_card(f"{len(df[df['type']=='Blanc']):,}", "Vins Blancs"),
        kpi_card(f"{df['quality'].mean():.2f}/10", "Qualité Moyenne"),
        kpi_card(f"{var_exp[0]+var_exp[1]:.1f}%", "Variance CP1+CP2"),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # ROW 1 : Corrélation + Distribution qualité
    html.Div([
        html.Div(dcc.Graph(figure=fig_corr),
                 style={'flex': '1', 'background': BLANC, 'borderRadius': '12px',
                        'border': f'1px solid {BORDEAUX_LIGHT}', 'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
        html.Div(dcc.Graph(figure=fig_qual),
                 style={'flex': '1', 'background': BLANC, 'borderRadius': '12px',
                        'border': f'1px solid {BORDEAUX_LIGHT}', 'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # ROW 2 : Boxplot + Variance ACP
    html.Div([
        html.Div(dcc.Graph(figure=fig_box),
                 style={'flex': '1', 'background': BLANC, 'borderRadius': '12px',
                        'border': f'1px solid {BORDEAUX_LIGHT}', 'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
        html.Div(dcc.Graph(figure=fig_var),
                 style={'flex': '1', 'background': BLANC, 'borderRadius': '12px',
                        'border': f'1px solid {BORDEAUX_LIGHT}', 'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # ROW 3 : Nuage ACP + Cercle corrélations
    html.Div([
        html.Div(dcc.Graph(figure=fig_pca),
                 style={'flex': '1', 'background': BLANC, 'borderRadius': '12px',
                        'border': f'1px solid {BORDEAUX_LIGHT}', 'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
        html.Div(dcc.Graph(figure=fig_cercle),
                 style={'flex': '1', 'background': BLANC, 'borderRadius': '12px',
                        'border': f'1px solid {BORDEAUX_LIGHT}', 'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # INTERPRÉTATION ACP
    html.Hr(style={'borderColor': BORDEAUX_LIGHT}),
    html.H3(" Interprétation de l'ACP",
            style={'color': '#000000', 'marginBottom': '16px'}),

    html.Div([
        info_card("CP1 — Axe de la Qualité Chimique",
                  "La première composante principale oppose les vins riches en acidité fixe, sulfates et alcool aux vins avec une forte acidité volatile et un pH élevé. Elle capture la structure chimique globale du vin."),
        info_card("CP2 — Axe de la Douceur vs Acidité",
                  "La deuxième composante distingue les vins avec un taux de sucre résiduel élevé (vins blancs) de ceux avec plus de dioxyde de soufre. Elle sépare clairement les vins rouges des vins blancs."),
        info_card("Séparation Rouge vs Blanc",
                  "Le nuage de points ACP montre une séparation nette entre les vins rouges et blancs sur CP2, confirmant que leurs propriétés chimiques sont fondamentalement différentes malgré des notes de qualité similaires."),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # RECOMMANDATIONS
    html.Hr(style={'borderColor': BORDEAUX_LIGHT}),
    html.Div([
        html.H3(" Conclusions et Recommandations",
                style={'color': '#000000', 'fontSize': '1rem', 'marginBottom': '12px'}),
        html.Div(" Les vins rouges et blancs ont des profils chimiques distincts - l'ACP les sépare clairement sur le deuxième axe.",
                 style={'padding': '8px 0', 'borderBottom': f'1px solid {BORDEAUX_LIGHT}',
                        'fontSize': '0.88rem', 'color': '#000000'}),
        html.Div("L'alcool et les sulfates sont les variables les plus corrélées avec la qualité du vin.",
                 style={'padding': '8px 0', 'borderBottom': f'1px solid {BORDEAUX_LIGHT}',
                        'fontSize': '0.88rem', 'color': '#000000'}),
        html.Div("Les deux premières composantes expliquent une part significative de la variance - suffisant pour visualiser la structure des données.",
                 style={'padding': '8px 0', 'fontSize': '0.88rem', 'color': '#000000'}),
    ], style={'background': BLANC, 'border': f'1px solid {BORDEAUX_LIGHT}',
              'borderLeft': f'4px solid {BORDEAUX}', 'borderRadius': '12px',
              'padding': '20px 24px', 'marginBottom': '24px',
              'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),

    # FOOTER
    html.Hr(style={'borderColor': BORDEAUX_LIGHT}),
    html.Div("© 2026 DJAGBA Kuinambe Véronique · Projet 6 ",
             style={'textAlign': 'center', 'color': '#333333',
                    'fontSize': '0.82rem', 'padding': '10px 0'})

], style={'backgroundColor': FOND, 'padding': '24px 32px',
          'fontFamily': 'Inter, sans-serif', 'minHeight': '100vh'})

if __name__ == '__main__':
    app.run(debug=False)