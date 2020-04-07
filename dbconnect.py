# import pymysql
# pymysql.install_as_MySQLdb() 
import MySQLdb


def connection():
	conn=MySQLdb.connect(host="localhost",
						user="username",
						passwd="password",
						db="DBMS")
	c=conn.cursor()
	return c,conn

