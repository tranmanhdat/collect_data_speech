import os
import re

import flask
import requests
from flask import flash, request, redirect, render_template, \
    send_from_directory, jsonify
from werkzeug.utils import secure_filename
from connect_database import get_all_sentences

app = flask.Flask(__name__)

app.secret_key = "colect_data"
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/demo'
app.config['MAX_CONTENT_LENGTH'] = 20000 * 1024 * 1024

@app.route('/get_ids', methods=['GET'])
def get_ids():
    dict_sentences = get_all_sentences()
    print(dict_sentences)
    # for key, value in dict_sentences:
    #     result.append({"id":str(key), "sentence":value})
    return jsonify(dict_sentences)
@app.route('/upload_files', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('file')
        if files.count == 0:
            print('no file uploading!')
            return jsonify({'message':'empty file'}), 400
        else:
            print(len(files))
            accepted_file = []
            for file in files:
                print(file.filename)
                if file:
                    filename = secure_filename(file.filename)
                    path_to_file = os.path.join(
                            str(app.config['UPLOAD_FOLDER']), filename)
                    file.save(path_to_file)
                    accepted_file.append(filename)
            if len(accepted_file)==0:
                return jsonify({'message':'file extension is not allowed'}), 400
            else:
                return jsonify({'message':'upload '+str(len(accepted_file))+' files'}), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0')