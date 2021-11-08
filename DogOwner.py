# class for helping us to defind onject Dogowner and doing function on it

import logging
import db_handler
import datetime
class DogOwner:
    def __init__(self, mail, name=None, birth=None, phone=None, city=None): # Builder
        self.mail = mail
        self.name = name
        self.birth = birth
        self.phone = phone
        self.city = city

    def get_mail(self):
        return  self.mail
    def get_name(self):
        return  self.name
    def get_birth(self):
        return  self.birth
    def get_phone(self):
        return  self.phone
    def get_city(self):
        return  self.city
    def get_dogs (self):##returning list of dogs names # Getting the dogs of dogowner
        logging.info('In DogOwner.get_dogs')
        db = db_handler.DbHandler()
        cursor=db.getCursor()
        cursor.execute("select Name, NumDog from Dogs where  Dogs.Email=%s",(str(self.mail),))
        #cursor.execute(sql4, (str("guy1@gmail.com")))
        dogs =cursor.fetchall()
        db.commit()
        db.disconnectFromDb()
        return dogs
    def get_dog_type(self, dognum):##get the num dog and returns the type # Getting type of dog by numdog
        logging.info('In DogOwner.get_dogs')
        db = db_handler.DbHandler()
        cursor=db.getCursor()
        sql3="""
            select TypeName from Dogs where Dogs.NumDog= '%s'
            """ %str(dognum)
        cursor.execute(sql3)
        dog_type =str(cursor.fetchone()[0])
        db.commit()
        db.disconnectFromDb()
        return dog_type


    def InsertDB(self):        #insert dogOwner to the DB
        logging.info('In DogOwner.insertDB')
        db = db_handler.DbHandler()
        cursor=db.getCursor()
        sql1 = 	"""
				INSERT INTO DogOwner (BirthDate, email, Name, PhoneNumber, City) VALUES (%s, %s, %s, %s,%s)
				"""
        cursor.execute(sql1,(str(self.birth),str(self.mail),str(self.name),str(self.phone),str(self.city)))
        db.commit()
        db.disconnectFromDb()
        return

    def findDogWalkers(self, dognum, sdate, edate, days):  # Getting dogwalkers available for trips in specific dates and days
        logging.info('In DogOwner.insertDB')
        db = db_handler.DbHandler()
        cursor = db.getCursor()
        dogtype = self.get_dog_type(dognum)##get the dog type
        sql2=self.sqlMaker(edate,sdate,days,dogtype)##make SQL string
        cursor.execute(sql2)
        db.commit()
        dogwalker=cursor.fetchall()#get dogwalkers list of lists (email,name,phonenumber,price)
        db.disconnectFromDb()
        return dogwalker
            
    def sqlMaker(self,edate,sdate,days,dogtype): # Creating sql string
        sql1="""select email,name,phonenumber, sum(price)
        from DogWalker JOIN DogWalkersAvailableDays USING(EMAIL) join Availabetypes using(email)
        where ("""
        daysSQL="""day=%s"""%str(days[0])
        for i in range(1,len(days)):
            daysSQL+=""" or day=%s"""%str(days[i])
        sql1+=daysSQL+') '
        sql2="""and typename="%s" and email not in(select email
        From Trips  join DogWalkersAvailableDays using(email)
        where (dayofweek(walkdate)=day  AND walkdate between '%s' and '%s') and ("""%(str(dogtype),str(sdate),str(edate))+daysSQL+')'+""" group by email,walkdate,dogsmaxnum
        having count(walkdate)>dogsmaxnum)
        group by email,name,phonenumber
        having count(day)=%s;""" % len(days)
        sql1+=sql2
        return sql1
    
    def TripsMaker(self, mail, dognum, edate, sdate,dayss):  # Building specific trips
        start = datetime.datetime.strptime(sdate, "%Y-%m-%d")
        end = datetime.datetime.strptime(edate, "%Y-%m-%d")
        ndays=[]
        logging.info('In DogOwner.TripsMaker')
        db = db_handler.DbHandler()
        cursor = db.getCursor()
        date_array = \
            (start + datetime.timedelta(days=x) for x in range(0, (end - start).days))
        for i in range(len(dayss)):
            number=int(dayss[i])
            ndays.append(number-1)
        for date_object in date_array:
            if int(date_object.strftime('%w')) in ndays:
                sql4="""select count(*) from Trips where WalkDate='%s' and Email='%s' and NumDog='%s'"""%(str(date_object.strftime("%Y-%m-%d")),str(mail),str(dognum))
                cursor.execute(sql4)
                row=cursor.fetchall()
                if row[0][0]==0:
                    self.addtrip(date_object.strftime("%Y-%m-%d"),dognum,mail)
        return        


    def DayInRangeDates(self,sdate,edate,dayss):
        start = datetime.datetime.strptime(sdate, "%Y-%m-%d")
        end = datetime.datetime.strptime(edate, "%Y-%m-%d")
        ndays = []
        count=0
        date_array = \
            (start + datetime.timedelta(days=x) for x in range(0, (end - start).days))
        for i in range(len(dayss)):
            number = int(dayss[i])
            ndays.append(number - 1)
        for date_object in date_array:
            if int(date_object.strftime('%w')) in ndays:
                count+=1
        return count,len(ndays)


    def addtrip(self,walkdate,numdog,mail): # Inserting trips to db if it doesnt exists already
        logging.info('In DogOwner.addtrip')
        db = db_handler.DbHandler()
        cursor = db.getCursor()
        sql="""INSERT INTO Trips (WalkDate, PickUpNeeded, Email, NumDog) VALUES (%s, %s, %s, %s);"""
        cursor.execute(sql,(str(walkdate),str(0),str(mail),str(numdog)))
        db.commit()
        db.disconnectFromDb()
