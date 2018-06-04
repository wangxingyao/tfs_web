#coding: utf-8

# app/main/views.py：带有蓝图的应用程序路由
from flask import render_template

from . import main
from ..models import UploadFile

NGINX_HOST = "192.168.159.133"

@main.route('/', methods = ['POST', 'GET'])
def index():
    uf = UploadFile.query.order_by(-UploadFile.mtime).limit(31).all()
    urls = []
    for e in uf:
        url = "http://{}/v1/tfs/{}".format(NGINX_HOST, e.tfsname)
        urls.append(url)
    return render_template('index.html', urls=urls)


@main.route('/upload', methods = ['POST', 'GET'])
def upload():
    return render_template('upload.html')
