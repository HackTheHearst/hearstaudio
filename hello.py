from flask import Flask, request
import requests
import json
from jinja2 import Environment, PackageLoader

app = Flask(__name__)

@app.route('/')
def input():
	env = Environment(loader=PackageLoader('scriptname', 'template'))
	template = env.get_template('input.html')
	return template.render()

@app.route('/output', methods=['POST'])
def output():
    #Headers with API Keys
	url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
	headers = {}
	headers['app_key'] = "43ca2baad599b4ffed25c2fc22c4dbfd"
	headers['app_id'] = "20a6d157"

	#Defines parameters
	params = {
		'q': 'objname_s:fork',
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

	env = Environment(loader=PackageLoader('scriptname', 'template'))
	template = env.get_template('myhtmlpage.html')
	templateVars = {
		"title":		"Test Example",
		"description":	"A simple inquiry of function.",
		"array": imgArr
	}

	return template.render(templateVars)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
