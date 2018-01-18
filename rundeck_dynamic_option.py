#!/usr/bin/python
#coding: utf-8

l = [
"fin-cashier",
"fin-fbm",
"fin-feim",
"fin-fxio",
"fin-mgw",
"fin-paycore",
"fin-tradeprocess"
]

from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/QJS/deploy.json')
def show():
    return jsonify(l)

app.run(port=19081)
