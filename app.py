from flask import Flask, render_template, request, send_from_directory
from Models.Gif_generator import simulateGif
import random
import string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/simulation.gif', methods=['POST'])
def simulation_gif():
    parameters = request.get_json()
    print(parameters)
    filename = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    print(filename)
    simulateGif(filename, **parameters)
    return send_from_directory('images', filename + '.gif')

