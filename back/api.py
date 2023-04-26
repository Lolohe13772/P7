from flask import Flask, jsonify, request
import pandas as pd
from numpy import array
import pickle
import io
from flask import send_file
NAME_COLS_TRAIN =['BURO_DAYS_CREDIT_MEAN', 'DAYS_BIRTH', 'PREV_NAME_CONTRACT_STATUS_Refused_MEAN', 'BURO_DAYS_CREDIT_MIN', 'CLOSED_DAYS_CREDIT_MIN', 'CLOSED_DAYS_CREDIT_MEAN', 'BURO_DAYS_CREDIT_UPDATE_MEAN', 'CC_CNT_DRAWINGS_ATM_CURRENT_MEAN', 'REGION_RATING_CLIENT_W_CITY']
app = Flask(__name__)

# Charger le modèle entraîné
with open('../Data/model.pickle', 'rb') as f:
    model = pickle.load(f)

# Charger le dataframe df_scoring.csv
df = pd.read_csv('../Data/df_scoring.csv')
df = df.set_index('SK_ID_CURR')

# Définition de la route pour prédire la solvabilité d'un client
@app.route('/predict_solvabilite/<int:id_client>')
def predict_solvabilite(id_client):
    print(id_client)
    info_client=df.loc[id_client]
    useful_data=array(info_client[NAME_COLS_TRAIN])
    useful_data= useful_data.reshape(1, -1)
    target=model.predict_proba(useful_data)[0][0]
    return str(target)

# Définition de la route pour récupérer les données d'âge du client
@app.route('/age_client/<int:id_client>')
def age_client(id_client):
    info_client = df.loc[id_client]
    age = info_client['DAYS_BIRTH'] / -365 # Convertir les jours en années
    return jsonify({'age': age})

# Définition de la route pour récupérer le statut salarié du client
@app.route('/statut_salarie/<int:id_client>')
def statut_salarie(id_client):
    info_client = df.loc[id_client]
    statut = "salarié" if info_client['NAME_INCOME_TYPE_Working'] == 1 else "non salarié"
    return jsonify({'statut': statut})

# Définition de la route pour afficher les données d'un client
@app.route('/client/<int:id_client>')
def afficher_client(id_client):
    info_client = df.loc[id_client] # Récupérer les informations sur le client
    age = info_client['DAYS_BIRTH'] / -365 # Calculer l'âge du client
    statut_salarie = "salarié" if info_client['NAME_INCOME_TYPE_Working'] == 1 else "non salarié" # Déterminer le statut salarié du client

    # Créer un dictionnaire contenant les données du client à afficher
    data = {
        'age': age,
        'statut_salarie': statut_salarie,
        'BURO_DAYS_CREDIT_MEAN': info_client['BURO_DAYS_CREDIT_MEAN'],
        'PREV_NAME_CONTRACT_STATUS_Refused_MEAN': info_client['PREV_NAME_CONTRACT_STATUS_Refused_MEAN'],
        'BURO_DAYS_CREDIT_MIN': info_client['BURO_DAYS_CREDIT_MIN'],
        'CLOSED_DAYS_CREDIT_MIN': info_client['CLOSED_DAYS_CREDIT_MIN'],
        'CLOSED_DAYS_CREDIT_MEAN': info_client['CLOSED_DAYS_CREDIT_MEAN'],
        'BURO_DAYS_CREDIT_UPDATE_MEAN': info_client['BURO_DAYS_CREDIT_UPDATE_MEAN'],
        'CC_CNT_DRAWINGS_ATM_CURRENT_MEAN': info_client['CC_CNT_DRAWINGS_ATM_CURRENT_MEAN'],
        'REGION_RATING_CLIENT_W_CITY': info_client['REGION_RATING_CLIENT_W_CITY']
    }

    return jsonify(data) # Renvoyer les données au format JSON

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050)
