import requests
from bs4 import BeautifulSoup
from pprint import pprint
from tqdm import tqdm
from time import sleep
from random import randint
import json

url = 'http://www.speeches-usa.com'
data = requests.get(url)

soup = BeautifulSoup(data.text, features="lxml")

output = list()
for a in soup.body.find_all('a', href=True):
    href = a['href']
    if 'Transcripts/' in href:

        speech = {
            'url': url + '/' + href
        ,   'title': a.getText()
        }
        output.append(speech)
    

for i in tqdm(range(len(output))):

    data = requests.get(output[i]["url"])
    soup = BeautifulSoup(data.text, features="lxml")

    text_output = []
    for resourceBody in soup.body.find_all('p', {"class": "resourceBody"}):
        text = resourceBody.getText()
        text = text.split('(function(')[0]
        text_output.append(text)

    output[i]["text"] = text_output


with open('speeches.json', 'w') as outfile:
    json.dump(output, outfile)