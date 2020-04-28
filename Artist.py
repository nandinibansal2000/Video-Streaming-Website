#Sanskar sachdeva
#Artist

# import mysql.connector
# from passlib.hash import sha256_crypt
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="qwerty2799"
# )
# if(mydb.is_connected()):
# 	print("Successfully Connected")
#SQL Queries

def get_specific_movie(mydb, input_Artist_ID):   
    #this would return the info of a particuler movie
    #like rating, no. of views etc.
    
    mycursor= mydb.cursor()
    sql= "select Movie_Name, Overall_Rating from Movies where Movie_id in(select MovieID from Starcast where ArtistID= '%d')"%(input_Artist_ID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    else :
        ans = ""
        for x in result:
            ans += "<tr> <td>'%s'</td> <td>'%s'</td> </tr>"%(x[0], x[1])
        return ans

def top_genre(mydb, input_Artist_ID):    
    # this would return the genres with their respective ranks
    # in a table.
    
    mycursor= mydb.cursor()
    sql= "select Genre, AVG(Overall_Rating) as r from Movies where Movie_id in (select MovieID from Starcast where ArtistID=%d) group by Genre order by r desc;"%(input_Artist_ID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result[0][0]

def content(mydb, input_Artist_ID):
    # this would return all the movies, the artist has
    # been  a part of available on the platform.
    
    mycursor= mydb.cursor()
    sql= "select Movie_Name, Overall_Rating, Genre from Movies where Movie_id in(select MovieID from Starcast where ArtistID= '%d')"%(input_Artist_ID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result
    
def artist_info(mydb, input_Artist_ID):
    # this returns info about the rating like his age,
    # total movies acted in, movies he is best known for etc.
    
    mycursor= mydb.cursor()
    sql= " select Name, Age from Artists where ArtistID=  '%d'" %(input_Artist_ID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0]
    else :
        return result

#Python Queries

def artist_rating(mydb, input_Artist_ID):
    # this returns the avg rating of the artist given by the
    # users, based on all his performances.
    
    mycursor= mydb.cursor()
    sql= "select  avg(Overall_Rating) from Movies where Movie_id in(select MovieID from Starcast where ArtistID= '%d')"%(input_Artist_ID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result

def artist_official_rating(mydb, input_Artist_ID):
    # this returns the official rating of the artist, 
    # given by the rating authority like imdb.
    
    mycursor = mydb.cursor()
    sql = "select  avg(IMDB) from Movies where Movie_id in(select MovieID from Starcast where ArtistID= '%d')"%(input_Artist_ID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result
    
def getCompetentArtist(mydb , ArtistID) :   # specifically based on genre / taste of user
    mycursor= mydb.cursor()
    sql= "select MovieID from Starcast where ArtistID= '%d' "%(ArtistID)
    mycursor.execute(sql)
    movies = mycursor.fetchall() ;
    # return movies    # ignoring the number of user that wathced the movie as they may or may not be iportant to affect.
    FanUsers = set()
    CompMoviesID = dict()   # other movies than Artis's watched by Fans of Artist
    for m_id in movies :
        sql= "SELECT UID FROM Watch_List WHERE MovieID = '%d' "%(m_id[0])
        mycursor.execute(sql)
        Fans = set(mycursor.fetchall()) # Fans of Artist
        for User in Fans :
            if(User not in FanUsers) :
                FanUsers.add(User[0])
                sql= "SELECT MovieID FROM Watch_List WHERE UID= '%d' "%(User[0])
                mycursor.execute(sql)
                FansMovies = mycursor.fetchall() ;
                for movie in FansMovies :   # time to fill CompMoviesID
                    # print(movie[0])
                    if(movie not in movies) :
                        if(movie[0] in CompMoviesID) :
                            CompMoviesID[movie[0]] += 1
                        else :
                            CompMoviesID[movie[0]] = 1
    TopCompMoviesID = list({k: v for k, v in sorted(CompMoviesID.items(), key=lambda item: item[1])}.keys())[::-1]
    CompArtistID = dict()
    for movie in TopCompMoviesID :
        sql = "SELECT ArtistID FROM Starcast WHERE MovieID = '%d' "%(movie)
        mycursor.execute(sql)
        Artists = mycursor.fetchall()
        for artist in Artists :
            if(artist[0] != ArtistID) :
                if(artist[0] in CompArtistID) : # rated Competant Artist with voting sys based on num of movies watched
                    CompArtistID[artist[0]] += 1
                else :
                    CompArtistID[artist[0]] = 1
    TopCompArtistID = list({k: v for k, v in sorted(CompArtistID.items(), key=lambda item: item[1])}.keys())[::-1]
    for i in [49,81,259,15,56,130,20,149,23] :  # adding some random Artist for atleast filling 3 comp Artist
        if(i not in TopCompArtistID) :
            TopCompArtistID.append(i)
    return TopCompArtistID[:3]  # to send top rated 3 movies

# +----------------+--------------+------+-----+---------+-------+
# | Field          | Type         | Null | Key | Default | Extra |
# +----------------+--------------+------+-----+---------+-------+
# | ArtistID       | int(11)      | NO   | PRI | NULL    |       |
# | Age            | int(2)       | NO   |     | NULL    |       |
# | Name           | varchar(12)  | NO   |     | NULL    |       |
# +----------------+--------------+------+-----+---------+-------+


if __name__ == "__main__":
    import mysql.connector
    mydb = mysql.connector.connect(
      host="localhost",
      user="user",
      passwd="password",
      database="myDB2"
    )
    print(top_genre(mydb, 1))
