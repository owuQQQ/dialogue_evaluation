from flask import Flask, request, send_from_directory, render_template_string, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    with open('dialogue.html', encoding='utf-8') as f:
        html = f.read()
    return render_template_string(html)

@app.route('/samples.txt')
def samples():
    return send_from_directory('.', 'samples.txt')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    results = data.get('results', [])
    save_path = 'results.csv'
    file_exists = os.path.isfile(save_path)
    with open(save_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['id', 'dialogue_id', 'dialogue_index', 'understandable', 'natural', 'backchannels'])
        for row in results:
            writer.writerow([
                row.get('id', ''),
                row.get('dialogue_id', ''),
                row.get('dialogue_index', ''),
                row.get('understandable', ''),
                row.get('natural', ''),
                row.get('backchannels', '')
            ])
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)