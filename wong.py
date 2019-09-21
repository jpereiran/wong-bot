# import flask dependencies
from flask import Flask, request, make_response, jsonify
import os
import requests
import json

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
			
	return respuesta

#busqueda
def busqueda(text):
	url = 'https://www.wong.pe/api/catalog_system/pub/products/search/?ft='+text+'&_from=0&_to=0'
	resp = requests.get(url)
	resultados = resp.json()
	respuesta = ''
	for res in resultados:
		nombre = res['productName']
		marca = res['brand']
		categorias = res['categoriesIds']
		link = res['link']
		imageId = res['items'][0]['images'][0]['imageId']
		print(nombre)
		print(marca)
		print(categorias)
		print(link)
		print(imageId)
		imageUrl = 'https://wongfood.vteximg.com.br/arquivos/ids/'+imageId+'-120-120/' 
		print(imageUrl)
			
	return respuesta

# function for responses
def results():
	# build a request object
	req = request.get_json(force=True)

	# fetch action from json
	intent = req.get('queryResult').get('intent').get('displayName')
	
	if intent == 'wong.tiendas':
		return {'fulfillmentText': tiendas()}
	elif intent == 'test_scrape':
		j= ''' [
		      {
			"card": {
			  "title": "Coca Cola Regular",
			  "subtitle": "Coca Cola",
			  "imageUri": "https://wongfood.vteximg.com.br/arquivos/ids/308010-250-250/",
			  "buttons": [
			    {
			      "text": "Detalles",
			      "postback": "https://www.wong.pe/coca-cola-regular-pack-6-botellas-de-300-ml-c-u-713716/p"
			    },
			    {
			      "text": "Similares",
			      "postback": "https://www.wong.pe/Comidas%20Preparadas/Comidas/Comidas%20Frescas/"
			    }
			  ]
			},
			"platform": "FACEBOOK"
		      }
		    ]
		'''
		data = json.loads(j)
		return {'fulfillmentMessages': data}
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
