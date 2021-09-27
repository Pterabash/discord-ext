import logging
import time
import threading
from urllib.request import urlopen

from flask import Flask
from replit import info

# Variables
__all__ = ['up']

# Instances
app = Flask('')
home = app.route('/')(lambda: 'Bot is up!')

# Functions
run = lambda: app.run(host='0.0.0.0', port=8080)

def ping() -> None:
    while True:
        urlopen(info.co_url)
        time.sleep(5*60)

def up() -> None: 
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    threading.Thread(target=run).start()
    threading.Thread(target=ping).start()
