
from flask import Flask 
from main.app_route import wedding
from main.extention import db,bucket,socketio
from flask_socketio import SocketIO

def create_app():
    #app是我的專案環境我的全局 代表我的全部 所以我要在這裡初始化所有的東西 

    app = Flask(__name__)#主要的Flask Blueprint是小flask
    app.register_blueprint(wedding)
    socketio.init_app(app)
    return app

