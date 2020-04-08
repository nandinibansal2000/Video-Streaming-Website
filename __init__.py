# import pymysql
# pymysql.install_as_MySQLdb()
import MySQLdb
from wtforms import Form, BooleanField , TextField, PasswordField, validators
from flask import Flask,render_template,flash,request,url_for,redirect,session
from dbconnect import connection
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
import utkarsh
import mysql.connector
from passlib.hash import sha256_crypt


app = Flask(__name__)

mydb = mysql.connector.connect(
	  host="localhost",
	  user="user",
	  passwd="password",
	  database="myDB"
	)

@app.route('/')
def home():
    return render_template("main.html")

@app.route('/Dashboard')
def Dashboard():
    return render_template("Dashboard.html")
@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/user/<int:UID>')
def userPage(UID):
	
	name1 = utkarsh.getName(mydb, UID)[0][0]
	LoginID1 = utkarsh.getLoginID(mydb, UID)[0][0]
	Hours1 = utkarsh.getHoursWatched(mydb, UID)[0][0]
	return render_template("user.html", name=name1, LoginID=LoginID1, hours=Hours1)

@app.route('/movie/<int:UID>/<int:MovieID>')
def moviePage(UID, MovieID):
	
	Hours1 = utkarsh.getHoursWatched(mydb, UID)[0][0]
	return render_template("movie.html", hours=Hours1)


# @app.route('/login/', methods = ['GET','POST'])
# def login_page():
#     return render_template("login.html")

# class RegisterationForm(Form):
# 	username = TextField('Username', [validators.Length(min=4, max=20)])
# 	# email = TextField('Email Address', [validators.Length(min=6, max=50)])
# 	password = PasswordField('New Password', [validators.Required(),validators.EqualTo('confirm', message='Passwords must match')])
# 	confirm = PasswordField('Repeat Password')
# 	# accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])



@app.route('/', methods = ['GET','POST']) 
def get_data():
	try:
		# form = RegisterationForm(request.form)
		print("aaaaa")
		if request.method == "POST":
			if( "signup" in request.form):
				username  = request.form["uname"]
				# email = form.email.data
				#	password = sha256_crypt.encrypt((str(request.form["psw"])))
				# print("lol")
				password = request.form["psw"]
				# print("kljh")
				# print(username)
				# print(type(username))
				c, conn = connection()
				# print("erjkh")
				x = c.execute("SELECT * FROM Passwords WHERE LoginID = '%s'"%
				          (username))
				# print("erkljkgt")
				# print(x)
				if int(x) > 0:

					flash("That username is already taken, please choose another")
					return render_template('register.html')

				else:
					# print("pppp")
					c.execute("INSERT INTO Passwords VALUES (%s, %s)",
					          (thwart(username),thwart(password)))
					# print("llll")
					conn.commit()
					flash("Thanks for registering!")
					c.close()
					conn.close()
					gc.collect()
					# print("yyyyyyyyyyyy")

					session['logged_in'] = True
					session['username'] = username
					print("llllllllll")
					return redirect(url_for('userPage', UID=uid1))
			else:
				username  = request.form["name"]
				# email = form.email.data
				#	password = sha256_crypt.encrypt((str(request.form["psw"])))
				# print("lol")
				password = request.form["pass"]
				# print("poi")
				# print(username,password)
				print("yayy")
				c, conn = connection()
				# print("erjkh")
				x = c.execute("SELECT * FROM Passwords WHERE LoginID = '%s' AND passwd='%s'"%
				          (username,password))
				# print(x)
				if(int(x)==1):
					uid1 = utkarsh.getUID(mydb, username)
					return redirect(url_for('userPage', UID=uid1))
				else:
					# print("oooof")
					flash("Wrong Credentials")
					return render_template("register.html")


		return render_template("register.html")
	except Exception as e:
		return (str(e))



if __name__ == '__main__':
	# app.secret_key = 'super secret key'
	# app.config['SESSION_TYPE'] = 'filesystem'

	# session.init_app(app)
	app.secret_key = 'SECRET KEY'
	app.run(debug=True) 