# class for helping us to defind onject dog and doing function on it
import logging
import db_handler

class Dog:
        def __init__(self,  name,gender,age,dtype, email,num=None): # Builder
            self.num =num
            self.name=name
            self.gender=gender
            self.age=age
            self.dtype=dtype
            self.email=email
        def get_num(self):
            return self.num

        def get_name(self):
            return self.name

        def get_gender(self):
            return self.gender

        def get_age(self):
            return self.age

        def get_type(self):
            return self.type


        def GetMaxDog(self): # Getting Id of last dog inserted to DB
            db = db_handler.DbHandler()
            cursor = db.getCursor()
            sql1="""select max(NumDog) from Dogs
                           """
            cursor.execute(sql1)
            db.commit()
            maxnum = cursor.fetchall()
            db.disconnectFromDb()
            return maxnum

        def InsertDB(self): # Inserting dog to db
            logging.info('In Dogs.insertDB')
            db = db_handler.DbHandler()
            cursor = db.getCursor()
            sql1 = 	"""
                    INSERT INTO Dogs (NumDog, Name, Age, Gender, Email, TypeName) VALUES (%s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(sql1,(self.num,self.name,self.age,self.gender,self.email,self.dtype))
            db.commit()
            db.disconnectFromDb()
            return