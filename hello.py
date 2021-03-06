from flask import Flask, request
import requests
import json
from jinja2 import Environment, PackageLoader
import os

app = Flask(__name__)

@app.route('/')
def input():
	env = Environment(loader=PackageLoader('scriptname', 'template'))
	template = env.get_template('input.html')
	return template.render()

@app.route('/output', methods=['POST'])
def output():
	#get information from front page
	inputResult = request.form
	searchWord = inputResult['query']

    #Headers with API Keys
	url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
	headers = {}
	headers['app_key'] = "43ca2baad599b4ffed25c2fc22c4dbfd"
	headers['app_id'] = "20a6d157"

	#Defines parameters
	params = {
		'q': 'objname_s:' + str(searchWord),
		#'q': 'objcollector_ss: Dr. David P. Barrows',
		'wt': 'json',
		'indent': 'True',
		'facet': 'true',
		'facet.field':'blob_ss',
		'rows': 0
	}
	r = requests.get(url, params=params, headers=headers)		

	#array of images we push to the website
	imgArr = []
	#set an limit to the number of itmes we get
	itemLimit = 20
	data = json.loads(r.text)
	print data['response']['numFound']
	for item in data['facet_counts']['facet_fields']['blob_ss']:
		if item > 100 and itemLimit > 0:
			imgArr.append(item)
			itemLimit -= 1

	#Image Titles
	txtDict = {	"dbda1dd7-70ac-4d2a-85d6":"Pang gamit sa usok ng tobacco galing sa Luzon Province",
				"2699d4e9-e946-4afe-9ef6":"Ang buslo galing sa Visayan Province.",
				"4a985ea9-6b22-4a68-be26":"sample text"
				}

	#Jinja template
	env = Environment(loader=PackageLoader('scriptname', 'template'))
	template = env.get_template('myhtmlpage.html')
	templateVars = {
		"title":		"HearstAudio",
		"description":	"We take pictures and add context to them!",
		"array": 		imgArr,
		"txtDict":		txtDict
	}

	return template.render(templateVars)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
