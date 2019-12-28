import hashlib
import json
import random
import time

from flask import Flask, render_template, Response, request, redirect
from flask_bootstrap import Bootstrap

wa_app = Flask(__name__)

passports = []
password = str(hash(random.random()))

class Yuuki_WebAdmin:
    def __init__(self):
        self.app = wa_app
        Bootstrap(self.app)

    @staticmethod
    @wa_app.route("/")
    def index():
        if "yuuki_admin" in request.cookies:
            if request.cookies["yuuki_admin"] in passports:
                return render_template('manage.html')
            else:
                response = redirect("/")
                response.set_cookie(
                    key='yuuki_admin',
                    value='',
                    expires=0
                )
                return response
        else:
            return render_template('index.html')

    @staticmethod
    @wa_app.route("/verify", methods=['GET', 'POST'])
    def verify():
        result = {"status": 403}
        if request.method == "POST" and "code" in request.values:
            if request.values["code"] == password:
                seed = hash(random.random() + time.time())
                seed = str(seed).encode('utf-8')
                session_key = hashlib.sha256(seed).hexdigest()
                passports.append(session_key)
                result = {"status": 200, "session": session_key}
            else:
                result = {"status": 401}
        return Response(json.dumps(result), mimetype='application/json')


    @staticmethod
    @wa_app.route("/logout")
    def logout():
        response = redirect("/")
        if "yuuki_admin" in request.cookies:
            if request.cookies.get("yuuki_admin") in passports:
                passports.remove(request.cookies.get("yuuki_admin"))
            response.set_cookie(
                key='yuuki_admin',
                value='',
                expires=0
            )
        return response

    @staticmethod
    def set_password(code):
        global password
        password = code

    def start(self, admin_password):
        self.set_password(admin_password)
        self.app.run(port=2020, debug=True)
