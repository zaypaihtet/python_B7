from flask import render_template

from . import public_bp


@public_bp.get("/")
def home():
    return render_template("index.html")


@public_bp.get("/about")
def about():
    return render_template("about.html")


@public_bp.get("/projects")
def projects():
    return render_template("projects.html")


@public_bp.get("/github")
def github():
    return render_template("github.html")


