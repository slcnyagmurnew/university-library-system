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
    message = ''
    if request.method == "POST":
        if request.form['submit_button'] == 'Leave the Item':
            item_id = request.form['leftId']
            remove_from_belonging(item_id)
            message = 'Item has been successfully released!'
            # reserve ise email
        elif request.form['submit_button'] == 'Add Money':
            amount = request.form['amount_money']
            card_id = get_user_card(current_user.user_id).card_id
            card_operation(amount, True, card_id)
            message = 'Money successfully added!'
        elif request.form['submit_button'] == 'Borrow the Item':
            item_id = request.form['borrowedId']
            if is_still_borrowed(item_id):
                message = "The item is still in the user!"
            else:
                remove_from_reserve(item_id)
                borrow_item(current_user, item_id)
                message = 'You were successfully get item!'
        else:
            print("nothing to do")
    current_card = get_user_card(current_user.user_id)
    belonging_list = get_belonging_items(current_user)
    reserved_list = get_reserved_items(current_user)
    return render_template("personal_page.html",
                           user_information=current_user.display(),
                           card_information=current_card.display(),
                           belonging_items=belonging_list,
                           reserved_items=reserved_list,
                           message=message)


@app.route('/send_item', methods=['POST'])
def send_item():
    message = ''
    current_user = session.get('user')
    json_data = request.get_json()
    selected_item = Stock(json_data[0], json_data[1], json_data[2],
                          json_data[3], json_data[4], json_data[5],
                          json_data[6], json_data[7])
    if not control_get_operation(current_user):
        message = 'You have reached the maximum number of items you can get!'
    elif not control_get_book(current_user, selected_item):
        message = 'You dont have the necessary role to take it!'
    elif have_expired_item(current_user):
        message = 'You have overdue items!'
    else:
        result = can_borrow_item(selected_item)
        if result == "available":
            borrow_item(current_user, selected_item.item_id)
            message = 'You were successfully get item!'
        elif result == "reserve":
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
