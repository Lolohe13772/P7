import dash
from dash import dcc, html, Input, Output
import requests
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np
app = dash.Dash( external_stylesheets=[dbc.themes.BOOTSTRAP])

# Chargement des identifiants clients depuis le fichier csv
url = f"http://127.0.0.1:8050/get_id_clients"
response = requests.get(url).json()
id_clients = response["id_clients"][:30]
NAME_COLS_TRAIN =['BURO_DAYS_CREDIT_MEAN', 'DAYS_BIRTH', 'PREV_NAME_CONTRACT_STATUS_Refused_MEAN', 'BURO_DAYS_CREDIT_MIN', 'CLOSED_DAYS_CREDIT_MIN', 'CLOSED_DAYS_CREDIT_MEAN', 'BURO_DAYS_CREDIT_UPDATE_MEAN', 'CC_CNT_DRAWINGS_ATM_CURRENT_MEAN', 'REGION_RATING_CLIENT_W_CITY']
# tout le site va fonctionner à travers le layout
app.layout = html.Div([
    html.H1("Prêt à dépenser - Etude de solvabilité", style={'text-align': 'center'}),
    dbc.Row(
    [
        dbc.Col( 
            html.Div([
                html.Div([
                    html.H3('Sélectionnez un identifiant client dans le menu déroulant ci-dessous : '),
                    dcc.Dropdown(
                        id='client-dropdown',
                        options=id_clients,
                        value=id_clients[0]
                    )
                ], className='three columns'),
                html.Div([
                    html.Div(id='solvabilite')
                ], className='nine columns'),
            html.H4("1", style={"color":"orange"}, id="age"),
            html.H4("2", style={"color":"orange"}, id="year_employe"),
            html.H4("3", style={"color":"orange"}, id="gender"),
            ], className='row'), width={"size": 5, "offset": 1},),
        dbc.Col(
            html.Div([
                dcc.Graph(id='gauge'),
                html.H5(id="solva")
            ]), width=6),
        ]),
    dcc.Dropdown(
        id='name_column',
        options=NAME_COLS_TRAIN,
        value=NAME_COLS_TRAIN[0]
    ),
    dcc.Graph(id='histo_colonne'),
])

@app.callback(
    Output('histo_colonne', 'figure'),
    Input('name_column', 'value'), 
    Input('client-dropdown', 'value'), 
    )
def update_graph(name_column,id_client):
    # Récupérer l'âge du client depuis le dataframe
    url = f"http://127.0.0.1:8050/get_column_data/{id_client}/{name_column}"
    print(url)
    response = requests.get(url).json()
    data_colonne = response["data_colonne"]
    info_col_client = response["info_col_client"]
    values_sorted = np.array(data_colonne)
    values_sorted.sort()
    n_quantile = 20
    compteur = 0
    x = []
    y = []
    value_client = -1
    min_value_data = min(values_sorted)
    max_value_data = max(values_sorted)
    jump = (max_value_data - min_value_data) / n_quantile
    for value in values_sorted:
        if value > min_value_data + jump:
            if info_col_client > min_value_data and info_col_client < min_value_data + jump:
                value_client = min_value_data
            y.append(compteur)
            x.append(min_value_data)
            compteur = 0
            min_value_data = min_value_data + jump
        else:
            compteur += 1

    # Créer le graphique
    fig = {
        'data': [{
            'x': x,
            'y': y,
            'type': 'bar',
            'marker': {'color': '#1E90FF'}
        }],
        'layout': {
            'annotations': [
                {'x': value_client, 
                'text': f"Valeur du client : {value_client}",
                'font': {'color': '#FF0000'}, 
                'showarrow': False, 
                'yanchor': 'bottom'}
            ],
            'title': f'Répartition de la variable {name_column}',
            'xaxis': {'title': f'Répartition de la variable {name_column}'},
            'yaxis': {'title': 'Nombre de clients'},
            'barmode': 'stack'
        }
    }
    return fig
# Callback pour mettre à jour la solvabilité affichée lorsque l'utilisateur sélectionne un client dans le menu déroulant
@app.callback(
    Output('gauge', 'figure'),
    Output('solva', 'children'),
    Input('client-dropdown', 'value'))
def get_solvabilite(id_client):
    url = f"http://127.0.0.1:8050/predict_solvabilite/{id_client}"
    response = requests.get(url)
    print (response)
    solvabilite = float(response.text)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = solvabilite,
        domain = {'x': [0, 1]},
        title = {'text': "Solvabilité du client"},
        gauge = {'axis': {"range":[0,1]}}
        ))
    if solvabilite > 0.5:
        message = "Le client est solvable ! Un prêt peut lui être accordé"
    else:
        message = "Le client n'est pas solvable ! Il aura rien ce fdp"
    return fig, message

@app.callback(
    Output('age', 'children'),
    Output('year_employe', 'children'),
    Output('gender', 'children'),
    Input('client-dropdown', 'value'))
def info_client(id_client):
    url = f"http://127.0.0.1:8050/get_useful_infos/{id_client}"
    response = requests.get(url).json()
    print(response)
    age = f'L âge du client est de {response["age"]} ans'
    years_employed = f'Il est employé depuis {response["years_employed"]} ans'
    gender = f'Son genre est : {response["gender"]}'
    return (age, years_employed, gender)

if __name__ == '__main__':
    app.run_server(port=8080)
