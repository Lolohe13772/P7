import dash
from dash import dcc
from dash import html, Input, Output
import requests
import pandas as pd

app = dash.Dash(__name__)

# Chargement des identifiants clients depuis le fichier csv
df = pd.read_csv("df_scoring.csv")
clients = [{'label': str(client), 'value': client} for client in df["SK_ID_CURR"]]

app.layout = html.Div([
    html.H1("Prêt à dépenser - Etude de solvabilité"),
    html.Div([
        html.Div([
            html.Label('Sélectionnez un client dans le menu déroulant ci-dessous : '),
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
    ], className='row')
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
        return f"Le client est solvable: un prêt peut lui être accordé(solvabilité:{solvabilite})"
    else:
        return f"Le client n'est pas solvable: il est impossible de lui octroyer un emprunt, risque de perte en capital(solvabilité:{solvabilite})"
    
if __name__ == '__main__':
    app.run_server(port=8080)