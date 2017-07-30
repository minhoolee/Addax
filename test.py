import requests
import json
from glob import glob

data = []
for file_name in glob('*.json'):
	file_name = file_name[:-5]
	url =  'http://AddaxServer-env.ubepzwztwv.us-west-2.elasticbeanstalk.com/upload'
	files = {'video': (file_name + '.mp4',open(file_name + '.mp4', 'rb'),'video/mp4'),'info': (file_name + '.json',open(file_name + '.json', 'rb'),'application/json')}
	r = requests.post(url, files=files)
