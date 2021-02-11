import os
import urllib.request
from app import app
from widgettest import WidgetTest
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename

@app.route('/api/sensor-log-parser/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and file.filename.lower().endswith('.txt'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        sensor_pattern = os.environ.get('SENSOR_PATTERN', 'thermometer temp-, humidity hum-')
        c = WidgetTest(file_path, sensor_pattern)
        resp = c.sort_dict()
        return resp
    else:
        resp = jsonify({'message' : 'Only txt files are allowed'})
        resp.status_code = 400
        return resp
        
@app.route('/api/sensor-log-parser/healthz')
def healthz():
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')