import json
from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify, flash
from flask_session import Session
import setup
from classes.Card import Card
from db import *

app = Flask(__name__)
app.secret_key = b'_523#y2L"F4Q8z\n\xec]/'
SESSION_TYPE = 'filesystem'
app.config['SESSION_TYPE'] = SESSION_TYPE
app.config["SESSION_PERMANENT"] = False
Session(app)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = setup.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = setup.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = setup.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = setup.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = setup.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = setup.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = setup.RESTPLUS_ERROR_404_HELP


def initialize_app(a):
    configure_app(a)


def main():
    initialize_app(app)
    # log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=setup.FLASK_DEBUG)


headers = ('Category', 'Type', 'Name', 'Creator', 'ID',
           'Incoming Date', 'Shelf', 'Is Available?')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        barcode = request.form['barcode_no']
        user_role = request.form['select_role']
        user = get_user(barcode)
        session['user'] = user
        session['role'] = user_role
        return redirect('/')
    return render_template("login_page.html")


@app.route('/', methods=['POST', 'GET'])
def home():
    if not session.get('user'):
        return redirect(url_for('login'))
    else:
        current_user = session.get('user')
        role = session.get('role')
        items = get_all_stock()
        if current_user.category == role:
            return render_template("main_page.html", headers=headers, items=items)


@app.route('/personal', methods=['POST', 'GET'])
def personal():
    current_user = session.get('user')
    current_card = get_user_card(current_user.user_id)
    return render_template("personal_page.html", user=current_user.display(), card=current_card.display())


@app.route('/send_item', methods=['POST'])
def send_item():
    message = ''
    if not control_get_operation(session.get('user', None)):
        print("f")
        # alert
    else:
        current_user = session.get('user')
        json_data = request.get_json()
        selected_item = Stock(json_data[0], json_data[1], json_data[2],
                              json_data[3], json_data[4], json_data[5],
                              json_data[6], json_data[7])
        result = can_borrow_item(selected_item)
        if result[0] is True and result[1] == "available":
            borrow_item(current_user, selected_item)
            message = 'You were successfully get item!'
        elif result[0] is True and result[1] == "reserve":
            reserve_item(current_user, selected_item)
            message = 'You were successfully reserve item!'
        else:
            message = 'Sorry, this item not available'
    duple = {'status': 'success', 'message': message}
    return json.dumps(duple)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['user'] = None
    session['role'] = None
    return render_template("login_page.html")


if __name__ == '__main__':
    app.run(debug=True)
