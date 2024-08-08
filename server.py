import json
from flask import Flask, send_file, request
from main import encrypt_files, decrypt_files
import tempfile
from flask_cors import CORS
import io
import zipfile

app = Flask(__name__)
CORS(app=app)

def handle_files(files):
    file_list = []
    for i in range(len(files)):
        file_list.append({
            "file": files[i].read(),
            "filename": files[i].filename
        })
    return file_list

@app.route('/')
def welcome():
    return "201"

@app.route('/decrypt_file', methods=['POST'])
def decrypt_file_request():
    file = request.files['file']
    key = request.form["key"]
    files_returned = decrypt_files(file, key)
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for i in range(len(files_returned)):
            zip_file.writestr(files_returned[i]["filename"], files_returned[i]["file"])

    return send_file(io.BytesIO(zip_buffer.getvalue()), mimetype="application/octet-stream")

@app.route('/encrypt_file', methods=['POST'])
def encrypt_file_request():
    files = request.files.getlist("file")
    key = request.form["key"]
    return send_file(io.BytesIO(encrypt_files(handle_files(files), key)), mimetype="application/octet-stream")
 


if __name__ == '__main__':
   app.run(port=5000)  