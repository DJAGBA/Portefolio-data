import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import scipy.stats as stats
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
chemin = os.path.join(BASE_DIR, "Extended_Employee_Performance_and_Productivity_Data.csv")
df = pd.read_csv(chemin)

stats_dept = df.groupby('Department').agg(
    Effectif=('Employee_ID', 'count'),
    Performance_Moy=('Performance_Score', 'mean'),
    Satisfaction_Moy=('Employee_Satisfaction_Score', 'mean'),
    Heures_Hebdo=('Work_Hours_Per_Week', 'mean'),
    Heures_Sup=('Overtime_Hours', 'mean')
).round(2).reset_index()

groupes = [g['Performance_Score'].values for _, g in df.groupby('Department')]
f_stat, p_anova = stats.f_oneway(*groupes)
h_stat, p_kw = stats.kruskal(*groupes)
stat_lev, p_lev = stats.levene(*groupes)

table_croisee = pd.crosstab(df['Department'], df['Education_Level'])
chi2_stat, p_chi2, dof, _ = stats.chi2_contingency(table_croisee)
n_obs = table_croisee.sum().sum()
cramer_v = np.sqrt(chi2_stat / (n_obs * (min(table_croisee.shape) - 1)))

r_pearson, p_pearson = stats.pearsonr(df['Work_Hours_Per_Week'], df['Performance_Score'])
r_spearman, p_spearman = stats.spearmanr(df['Work_Hours_Per_Week'], df['Performance_Score'])
r_sal, p_sal = stats.pearsonr(df['Monthly_Salary'], df['Performance_Score'])

ORANGE = "#CC785C"
ORANGE_LIGHT = "#F5E6DC"
ORANGE_DARK = "#A85A3E"
FOND = "#F8FAFC"
BLANC = "#FFFFFF"
TEXTE = "#000000"
GRIS = "#333333"

fig_box = px.box(df, x='Department', y='Performance_Score',
                 color='Department',
                 title="Distribution de la Performance par Département",
                 color_discrete_sequence=px.colors.sequential.Oranges[2:])
fig_box.update_layout(plot_bgcolor=BLANC, paper_bgcolor=FOND,
                      font_color=TEXTE, showlegend=False,
                      title_font_color=TEXTE, xaxis_tickangle=30,
                      margin=dict(t=50, b=60, l=20, r=20))

fig_bar = px.bar(stats_dept, x='Department', y='Performance_Moy',
                 title="Performance Moyenne par Département",
                 color='Performance_Moy',
                 color_continuous_scale='Oranges', text='Performance_Moy')
fig_bar.update_traces(textposition='outside')
fig_bar.update_layout(plot_bgcolor=BLANC, paper_bgcolor=FOND,
                      font_color=TEXTE, title_font_color=TEXTE,
                      showlegend=False, xaxis_tickangle=30,
                      margin=dict(t=50, b=60, l=20, r=20))

cols = ['Performance_Score', 'Monthly_Salary', 'Work_Hours_Per_Week', 'Overtime_Hours', 'Employee_Satisfaction_Score']
noms = {'Performance_Score': 'Performance', 'Monthly_Salary': 'Salaire',
        'Work_Hours_Per_Week': 'Heures/Sem', 'Overtime_Hours': 'Heures Sup',
        'Employee_Satisfaction_Score': 'Satisfaction'}
corr = df[cols].corr().round(2)
corr.index = [noms[c] for c in cols]
corr.columns = [noms[c] for c in cols]
fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='Oranges',
                     title="Matrice de Corrélation")
fig_corr.update_layout(paper_bgcolor=FOND, font_color=TEXTE,
                       title_font_color=TEXTE, margin=dict(t=50, b=20, l=20, r=20))

sample = df.sample(2000, random_state=42)
fig_scatter = px.scatter(sample, x='Performance_Score', y='Monthly_Salary',
                         color='Department', opacity=0.5,
                         title="Relation Salaire vs Performance",
                         color_discrete_sequence=px.colors.sequential.Oranges[2:],
                         labels={'Performance_Score': 'Score Performance', 'Monthly_Salary': 'Salaire ($)'})
fig_scatter.update_layout(plot_bgcolor=BLANC, paper_bgcolor=FOND,
                          font_color=TEXTE, title_font_color=TEXTE,
                          margin=dict(t=50, b=20, l=20, r=20))

fig_chi = px.imshow(table_croisee, text_auto=True, color_continuous_scale='Oranges',
                    title="Tableau Croisé — Département vs Niveau d'Études")
fig_chi.update_layout(paper_bgcolor=FOND, font_color=TEXTE,
                      title_font_color=TEXTE, margin=dict(t=50, b=20, l=20, r=20))

def kpi_card(valeur, label):
    return html.Div([
        html.Div(valeur, style={'fontSize': '1.5rem', 'fontWeight': '700',
                                'color': ORANGE, 'marginBottom': '4px'}),
        html.Div(label, style={'fontSize': '0.7rem', 'color': GRIS,
                               'textTransform': 'uppercase', 'letterSpacing': '1px'})
    ], style={'background': BLANC, 'borderRadius': '12px', 'padding': '16px',
              'textAlign': 'center',
              'boxShadow': '0 1px 4px rgba(0,0,0,0.08)',
              'border': f'1px solid {ORANGE_LIGHT}',
              'flex': '1'})

def stat_card(titre, lignes, conclusion, positif=True):
    couleur_bg = '#FFF7F0' if positif else '#FFF0F0'
    couleur_txt = '#000000'
    return html.Div([
        html.Div(titre, style={'fontSize': '0.88rem', 'fontWeight': '600',
                               'color': '#000000', 'marginBottom': '10px',
                               'paddingBottom': '8px',
                               'borderBottom': f'2px solid {ORANGE_LIGHT}'}),
        *[html.Div([
            html.Span(k, style={'color': '#000000', 'fontSize': '0.82rem'}),
            html.Span(v, style={'fontWeight': '600', 'color': '#000000', 'fontSize': '0.82rem'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '3px 0'})
          for k, v in lignes],
        html.Div(conclusion, style={'marginTop': '10px', 'padding': '8px 12px',
                                    'borderRadius': '8px', 'fontSize': '0.78rem',
                                    'fontWeight': '500', 'background': couleur_bg,
                                    'color': couleur_txt})
    ], style={'background': BLANC, 'border': f'1px solid {ORANGE_LIGHT}',
              'borderRadius': '12px', 'padding': '20px',
              'boxShadow': '0 1px 4px rgba(0,0,0,0.08)', 'flex': '1'})

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    # HEADER
    html.Div([
        html.H1("Tableau de Bord RH-Écarts de Performance entre Départements",
                style={'color': '#000000', 'fontSize': '1.4rem', 'fontWeight': '700', 'marginBottom': '4px'}),
        html.P("Analyse statistique · Tests ANOVA · Chi-2 · Corrélations · Kruskal-Wallis",
               style={'color': '#333333', 'fontSize': '0.88rem', 'margin': '0'})
    ], style={'background': BLANC,
              'border': f'1px solid {ORANGE_LIGHT}',
              'borderLeft': f'5px solid {ORANGE}',
              'padding': '24px 32px', 'borderRadius': '12px', 'marginBottom': '24px',
              'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),

    # KPIs
    html.Div([
        kpi_card(f"{len(df):,}", "Total Employés"),
        kpi_card(f"{df['Performance_Score'].mean():.2f}", "Performance Moyenne"),
        kpi_card(f"{df['Employee_Satisfaction_Score'].mean():.2f}/5", "Satisfaction"),
        kpi_card(f"{df['Work_Hours_Per_Week'].mean():.1f}h", "Heures/Semaine"),
        kpi_card(f"{df['Department'].nunique()}", "Départements"),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # ROW 1
    html.Div([
        html.Div(dcc.Graph(figure=fig_box), style={'flex': '1', 'background': BLANC,
                                                    'borderRadius': '12px', 'border': f'1px solid {ORANGE_LIGHT}',
                                                    'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
        html.Div(dcc.Graph(figure=fig_bar), style={'flex': '1', 'background': BLANC,
                                                    'borderRadius': '12px', 'border': f'1px solid {ORANGE_LIGHT}',
                                                    'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # ROW 2
    html.Div([
        html.Div(dcc.Graph(figure=fig_corr), style={'flex': '1', 'background': BLANC,
                                                     'borderRadius': '12px', 'border': f'1px solid {ORANGE_LIGHT}',
                                                     'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
        html.Div(dcc.Graph(figure=fig_scatter), style={'flex': '1', 'background': BLANC,
                                                        'borderRadius': '12px', 'border': f'1px solid {ORANGE_LIGHT}',
                                                        'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # ROW 3
    html.Div([
        html.Div(dcc.Graph(figure=fig_chi), style={'flex': '1', 'background': BLANC,
                                                    'borderRadius': '12px', 'border': f'1px solid {ORANGE_LIGHT}',
                                                    'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
        html.Div([
            html.H3(" Statistiques par Département",
                    style={'color': '#000000', 'fontSize': '1rem', 'marginBottom': '12px'}),
            dash_table.DataTable(
                data=stats_dept.to_dict('records'),
                columns=[{"name": c, "id": c} for c in stats_dept.columns],
                style_header={'backgroundColor': ORANGE, 'color': BLANC,
                              'fontWeight': '600', 'fontSize': '0.78rem'},
                style_cell={'textAlign': 'center', 'fontSize': '0.78rem',
                            'padding': '8px', 'color': '#000000'},
                style_data_conditional=[{'if': {'row_index': 'odd'},
                                         'backgroundColor': ORANGE_LIGHT}],
            )
        ], style={'flex': '1', 'background': BLANC, 'borderRadius': '12px',
                  'padding': '20px', 'border': f'1px solid {ORANGE_LIGHT}',
                  'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # TESTS STATISTIQUES
    html.Hr(style={'borderColor': ORANGE_LIGHT}),
    html.H3("Résultats des Tests Statistiques",
            style={'color': '#000000', 'marginBottom': '16px'}),

    html.Div([
        stat_card("ANOVA-Performance par Département",
                  [("Statistique F", f"{f_stat:.4f}"), ("p-value", f"{p_anova:.4e}")],
                  f"{' Différence significative entre départements' if p_anova < 0.05 else ' Pas de différence significative'}",
                  p_anova < 0.05),
        stat_card("Kruskal-Wallis (Non paramétrique)",
                  [("Statistique H", f"{h_stat:.4f}"), ("p-value", f"{p_kw:.4e}")],
                  f"{'Différence confirmée' if p_kw < 0.05 else ' Pas de différence significative'}",
                  p_kw < 0.05),
        stat_card("Levene-Homogénéité des Variances",
                  [("Statistique", f"{stat_lev:.4f}"), ("p-value", f"{p_lev:.4e}")],
                  f"{'Variances homogènes' if p_lev > 0.05 else 'Variances hétérogènes'}",
                  p_lev > 0.05),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '16px'}),

    html.Div([
        stat_card("Chi-2-Département vs Niveau d'Études",
                  [("Chi2", f"{chi2_stat:.4f}"), ("p-value", f"{p_chi2:.4e}"),
                   ("V de Cramer", f"{cramer_v:.4f}")],
                  f"{'Relation significative' if p_chi2 < 0.05 else ' Variables indépendantes'}",
                  p_chi2 < 0.05),
        stat_card("Pearson-Heures vs Performance",
                  [("Coefficient r", f"{r_pearson:.4f}"), ("p-value", f"{p_pearson:.4e}"),
                   ("Spearman ρ", f"{r_spearman:.4f}")],
                  f"{' Corrélation significative' if p_pearson < 0.05 else ' Pas de corrélation'}",
                  p_pearson < 0.05),
        stat_card("Pearson-Salaire vs Performance",
                  [("Coefficient r", f"{r_sal:.4f}"), ("p-value", f"{p_sal:.4e}")],
                  f"{'Salaire lié à la performance' if p_sal < 0.05 else ' Pas de lien significatif'}",
                  p_sal < 0.05),
    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px'}),

    # RECOMMANDATIONS
    html.Hr(style={'borderColor': ORANGE_LIGHT}),
    html.Div([
        html.H3(" Recommandations Stratégiques",
                style={'color': '#000000', 'fontSize': '1rem', 'marginBottom': '12px'}),
        html.Div(" Identifier les départements sous-performants et mettre en place des plans de formation ciblés.",
                 style={'padding': '8px 0', 'borderBottom': f'1px solid {ORANGE_LIGHT}',
                        'fontSize': '0.88rem', 'color': '#000000'}),
        html.Div(" Surveiller les heures supplémentaires - elles peuvent nuire à la performance à long terme.",
                 style={'padding': '8px 0', 'borderBottom': f'1px solid {ORANGE_LIGHT}',
                        'fontSize': '0.88rem', 'color': '#000000'}),
        html.Div(" Revoir la politique salariale pour mieux récompenser les hautes performances.",
                 style={'padding': '8px 0', 'fontSize': '0.88rem', 'color': '#000000'}),
    ], style={'background': BLANC, 'border': f'1px solid {ORANGE_LIGHT}',
              'borderLeft': f'4px solid {ORANGE}', 'borderRadius': '12px',
              'padding': '20px 24px', 'marginBottom': '24px',
              'boxShadow': '0 1px 4px rgba(0,0,0,0.06)'}),

    # FOOTER
    html.Hr(style={'borderColor': ORANGE_LIGHT}),
    html.Div("© 2026 DJAGBA Kuinambe Véronique · Projet 4:Écarts de Performance ·",
             style={'textAlign': 'center', 'color': '#333333',
                    'fontSize': '0.82rem', 'padding': '10px 0'})

], style={'backgroundColor': FOND, 'padding': '24px 32px',
          'fontFamily': 'Inter, sans-serif', 'minHeight': '100vh'})

if __name__ == '__main__':
    app.run(debug=True)