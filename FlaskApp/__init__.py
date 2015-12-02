from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc, sys
from content_management import Content, connect_to_db

app = Flask(__name__)

# to use Flask forms module - WTForms - need to create a class for our form

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

@app.route('/')
def homepage():
	print("homepage")
	return render_template("main.html")

@app.route('/dashboard')
def dashboard_page():
	return render_template("dashboard.html")

@app.route('/register/', methods=["GET", "POST"])
def register_page():

	try:
		form = RegistrationForm(request.form)

		if request.method == "POST" and form.validate():
			username = form.username.data
			email = form.email.data
			password = sha256_crypt.encrypt((str(form.password.data)))
			c, conn = connect_to_db()

			x = c.execute("SELECT * FROM users WHERE username = (%s)", (thwart(username)))

			if int(x) > 0:
				flash("That username is already taken, please choose another")
				return render_template('register.html', form=form)
			else:
				c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
				conn.commit()
				flash("Thanks for registering!")
				c.close()
				conn.close()
				gc.collect()

				session["logged_in"] = True
				session['username'] = username

				return redirect(url_for('dashboard_page'))
		
		return render_template('register.html', form=form)
	
	except Exception as e:
		return(str(e))

if __name__ == "__main__":
    app.run()

