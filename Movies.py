import mysql.connector
from flask import url_for
def getSuggestion(mydb , UID) :
    mycursor = mydb.cursor()
    sql = "SELECT W.UID , count(*) FROM Watch_List W WHERE W.MovieID in (SELECT DISTINCT MovieID from Watch_List WHERE UID = '%d') GROUP BY W.UID HAVING count(*) > 0 ORDER BY count(*) DESC ;"%(UID)
    mycursor.execute(sql) # TODO : decide the threshold in above SQL command
    result = mycursor.fetchall()
    # print(result)
    MovieList = dict()
    for i in result :
        sql = "SELECT MovieID FROM Watch_List W WHERE W.UID = '%d' and MovieID not in (SELECT DISTINCT MovieID from Watch_List WHERE UID = '%d') ;"%(i[0] , UID)
        mycursor.execute(sql)
        Movies = mycursor.fetchall()
        for m in Movies :
            # print( type(m[0]) ,type(i[1]) )
            if(m[0] in MovieList) :
                MovieList[m[0]] += i[1]/( result[0][1] * (len(result)-1) )
            else :
                MovieList[m[0]] = i[1]/( result[0][1] * (len(result)-1) )
    # print(MovieList , list(MovieList.items()))
    return list(MovieList.items()) # return MovieID and Weighted_similarity (diff from biased rating)
def getBiasedRating(mydb , UID , MovieID) :
    mycursor = mydb.cursor()
    sql = "SELECT W.UID , W.Rating FROM Watch_List W WHERE W.MovieID = '%d' and UID != '%d' ;"%(MovieID , UID)
    mycursor.execute(sql)
    personList = mycursor.fetchall() # person who have watched the movie
    # print(personList)
    BiasedRating = 0
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(*) FROM Watch_List GROUP BY UID HAVING UID = '%d' ;"%(UID)
    mycursor.execute(sql)
    UID_num_movies = mycursor.fetchall()[0][0]  # number of movies watched by User UID

    for person in personList :
        mycursor = mydb.cursor()
        sql = "SELECT COUNT(W2.MovieID) FROM Watch_List W1 , Watch_List W2 WHERE W1.UID = '%d' and W2.UID = '%d' and W1.MovieID = W2.MovieID ;"%(UID , person[0])
        mycursor.execute(sql) # Count number of movies watched by both users;
        similarity = int(mycursor.fetchall()[0][0]) / UID_num_movies  # weighteg the similarity with Number of movies matched by total movies
        BiasedRating += similarity * float(person[1]) / len(personList) # calculating Weighted mean
    return BiasedRating
def getMovieName(mydb , MovieID) :
    mycursor = mydb.cursor()
    sql = "SELECT Movie_Name FROM Movies WHERE Movie_id = '%d';"%(MovieID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result # if something is buggy
def getProductionHouseID(mydb , MovieID) :
    mycursor = mydb.cursor()
    sql = "SELECT P_HouseID FROM Movies WHERE Movie_id = '%d';"%(MovieID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result # if something is buggy
def getProductionHouseName(mydb , MovieID) :
    pid = getProductionHouseID(mydb , MovieID)
    mycursor = mydb.cursor()
    sql = "SELECT Name FROM Production_Houses WHERE PHID='%d'"%(pid)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    return result[0][0]
def getOverall_Rating(mydb , MovieID) :
    mycursor = mydb.cursor()
    sql = "SELECT Overall_Rating FROM Movies WHERE Movie_id = '%d';"%(MovieID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result # if something is buggy
def RefreshOverall_Rating(mydb , MovieID) : # it must be like refreshing the rating after any updation in the watchlist rating by any user .
    mycursor = mydb.cursor()
    sql = "SELECT Rating FROM Watch_List WHERE MovieID = '%d';"%(MovieID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    num = 0 ; sum = 0 ;
    for i in result :
        sum += i[0]
        num += 1
    num = round(sum/num,1)
    sql = "UPDATE Movies SET Overall_Rating = '%f' WHERE Movie_id = '%d';"%( num , MovieID)
    mycursor.execute(sql)
    mydb.commit()
def getIMDB_Rating(mydb , MovieID) :
    mycursor = mydb.cursor()
    sql = "SELECT IMDB FROM Movies WHERE Movie_id = '%d';"%(MovieID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result # if something is buggy
def getDuration(mydb , MovieID) :
    mycursor = mydb.cursor()
    sql = "SELECT Duration FROM Movies WHERE Movie_id = '%d';"%(MovieID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result # if something is buggy
def getGenre(mydb , MovieID) :
    mycursor = mydb.cursor()
    sql = "SELECT Genre FROM Movies WHERE Movie_id = '%d';"%(MovieID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result # if something is buggy
def getMovieID(mydb , Movie_Name) : # must be private for internal use only --> guessing MID from name
    mycursor = mydb.cursor()
    sql = "SELECT Movie_id FROM Movies WHERE Movie_Name = '%s';"%(Movie_Name)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result # if something is buggy

def getArtists(mydb, MovieID, img_addr):
    mycursor = mydb.cursor()
    sql = "SELECT Artists.Name from Starcast LEFT JOIN Artists ON Artists.ArtistID=Starcast.ArtistID WHERE Starcast.MovieID='%d'"%(MovieID)
    mycursor.execute(sql)
    result = mycursor.fetchall();
    ans = """ """
    for x in result:
        ans += """<a href="#" class="list-group-item list-group-item-action">
            <div class="card">
              <img src="""+img_addr+""" class="card-img-top" alt="...">
              <div class="card-body">
                <h5 class="card-title" align="center">"""+x[0]+"""</h5>
              </div>
            </div>
          </a>
          </a>"""
    return ans
# "SELECT W.MovieID FROM Watch_List W WHERE W.UID in (SELECT W.UID , count(*) FROM Watch_List W WHERE W.MovieID in (SELECT DISTINCT MovieID from Watch_List WHERE UID = 1) GROUP BY W.UID HAVING count(*) > 0 ORDER BY count(*)) ;"

# +----------------+--------------+------+-----+---------+-------+
# | Field          | Type         | Null | Key | Default | Extra |
# +----------------+--------------+------+-----+---------+-------+
# | Movie_id       | int(3)       | NO   | PRI | NULL    |       |
# | P_HouseID      | int(3)       | NO   | MUL | NULL    |       |
# | Movie_Name     | varchar(71)  | NO   |     | NULL    |       |
# | Overall_Rating | decimal(3,1) | YES  |     | NULL    |       |
# | IMDB           | decimal(3,1) | YES  |     | NULL    |       |
# | Duration       | int(3)       | NO   |     | NULL    |       |
# | Genre          | varchar(40)  | NO   |     | NULL    |       |
# +----------------+--------------+------+-----+---------+-------+

def shell(mydb) :
    command = ""
    temp = ""
    while(True) :
        command = input().split()
        command[0] = command[0].lower()
        if(command[0] == "exit") :
            print("bye")
            break ;
        elif(command[0] == "getmoviename") :
            print(getMovieName(mydb , int(command[1])))
        elif(command[0] == "getmovieid") :
            s = ""
            for i in command[1:] :
                s += i + " "
            print(getMovieID(mydb , s))
        elif(command[0] == "getduration") :
            print(getDuration(mydb , int(command[1])))
        elif(command[0] == "getimdb") :
            print(getIMDB_Rating(mydb , int(command[1])))
        elif(command[0] == "getphouseid") :
            print(getProductionHouseID(mydb , int(command[1])))
        elif(command[0] == "getgenre") :
            print(getGenre(mydb , int(command[1])))
        else :
            print("damn")


# if __name__ == '__main__' :
#     # mydb = mysql.connector.connect(host = "localhost" , user = "usr" , passwd = "pass" , database = "A")
#     # shell(mydb)
#     # getSuggestion(mydb,2)
#     print(getBiasedRating(mydb , 185 , 3))
#     # 46 , 96
#     mydb.close()
