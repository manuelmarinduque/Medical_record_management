from flask import Blueprint, render_template, redirect, url_for

auth_app = Blueprint('auth', __name__)

@auth_app.route("/home")
def index():
    return 'test from bp'