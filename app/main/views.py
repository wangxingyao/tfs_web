#coding: utf-8

# app/main/views.py：带有蓝图的应用程序路由
from datetime import datetime

from flask import render_template, session, redirect, url_for

from . import main
from ..models import User

@main.route('/',methods = ['POST','GET'])
def index():
    return render_template('index.html')
