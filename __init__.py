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
import productionHouse
import pygal
import Movies
import Artist

app = Flask(__name__)

# mydb = mysql.connector.connect(
# 	  host="localhost",
# 	  user="user",
# 	  passwd="passwd",
# 	  database="mydb"
# 	)
mydb = mysql.connector.connect(
	  host="localhost",
	  user="user",
	  passwd="password",
	  database="myDB2"
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

@app.route("/upload/", methods=['POST'])
def upload():

	if request.method == "POST":
		if( "upload" in request.form):
		
			#Moving forward code
			print("Moving Forward...")
	return render_template('main.html')
@app.route("/payment/<UID>", methods=['POST'])
def payment(UID):
	UID = int(UID)
	if request.method == "POST":
		if( "user" in request.form):
			utkarsh.makePaymentForUser(mydb, UID)
		if( "family" in request.form):
			utkarsh.makePaymentForUser(mydb, UID)
		#Moving forward code
	print("Moving Forward...")
	return redirect(url_for('userPage', UID=UID))

@app.route("/Rating/<UID>/<MovieID>", methods=['POST'])
def Rating(UID, MovieID):
	if(not utkarsh.checkPayment(mydb, UID)):
		return render_template("<h1>Please make payment to watch the movie</h1>")
	if request.method == "POST":
		if( "rate" in request.form):
			rating = request.form["rating"]
			utkarsh.watchNewMovie(mydb, int(UID), int(MovieID), int(rating))
	return redirect(url_for('userPage', UID=int(UID)))

@app.route('/user/<int:UID>', methods=['GET', 'POST'])
def userPage(UID):
	name1 = utkarsh.getName(mydb, UID)[0][0]
	LoginID1 = utkarsh.getLoginID(mydb, UID)[0][0]
	Hours1 = utkarsh.getHoursWatched(mydb, UID)[0][0]
	url1 = "/payment/"+str(UID)
	if request.method == 'GET':		
		return render_template("user.html", name=name1, LoginID=LoginID1, hours=Hours1, url=url1)
	elif request.method == 'POST':
		try:
			movie_name = request.form["search_movie"]
			print(movie_name)
			search_movie_result = utkarsh.searchMovie(mydb, movie_name, UID)
			return render_template("user.html", name=name1, LoginID=LoginID1, hours=Hours1, search_movie_result_embed=search_movie_result, url=url1)
		except:
			return render_template("user.html", name=name1, LoginID=LoginID1, hours=Hours1, url=url1)


@app.route('/user/<int:UID>/movie/<int:MovieID>')
def moviePage(UID, MovieID):
	name1 = Movies.getMovieName(mydb, MovieID)
	genre1 = Movies.getGenre(mydb, MovieID)
	imdb1 = Movies.getIMDB_Rating(mydb, MovieID)
	prating1 = Movies.getBiasedRating(mydb, UID, MovieID)
	duration1 = Movies.getDuration(mydb, MovieID)
	img_addr = url_for('static', filename='images/actor.jpg')
	artists = Movies.getArtists(mydb, MovieID, img_addr)
	phouse1 = Movies.getProductionHouseName(mydb, MovieID)
	Hours1 = utkarsh.getHoursWatched(mydb, UID)[0][0]
	url1 = "/Rating/"+str(UID)+"/"+str(MovieID)
	return render_template("movie.html", hours=Hours1, name=name1, genre=genre1, imdb=imdb1, prating=prating1, phouse=phouse1, duration=duration1, artist_embed=artists, url=url1)

@app.route('/movie/<int:MovieID>')
def movieInfoPage(MovieID):
	name1 = Movies.getMovieName(mydb, MovieID)
	genre1 = Movies.getGenre(mydb, MovieID)
	imdb1 = Movies.getIMDB_Rating(mydb, MovieID)
	duration1 = Movies.getDuration(mydb, MovieID)
	img_addr = url_for('static', filename='images/actor.jpg')
	artists = Movies.getArtists(mydb, MovieID, img_addr)
	phouse1 = Movies.getProductionHouseName(mydb, MovieID)

	return render_template("movie_info.html", name=name1, genre=genre1, imdb=imdb1, phouse=phouse1, duration=duration1, artist_embed=artists)


@app.route('/pHouse/<int:PID>')
def productionHousePage(PID):
	mycursor = mydb.cursor()
	name1 = productionHouse.getName(mycursor, PID)
	movies = productionHouse.getMovies(mycursor, name1)
	upcoming_movies = productionHouse.getUpcomingMovies(mycursor, PID)
	graph1 = productionHouse.graph1(mycursor, PID)
	graph2 = productionHouse.graph2(mycursor, PID)
	gvr = productionHouse.genreVSrating(mycursor, PID)
	return render_template("productionHouse.html", name=name1, Movies_embed=movies, Upcoming_Movies_embed=upcoming_movies, chart1=graph1, chart2=graph2, genreVSrating=gvr)

@app.route('/artist/<int:AID>')
def artistPage(AID):
	name1 = Artist.artist_info(mydb, AID)[0]
	age1 = Artist.artist_info(mydb, AID)[1]
	genre = Artist.top_genre(mydb, AID)
	#genre = "Action"
	uRating = Artist.artist_rating(mydb, AID)
	imdb1 = Artist.artist_official_rating(mydb, AID)
	table1 = Artist.get_specific_movie(mydb, AID)
	return render_template("artists.html", name=name1, age=age1, top_genre=genre, user_rating=uRating, imdb=imdb1, table=table1)

def user_signup(c,conn,username,password,designation,age):
	c.execute("SELECT MAX(UID) FROM Users ")+1
	m= c.fetchone() 
	ID=int(m[0]+1)
	print(ID)
	c.execute("INSERT INTO Users(UID,LoginID,Name,Age,IndividualPayment,AvgTime,SubscriptionType) VALUES(%s,%s,%s,%s,%s,%s,%s)",(ID,username,username,age,'0',0,"none"))
	conn.commit()
	flash("Thanks for registering!")
	c.close()
	conn.close()
	gc.collect()
	

	session['logged_in'] = True
	session['username'] = username

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
				# password = request.form["psw"]
				designation= request.form["designation"]
				age  = request.form["age"]
	
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
					print("pppp")
					c.execute("INSERT INTO Passwords VALUES (%s, %s,%s)",
					          (thwart(username),thwart(password),thwart(designation)))
				
					# print("llll")
					
					flash("Thanks for registering!")
					
					if(designation=="User"):

						user_signup(c,conn,username,password,designation,age)
						uid1 = utkarsh.getUID(mydb, username)
						return redirect(url_for('userPage', UID=uid1))
			else:
				username  = request.form["name"]
				# email = form.email.data
				#	password = sha256_crypt.encrypt((str(request.form["psw"])))
				# print("lol")
				password = request.form["pass"]
				# password = sha256_crypt.encrypt(password)
				# print("poi")
				# print(username,password)
				print("yayy")
				c, conn = connection()
				# print("erjkh")
				x = c.execute("SELECT * FROM Passwords WHERE LoginID = '%s' AND passwd='%s'"%
				          (username,password))
				print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"+str(x))
				print(x)
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
