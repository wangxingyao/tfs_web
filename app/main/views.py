#coding: utf-8

# app/main/views.py：带有蓝图的应用程序路由
from flask import render_template

from . import main
from ..models import UploadFile

@main.route('/', methods = ['POST', 'GET'])
@main.route('/index', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')


@main.route('/upload', methods = ['POST', 'GET'])
def upload():
    return render_template('upload.html')

@main.route('/download', methods = ['POST', 'GET'])
def download():
    uf = UploadFile.query.all()
    urls = []
    for e in uf:
        url = "http://192.168.159.133/v1/tfs/{}".format(e.tfsname)
        urls.append(url)
        print url

    return render_template('download.html', urls=urls)
