# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 16:18:20 2020

@author: Himanshu.Manjarawala
"""

import tempfile
from flask import Flask, render_template, request, Response, jsonify
from os.path import join
import QRCode


app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home_page():
    return render_template("index.html")

@app.route("/api/qr", methods=["GET","POST"])
def generate_qrcode():
    if request.method == "GET":
        return generate_image_response("www.google.com")
    elif request.method == "POST":
        if "qrstring" not in request.form:
            return create_error_json_message("No string entered to generate Qrcode!!!", 500)
        
        qrstring = request.form["qrstring"]
        return generate_image_response(qrstring)

def generate_image_response(qrstring):
    
    with tempfile.TemporaryDirectory() as path:
        QRCode.generate_qrcode(qrstring, join(path, "qr.png"))
        with open(join(path, "qr.png"), "rb") as f:
            stream = f.read()
    res = Response(stream, mimetype="image/png",
    headers={"Content-disposition":
             "attachment; filename=qr.png"})
    return res

def create_error_json_message(message, status_code):
    message = {
        'status': status_code,
        'message': message,
    }
    resp = jsonify(message)
    resp.status_code = status_code
    return resp

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=False)