import time
import logging
from flask import Flask
from threading import Thread
from urllib.request import urlopen

app = Flask('')

@app.route('/')
def home():
    return 'Bot is up.'

def run():
    app.run(host='0.0.0.0',port=8080) 

def ping(target, debug):
    while True:
        r = urlopen(target)
        if debug: print(f'Status Code: {r.getcode()}')
        time.sleep(30*60)

def up(url, debug=False):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    Thread(target=run).start()
    Thread(target=ping, args=(url, debug,)).start()

