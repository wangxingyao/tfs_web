#coding: utf-8

# app/api/views.py：带有蓝图的应用程序路由

from flask import redirect, request, jsonify
from flask import current_app
from werkzeug.utils import secure_filename
import os, pytfs, commands
from datetime import datetime

from . import api
from ..models import UploadFile
from .. import db

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def query_md5(md5):
    pass

def save_tfs(file, filename):
    app = current_app._get_current_object()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    tfs = pytfs.TfsClient()
    tfs.init(app.config['TFS_SERVER'])
    tfsname = tfs.put(filepath)
    return tfsname

def update_name_map(filename, md5):
    uf = UploadFile.query.filter_by(md5=md5).all()
    if uf:
        uf = uf[0]
        uf.filename = filename
        uf.mtime = datetime.now()
        return True
    return False

def save_name_map(filename, tfsname, md5):
    uf = UploadFile(tfsname=tfsname, md5=md5, filename=filename, mtime=datetime.now())
    db.session.add(uf)
    db.session.commit()

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
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            md5 = commands.getoutput("md5sum " + filepath).split()[0]
            file.save(filepath)
            file.close()

            if not update_name_map(filename, md5):
                tfsname = save_tfs(file, filename)
                save_name_map(filename, tfsname, md5)

        return jsonify({'code': '200'})
    return jsonify({'code': '200', 'content': 'None'})
