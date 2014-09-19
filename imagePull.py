import requests
import json

url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
headers = {}
headers['app_key'] = "43ca2baad599b4ffed25c2fc22c4dbfd"
headers['app_id'] = "20a6d157"

params = {
#'q': 'objculturetree_txt:Arctic',
'q': 'objname_s:headdress',
'wt': 'json',
'indent': 'True',
'facet': 'true',
'facet.field':'objcollector_ss',
'rows': 0
}
r = requests.get(url, params=params, headers=headers)

print r.url
print r.status_code
print json.dumps(json.loads(r.text), indent=4)

#
