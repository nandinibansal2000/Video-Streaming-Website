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



def main(input_username):
	import mysql.connector

	mydb = mysql.connector.connect(
	  host="localhost",
	  user="user",
	  passwd="password",
	  database="myDB"
	)

	mycursor = mydb.cursor()

	sql = "SELECT * from Passwords WHERE LoginID='%s'"%(input_username)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	for x in myresult:
	  print(x)




if __name__ == '__main__':
	main("rauhv502")