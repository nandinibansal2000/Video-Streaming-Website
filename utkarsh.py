""" TODO:
	Update Family table to align it to Users
"""

import mysql.connector
from passlib.hash import sha256_crypt

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
	sql = "SELECT Name FROM Users WHERE UID='%d'"%(input_UID)
	mycursor.execute(sql)
	return  mycursor.fetchall()

def getLoginID(mydb, input_UID):
	mycursor = mydb.cursor()
	sql = "SELECT LoginID FROM Users WHERE UID='%d'"%(input_UID)
	mycursor.execute(sql)
	return  mycursor.fetchall()

def getUID(mydb, input_LogonID):
	mycursor = mydb.cursor()
	sql = "SELECT UID FROM Users WHERE LoginID='%s'"%(input_LogonID)
	mycursor.execute(sql)
	return  mycursor.fetchall()[0][0]

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







def encryptFunc(text):
	return text

def CreatePasswords(mydb):
	# Optimisation: Make index on UID in Watch_List (check if useful)
	mycursor = mydb.cursor()
	sql = "SELECT * FROM Passwords"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		LoginID1 = x[0]
		Password1 = encryptFunc(LoginID1)
		sql2 = "UPDATE Passwords SET Passwd='%s' WHERE LoginID = '%s'"%(Password1, LoginID1)
		mycursor.execute(sql2)
		mydb.commit()


	sql = "SELECT * FROM Artists"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		LoginID1 = x[1]
		Password1 = encryptFunc(LoginID1)
		sql2 = "UPDATE Artists SET Passwd='%s' WHERE Name = '%s'"%(Password1, LoginID1)
		mycursor.execute(sql2)
		mydb.commit()

	sql = "SELECT * FROM Production_Houses"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		LoginID1 = x[1]
		Password1 = encryptFunc(LoginID1)
		sql2 = "UPDATE Production_Houses SET Passwd='%s' WHERE LoginID = '%s'"%(Password1, LoginID1)
		mycursor.execute(sql2)
		mydb.commit()

	sql = "SELECT * FROM Production_Houses"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		print(x)

def updateFamilyTable(mydb):
	mycursor = mydb.cursor()
	sql = "SELECT * FROM Family"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		f = int(x[0])
		for i in range(1,5):
			u = x[i]
			sql = "UPDATE Users SET FamilyID='%d' WHERE LoginID='%s'"%(f, u)
			mycursor.execute(sql)
			mydb.commit()

def PasswordsCorrection(mydb):
	mycursor = mydb.cursor()

	# # DROP FORIEGN KEY CONSTRAINS
	# sql = "ALTER TABLE Passwords MODIFY COLUMN Passwd varchar(150)"
	# mycursor.execute(sql)
	# mydb.commit()
	# # ADD FORIEGN KEY CONSTRAINS

	# sql = "ALTER TABLE Passwords MODIFY COLUMN LoginID varchar(150)"
	# mycursor.execute(sql)
	# mydb.commit()


	# sql = "ALTER TABLE Passwords ADD Designation varchar(30)"
	# mycursor.execute(sql)
	# mydb.commit()

	# sql = "UPDATE Passwords SET Designation='User'"
	# mycursor.execute(sql)
	# mydb.commit()

	sql = "SELECT * FROM Artists"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		sql = "insert into Passwords values('%s', 'TBD', 'Artist')"%(x[1])
		mycursor.execute(sql)
		mydb.commit()

	sql = "SELECT * FROM Production_Houses"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		sql = "insert into Passwords values('%s', 'TBD', 'ProductionHouse')"%(x[1])
		mycursor.execute(sql)
		mydb.commit()

	sql = "SELECT * FROM Passwords"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		l = x[0]
		sql = "UPDATE Passwords SET Passwd='%s' WHERE LoginID='%s'"%(sha256_crypt.encrypt(l), l)
		mycursor.execute(sql)
		mydb.commit()

if __name__ == '__main__':


	mydb = mysql.connector.connect(
	  host="localhost",
	  user="user",
	  passwd="password",
	  database="aniket3"
	)

	PasswordsCorrection(mydb)
