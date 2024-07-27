from flask import Flask, request, render_template
import socket
import json

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
    matches = calculateAverageWait(band,designation,postcode)

    #return str(len(matches))

    output = ""
    for item in matches:
        output += f"{item[0]}, {item[1]}\n"
    return output

def calculateAverageWait(band, designation, postcode):

    # Load data from data.json
    with open('src/data.json') as file:
        data = json.load(file)

    # Filter data based on band, designation, and area
    filteredData = [(item['letDate'], item['priorityDate']) for item in data if item['band'] == band and item['designation'] == designation and item['postcode'] == postcode]

    return filteredData

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)