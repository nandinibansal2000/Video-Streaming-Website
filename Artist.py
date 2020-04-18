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
    sql= "select Genre, max(Overall_Rating) from Movies where Movie_id in(select MovieID from Starcast where ArtistID= '%d')"%(input_Artist_ID)
    mycursor.execute(sql)
    result = mycursor.fetchall() ;
    if( len(result) == 0 ) :
        return None
    elif( len(result) == 1 ) :
        return result[0][0]
    else :
        return result

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
    
# +----------------+--------------+------+-----+---------+-------+
# | Field          | Type         | Null | Key | Default | Extra |
# +----------------+--------------+------+-----+---------+-------+
# | ArtistID       | int(11)      | NO   | PRI | NULL    |       |
# | Age            | int(2)       | NO   |     | NULL    |       |
# | Name           | varchar(12)  | NO   |     | NULL    |       |
# +----------------+--------------+------+-----+---------+-------+
