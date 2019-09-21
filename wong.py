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

def lugares_envio():
	link = 'https://www.wong.pe/institucional/costos-de-envio'
	imageUrl='data:image/jpeg;base64,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'
	title='Nuestras tiendas'
	respuesta = ('[{"card": { "title": "' + nombre + '","imageUri":"' + imageUrl + '",' +
			   '"buttons": [{"text": "Ver lugares de envio","postback":"' + link + '"}]},"platform": "FACEBOOK"}]')
#busqueda
def busqueda(parameter):
	url = 'https://www.wong.pe/api/catalog_system/pub/products/search/?ft='+parameter+'&_from=0&_to=0'
	resp = requests.get(url)
	resultados = resp.json()
	for res in resultados:
		nombre = res['productName']
		marca = res['brand']
		categorias = res['categoriesIds'][0]
		link = res['link']
		imageId = res['items'][0]['images'][0]['imageId']
		categoria = "https://www.wong.pe" + categorias
		imageUrl = 'https://wongfood.vteximg.com.br/arquivos/ids/'+imageId+'-250-250/' 

	respuesta = ('[{"card": { "title": "' + nombre + '","subtitle":"' + marca +'","imageUri":"' + imageUrl + '",' +
			   '"buttons": [{"text": "Detalles","postback":"' + link + '"},{"text": "Similares","postback":"' +
			   categoria + '"}]},"platform": "FACEBOOK"}]')
	print(respuesta)
	return  json.loads(respuesta)

#ofertas
def ofertas():
	url = 'https://www.wong.pe/api/catalog_system/pub/products/search/?&fq=H%3a4234&_from=0&_to=2'
	resp = requests.get(url)
	resultados = resp.json()
	respuesta = '['
	for res in resultados:
		nombre = res['productName']
		marca = res['brand']
		link = res['link']
		imageId = res['items'][0]['images'][0]['imageId']
		imageUrl = 'https://wongfood.vteximg.com.br/arquivos/ids/'+imageId+'-250-250/'
		precio_ofe = res['items'][0]['sellers'][0]['commertialOffer']['Price']
		precio_ori = res['items'][0]['sellers'][0]['commertialOffer']['ListPrice']

		respuesta = respuesta + ('{"card": { "title":"' + nombre + '","subtitle":"' + marca +'","imageUri":"' + imageUrl + '",' +
					'"buttons": [{"text": "Precio Oferta:'+ precio_ofe +'"},{"text": "Precio Normal:'+precio_ori+
					'"},{"text": "Detalles","postback":"' + link + '"}]},"platform": "FACEBOOK"},')

	respuesta = respuesta + ']'

	return  json.loads(respuesta)


# function for responses
def results():
	# build a request object
	req = request.get_json(force=True)

	# fetch action from json
	intent = req.get('queryResult').get('intent').get('displayName')
	text = req.get('queryResult').get('queryText')
	
	if intent == 'wong.tiendas':
		return {'fulfillmentText': tiendas()}
	elif intent == 'wong.buscar':
		parameter = req.get('queryResult').get('parameters').get('any')
		if parameter == '':
			return {'fulfillmentText': 'No entendí lo que buscas, por favor intenta nuevamente'}
		return {'fulfillmentMessages': busqueda(parameter)}
	elif intent == 'wong.envios':
		return {'fulfillmentMessages': lugares_envio()}
	elif intent == 'wong.ofertas':
		return {'fulfillmentMessages': ofertas()}
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
