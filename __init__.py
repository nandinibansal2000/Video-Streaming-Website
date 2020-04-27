# import pymysql
# pymysql.install_as_MySQLdb()
# import MySQLdb
from wtforms import Form, BooleanField , TextField, PasswordField, validators
from flask import Flask,render_template,flash,request,url_for,redirect,session

from passlib.hash import sha256_crypt
# from MySQLdb import escape_string as thwart
import gc
import user
import mysql.connector
import productionHouse
import pygal
import Movies
import Artist
import merchandise

app = Flask(__name__)

mydb = mysql.connector.connect(
	  host="localhost",
	  user="user",
	  passwd="password",
	  database="newdb2"
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

@app.route('/likeMerch/<MerchID>')
def likeMerch(MerchID):
	MerchID = int(MerchID)
	mycursor = mydb.cursor()
	merchandise.likeMerch(mycursor, MerchID)
	return "You have liked a merch.\n THANK YOU!!!"

@app.route('/dislikeMerch/<MerchID>')
def dislikeMerch(MerchID):
	MerchID = int(MerchID)
	mycursor = mydb.cursor()
	merchandise.dislikeMerch(mycursor, MerchID)
	return "You have disliked a merch.\n THANK YOU!!!"



@app.route("/upload/<PID>", methods=['POST'])
def upload(PID):
	PID = int(PID)
	if request.method == "POST":
		if( "upload" in request.form):
			name = request.form["name"]
			duration = request.form["duration"]
			genre = request.form["genre"]
			IMDB = request.form["imdb"]
			prequelID = request.form["PrequelID"]
			print(PID, name, IMDB, duration, genre, prequelID)
			if(prequelID==""):
				productionHouse.uploadMovie(mydb, PID, name, IMDB, duration, genre)
			else:
				productionHouse.uploadMovie(mydb, PID, name, IMDB, duration, genre, int(prequelID))
		elif ("upcoming" in request.form):
			name = request.form["name"]
			duration = request.form["duration"]
			genre = request.form["genre"]
			release = request.form["release"]
			print(PID, name, release, duration, genre)
			productionHouse.uploadUpcomingMovie(mydb, PID, name, release, duration, genre)
				
	return redirect(url_for('productionHousePage', PID=PID))
@app.route("/payment/<UID>", methods=['POST'])
def payment(UID):
	UID = int(UID)
	if request.method == "POST":
		if( "user" in request.form):
			user.makePaymentForUser(mydb, UID)
		if( "family" in request.form):
			user.makePaymentForUser(mydb, UID)
		#Moving forward code
	print("Moving Forward...")
	return redirect(url_for('userPage', UID=UID))

@app.route("/Rating/<UID>/<MovieID>", methods=['POST'])
def Rating(UID, MovieID):
	if(not user.checkPayment(mydb, UID)):
		return "<h1>Please make payment to watch the movie</h1>"
	if request.method == "POST":
		if( "rate" in request.form):
			rating = request.form["rating"]
			user.watchNewMovie(mydb, int(UID), int(MovieID), int(rating))
	return redirect(url_for('userPage', UID=int(UID)))

@app.route('/user/<int:UID>', methods=['GET', 'POST'])
def userPage(UID):
	name1 = user.getName(mydb, UID)[0][0]
	LoginID1 = user.getLoginID(mydb, UID)[0][0]
	Hours1 = user.getHoursWatched(mydb, UID)[0][0]
	url1 = "/payment/"+str(UID)
	img_addr1 = url_for('static', filename='images/merch.jpeg')
	arr = merchandise.getMerchandiseFromUser(mydb, UID)
	merch_embed1 = merchandise.getMerchandiseHTML(arr, img_addr1)
	img_addr = url_for('static', filename='images/poster.jpg')
	suggested = Movies.getSuggestionsEmbed(mydb, UID, img_addr)
	if request.method == 'GET':		
		return render_template("user.html", name=name1, LoginID=LoginID1, hours=Hours1, url=url1, merch_embed=merch_embed1, suggested_embed=suggested)
	elif request.method == 'POST':
		try:
			movie_name = request.form["search_movie"]
			print(movie_name)
			search_movie_result = user.searchMovie(mydb, movie_name, UID)
			return render_template("user.html", name=name1, LoginID=LoginID1, hours=Hours1, search_movie_result_embed=search_movie_result, url=url1, merch_embed=merch_embed1, suggested_embed=suggested)
		except:
			return render_template("user.html", name=name1, LoginID=LoginID1, hours=Hours1, url=url1, merch_embed=merch_embed1, suggested_embed=suggested)


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
	Hours1 = user.getHoursWatched(mydb, UID)[0][0]
	url1 = "/Rating/"+str(UID)+"/"+str(MovieID)
	img_addr1 = url_for('static', filename='images/merch.jpeg')
	arr = merchandise.getMerchandiseFromMovie(mydb, MovieID)
	merch_embed1 = merchandise.getMerchandiseHTML(arr, img_addr1)
	prequel1 = Movies.getPrequelSequel(mydb, UID, MovieID)
	print(prequel1)
	return render_template("movie.html", hours=Hours1, name=name1, genre=genre1, imdb=imdb1, prating=prating1, phouse=phouse1, duration=duration1, artist_embed=artists, url=url1, merch_embed=merch_embed1, prequel=prequel1)

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
	
	if(movies==""):
		line_chart = pygal.HorizontalBar()
		line_chart.title = "Number of users corresponding to Age"
		graph2 = line_chart.render_data_uri()

	else:
		graph2 = productionHouse.graph2(mycursor, PID)
		
	gvr = productionHouse.genreVSrating(mycursor, PID)
	url = "/upload/"+str(PID)
	img_addr1 = url_for('static', filename='images/merch.jpeg')
	arr = merchandise.getMerchandiseFromProductionHouse(mydb, PID)
	merch_embed1 = merchandise.getMerchandiseHTML(arr, img_addr1)
	Merch_info_embed1 = productionHouse.getMerchDetails(mydb, PID)
	rank1 = productionHouse.getRank(mydb, PID)
	return render_template("productionHouse.html", name=name1, Movies_embed=movies, Upcoming_Movies_embed=upcoming_movies, chart1=graph1, chart2=graph2, genreVSrating=gvr, url_upload=url, Merch_info_embed=Merch_info_embed1, rank=rank1)

@app.route('/artist/<int:AID>')
def artistPage(AID):
	name1 = Artist.artist_info(mydb, AID)[0]
	age1 = Artist.artist_info(mydb, AID)[1]
	genre = Artist.top_genre(mydb, AID)
	#genre = "Action"
	uRating = Artist.artist_rating(mydb, AID)
	imdb1 = Artist.artist_official_rating(mydb, AID)
	table1 = Artist.get_specific_movie(mydb, AID)
	img_addr1 = url_for('static', filename='images/merch.jpeg')
	arr = merchandise.getMerchandiseFromArtist(mydb, AID)
	merch_embed1 = merchandise.getMerchandiseHTML(arr, img_addr1)
	return render_template("artists.html", name=name1, age=age1, top_genre=genre, user_rating=uRating, imdb=imdb1, table=table1, merch_embed=merch_embed1)

def user_signup(username,age,fam):
	print("fjnckf")
	mycursor = mydb.cursor()
	sql = "SELECT MAX(UID) FROM Users "
	mycursor.execute(sql)
	c=mycursor.fetchall()
	print(fam)
	if(str(fam)=="NO"):
		sql = "SELECT MAX(FamilyID) FROM Family "
		mycursor.execute(sql)
		f=mycursor.fetchall()

		print(f,"fffffffffffff")
		fam = int(f[0][0])+1
		sql="insert into Family values('%s','%s')"%(fam,"false")
		mycursor.execute(sql)


	# print(c)
	# c.execute("SELECT MAX(UID) FROM Users ")+1
	# m= c.fetchone() 
	ID=int(c[0][0])+1
	print(ID,"wfjcklwcd")
	print("fnvjfdv")
	print(fam)
	sql = "insert into Users values('%s','%s','%s','%s','%s','%s','%s','%s')"%(ID,username,fam,username,age,'0',0,"none")
	# sql="INSERT INTO Users(UID,LoginID,Name,Age,IndividualPayment,AvgTime,SubscriptionType) VALUES(%s,%s,%s,%s,%s,%s,%s)",(ID,username,username,age,'0',0,"none")
	mycursor.execute(sql)
	

	session['logged_in'] = True
	session['username'] = username

def artist_signup(username,age):
	mycursor = mydb.cursor()
	sql = "SELECT MAX(ArtistID) FROM Artists "
	mycursor.execute(sql)
	c=mycursor.fetchall()
	# c.execute("SELECT MAX(UID) FROM Users ")+1
	# m= c.fetchone() 
	ID=int(c[0][0])+1
	print(ID)
	sql = "insert into Artists values('%s','%s','%s')"%(ID,username,age)

	# sql="INSERT INTO Artists(ArtistID,Name,Age) VALUES(%s,%s,%s)",(ID,username,age)
	mycursor.execute(sql)
	print("lllalallalala")

	

	session['logged_in'] = True
	session['username'] = username

def production_signup(username):
	mycursor = mydb.cursor()
	sql = "SELECT MAX(PHID) FROM Production_Houses "
	mycursor.execute(sql)
	c=mycursor.fetchall()
	ID=int(c[0][0])+1
	print(ID)
	sql = "insert into Production_Houses values('%s','%s','%s','%s')"%(ID,username,"0",username)
	# sql="INSERT INTO Production_Houses(PHID,LoginID,Overall_Rating,Name) VALUES(%s,%s,%s)",(ID,username,0,username)
	print(sql)
	mycursor.execute(sql)
	

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
def ARTISTID(mydb, input_LogonID):
    mycursor = mydb.cursor()
    sql = "SELECT ArtistID FROM Artists WHERE Name='%s'"%(input_LogonID)
    mycursor.execute(sql)
    print(mycursor.fetchall()[0][0],"kkkk")
    return 301

@app.route('/', methods = ['GET','POST']) 
def get_data():
	try:
		# form = RegisterationForm(request.form)
		print("aaaaa")
		if request.method == "POST":
			if( "signup" in request.form):
				print("kkkkkkkllllllllll")
				username  = request.form["uname"]
				# email = form.email.data
				#	password = sha256_crypt.encrypt((str(request.form["psw"])))
				# print("lol")
				# password = sha256_crypt.encrypt((str(request.form["psw"])))
				password = request.form["psw"]
				print(password,"xxxxxxxxxxxxxxxxxxxx")
				designation= request.form["designation"]
				age  = request.form["age"]
				fam = request.form["fam"]
	
				# print("kljh")
				# print(username)
				# print(type(username))
				print("cccccccccccccccc")
				mycursor = mydb.cursor()
				sql = "SELECT * FROM Passwords WHERE LoginID = '%s'"%(username)
				mycursor.execute(sql)
				x=mycursor.fetchall()
				
				if len(x) > 0:

					flash("That username is already taken, please choose another")
					return render_template('main.html')

				else:
					print("pppp")
					# sql ="INSERT INTO Passwords VALUES (%s, %s,%s)",(username,password,designation)
					sql = "insert into Passwords values('%s', '%s', '%s')"%(username,password,designation)
					print(sql,"skcldsc")
					mycursor.execute(sql)
				
				
					print("llll")
					
					flash("Thanks for registering!")
					
					if(designation=="User"):

						user_signup(username,age,fam)
						uid1 = user.getUID(mydb, username)
						return redirect(url_for('userPage', UID=uid1))
					elif(designation=="Artist"):

						artist_signup(username,age)
						uid1 = ARTISTID(mydb, username)
						print(uid1)
						return redirect(url_for('artistPage', AID=uid1))

					elif(designation=="Production"):

						production_signup(username)
						uid1 = productionHouse.PhID(mydb, username)
						return redirect(url_for('productionHousePage', PID=uid1))
			else:
				print("zzzzzzzzzzzzzzzz")
				username  = request.form["name"]
				# email = form.email.data
				#	password = sha256_crypt.encrypt((str(request.form["psw"])))
				print("lol")
				# password = sha256_crypt.encrypt((str(request.form["pass"])))
				# print(password,"yyyyyyyyyyyyyy")

				password = request.form["pass"]
				# password = sha256_crypt.encrypt(password)
				# print("poi")
				# print(username,password)
				print("yayy")
				mycursor = mydb.cursor()
				sql = "SELECT Designation FROM Passwords WHERE LoginID = '%s' AND passwd='%s'"% (username,password)
				mycursor.execute(sql)

				x=mycursor.fetchall()
				
				print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"+str(x))
				if(len(x)>0):
					x=x[0][0]
					if(x=="User"):
						uid1 = user.getUID(mydb, username)
						return redirect(url_for('userPage', UID=uid1))
					elif(x=="Artist"):
						uid1 = ARTISTID(mydb, username)
						print(uid1)
						return redirect(url_for('artistPage', AID=uid1))
					elif(x=="Production"):
						uid1 = productionHouse.PhID(mydb, username)
						return redirect(url_for('productionHousePage', PID=uid1))
					else:
						# print("oooof")
						flash("Wrong Credentials")
						return render_template("main.html")


		return render_template("main.html")
	except Exception as e:
		return (str(e))



if __name__ == '__main__':
	# app.secret_key = 'super secret key'
	# app.config['SESSION_TYPE'] = 'filesystem'

	# session.init_app(app)


	import mysql.connector
	# mydb = mysql.connector.connect(
	# host="localhost",
	# user="new",
	# passwd="passwd",
	# database="mydb"
	# )
	app.secret_key = 'SECRET KEY'
	app.run(debug=True) 
