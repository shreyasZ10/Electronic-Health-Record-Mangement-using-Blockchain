import datetime
import json
import os
import secrets
import requests
from flask import render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db, bcrypt
from . import ocr
import cv2
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\SHREYAS\AppData\Local\Tesseract-OCR\tesseract.exe'

from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, profession=form.choice.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            print(current_user.profession, current_user.username)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                print(current_user.profession, current_user.username)
                if current_user.profession == 'patient':
                    if tx["author"] == current_user.username:
                        tx["index"] = block["index"]
                        tx["hash"] = block["previous_hash"]
                        content.append(tx)
                else:
                    userid = current_user.user_id
                    user = User.query.filter_by(id=userid).all()
                    username1 = []
                    for i in user:
                        username1.append(i.username)

                    print(user, username1)
                    for block in chain["chain"]:
                        for tx in block["transactions"]:
                            if tx["author"]  in username1:
                                tx["index"] = block["index"]
                                tx["hash"] = block["previous_hash"]
                                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)

# def fetch_posts_doc():
#     """
#     Function to fetch the chain from a blockchain node, parse the
#     data and store it locally.
#     """
#     get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
#     response = requests.get(get_chain_address)
#     if response.status_code == 200:
#         content = []
#         chain = json.loads(response.content)
#         print(current_user.username)
#         userid = current_user.user_id
#         user = User.query.filter_by(id=userid).all()
#         username1 = []
#         for i in user:
#             username1.append(i.username)

#         print(user, username1)
#         for block in chain["chain"]:
#             for tx in block["transactions"]:
#                 if tx["author"]  in username1:
#                     tx["index"] = block["index"]
#                     tx["hash"] = block["previous_hash"]
#                     content.append(tx)

#         global posts
#         posts = sorted(content, key=lambda k: k['timestamp'],
#                        reverse=True)



@login_required
@app.route('/home')
def home():
    fetch_posts()
    return render_template('index.html',
                           title='Patient Page',
                           profession = current_user.profession,
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)
# @login_required
# @app.route('/homedoc')
# def homedoc():
#     fetch_posts_doc()
#     return render_template('indexdoc.html',
#                            title='Doctor Page',
#                            posts=posts,
#                            node_address=CONNECTED_NODE_ADDRESS,
#                            readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.files["content"]
    # author = request.form["author"]
    author = current_user.username
    
    filename = secure_filename(post_content.filename) 
    # os.path.join is used so that paths work in every operating system
    post_content.save("app/images/"+filename)
    # You should use os.path.join here too.
    IMG_DIR = "app/images/"
    image = cv2.imread(IMG_DIR + filename)
    b,g,r = cv2.split(image)
    rgb_img = cv2.merge([r,g,b])
    
    # Preprocess image
        
    scaling_image = ocr.scaling(image)
    gray = ocr.get_grayscale(scaling_image)
    thresh = ocr.thresholding(gray)
    remove_noise_image = ocr.remove_noise(thresh)
    preprocessed_image = remove_noise_image

    file_content = tess.image_to_string(preprocessed_image)
    
    post_object = {
        'author': author,
        'content': file_content,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/home')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
