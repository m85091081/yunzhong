# -*- coding: utf-8 -*-
# muMDAU_app init file 
# some debug code of server like update/restart code
from flask import Flask, request, session, redirect, url_for
from flask import render_template 
from flask_socketio import SocketIO
import eventlet,os
template_dir = os.path.abspath('../core_template/templates')
app = Flask(__name__,template_folder=template_dir)
socketio = SocketIO(app, async_mode='eventlet')

