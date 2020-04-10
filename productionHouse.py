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


def getCursor(mydb):
	#get cursor from database
	#Call this function first

	return mydb.cursor()


# #SQL Queries
def getMovies(mycursor, productionHouse):
	#Get movies corresponding to production house

	productionHouseName = (productionHouse, )
	sql_query = ("SELECT MOVIE_ID, GENRE FROM MOVIES WHERE P_HouseID IN (SELECT PHID FROM PRODUCTION_HOUSES WHERE NAME = (%s))")
	mycursor.execute(sql_query, productionHouseName)
	arr = mycursor.fetchall()
	return arr

def getName(mycursor, PID):
	sql = "SELECT Name from Production_Houses where PHID='%d'"%(PID)
	mycursor.execute(sql)
	return mycursor.fetchall()[0][0]

def getMovieViewersFromMovie(mycursor, movie):
	#Get the list of people who watched the given movie

	movieID = (movie, )
	sql_query = ("SELECT UID FROM WATCH_LIST WHERE MOVIEID = %s")
	mycursor.execute(sql_query, movieID)		
	arr = mycursor.fetchall()
	return arr

def getMovieViewersFromMovieList(mycursor, movieList):
	#get all viewers of a publisher from their list of movies

	viewerSet = set()
	for i in movieList:
		arr2 = getMovieViewersFromMovie(mycursor, i[0])
		for j in arr2:
			viewerSet.add(j[0])
	return viewerSet


def getUpcomingMovies(mycursor, productionHouse):
	#get upcoming movies corresponding to production house

	productionHouseName = (productionHouse, )
	sql_query = ("SELECT EMID FROM UPCOMING_MOVIES WHERE Production_HouseID IN (SELECT PHID FROM PRODUCTION_HOUSES WHERE NAME = (%s))")
	mycursor.execute(sql_query, productionHouseName)
	arr = mycursor.fetchall()
	return arr

def uploadMovie(mycursor, productionHouseID, name, IMDB, duration, genre):
	#upload movie

	sql_query = ("INSERT INTO MOVIES (P_HOUSEID, MOVIE_NAME, IMDB, DURATION, GENRE) VALUES (%s, %s, %s, %s, %s)")
	entry = (productionHouseID, name, IMDB, duration, genre)
	mycursor.execute(sql_query, entry)
	#Uncomment when you want to make changes permanent
	#mydb.commit()

#Wont work right now due to foreign key constraint in Starcast
def removeMovie(mycursor, movie):
	#remove movie from name

	sql_query = ("DELETE FROM MOVIES WHERE MOVIE_NAME = %s")
	movieName = (movie, )
	mycursor.execute(sql_query, movieName)
	# mycursor.execute("SELECT * FROM MOVIES")
	# print(mycursor.fetchall())

# #Python Queries

def getMovieRatingFromID(mycursor, movie):
	#Get rating according to movie

	movieID = (movie, )
	sql_query = ("SELECT AVG(RATING) FROM WATCH_LIST WHERE MOVIEID = %s")
	mycursor.execute(sql_query, movieID)
	avg = mycursor.fetchone()
	avg = avg[0]
	return avg


def groupUsersByAge (mycursor, userlist):
	#get number of users belonging to a particular age

	userTuple = tuple(userlist)
	sql_query = ("SELECT AGE, COUNT(UID) FROM USERS WHERE UID IN {} GROUP BY AGE").format(userTuple)
	mycursor.execute(sql_query)
	arr = mycursor.fetchall()
	return arr

def groupMoviesByGenre (mycursor, movieList):
	#get rating for each genre

	ratingDict = {}
	for i in movieList:
		val = getMovieRatingFromID(mycursor, i[0])
		if(val==None):
			val = 0
		if(i[1] in ratingDict):
			ratingDict[i[1]].append(val)
		else:
			ratingDict[i[1]] = [val]
	for i in ratingDict.keys():
		ratingDict[i] = sum(ratingDict[i])/len(ratingDict[i])
	return ratingDict



def getProductionHouseRating (mycursor, movieList):
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

######################################################################################

def graphGenreVSMovies(inpDict):
	line_chart = pygal.HorizontalBar()
	line_chart.title = "Ratings corresponding to each Genre"
	for i in inpDict:
		line_chart.add(i, inpDict[i])
	line_chart.render_in_browser()

def graphUsersVSAge(inpSet):
	line_chart = pygal.HorizontalBar()
	line_chart.title = "Number of users corresponding to Age"
	for i in inpSet:
		line_chart.add(str(i[0]), i[1])
	line_chart.render_in_browser()

######################################################################################

# cursor = getCursor(mydb)
# arr = getMovies(cursor, "Sony Pictures Motion Picture Group")
# arr2 = groupMoviesByGenre(cursor, arr)
# graphGenreVSMovies(arr2)

# arr3 = getMovieViewersFromMovieList(cursor, arr)
# arr4 = groupUsersByAge(cursor, arr3)
# graphUsersVSAge(arr4)
