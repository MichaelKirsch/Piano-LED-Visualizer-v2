#!/usr/bin/env python3
"""Local preview server for web UI work — no Raspberry Pi or hardware required."""

import os
import sys

from flask import Flask, render_template

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
os.chdir(ROOT)
sys.path.insert(0, HERE)

from dev_api import register_dev_api

app = Flask(
    __name__,
    static_folder=os.path.join(HERE, "static"),
    template_folder=os.path.join(HERE, "templates"),
)
app.config["TEMPLATES_AUTO_RELOAD"] = True

register_dev_api(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/ledsettings")
def ledsettings():
    return render_template("ledsettings.html")


@app.route("/ledanimations")
def ledanimations():
    return render_template("ledanimations.html")


@app.route("/songs")
def songs():
    return render_template("songs.html")


@app.route("/sequences")
def sequences():
    return render_template("sequences.html")


@app.route("/ports")
def ports():
    return render_template("ports.html")


@app.route("/network")
def network():
    return render_template("network.html")


@app.route("/practice")
def practice():
    return render_template("practice.html")


if __name__ == "__main__":
    print("Web UI dev server: http://127.0.0.1:5000")
    print("Songs page with test MIDI: http://127.0.0.1:5000/#songs")
    print("Tip: click Learn on 'Fur Elise.mid' to open the sheet preview.")
    app.run(host="127.0.0.1", port=5000, debug=True)
