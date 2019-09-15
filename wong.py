# import flask dependencies
from flask import Flask, request, make_response, jsonify
import os
import requests

# initialize the flask app
app = Flask(__name__)


# default route
@app.route('/')
def index():
	return 'Hello World!'

#tiendas
def tiendas():
	url = 'https://www.wong.pe/files/PE-districts.json'
	resp = requests.get(url)
	tiendas = resp.json()
	respuesta = ''
	for tienda in tiendas:
		telefono = tienda['phone']
		if telefono != '':
			color = tienda['polygonColor']
			nombre = tienda['name']
			direccion = tienda['address']
			telefono = tienda['phone']
			anexo = tienda['anexo']
			respuesta = respuesta + nombre + ' - ' + direccion + '\n'
			
	respuesta = '"message":{"text":' + respuesta + '}'
	return respuesta


# function for responses
def results():
	# build a request object
	req = request.get_json(force=True)

	# fetch action from json
	intent = req.get('queryResult').get('intent').get('displayName')
	
	if intent == 'wong.tiendas':
		return {'fulfillmentText': {tiendas()}}

	# return a fulfillment response
	return {'fulfillmentText': intent}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
	# return response
	return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print("Starting app on port %d" % port)
	app.run(debug=False, port=port, host='0.0.0.0')
