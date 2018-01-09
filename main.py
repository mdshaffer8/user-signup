from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)

app.config['DEBUG'] = True

@app.route('/signup')
def display_signup_form():
    return render_template('signup_form.html')

def is_blank(x):
    if x:
        return False
    else:
        return True


@app.route('/signup', methods=['POST'])
def user_errors():

    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''


    # password
    if is_blank(password):
        password_error = "Field cannot be blank"
        password = ''
    else:
        password_length = len(password)
        if password_length > 20 or password_length < 3:
            password_error = "Password must be between 3 and 20 characters"
            password = ''
        else:
            if " " in password:
                password_error = "Password cannot contain spaces"
                password = ''
            else:
                if verify_password != password:
                    verify_password_error = "Passwords must match"
                    password = ''
                    verify_password = ''

    # username
    if is_blank(username):
        username_error = "Field cannot be blank"
        username = ''
    else:
        username_length = len(username)
        if username_length > 20 or username_length < 3:
            username_error = "Username must be between 3 and 20 characters"
            username = ''
        else:
            if " " in username:
                username_error = "Username cannot contain spaces"
                username = ''

    # email
    if not is_blank(email):
        email_length = len(email)
        if email_length > 20 or email_length < 3:
            email_error = "Email address must be between 3 and 20 characters"
            email = ''
        else:
            if "@" not in email:
                email_error = "Email address must contain the '@' symbol"
                email = ''
            else:
                if "." not in email:
                    email_error = "Email address must contain a period"
                    email = ''

    if not username_error and not password_error and not verify_password_error and not email_error:
        username = username
        return redirect('/welcome?username={0}'.format(username))
    else:
        return render_template('signup_form.html', username_error=username_error, username=username, password_error=password_error, password=password, verify_password_error=verify_password_error, verify_password=verify_password, email_error=email_error, email=email)


@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)


app.run()