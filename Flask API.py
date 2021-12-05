import flask
from flask import Flask, render_template, jsonify, request
import numpy as np
import pandas as pd
import sklearn
import json
import pickle as p
import requests

app = flask.Flask(__name__)

@app.route('/')
def index():
    return render_template("fraudmainpage.html")

@app.route("/fraudprediction",methods=['POST'])
def fraudprediction():
    print(model)
    data = request.get_json()
    prediction = np.array2string(model.predict(data))
    return jsonify(prediction)
@app.route('/frauddetails',methods= ['POST'])
def frauddetails():
    url = "http://192.168.1.5:5000/fraudprediction"
    SUM_INSURED = request.form['SUM_INSURED']
    ESTIMATED_AMOUNT= request.form['ESTIMATED_AMOUNT']
    PREMIUM= request.form['PREMIUM']
    MONTHS_AS_CUSTOMER= request.form['MONTHS_AS_CUSTOMER']
    VEHICLE_CATEGORY= request.form['VEHICLE_CATEGORY']
    STATUS= request.form['STATUS']
    ACCIDENT_TIME= request.form['ACCIDENT_TIME']
    PURPOSE_OF_USE= request.form['PURPOSE_OF_USE']
    MAKE= request.form['MAKE']
    GAP_IN_DAYS= request.form['GAP_IN_DAYS']

    data = [[SUM_INSURED,ESTIMATED_AMOUNT,PREMIUM,MONTHS_AS_CUSTOMER,VEHICLE_CATEGORY,STATUS,ACCIDENT_TIME,PURPOSE_OF_USE,MAKE, GAP_IN_DAYS]]
    j_data = json.dumps(data)
    headers = {'content-type':'application/json','Accept-Charset':'UTF-8'}
    r = requests.post(url,data=j_data,headers=headers)
    r1 = list(r.text)
    stat = ""
    if r1[2] == '0':
        stat = "Claim is not Fraud"
    else:
        stat="Claim is fraud"
    return render_template("result.html",result = stat)

if __name__ == '__main__':
    model_file = 'final_fraud_model.pickle'
    model = p.load(open(model_file,'rb'))
    app.run(debug=True,host='192.168.1.5')

