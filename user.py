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

def getFamilyID(mydb, UID):
	mycursor = mydb.cursor()
	sql = "SELECT FamilyID FROM Users WHERE UID=%d"%(UID)
	mycursor.execute(sql)
	return  mycursor.fetchall()[0][0]

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
	refreshAverageTime(mydb, input_UID)
	sql = "SELECT HoursWatched FROM Users WHERE UID='%d'"%(input_UID)
	mycursor.execute(sql)
	return  mycursor.fetchall()


def refreshAverageTime(mydb, input_UID):
	mycursor = mydb.cursor()
	sql = "SELECT Movies.Duration FROM Watch_List LEFT JOIN Movies ON Watch_List.MovieID=Movies.Movie_id WHERE Watch_List.UID='%d'"%(input_UID)
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	total = 0
	for x in myresult:
		total += int(x[0])
	total = int(total/60)
	sql = "UPDATE Users SET HoursWatched=%d WHERE UID=%d"%(total, input_UID)
	mycursor.execute(sql)
	mydb.commit()

def searchMovie(mydb, movieName, input_UID):
	mycursor = mydb.cursor()
	movieName = '%'+movieName+'%'
	print("percent debug", movieName)
	sql = "SELECT Movie_id, Movie_Name FROM Movies WHERE Movie_Name LIKE '%s'"%(movieName)
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	print(len(myresult))
	ans = ""
	for x in myresult:
		ans += '<a href="/user/'+str(input_UID)+'/movie/'+str(x[0])+'">'+'<button type="button" class="btn btn-light">'+str(x[1])+'</button>'+'</a>'
	return ans



def makePaymentForUser(mydb, input_UID):
	mycursor = mydb.cursor()
	sql = "UPDATE Users SET IndividualPayment='true' WHERE UID = '%d'"%(input_UID)
	mycursor.execute(sql)
	mydb.commit()

def makePaymentForFamily(mydb, input_UID):
	mycursor = mydb.cursor()
	sql = "UPDATE Family SET Payment_Status='true' WHERE FamilyID IN (SELECT FamilyID FROM Users WHERE UID='%d')"%(input_UID)
	mycursor.execute(sql)
	mydb.commit()


def checkPayment(mydb, input_UID):
	input_UID = int(input_UID)
	mycursor = mydb.cursor()
	sql = "SELECT IndividualPayment, FamilyID FROM Users WHERE UID='%d'"%(input_UID)
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	if(myresult[0][0]=='true'):
		return True
	else:
		FamilyID1 = myresult[0][1]
	sql = "SELECT Payment_Status FROM Family WHERE FamilyID='%d'"%(FamilyID1)
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	if(myresult[0][0]=='true'):
		return True	
	return False





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

def makeGenreAtomic(mydb):
	mycursor = mydb.cursor()
	sql = "SELECT Movie_id, Genre from Movies"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		if(x[1].find("|")!=-1):
			old = x[1].split("|")
			n = len(old)
			m = randint(0, n-1)
			new = old[m]
			print(old, new)
			sql = "UPDATE Movies SET Genre='%s' WHERE Movie_id='%d'"%(new, int(x[0]))
			mycursor.execute(sql)
			mydb.commit()
def makeGenreAtomicInUpcomingMovies(mydb):
	mycursor = mydb.cursor()
	sql = "SELECT Movie_name, Genre from Upcoming_movies"
	mycursor.execute(sql)
	myresult =  mycursor.fetchall()
	for x in myresult:
		if(x[1].find("|")!=-1):
			old = x[1].split("|")
			n = len(old)
			m = randint(0, n-1)
			new = old[m]
			print(old, new)
			sql = 'UPDATE Upcoming_movies SET Genre="%s" WHERE Movie_name="%s"'%(new, x[0])
			mycursor.execute(sql)
			mydb.commit()
# if __name__ == '__main__':

# 	from random import randint
# 	# mydb = mysql.connector.connect(
# 	#   host="bsv8fhdqqljnoq8jt44x-mysql.services.clever-cloud.com",
# 	#   user="u7yvejx2zsljnqyn",
# 	#   passwd="ooJHBCTBUvEIywAnEc2x",
# 	#   database="bsv8fhdqqljnoq8jt44x"
# 	# )
# 	mydb = mysql.connector.connect(
# 	  host="localhost",
# 	  user="user",
# 	  passwd="password",
# 	  database="newdb2"
# 	)
# 	makeGenreAtomicInUpcomingMovies(mydb)
