#coding: utf-8

# app/api/views.py：带有蓝图的应用程序路由

from flask import redirect, request, jsonify
from flask import current_app
import os
from werkzeug.utils import secure_filename

from . import api

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@api.route('/file/upload', methods = ['POST', 'GET'])
def upload_file():
    app = current_app._get_current_object()
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.close()
        return jsonify({'code': '200'})
    return jsonify({'code': '200', 'content': 'None'})
