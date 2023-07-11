from flask import Flask, request
import os
import pickle
import sqlite3


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

@app.route('/v2/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = float(request.args.get('tv', None))
    radio = float(request.args.get('radio', None))
    newspaper = float(request.args.get('newspaper', None))

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'


@app.route('/v2/ingest_data', methods=['POST'])
def ingest_data():
    tv = request.args('tv', None)
    radio = request.args('radio', None)
    newspaper = request.args('newspaper', None)
    sales = request.args('sales', None)

    connection = sqlite3.connect('data/ingest_data.db')
    cursor = connection.cursor()
    query = f'''
            INSERT INTO advertising (tv, radio, newspaper, sales)
            VALUES ({tv}, {radio}, {newspaper}, {sales})
            '''
    result = cursor.execute(query).fetchall()
    
    connection.commit()
    connection.close()

    return "Data ingested successfully!"

@app.route('/v2/retrain', methods=['PUT'])
def retrian():
    connection = sqlite3.connect('data/ingest_data.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM advertising'
    result = cursor.execute(query).fetchall()

    X = []
    y = []
    for row in result:
        tv, radio, newspaper, sales = row
        X.append([tv, radio, newspaper])
        y.append(sales)

    with open('data/advertising_model', 'rb') as f:
        model = pickle.load(f)

    model.fit(X,y)

    with open('data/advertising_model', 'wb') as f:
        pickle.dump(model, f)


    connection.close()

    return "Retraining completed!"

app.run()

