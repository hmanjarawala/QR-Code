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


@app.route("/api/v1/qr", methods=["GET","POST"])
def generate_qrcode():
    if request.method == "GET":
        
        return generate_image_response("www.google.com")
    
    elif request.method == "POST":
        
        if "qrstring" not in request.form:
            return create_error_json_message("No string entered to generate Qrcode!!!", 500)
        
        qrstring = request.form["qrstring"]
        return generate_image_response(qrstring)


@app.route("/api/v1/upiqr", methods=["GET","POST"])
def generate_upi_qrcode():
    if request.method == "GET":
        
        return generate_upi_string("hmanjarawala@okicici", "Himanshu%20Manjarawala", 0)
    
    elif request.method == "POST":
        
        if "vpa" not in request.form:
            return create_error_json_message("VPA not found!!!", 500)
        
        if "name" not in request.form:
            return create_error_json_message("Receiver name not found!!!", 500)
        
        if "amount" not in request.form:
            return create_error_json_message("Amount not found!!!", 500)
        
        vpa = request.form["vpa"]
        name = request.form["name"]
        amount = request.form["amount"]
        
        currency = "INR" if "currency" not in request.form else request.form["currency"]
        
        merchant_code = None if "merchant_code" not in request.form else request.form["merchant_code"]
        trRef = None if "trn_ref" not in request.form else request.form["trn_ref"]
        trNotes = None if "trn_notes" not in request.form else request.form["trn_notes"]
        refUri = None if "ref_uri" not in request.form else request.form["ref_uri"]
        
        return generate_upi_string(vpa, name, amount, merchant_code, currency, trRef, trNotes, refUri)

    
def generate_upi_string(vpa, name, amount, merchant_code=None, currency="INR", trRef=None, 
                        trNotes=None, refUri=None):
    qrstring="upi://pay?"
    qrstring += "pa={}".format(vpa)
    qrstring += "&pn={}".format(name)
    qrstring += "&am={}".format(amount)
    qrstring += "&cu={}".format(currency)
    qrstring += "&mc={}".format(merchant_code) if merchant_code != None else ""
    qrstring += "&tr={}".format(trRef) if trRef != None else ""
    qrstring += "&tn={}".format(trNotes) if trNotes != None else ""
    qrstring += "&url={}".format(refUri) if refUri != None else ""
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