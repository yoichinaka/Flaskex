# -*- coding: utf-8 -*-

from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session
import json
import sys
import os
from predict import *
import stripe

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
product = stripe.Product.create(
  name='My SaaS Platform',
  type='service',
)
print(product['id'])
plan = stripe.Plan.create(
  product=product['id'],
  nickname='SaaS Platform USD',
  interval='month',
  currency='usd',
  amount=10000,
)
print(plan)
plan_id = plan['id']


app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only

# Heroku
#from flask_heroku import Heroku
#heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    print('&&&&&&&&&&&&&&&&&&&&',user)
    return render_template('home.html')

#-----------------------------------------------------
@app.route('/charge', methods=['GET', 'POST'])
def charge():
    # customer = stripe.Customer.create(
    #         email="gg@gg.com",
    #         source=request.json['token'])

    checkout_session = stripe.checkout.Session.create(
                success_url="http://www.google.com", ##unknown
                cancel_url="http://www.yahoo.com", ##unknown
                payment_method_types=["card"],
                subscription_data={"items": [{"plan": plan_id}]}

            )
    print(checkout_session)

    return render_template('charge.html')
#------------------------------------------------------

@app.route("/predict0", methods=['GET', 'POST'])
def predict():
    error = ""
    if request.method == 'POST':
        # Form being submitted; grab data from form.
        home = request.form['home']
        away = request.form['away']
        print(home, away)
        # Validate form data
        if len(home) == 0 or len(away) == 0:
            # Form data failed validation; try again
            error = "Please supply both home and away name"
        else:

            #  !!!!!! make prediction
            print(predict1(home, away))
            result = predict1(home,away)

            return render_template('predict0.html', text=result +' win')
            #return redirect(url_for('result', text = home))
    # Render the sign-up page
    return render_template('predict0.html', text=error)
#----------------------------------------------------------
    #return render_template('home.html')
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
