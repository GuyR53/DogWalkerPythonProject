# class for helping us to defind onject Dogwalker and doing function on it
import logging
import db_handler

class DogWalker:
        def __init__(self, mail ,name=None,phone=None,city=None,typedogs=None,daysavailable=None): # Builder
            ##logging.info('Initializing DogWalker')
            self.mail=mail
            self.name=name
            self.phone=phone
            self.city=city
            self.typedogs=typedogs  ##list of types
            self.daysavailable=daysavailable    ##list of days and prices per each day  if day not available price=0[[0,100,numof dogs],[1,140],....,[6,price]]0=monday sunday=6 
            ##list of days and max number of dogs for the day[0,1,3,4,0,9,0]

        def get_mail(self):
            return self.mail

        def get_name(self):
            return self.name

        def get_phone(self):
            return self.phone

        def get_city(self):
            return self.city

        def get_typedogs(self):
            return self.typedogs

        def get_daysavailable(self):
            return self.daysavailable


        def InsertDB(self):# Inserting dogwalker to db if fit to conditions
            logging.info('In DogWalker.insertDB')
            db = db_handler.DbHandler()
            cursor=db.getCursor()
            sql1 = 	"""
				INSERT INTO DogWalker (Name, Email, PhoneNumber, City) VALUES (%s, %s, %s, %s)
				"""
            cursor.execute(sql1,(self.name,self.mail,self.phone,self.city))
            #?logging.info(self.daysavailable)
            for i in range(len(self.daysavailable)):            ##insert the dogwalker days and max num of dogs to the DB
                if self.daysavailable[i][0]:
                
                    sql2="""
                    INSERT INTO DogWalkersAvailableDays (Day, Price, DogsMaxNum, Email) VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute( sql2,(i,self.daysavailable[i][1],self.daysavailable[i][2],self.mail))##monday=0
                
            for breed in self.typedogs:#insert the dogwalker types to the DB
                if breed!="":
                    sql3="""INSERT INTO Availabetypes (Email, TypeName) VALUES (%s, %s)"""
                    cursor.execute(sql3,(self.mail,breed))
            db.commit()
            db.disconnectFromDb()
            return

        def ShowDogOwnerDetailsByParamaters(self,age, city): # Showing clients details by specific parameters
            logging.info('In DogWalker.insertDB')
            db = db_handler.DbHandler()
            cursor = db.getCursor()
            sql1 = """
            				SELECT birthdate,email,name,phonenumber,city 
            				FROM DogOwner AS D2
            				 where exists (select d.email from Trips as t join Dogs as d using (numdog) where t.email=%s and d.email=D2.email group by d.email)
            				 and 2020-year(birthdate)=%s 
            				and D2.city=%s 
            				"""
            cursor.execute(sql1, (self.mail,str(age),str(city)))
            db.commit()
            row = cursor.fetchall()
            db.disconnectFromDb()
            return row

        def ShowDogOwnerDetails(self): # showing clients details
            logging.info('In DogWalker.insertDB')
            db = db_handler.DbHandler()
            cursor = db.getCursor()
            sql1 = """
                   				SELECT birthdate,email,name,phonenumber,city 
                   				FROM DogOwner AS D2
                   				 where exists (select d.email from Trips as t join Dogs as d using (numdog) where t.email='%s' and d.email=D2.email group by d.email)
                   				""" %self.mail
            cursor.execute(sql1)
            db.commit()
            row = cursor.fetchall()
            db.disconnectFromDb()
            return row

