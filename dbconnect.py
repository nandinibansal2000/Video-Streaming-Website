# import pymysql
# pymysql.install_as_MySQLdb() 
import MySQLdb


def connection():
	conn=MySQLdb.connect(host="localhost",
						user="user",
						passwd="password",
						db="newdb")
	c=conn.cursor()
	return c,conn

