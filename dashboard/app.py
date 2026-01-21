from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Path to the shared data dump file
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hardlint_data.json')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """Reads the JSON data file dumped by hardlint.py and returns it for the graph."""
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "No data found. Run a search first!"})
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    print("Starting Hardlint Dashboard on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
