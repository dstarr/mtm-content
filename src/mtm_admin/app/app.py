import os
import sys
from flask import Flask, render_template
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'services'))

from content_service import ComtentService

content_service = ComtentService()

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    modules = content_service.get_all_modules()
    return render_template('index.html', modules=modules)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
