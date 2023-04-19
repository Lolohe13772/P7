from flask import Flask, jsonify, request
import pandas as pd
from numpy import array
import pickle
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

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050)