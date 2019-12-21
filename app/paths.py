from app import app
from flask import render_template, request, json, jsonify
import subprocess

status = {"radio" : False, 
		"lantern" : False}

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/radio', methods=['POST'])
def radio():
	content = json.loads(request.data)

	if content["status"] == "on" and not status["radio"]:
		subprocess.call(["python3", "commands/radio.py", "on"])
		subprocess.call(["at", "now", "+", "2", "hours", "-f", "commands/radio_off.txt"])
		print("radio on")
		status["radio"] = True

		return jsonify({"radio" : "on"})

	elif content["status"] == "off" and status["radio"]:
		print("radio off")
		subprocess.call(["python3", "commands/radio.py", "off"])
		status["radio"] = False

		return jsonify({"radio" : "off"})

@app.route('/lantern', methods=['POST'])
def lantern():
	content = json.loads(request.data)

	if content["status"] == "on" and not status["lantern"]:
		print("lantern on")
		subprocess.call(["rpi-rf_send", "-r", "12", "28527"])
		status["lantern"] = True

		return jsonify({"lantern" : "on"})

	elif content["status"] == "off" and status["lantern"]:
		print("lantern off")
		subprocess.call(["rpi-rf_send", "-r", "12", "20294"])
		status["lantern"] = False

		return jsonify({"lantern" : "off"})



	
