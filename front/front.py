import dash
from dash import dcc, html, Input, Output
import requests
import pandas as pd

app = dash.Dash(__name__)

# Chargement des identifiants clients depuis le fichier csv
df = pd.read_csv("df_scoring.csv")
clients = [{'label': str(client), 'value': client} for client in df["SK_ID_CURR"]]

app.layout = html.Div([
    html.H1("Prêt à dépenser - Etude de solvabilité", style={'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Label('Sélectionnez un identifiant client dans le menu déroulant ci-dessous : '),
            dcc.Dropdown(
                id='client-dropdown',
                options=clients,
                value=clients[0]['value']
            )
        ], className='three columns'),
        html.Div([
            html.Label('Résultat : '),
            html.Div(id='solvabilite')
        ], className='nine columns')
    ], className='row'),
    html.Div([
        dcc.Graph(id='age-graph')
    ])
])

# Callback pour mettre à jour la solvabilité affichée lorsque l'utilisateur sélectionne un client dans le menu déroulant
@app.callback(
    Output('solvabilite', 'children'),
    Input('client-dropdown', 'value'))
def get_solvabilite(id_client):
    url = f"http://127.0.0.1:8050/predict_solvabilite/{id_client}"
    response = requests.get(url)
    print (response)
    solvabilite = float(response.text)
    if solvabilite >= 0.5:
        return f"Le client est solvable: un prêt peut lui être accordé (solvabilité:{solvabilite})"
    else:
        return f"Le client n'est pas solvable: il est impossible de lui octroyer un emprunt, risque de perte en capital (solvabilité:{solvabilite})"
    
@app.callback(
    Output('age-graph', 'figure'),
    Input('client-dropdown', 'value'))
def update_age_graph(id_client):
    # Récupérer l'âge du client depuis le dataframe
    age = df[df["SK_ID_CURR"] == id_client]["DAYS_BIRTH"].values[0] / -365.25
    
    # Déterminer la colonne de l'âge du client sélectionné
    age_col = int(age // 10)
    
    # Créer les colonnes pour le graphique
    x = [f"{i * 10}-{i * 10 + 9}" for i in range(0, 10)]
    y = [len(df[(df["DAYS_BIRTH"] / -365.25 >= i * 10) & (df["DAYS_BIRTH"] / -365.25 < i * 10 + 10)]) for i in range(0, 10)]
    
    # Modifier la couleur de la colonne de l'âge du client sélectionné
    y[age_col] = {'y': y[age_col], 'fillcolor': '#FFA07A'}
    
    # Créer le graphique
    fig = {
        'data': [{
            'x': x,
            'y': y,
            'type': 'bar',
            'marker': {'color': '#1E90FF'}
        }],
        'layout': {
            'title': 'Répartition des âges des clients',
            'annotations': [
                {'x': age_col, 'y': y[age_col]['y'], 'text': f"Âge du client identifié: {int(age)} ans", 
                 'font': {'color': '#FFA07A'}, 'showarrow': False, 'yanchor': 'bottom'}
            ],
            'xaxis': {'title': 'Tranches d\'âge (années)'},
            'yaxis': {'title': 'Nombre de clients'},
            'barmode': 'stack'
        }
    }
    
    return fig

if __name__ == '__main__':
    app.run_server(port=8080)
