import time
import logging
import requests
from replit import info
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return 'Bot is alive!'

def run():
    app.run(host='0.0.0.0',port=8080) 

def ping(target, debug):
    while True:
        r = requests.get(target)
        if debug: print("Status Code: " + str(r.status_code))
        time.sleep(30*60)

def up(debug=False):
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True
    t = Thread(target=run)
    r = Thread(target=ping, args=(info.co_url,debug,))
    t.start()
    r.start()

