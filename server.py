from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import spacy
from collections import Counter
from string import punctuation

class MyHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        text = data['text']
        response = process_text(text)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, world!')
        
def by_value(item):
    return item[1]

def get_keywords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    nlp = spacy.load("pl_core_news_lg")
    doc = nlp(text.lower().replace("\n", ""))
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token)
    my_dic = dict(zip([token for token in result],
    [token.lemma_ for token in result]))
    lemmats = {value: 0 for key, value in my_dic.items()}
    for key in my_dic:
        value = my_dic[key]
        lemmats[value] = lemmats[value] + 1

    return lemmats
    
def process_text(text):
    keywords = get_keywords(text)
    i = 1
    last = 0
    result = []
    for k, v in sorted(keywords.items(), key=by_value, reverse=True):
        if i > 10 and last != v:
            break
        last = v
        if v > 0:
            result.append({'index': i, 'word': k, 'count': v})
        i = i + 1
    return result

def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

run()
