from flask import Flask, render_template, request, send_from_directory
from simulation import simulation

app = Flask(__name__)

@app.route("/")
def index():
        return render_template("index.html")

@app.route('/simulation.gif', methods=['GET'])
def simulation_gif():
    parameters = request.get_json()
    print(parameters)
    file = simulation(parameters)
    return send_from_directory('images', file)

