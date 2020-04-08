#Anshul Mendiratta
#Production House

import mysql.connector

mydb = mysql.connector.connect(

	host="localhost",
	user="Drigil",
	passwd="Anshul12",
	database = "dbmsproject",
	auth_plugin="mysql_native_password"

)

if(mydb.is_connected()):
	print("Successfully Connected")

mycursor = mydb.cursor()


# #SQL Queries
def getMovies(productionHouse):
	#Get movies corresponding to production house

	productionHouseName = (productionHouse, )
	sql_query = ("SELECT MOVIE_ID, GENRE FROM MOVIES WHERE P_HouseID IN (SELECT PHID FROM PRODUCTION_HOUSES WHERE NAME = (%s))")
	mycursor.execute(sql_query, productionHouseName)
	arr = mycursor.fetchall()
	return arr

def getMovieViewersFromMovie(movie):
	#Get the list of people who watched the given movie

	movieID = (movie, )
	sql_query = ("SELECT UID FROM WATCH_LIST WHERE MOVIEID = %s")
	mycursor.execute(sql_query, movieID)		
	arr = mycursor.fetchall()
	return arr

def getMovieViewersFromMovieList(movieList):
	#get all viewers of a publisher from their list of movies

	viewerSet = set()
	for i in movieList:
		arr2 = getMovieViewersFromMovie(i[0])
		for j in arr2:
			viewerSet.add(j[0])
	return viewerSet


def getUpcomingMovies(productionHouse):
	#get upcoming movies corresponding to production house

	productionHouseName = (productionHouse, )
	sql_query = ("SELECT EMID FROM UPCOMING_MOVIES WHERE Production_HouseID IN (SELECT PHID FROM PRODUCTION_HOUSES WHERE NAME = (%s))")
	mycursor.execute(sql_query, productionHouseName)
	arr = mycursor.fetchall()
	return arr

def uploadMovie(productionHouseID, name, IMDB, duration, genre):
	#upload movie

	sql_query = ("INSERT INTO MOVIES (P_HOUSEID, MOVIE_NAME, IMDB, DURATION, GENRE) VALUES (%s, %s, %s, %s, %s)")
	entry = (productionHouseID, name, IMDB, duration, genre)
	mycursor.execute(sql_query, entry)
	#Uncomment when you want to make changes permanent
	#mydb.commit()

#Wont work right now due to foreign key constraint in Starcast
def removeMovie(movie):
	#remove movie from name

	sql_query = ("DELETE FROM MOVIES WHERE MOVIE_NAME = %s")
	movieName = (movie, )
	mycursor.execute(sql_query, movieName)
	# mycursor.execute("SELECT * FROM MOVIES")
	# print(mycursor.fetchall())

# #Python Queries

def getMovieRatingFromID(movie):
	#Get rating according to movie

	movieID = (movie, )
	sql_query = ("SELECT AVG(RATING) FROM WATCH_LIST WHERE MOVIEID = %s")
	mycursor.execute(sql_query, movieID)
	avg = mycursor.fetchone()
	avg = avg[0]
	return avg


def groupUsersByAge (userlist):
	#get number of users belonging to a particular age

	userTuple = tuple(userlist)
	sql_query = ("SELECT AGE, COUNT(UID) FROM USERS WHERE UID IN {} GROUP BY AGE").format(userTuple)
	mycursor.execute(sql_query)
	arr = mycursor.fetchall()
	return arr

def groupMoviesByGenre (movieList):
	#get rating for each genre

	ratingDict = {}
	for i in movieList:
		val = getMovieRatingFromID(i[0])
		if(val==None):
			val = 0
		if(i[1] in ratingDict):
			ratingDict[i[1]].append(val)
		else:
			ratingDict[i[1]] = [val]
	for i in ratingDict.keys():
		ratingDict[i] = sum(ratingDict[i])/len(ratingDict[i])
	return ratingDict



def getProductionHouseRating (movieList):
	#get average rating of production house according to the list of movies provided

	ratingList = []
	for i in movieList:
		val = getMovieRatingFromID(i[0])
		if(val==None):
			val = 0
		ratingList.append(val)
	avg = sum(ratingList)/len(ratingList)
	return avg

######################################################################################	

# Using functions - 
# 1) First call getMovies to get movies corresponding to the production house
# 2) use this value for functions wherever movielist is needed
# 3) getMovieViewersFromMovieList gives list of users for that productionHouse, you can use this value for where userList is needed
