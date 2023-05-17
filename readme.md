# Analyse exploratoire

# Première instance: opérations de merging entre les différents dataframes

Rassemblement des différents dataframes en un seul. 
Opérations diverses de nettoyage du dataframe obtenu.
Imputation via K-Nearest Neighbors des valeurs manquantes
Vérification de la binarité parfaite de la colonne TARGET

# Seconde instance: Opérations de Machine Learning

Mise en lumière des colonnes les plus corrélées à la colonne TARGET.
Exécution d'un Train_test_split du dataframe, X correspondant à toutes les colonnes sauf la TARGET, Y correspondant à la TARET(valeurs binaires 0 et 1)
Entrainements respectifs de différents modèles comme la régression logistique, le DecisionTreeClassifier (Arbre de décision), le RandomForestClassifier (Forêt alétaoire), le XGBoost et enfin le DummyClassifier.
Observation de différentes métriques dont l'AUC
Amélioration de l'efficience des modèles par validation croisée (GridSearch) de manière à optimiser l'AUC par optimisation des hyper-paramètres.
Observation des matrices de confusion de chaque modèle de manière à prendre en compte la représentation des Faux Positifs, Faux Négatifs, Vrais Positifs et Vrais Négatifs.
Création d'une fonction "coût métier" représentant le coût risqué par l'entreprise en fonction de chaque modèle entraîné. 
Mise en lumière via SHAP (SHapley Additive exPlanations) des interprétabilités locale et globale. 

# Troisième et dernière strate: 

Réalisation d'une API Flask aux fins de la prédiction du Score Client
Réalisation d'un Dashboard à usages multiples avec menu contextuel dont l'hébergement et la disposition de l'usager sont permises par le serveur OVH. 