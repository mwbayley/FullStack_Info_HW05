# Importing flask library
from app import app
from flask import Flask, redirect, make_response, render_template, url_for, session, request, escape, flash
import os
app.secret_key = os.environ.get('SECRET_KEY') or 'hard to guess string'

@app.route('/')
@app.route('/index')
def index():
    username = ''
    if (username in session): 
        #check if the user is already in session, if so, direct the user to survey.html
        # Hint: render_template with a variable
        return render_template('survey.html', username=session['username'])
    else:
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST']) # You need to specify something here for the function to get requests
def login():
    # Here, you need to have logic like if there's a post request method, store the username and email from the form into
    # session dictionary
    if request.method=='GET':
        session['username'] = request.args.get('username')
        session['email'] = request.args.get('email')
    if request.method=='POST':
        session['username'] = request.form.get('username')
        session['email'] = request.form.get('email')
    return render_template('survey.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('email', None)
	return redirect(url_for('index'))

@app.route('/submit-survey', methods=['GET', 'POST'])
#@app.route('/submit-survey', methods=['POST'])
def submitSurvey():
    #username = session['username']
    #email = session['email']
    print("submitted")
    if('username' in session): #check if user in session
        username = session.get('username')
        surveyResponse = {
            'fe-before': request.form['feBefore'],
            'food': request.form['food'],
            'vacation': request.form['vacation'],
            'color': request.form['color'],
            'fe-after': request.form['feAfter']
            }
        #get the rest o responses from users using request library Hint: ~3 lines of code
       # surveyResponse['fe-before'] = request.form.get('feBefore')
        #surveyResponse['fe-after'] = request.form.get('feAfter')
        if surveyResponse['fe-after'] > surveyResponse['fe-before']:
            return render_template('results.html', surveyResponse=surveyResponse)
        else:
            return render_template('bad.html', surveyResponse=surveyResponse)

    else:
        return render_template('login.html')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
