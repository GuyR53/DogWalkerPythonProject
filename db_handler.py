# Class for handling connections to DataBase Easily
# Import logging - Helps us documenting messages in Logs.
import logging
# Import operating system library
import os
# Import Data Base library
import MySQLdb
# Our Database connection parameters
DB_USER_NAME='db_team26'
DB_PASSWORD='oliapchj'
DB_DEFALUT_DB='db_team26'

class DbHandler():
	def __init__(self):
		logging.info('Initializing DbHandler new')
		self.m_user=DB_USER_NAME
		self.m_password=DB_PASSWORD
		self.m_default_db=DB_DEFALUT_DB
		self.m_unixSocket='/cloudsql/dbcourse2015:mysql'
		self.m_charset='utf8'
		self.m_host='173.194.110.126'
		self.m_port=3306
		self.m_DbConnection=None

	def connectToDb(self):
		logging.info('In ConnectToDb')
		# external db connection
		if self.m_DbConnection is None:
			env = os.getenv('SERVER_SOFTWARE')
			if (env and env.startswith('Google App Engine/')):
				#external connection
				logging.info('In env - Google App Engine')
				# connect to the DB
				self.m_DbConnection = MySQLdb.connect(
				unix_socket=self.m_unixSocket,
				user=self.m_user,
				passwd=self.m_password,
				charset=self.m_charset,
				db=self.m_default_db)
			else:
				#Connecting from a local network.
				logging.info('In env - Launcher')
				# connect to the DB
				self.m_DbConnection = MySQLdb.connect(
				host=self.m_host,
				db=self.m_default_db,
				port=self.m_port,
				user= self.m_user,
				passwd=self.m_password,
				charset=self.m_charset)
				
	def disconnectFromDb(self):
		if self.m_DbConnection:
			self.m_DbConnection.close()
			
	def commit(self):
		if self.m_DbConnection:
			self.m_DbConnection.commit()			
			
	def getCursor(self):
		self.connectToDb()
		return (self.m_DbConnection.cursor())



