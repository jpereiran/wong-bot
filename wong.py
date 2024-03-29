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
	imageUrl='http://lucidez.pe/wp-content/uploads/2018/06/wong.jpg'
	title='Visitanos en nuestras nuestras tiendas'
	respuesta = ('[{"card": { "title": "' + title + '","imageUri":"' + imageUrl + '",' +
			   '"buttons": [{"text": "Ver lugares de envio","postback":"' + link + '"}]},"platform": "FACEBOOK"}]')
	return json.loads(respuesta)
#busqueda
def busqueda(parameter):
	url = 'https://www.wong.pe/api/catalog_system/pub/products/search/?ft='+parameter+'&_from=0&_to=0'
	resp = requests.get(url)
	resultados = resp.json()
	for res in resultados:
		nombre = res['productName']
		marca = res['brand']
		categorias = res['categories'][0]
		link = res['link']
		imageId = res['items'][0]['images'][0]['imageId']
		categoria = "https://www.wong.pe" + categorias
		imageUrl = 'https://wongfood.vteximg.com.br/arquivos/ids/'+imageId+'-250-250/' 

	respuesta = ('[{"card": { "title": "' + nombre + '","subtitle":"' + marca +'","imageUri":"' + imageUrl + '",' +
			   '"buttons": [{"text": "Detalles","postback":"' + link + '"},{"text": "Similares","postback":"' +
			   categoria + '"}]},"platform": "FACEBOOK"}]')
	print(respuesta)
	return  json.loads(respuesta)

#puntos bonus
def puntos_bonus(dni):
	url = 'https://widget-admin.mybluemix.net/anita/backend/db.php?action=consultarPuntos&doctype=1&dni='+dni
	resp = requests.get(url)
	resultado = resp.json()
	puntos = resultado['payload']['rewards']
	return ('Tienes ' + str(puntos) + ' puntos')

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
					'"buttons": [{"text": "Precio Oferta:'+ str(precio_ofe) +'"},{"text": "Precio Normal:'+str(precio_ori)+
					'"},{"text": "Detalles","postback":"' + link + '"}]},"platform": "FACEBOOK"},')

	respuesta = respuesta[:-1] + ']'

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
	elif intent == 'wong.bonus - custom':
		parameter = req.get('queryResult').get('parameters').get('any')
		return {'fulfillmentText': puntos_bonus(parameter)}
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
