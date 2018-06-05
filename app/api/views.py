#coding: utf-8

# app/api/views.py：带有蓝图的应用程序路由

from flask import redirect, request, jsonify
from werkzeug.utils import secure_filename
import pytfs, commands
from datetime import datetime

from . import api
from ..models import UploadFile
from .. import db

TEMP_FILE = '/root/uploads/temp.file'
TFS_SERVER = 'ns:8100'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def query_md5():
    cmd = "md5sum " + TEMP_FILE
    md5 = commands.getoutput(cmd).split()[0]
    return md5

def save_tfs(file, filename):
    tfs = pytfs.TfsClient()
    tfs.init(TFS_SERVER)
    tfsname = tfs.put(open(TEMP_FILE).read())
    return tfsname

def update_name_map(filename, md5):
    uf = UploadFile.query.filter_by(md5=md5).first()
    if uf:
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
            file.save(TEMP_FILE)
            file.close()
            md5 = query_md5()

            if not update_name_map(filename, md5):
                tfsname = save_tfs(file, filename)
                save_name_map(filename, tfsname, md5)

        return jsonify({'code': '200'})
    return jsonify({'code': '200', 'content': 'None'})
