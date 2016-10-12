# -*- coding: utf-8 -*-
# muMDAU_app init file 
# some debug code of server like update/restart code
from flask import Flask, request, session, redirect, url_for
from flask import render_template 
from flask_socketio import SocketIO
import eventlet
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

