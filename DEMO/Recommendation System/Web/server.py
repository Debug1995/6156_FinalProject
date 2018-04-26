from urllib2 import Request, urlopen
from flask import Flask, request, render_template, jsonify
import json
import os
from pprint import pprint

def request_project(topic, language, num, sort, headers):
    url = 'https://api.github.com/search/repositories?q='+topic+language+'&page=1&per_page='+num+sort
    request = Request(url, headers = headers)
    print url
    response = urlopen(request).read()
    result = json.loads(response.decode('utf-8'))
    return result

def query_project(field, language):
    headers = {'User-Agent':'Debug1995',
               'Authorization':'token 1b78d31ae40ea955cf8e4e95f7b704ef71d2e187'}
    '''
    topic = 'dataanalysisproject'   # choose the topic of project  
    language = ''               # choose the used language        format: +language:?
    '''
    num = 10                  # choose the number of request project
    sort = ''                   # stars/forks/update/(default)    format: &sort=?
    
    result = request_project(field, language, str(num), sort, headers)
    items = result['items']
    name = []
    url = []
    
    for item in items:
        name.append(item['full_name'])
        url.append(item['html_url'])
    
    data = {}   
    data["name"] = name
    data["url"] = url
    return data


app = Flask(__name__)

@app.route('/')
def index():
    print "start"
    return render_template('index.html')

@app.route('/query')
def query():
    field = request.args.get('field', '', type=str)
    if(field != ''):
        field = "topic:"+field

    extra = request.args.get('extra', '', type=str)
    if(extra != ''):
        if(field == ''):
            extra = "topic:"+extra
        else:
            extra = "+topic:"+extra

    language = request.args.get('language', '', type=str)
    if(language != ''):
        language = "+language:"+language

    data = json.dumps(query_project(field+extra, language))
    # print data
    return data

@app.route('/save')
def save():
    text = request.args.get('text', '', type=str)
    print text
    fo = open("log.txt", "a")
    fo.write(text+'\n')
    fo.close()
    return text


if __name__ == '__main__':
    app.run()