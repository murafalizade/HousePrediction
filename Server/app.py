from flask import Flask,render_template,request,jsonify
import pandas as pd
import csv
import sqlalchemy
from middleware import middleware
import json
from model import predictBina



app = Flask(__name__)
#app.wsgi_app = middleware(app.wsgi_app)

def make_json(csvFilePath):
     
    # create a dictionary
    data = []
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data\
        k = 0 
        for rows in csvReader:
             
            # Assuming a column named 'No' to
            # be the primary key
            if k!=100:
                k+=1
                data.append(rows)
        #return json.dumps(data, indent=4,ensure_ascii=False)
        return data
@app.route("/api/v1/datas")
def calc():
    cdv = r'all_binas.csv'
    #user = request.environ['user']
    engine = sqlalchemy.create_engine("oracle://murad99:asd@localhost:1521")
    res = engine.execute("""select * from estate""")
    sd = json.dumps([dict(r) for r in res])
    df = pd.read_sql("""select * from estate""",con='oracle://murad99:asd@localhost:1521')
    return render_template('calc.html',binas=[dict(r) for r in res],loc = list(df['Locations'].unique()))
@app.route('/api/v1/predict',methods=['POST'])
def predict():
    predict_data = request.get_json()
    rm = predict_data['room']
    all_floor = predict_data['allFloor']
    floor = predict_data['floor']
    area = predict_data['area']
    loc = predict_data['city']
    if loc=='Bakı':
        loc = predict_data['region']
    price = predictBina(int(area),int(rm),int(all_floor),int(floor),loc,predict_data['types'])
    return str(price)
if __name__=='__main__':
    app.run(port=8000,debug=True)