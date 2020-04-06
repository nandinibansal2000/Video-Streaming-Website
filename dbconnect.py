# import pymysql
# pymysql.install_as_MySQLdb() 
import MySQLdb


def connection():
	conn=MySQLdb.connect(host="localhost",
						user="new",
						passwd="jatin1995@2000",
						db="DBMS")
	c=conn.cursor()
	return c,conn

