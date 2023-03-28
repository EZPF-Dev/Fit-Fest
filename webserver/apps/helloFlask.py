# import json
# from flask import Flask, render_template, request, jsonify


# app = Flask(__name__)
# app.run(host="0.0.0.0")

# @app.route("/")
# def hello_world():
#     return render_template('prueba.html', user=user)

# @app.route('/', methods=['POST'])
# def update_record():
#     record = json.loads(request.data)
#     print(record)
#     return jsonify(record)

from flask import Flask, render_template, request, jsonify
import json
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
print(open("prueba.css"))
ingredients = ['']
@app.route('/')
def hello_world():
    print("Refresh")
    print(ingredients)
    return render_template('prueba.html', ingredients=ingredients)
    
@app.route('/ingredients', methods=['POST'])
def new_ingredients():
    #global ingredients
    print(request.data)
    ingredientsx = json.loads(request.data)
    ingred2 = json.loads(ingredientsx)
    ingred3 = ingred2["ingredients"]
    global ingredients
    for ing in ingred3:
        if ing not in ingredients:
            ingredients.append(ing)
    return "true"

app.run(host="0.0.0.0")