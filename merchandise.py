#Anshul Mendiratta
#Production House

#graphs and mydb as argument

import mysql.connector
import pygal


# mydb = mysql.connector.connect(

# 	host="localhost",
# 	user="Drigil",
# 	passwd="Anshul12",
# 	database = "dbmsproject",
# 	auth_plugin="mysql_native_password"

# )

# if(mydb.is_connected()):
# 	print("Successfully Connected")


# def getCursor(mydb):
# 	#get cursor from database
# 	#Call this function first

# 	return mydb.cursor()

def getMovieIDFromMovieName(mycursor, movie):
	#get movie ID from movie name

	movieName = (movie, )
	sql_query = "SELECT	MOVIE_ID FROM MOVIES WHERE MOVIE_NAME = %s"
	mycursor.execute(sql_query, movieName)
	result = mycursor.fetchone()
	return result[0]	


def getMerchandiseFromMovie(mydb, movie):
	#Get movie merchandise from movie ID
	mycursor = mydb.cursor()
	movieName = (movie, )
	sql_query = ("SELECT MERCHID, MERCHNAME, LINK FROM Merchandise WHERE MOVIEID = %s")
	mycursor.execute(sql_query, movieName)
	arr = mycursor.fetchall()
	return arr

def getMerchandiseHTML(arr, img_addr):
	if(len(arr)==0):
		return
	ans = """<div id="carouselExampleCaptions" class="carousel slide" data-ride="carousel">
		  <ol class="carousel-indicators">
			<li data-target="#carouselExampleCaptions" data-slide-to="0" class="active"></li>"""
	for i in range(1, len(arr)):
		ans += """<li data-target="#carouselExampleCaptions" data-slide-to="%d"></li>\n"""%(i)
	ans += """ </ol>
		  <div class="carousel-inner">
			<div class="carousel-item active">
			<a href = "%s">
			  <img src="%s" class="d-block w-100" alt="Merch"></a>
			  <div class="carousel-caption d-none d-md-block">
				<h5>%s</h5>
				<p><a href="%s">Like</a> | <a href="%s">Dislike</a></p>
			  </div>
			</div>"""%(arr[0][2], img_addr, arr[0][1], "/likeMerch/"+str(arr[0][0]), "/dislikeMerch/"+str(arr[0][0]))
	for i in range(1, len(arr)):
		ans += """<div class="carousel-item">
			 <a href = "%s">
			  <img src="%s" class="d-block w-100" alt="Merch"></a>
			  <div class="carousel-caption d-none d-md-block">
				<h5>%s</h5>
				<p><a href="%s">Like</a> | <a href="%s">Dislike</a></p>
			  </div>
			</div>"""%(arr[i][2], img_addr, arr[i][1], "/likeMerch/"+str(arr[0][0]), "/dislikeMerch/"+str(arr[0][0]))
	ans += """</div>
		  <a class="carousel-control-prev" href="#carouselExampleCaptions" role="button" data-slide="prev">
			<span class="carousel-control-prev-icon" aria-hidden="true"></span>
			<span class="sr-only">Previous</span>
		  </a>
		  <a class="carousel-control-next" href="#carouselExampleCaptions" role="button" data-slide="next">
			<span class="carousel-control-next-icon" aria-hidden="true"></span>
			<span class="sr-only">Next</span>
		  </a>
		</div>"""
	return ans

	"""<div id="carouselExampleCaptions" class="carousel slide" data-ride="carousel">
		  <ol class="carousel-indicators">
			<li data-target="#carouselExampleCaptions" data-slide-to="0" class="active"></li>
			<li data-target="#carouselExampleCaptions" data-slide-to="1"></li>
			<li data-target="#carouselExampleCaptions" data-slide-to="2"></li>
		  </ol>
		  <div class="carousel-inner">
			<div class="carousel-item active">
			  <img src="{{ url_for('static', filename='images/merch.jpeg') }}" class="d-block w-100" alt="...">
			  <div class="carousel-caption d-none d-md-block">
				<h5>Merch Name</h5>
			  </div>
			</div>
			<div class="carousel-item">
			  <img src="{{ url_for('static', filename='images/merch.jpeg') }}" class="d-block w-100" alt="...">
			  <div class="carousel-caption d-none d-md-block">
				<h5>Second slide label</h5>
				<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
			  </div>
			</div>
			<div class="carousel-item">
			  <img src="{{ url_for('static', filename='images/merch.jpeg') }}" class="d-block w-100" alt="...">
			  <div class="carousel-caption d-none d-md-block">
				<h5>Third slide label</h5>
				<p>Praesent commodo cursus magna, vel scelerisque nisl consectetur.</p>
			  </div>
			</div>
		  </div>
		  <a class="carousel-control-prev" href="#carouselExampleCaptions" role="button" data-slide="prev">
			<span class="carousel-control-prev-icon" aria-hidden="true"></span>
			<span class="sr-only">Previous</span>
		  </a>
		  <a class="carousel-control-next" href="#carouselExampleCaptions" role="button" data-slide="next">
			<span class="carousel-control-next-icon" aria-hidden="true"></span>
			<span class="sr-only">Next</span>
		  </a>
		</div>"""

def getMoviesFromArtist(mydb, artist):
	#get movieID from artistID
	mycursor = mydb.cursor()
	artistID = (artist, )
	sql_query = ("SELECT MOVIEID FROM Starcast WHERE ARTISTID = %s")
	mycursor.execute(sql_query, artistID)
	arr = mycursor.fetchall()
	return arr


def getMerchandiseFromArtist(mydb, artist):
	#get merchandise from artist ID
	mycursor = mydb.cursor()
	arr = getMoviesFromArtist(mydb, artist)
	merch_arr = []
	for i in arr:
		merch_arr.extend(getMerchandiseFromMovie(mydb, i[0]))
	return merch_arr


def getMoviesFromProductionHouse(mycursor, productionHouse):
	#Get movies corresponding to production house ID

	productionHouseName = (productionHouse, )
	sql_query = ("SELECT MOVIE_ID, GENRE FROM Movies WHERE P_HouseID = %s")
	mycursor.execute(sql_query, productionHouseName)
	arr = mycursor.fetchall()
	return arr

def getMerchandiseFromProductionHouse(mydb, productionHouse):
	#get merchandise from production house
	mycursor = mydb.cursor()
	arr = getMoviesFromProductionHouse(mycursor, productionHouse)
	merch_arr = []
	for i in arr:
		merch_arr.extend(getMerchandiseFromMovie(mydb, i[0]))
	return merch_arr


def getMoviesFromUser(mycursor, user):
	#Get the list of movies watced by userID

	userID = (user, )
	sql_query = ("SELECT MOVIEID FROM Watch_List WHERE UID = %s")
	mycursor.execute(sql_query, userID)		
	arr = mycursor.fetchall()
	return arr


def getMerchandiseFromUser(mydb, user):
	#get merchandise from user
	mycursor = mydb.cursor()
	arr = getMoviesFromUser(mycursor, user)
	merch_arr = []
	for i in arr:
		merch_arr.extend(getMerchandiseFromMovie(mydb, i[0]))
	return merch_arr

def likeMerch(mycursor, merch):
	#Like the merch of the given merchID
	
	merchID = (merch, )
	sql_query = ("SELECT LIKES FROM Merchandise WHERE MERCHID = %s")
	mycursor.execute(sql_query, merchID)
	curr_likes = mycursor.fetchone()
	curr_likes = curr_likes[0]
	
	updated_likes = curr_likes + 1
	sql_query2 = ("UPDATE Merchandise SET LIKES = %s WHERE MERCHID = %s")
	vals = (updated_likes, merch)
	mycursor.execute(sql_query2, vals)
	#Uncomment when you want to make changes permanent
	#mydb.commit()

def dislikeMerch(mycursor, merch):
	#Dislike the merch of the given merchID

	merchID = (merch, )
	sql_query = ("SELECT DISLIKES FROM Merchandise WHERE MERCHID = %s")
	mycursor.execute(sql_query, merchID)
	curr_dislikes = mycursor.fetchone()
	curr_dislikes = curr_dislikes[0]
	
	updated_dislikes = curr_dislikes + 1
	sql_query2 = ("UPDATE Merchandise SET DISLIKES = %s WHERE MERCHID = %s")
	vals = (updated_dislikes, merch)
	mycursor.execute(sql_query2, vals)
	
def getLikes(mycursor, merch):
	#Get number of likes for some merch

	merchID = (merch, )
	sql_query = ("SELECT LIKES FROM Merchandise WHERE MERCHID = %s")
	mycursor.execute(sql_query, merchID)
	curr_likes = mycursor.fetchone()
	curr_likes = curr_likes[0]
	return curr_likes

def getDislikes(mycursor, merch):
	#Get number of likes for some merch

	merchID = (merch, )
	sql_query = ("SELECT DISLIKES FROM Merchandise WHERE MERCHID = %s")
	mycursor.execute(sql_query, merchID)
	curr_dislikes = mycursor.fetchone()
	curr_dislikes = curr_dislikes[0]
	return curr_dislikes	



# cursor = getCursor(mydb)



# print(getMovieIDFromMovieName(cursor, "American Me"))
# print(getMerchandiseFromMovie(cursor, 1))
#print(getMoviesFromArtist(cursor, 1))
#arr = getMerchandiseFromUser(cursor, 5)

if __name__ == '__main__':
	import mysql.connector
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="user",
	  passwd="password",
	  database="newdb"
	)
	# img_addr1 = url_for('static', filename='images/merch.jpeg')
	arr = getMerchandiseFromArtist(mydb, 5)
	print("arr", arr[0])
	getMerchandiseHTML(arr, "")
