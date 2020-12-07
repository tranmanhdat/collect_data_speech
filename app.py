#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from flask import Flask, flash, redirect, url_for, send_from_directory, \
    send_file
from flask import request, jsonify
from flask import render_template
from werkzeug.utils import secure_filename
from connect_database import get_all_sentences
import os
import re
from thongke import get_all_info

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/audios'
#
# # for mobile call APIs
# @app.route('/get_ids', methods=['GET'])
# def get_ids():
#     temp = []
#     dict_sentences = get_all_sentences()
#     for dict_sentence in dict_sentences:
#         temp_id = {}
#         temp_id["id"] = dict_sentence["id"]
#         temp.append(temp_id)
#     return jsonify(temp)
# @app.route('/get_sentence', methods=['POST'])
# def get_sentence():
#     sentence = None
#     id = request.form["id"]
#     dict_sentences = get_all_sentences()
#     for dict_sentence in dict_sentences:
#         if int(id) == int(dict_sentence["id"]):
#             sentence = dict_sentence["sentence"]
#             break
#     return jsonify({"sentence":sentence})
# @app.route('/upload_audios', methods=['POST'])
# def upload_files():
#     if request.method == 'POST':
#         files = request.files.getlist('file')
#         if files.count == 0:
#             flash('No file selected for uploading')
#             return redirect(request.url)
#         else:
#             time_upload = time.time()
#             time_upload = time.localtime(time_upload)
#             time_name = time.strftime("%Y%m%d%H%M", time_upload)
#             folder_upload = os.path.join(str(app.config['UPLOAD_FOLDER']), time_name)
#             if not os.path.exists(folder_upload):
#                 os.mkdir(folder_upload)
#             file_names = []
#             for file in files:
#                 if file:
#                     filename = secure_filename(file.filename)
#                     path_to_file = os.path.join(folder_upload, filename)
#                     file.save(path_to_file)
#                     file_names.append(filename)
#             return jsonify({"upload":"Success"})


dict_sentences = get_all_sentences()
with open("id.txt", "r") as f_id:
    cur_id = int(f_id.read())


# for web view
@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("login.html")


@app.route("/record", methods=['GET'])
def record():
    global cur_id, dict_sentences
    user_name = request.args.get("user_name")
    user_name = "".join(re.findall("[a-zA-Z]+", user_name))
    # print(user_name)
    id_1 = cur_id
    id_2 = cur_id + 9
    cur_id = cur_id + 10
    if cur_id > len(dict_sentences) - 1:
        cur_id = 0
    with open("id.txt", "w+") as f_out:
        f_out.write(str(cur_id))
    # id_2 = int(request.args.get("id_2"))
    # if id_2 < id_1:
    #     id_1, id_2 = id_2, id_1
    # id_sentence = {}
    id = []
    sentence = []
    for dict_sentence in dict_sentences:
        if id_1 <= dict_sentence["id"] <= id_2:
            id.append(dict_sentence["id"])
            sentence.append(dict_sentence["sentence"])
            # id_sentence[dict_sentence["id"]] = dict_sentence["sentence"]
    # print(id_sentence)
    return render_template("record.html", user_name=user_name, id=id,
                           sentence=sentence, number_id=len(id))


@app.route("/save_audios", methods=['POST'])
def save_audios():
    if request.method == 'POST':
        time_upload = time.time()
        time_upload = time.localtime(time_upload)
        time_name = time.strftime("%Y%m%d%H%M", time_upload)
        folder_upload = os.path.join(str(app.config['UPLOAD_FOLDER']),
                                     time_name)
        if not os.path.exists(folder_upload):
            os.mkdir(folder_upload)
        files = request.files.getlist('audio_data')
        if files.count == 0:
            flash('No file selected for uploading')
            return redirect(request.url)
        else:
            # file_names = []
            for file in files:
                if file:
                    filename = secure_filename(file.filename)
                    path_to_file = os.path.join(folder_upload, filename)
                    # print(path_to_file)
                    file.save(path_to_file)
                    # file_names.append(filename)
            return jsonify({"upload": "Success"})


# Route for handling the login page logic
# @app.route('/login_admin', methods=['GET', 'POST'])
# def login_admin():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin123':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('thongke'))
#     return render_template('login_admin.html', error=error)

names, number_files, duration_each_user, files_path_each_user, ids_each_user = [], [], [], [], []


@app.route('/thongke', methods=['GET', 'POST'])
def thongke():
    global names, number_files, duration_each_user, files_path_each_user, ids_each_user
    names, number_files, duration_each_user, files_path_each_user, ids_each_user = get_all_info()
    return render_template("thongke.html", names=names,
                           number_files=number_files,
                           duration_each_user=duration_each_user,
                           files_path_each_user=files_path_each_user,
                           number_names=len(names))


@app.route('/nghethu/<int:id>', methods=['GET', 'POST'])
def nghethu(id):
    global names, number_files, duration_each_user, files_path_each_user, ids_each_user
    name = names[id]
    print(name)
    number_file = number_files[id]
    files_path = files_path_each_user[id]
    # for i in range(0, len(files_path)):
    #     files_path[i] = "/".join(files_path[i].split("/")[1:])
    ids = ids_each_user[id]
    ids.sort()
    transcripts = []
    global dict_sentences
    i=0
    for dict_sentence in dict_sentences:
        if dict_sentence["id"]==int(ids[i]):
            transcripts.append(dict_sentence["sentence"])
            i = i + 1
            if i==len(ids):
                break
    return render_template("nghethu.html", name=name, number_file=number_file,
                           ids=ids, transcripts=transcripts, files_path=files_path)
@app.route('/audios/<path:filename>')
def download_file(filename):
    print(filename)
    return send_file(filename, as_attachment=True)
    # return send_from_directory('static', filename)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'))
