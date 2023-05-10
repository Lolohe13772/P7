import pickle
import numpy
def test_model():
    with open('../Data/model.pickle', 'rb') as f:
        model = pickle.load(f)

    with open('../Data/cols.pkl', 'rb') as f:
        columns = pickle.load(f)   
    fake_data= [0 for i in range (9)]
    datatest=numpy.array([fake_data, fake_data])
    prediction=model.predict_proba(datatest)

    assert prediction[0][0]>=0 and prediction[0][0]<=1