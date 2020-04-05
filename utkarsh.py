""" TODO:
	Update Family table to align it to Users
"""



def getWatchHistoryNames(mydb, input_UID):
	# Optimisation: Make index on UID in Watch_List (check if useful)
	mycursor = mydb.cursor()
	sql = "select Movie_Name from Movies where Movie_id in (select MovieID from Watch_List where UID='%d')"%(input_UID)
	mycursor.execute(sql)
	return  mycursor.fetchall()

def watchNewMovie(mydb, input_UID, input_MovieID, input_Rating):
	mycursor = mydb.cursor()
	sql = "insert into Watch_List values('%d', '%d', '%d')"%(input_UID, input_MovieID, input_Rating)
	mycursor.execute(sql)
	mydb.commit()

def getName(mydb, input_UID):
	mycursor = mydb.cursor()
	sql = "SELECT LoginID FROM Users WHERE UID='%d'"%(input_UID)
	mycursor.execute(sql)
	return  mycursor.fetchall()

def getHoursWatched(mydb, input_UID):
	mycursor = mydb.cursor()
	refreshAverageTime()
	sql = "SELECT AvgTime FROM Users WHERE UID='%d'"%(input_UID)
	mycursor.execute(sql)
	return  mycursor.fetchall()


def refreshAverageTime():
	# Calculate average time from WatchHistory and Update AvgTime in Users
	pass

def searchMovie(mydb, movieName):
	mycursor = mydb.cursor()
	movieName = '%'+movieName+'%'
	sql = "SELECT Movie_id FROM Movies WHERE Movie_Name LIKE '%s'"%(movieName)
	mycursor.execute(sql)
	return  mycursor.fetchall()

def getSuggestions(mydb):
	pass

def makePaymentForUser(mydb, input_UID):
	pass

def makePaymentForFamily(mydb, input_UID):
	pass

def func(mydb):
	mycursor = mydb.cursor()
	sql = ""
	mycursor.execute(sql)

def func(mydb):
	mycursor = mydb.cursor()
	sql = ""
	mycursor.execute(sql)


def main(input_username):
	pass




if __name__ == '__main__':
	main("rauhv502")