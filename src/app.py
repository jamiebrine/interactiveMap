from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
from datetime import date
import os

app = Flask(__name__)

areaDict = {
    "NP7": "Abergavenny",
    "NP16": "Chepstow",
    "NP26": "Caldicot",
    "NP25": "Monmouth",
    "NP15": "Usk",
}

designationDict = {
    "gen": "under 60s accomodation",
    "oap": "over 60s accomodation",
    "soap": "sheltered over 60s accomodation",
}

# [x,y] = [band,bedrooms]
bandSizes = [[230,130,30,26],[170,260,140,50],[480,190,80,20],[600,420,220,50]]
bandSizesOAP = [[40,50],[40,20],[120,60],[340,120]]

@app.route("/")
def index():
    try:
        return render_template('index.html')
    except:
        return render_template('error.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return redirect(url_for('index'))
    band = request.form.get('band')
    designation = request.form.get('designation')
    postcode = request.form.get('postcode')
    bedrooms = request.form.get('bedrooms')

    if band == None or designation == None or postcode == None or bedrooms == None:
        return jsonify(result="Please fill out all fields", numLets="", parameters="")
    
    averageWait = calculateAverageWait(band,designation,postcode,bedrooms)
    parametersOut = f'(Band {band}, {designationDict[designation]}, {bedrooms} bedroom properties in {areaDict[postcode]})'

    if averageWait == -1:
        resultOut = "No recent lets"
        numLetsOut = ""
    else:
        resultOut = f'{averageWait[0]} months'
        numLetsOut = f'Based on {averageWait[1]} previous lets. There are around {averageWait[2]} people in this band waiting for a property of this size'

    return jsonify(result=resultOut, numLets=numLetsOut, parameters=parametersOut)

def calculateAverageWait(band, designation, postcode, bedrooms):

    file_path = os.path.join(os.path.dirname(__file__), 'data.json')

    try:
        with open(file_path) as file:
            data = json.load(file)

        filteredData = [(item['priorityDate'], item['letDate']) for item in data if item['band'] == band and item['designation'] == designation and item['postcode'] == postcode and item['bedrooms'] == bedrooms]

        sumDays = 0

        for item in filteredData:
            initDate = parseDate(item[0])
            endDate = parseDate(item[1])
            sumDays += (endDate - initDate).days

        if len(filteredData) == 0:
            return -1
        
        avgWait = (sumDays // (30 * len(filteredData))) + 1

        if designation == "gen":
            numInBand = bandSizes[int(band)-1][int(bedrooms)-1]
        else:  
            numInBand = bandSizesOAP[int(band)-1][int(bedrooms)-1]
        
        return (avgWait, len(filteredData), numInBand)

    except FileNotFoundError:
        return "Data file not found"

def parseDate(dateString):
    y = int(dateString[0:4])
    m = int(dateString[5:7])
    d = int(dateString[8:10])

    return date(y,m,d)          

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)