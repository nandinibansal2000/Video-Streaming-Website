#Anshul Mendiratta
#Production House

#graphs and mydb as argument

import mysql.connector
import pygal


mydb = mysql.connector.connect(

	host="localhost",
	user="Drigil",
	passwd="Anshul12",
	database = "dbmsproject",
	auth_plugin="mysql_native_password"

)

if(mydb.is_connected()):
	print("Successfully Connected")


def getCursor(mydb):
	#get cursor from database
	#Call this function first

	return mydb.cursor()

def getMovieIDFromMovieName(mycursor, movie):
	#get movie ID from movie name

	movieName = (movie, )
	sql_query = "SELECT	MOVIE_ID FROM MOVIES WHERE MOVIE_NAME = %s"
	mycursor.execute(sql_query, movieName)
	result = mycursor.fetchone()
	return result[0]	


def getMerchandiseFromMovie(mycursor, movie):
	#Get movie merchandise from movie ID

	movieName = (movie, )
	sql_query = ("SELECT MERCHID, MERCHNAME FROM MERCHANDISE WHERE MOVIEID = %s")
	mycursor.execute(sql_query, movieName)
	arr = mycursor.fetchall()
	return arr

def getMoviesFromArtist(mycursor, artist):
	#get movieID from artistID

	artistID = (artist, )
	sql_query = ("SELECT MOVIEID FROM STARCAST WHERE ARTISTID = %s")
	mycursor.execute(sql_query, artistID)
	arr = mycursor.fetchall()
	return arr


def getMerchandiseFromArtist(mycursor, artist):
	#get merchandise from artist ID

	arr = getMoviesFromArtist(mycursor, artist)
	merch_arr = []
	for i in arr:
		merch_arr.extend(getMerchandiseFromMovie(mycursor, i[0]))
	return merch_arr


def getMoviesFromProductionHouse(mycursor, productionHouse):
	#Get movies corresponding to production house ID

	productionHouseName = (productionHouse, )
	sql_query = ("SELECT MOVIE_ID, GENRE FROM MOVIES WHERE P_HouseID = %s")
	mycursor.execute(sql_query, productionHouseName)
	arr = mycursor.fetchall()
	return arr

def getMerchandiseFromProductionHouse(mycursor, productionHouse):
	#get merchandise from production house

	arr = getMoviesFromProductionHouse(mycursor, productionHouse)
	merch_arr = []
	for i in arr:
		merch_arr.extend(getMerchandiseFromMovie(mycursor, i[0]))
	return merch_arr


def getMoviesFromUser(mycursor, user):
	#Get the list of movies watced by userID

	userID = (user, )
	sql_query = ("SELECT MOVIEID FROM WATCH_LIST WHERE UID = %s")
	mycursor.execute(sql_query, userID)		
	arr = mycursor.fetchall()
	return arr


def getMerchandiseFromUser(mycursor, user):
	#get merchandise from user

	arr = getMoviesFromUser(mycursor, user)
	merch_arr = []
	for i in arr:
		merch_arr.extend(getMerchandiseFromMovie(mycursor, i[0]))
	return merch_arr

def likeMerch(mycursor, merch):
	#Like the merch of the given merchID
	
	merchID = (merch, )
	sql_query = ("SELECT LIKES FROM MERCHANDISE WHERE MERCHID = %s")
	mycursor.execute(sql_query, merchID)
	curr_likes = mycursor.fetchone()
	curr_likes = curr_likes[0]
	
	updated_likes = curr_likes + 1
	sql_query2 = ("UPDATE MERCHANDISE SET LIKES = %s WHERE MERCHID = %s")
	vals = (updated_likes, merch)
	mycursor.execute(sql_query2, vals)
	#Uncomment when you want to make changes permanent
	#mydb.commit()

def dislikeMerch(mycursor, merch):
	#Dislike the merch of the given merchID

	merchID = (merch, )
	sql_query = ("SELECT DISLIKES FROM MERCHANDISE WHERE MERCHID = %s")
	mycursor.execute(sql_query, merchID)
	curr_dislikes = mycursor.fetchone()
	curr_dislikes = curr_dislikes[0]
	
	updated_dislikes = curr_dislikes + 1
	sql_query2 = ("UPDATE MERCHANDISE SET DISLIKES = %s WHERE MERCHID = %s")
	vals = (updated_dislikes, merch)
	mycursor.execute(sql_query2, vals)


cursor = getCursor(mydb)



# print(getMovieIDFromMovieName(cursor, "American Me"))
# print(getMerchandiseFromMovie(cursor, 1))
#print(getMoviesFromArtist(cursor, 1))
#arr = getMerchandiseFromUser(cursor, 5)

