from flask import Flask, request, render_template
import socket
import json
from datetime import date

app = Flask(__name__)

@app.route("/")
def index():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return render_template('index.html', hostname=host_name, ip=host_ip)
    except:
        return render_template('error.html')

@app.route('/submit', methods=['POST'])
def submit():
    band = request.form.get('band')
    designation = request.form.get('designation')
    postcode = request.form.get('postcode')

    averageWait = calculateAverageWait(band,designation,postcode)
    
    if averageWait == -1:
        return "No previous lets found"
    return str(averageWait)


def calculateAverageWait(band, designation, postcode):

    # Load data from data.json
    with open('src/data.json') as file:
        data = json.load(file)

    # Filter data based on band, designation, and area
    filteredData = [(item['priorityDate'], item['letDate']) for item in data if item['band'] == band and item['designation'] == designation and item['postcode'] == postcode]

    count = 0
    sumDays = 0

    for item in filteredData:
        count += 1
        initDate = parseDate(item[0])
        endDate = parseDate(item[1])
        sumDays += (endDate - initDate).days

    if count == 0:
        return -1
    
    return int(float(sumDays) / len(filteredData))

def parseDate(dateString):
    y = int("20" + dateString[6:8])
    m = int(dateString[3:5])
    d = int(dateString[0:2])

    return date(y,m,d)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)