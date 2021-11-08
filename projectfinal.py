#The aplication connects between dogowners and dogwalkers, using database that stores all the trips and details of
#both dog owner and walker and present them the details and trips and alows them to sign for trips.
#Editors: Group 26 the best!
#Last Edition:19/01/2019
# import webapp2  - Python web framework compatible with Google App Engine
import webapp2
import logging
#import Jinja and os libraries
import jinja2
import datetime
# for jinja using
import os
#using dates
#for using our database
import MySQLdb
#Load Jinja
jinja_environment =jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
#import our classes for oop programming
from DogOwner import DogOwner
from Dog import Dog
from DogWalker import DogWalker
# class that helps us use db connection
import db_handler
#class that helps us use gmail and google account for connecting
from google.appengine.api import users
# The class displays our main page when url opens

class MainPage(webapp2.RequestHandler):     # displays our html mainpage we built


    def get(self): #checks what page to show, determined by the user who logged in and suit menu for the specific user
        user = users.get_current_user()
        if user: # if user is online
            nickname = user.nickname()
            email = user.email()
            db=db_handler.DbHandler()
            cursor=db.getCursor()
            sql="""SELECT count(*) FROM db_team26.DogOwner WHERE email = %s""" # checking whether the user is dogowner
            cursor.execute(sql,[email])
            row=cursor.fetchall()
            if row[0][0] > 0: # if dogowner load his html page that suit for him
                parameters_for_template = {'i_user_object': user}
                my_name_template = jinja_environment.get_template('dogowner.html')
                self.response.write(my_name_template.render(parameters_for_template))
            else:
                cursor.execute('SELECT count(*) FROM db_team26.Premium WHERE email = %s', [email]) #checking whther he is dogwalkerpremium
                row = cursor.fetchall()

                if row[0][0] > 0: # if so upload his page
                    parameters_for_template = {'i_user_object': user}
                    my_name_template = jinja_environment.get_template('dogwalkerpremium.html')
                    self.response.write(my_name_template.render(parameters_for_template))
                else:
                    cursor.execute('SELECT count(*) FROM db_team26.Regular WHERE email = %s', [email]) #checking whther he is dogwalkerregular
                    row = cursor.fetchall()
                    if row[0][0] > 0: # if so upload dogwalkerpremiumpage cause there is no differences in their action on the site
                        parameters_for_template = {'i_user_object': user}
                        my_name_template = jinja_environment.get_template('dogwalkerpremium.html')
                        self.response.write(my_name_template.render(parameters_for_template))
                    else:
                        cursor.execute('SELECT count(*) FROM db_team26.DogWalker WHERE email = %s', [email])  #again checking if he is dogwalker
                        row = cursor.fetchall()
                        if row[0][0] > 0: # upload his page
                            parameters_for_template = {'i_user_object': user}
                            my_name_template = jinja_environment.get_template('dogwalkerpremium.html')
                            self.response.write(my_name_template.render(parameters_for_template))
                        else: # if he is not dogwalker or dogowner and he is online, he is user online and upload his page

                              parameters_for_template = {'i_user_object': user}
                              my_name_template = jinja_environment.get_template('mainpageonline.html')
                              self.response.write(my_name_template.render(parameters_for_template))
            db.disconnectFromDb() # disconnecting from db
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write("<html>\n")
            self.response.write(" <head>\n")
            self.response.write(" </head>\n")
            self.response.write(" <body>\n")  # create a link to /login
            self.response.write(" <a class='logout' href='/logout'>Logout</a></br>\n") # starting html online orders for user online

            self.response.write(" </body>\n")
        else: # if he is not online opening mainpage for user that arent online
            self.response.write(" <a style=font-size:20px;float:right; class='logout' href='/login'>Sign in</a></br>\n")
            printed_text= jinja_environment.get_template('mainpage.html')
            self.response.write(printed_text.render())



       
class DogOwnerRegistration(webapp2.RequestHandler): # Registaring dogowner to the site
    def get(self):
        user = users.get_current_user()
        nickname = user.nickname()
        email = user.email()
        parameters_for_template = {'i_user_object': user}
        my_name_template = jinja_environment.get_template('dog_owner_register.html') #opening html page for collecting details of the dogowner
        self.response.write(my_name_template.render(parameters_for_template))



class dog_register(webapp2.RequestHandler): # collecting the details of the dogowner and opening new form for details of the dogs

    def post(self):
        user = users.get_current_user()
        nickname = user.nickname()
        email = str(user.email())
        name = str(self.request.get('name'))  # collecting all dogowner details
        city = str(self.request.get('City'))
        phone_number = str((self.request.get('phone_number')))
        birth_date = str((self.request.get('birth_date')))
        number_of_dogs = int(self.request.get('number_of_dogs'))
        dogowner=DogOwner(email,name,birth_date,phone_number,city) # defining new object dogowner and inserting his details to db
        dogowner.InsertDB()
        parameters_for_template1 = {'i_user_object': user,'number_of_dogs': number_of_dogs}  # sending parameters to html and opening dog registration by the paramater numofdogs that dogowner inserted
        # Create a template object
        template = jinja_environment.get_template('dog_register.html')
        # sending the paramaters to html page that we made
        self.response.write(template.render(parameters_for_template1))

class FinishRegistrationdogowner(webapp2.RequestHandler): # finishing registration of dog
     def post(self):
             user=users.get_current_user()
             email=user.email()
             number_of_dogs = int(self.request.get('number_of_dogs')) # collecting numofdogs from other class by hidden input
             for i in range (number_of_dogs): # running over the number of dogs that inserted before and inserting each to db by maxnumdog+1
                 name = str(self.request.get('name'+str(i)))
                 gender = str(self.request.get('gender' +str(i)))
                 age = str(self.request.get('age' + str(i)))
                 typeofdogs = str(self.request.get('dtype' + str(i)))
                 dog=Dog(name,gender,age,typeofdogs,email)
                 listoflists=dog.GetMaxDog()
                 maxnum=int(listoflists[0][0]+1)
                 dog=Dog(name,gender,age,typeofdogs,email,maxnum)
                 dog.InsertDB() # Inserting do DB


             self.response.write('<script> {alert("Registration succesful!"); location.href ="/";}</script>')# jumping message of finish registration


class dog_walker_register(webapp2.RequestHandler): # regitration of dogwalker
    def get(self):
        user = users.get_current_user()
        parameters_for_template = {'i_user_object': user}
        my_name_template = jinja_environment.get_template('dog_walker_register.html') # uploading html for registration
        self.response.write(my_name_template.render(parameters_for_template))


class dog_walker_thank_you(webapp2.RequestHandler): # finishing registration of dogwalker and inserting details to db
    def post(self):

        types = []
        name = str(self.request.get('name'))
        city = str(self.request.get('City'))
        phone_number = str(self.request.get('phone_number'))
        user = users.get_current_user()
        email = user.email()
        for i in range(7):  ##the dog type selected-None/some type types[i]=value
            types.append(self.request.get('type ' + str(i)))
        days = []
        for i in range(7):
            days.append((str(self.request.get('day ' + str(i))), str(self.request.get('ppd' + str(i))), str(
                self.request.get('maxnod' + str(i)))))
        dogwalker = DogWalker(email, name, phone_number, city, types, days) # making dogwalker object by oop and inserting his details to db
        dogwalker.InsertDB()
        self.response.write('<script> {alert("Registration succesful!"); location.href ="/";}</script>')# jumping message of finish registration

        
class dog_register_thank_you(webapp2.RequestHandler): # after registration opening new html page for thanking for registrating
    def post(self):
        user = users.get_current_user()
        nickname = user.nickname()
        email = user.email()
        parameters_for_template = {'i_user_object': user}
        my_name_template = jinja_environment.get_template('dog_register_thank_you.html')
        self.response.write(my_name_template.render(parameters_for_template))
        self.response.write(" <a class='logout' href='/logout'>Logout</a></br>\n")

class CustomerDetails(webapp2.RequestHandler): # class for dogwalkers showing their costumer's details
        def get(self):
            user = users.get_current_user()
            dogwalker=DogWalker(user.email())
            details=dogwalker.ShowDogOwnerDetails()
            lendetails=len(details)
            if lendetails==0: # if they dont have any customers opening html that says that
                parameters_for_template = {'i_user_object': user}
                my_name_template = jinja_environment.get_template('0costumers.html')
                self.response.write(my_name_template.render(parameters_for_template))
            else: # opening html where they can see their customers
                parameters_for_template = {'i_user_object': user,'details':details,'lendetails':lendetails}
                my_name_template = jinja_environment.get_template('costumerdetails.html')
                self.response.write(my_name_template.render(parameters_for_template))

class CustomerDetailsResults(webapp2.RequestHandler): # they can search customers by specific city and specific age of dogowner
        def post(self):
            user=users.get_current_user()
            city = str(self.request.get("City"))
            age = int(self.request.get("number"))
            dogwalker=DogWalker(user.email())
            CustomerResults=dogwalker.ShowDogOwnerDetailsByParamaters(age,city) # presents the details of costumers by city and age
            lenlist=len(CustomerResults)
            parameters_for_template = {'CustomerResults': CustomerResults,'lenlist': lenlist,'i_user_object': user}
            my_name_template = jinja_environment.get_template('CustomerDetailsResults.html')
            self.response.write(my_name_template.render(parameters_for_template))

class SearchDogWalker(webapp2.RequestHandler): # class for dogowner where they can search for dogwalkers
      def get(self):
            user = users.get_current_user()
            dogowner = DogOwner(str(user.email())) # defining dogowner by mail
            lst1 = dogowner.get_dogs() # creating list of dogs of the specific dogowner
            len1 = len(lst1)
            parameters_for_template = {'lst1': lst1,'len1': len1,'i_user_object': user} # sending this parameters to heml to present for the dogowner
            my_name_template = jinja_environment.get_template('searchdogwalker.html')
            self.response.write(my_name_template.render(parameters_for_template))


class DogWalkerResults(webapp2.RequestHandler): # collecting the parameters from the other class and presenting the dogwalkers available by the terms suplied to us
        def post(self):
            user = users.get_current_user()
            dogowner = DogOwner(str(user.email()))
            lst = dogowner.get_dogs() # getting dogs by email
            len1 = len(lst)
            startdate = str(self.request.get("startdate")) # getting the html input by dogowner from other page
            finishdate = str(self.request.get("finishdate"))
            semmek=[]
            for i in range(1,8):#list of wanted days
                if (self.request.get("day "+str(i))!=''):
                   semmek.append(self.request.get("day "+str(i)))
            dognum = str(self.request.get("selectdogtype"))
            harta=dogowner.findDogWalkers(dognum,startdate,finishdate,semmek)
            lenharta=len(harta)
            count,nday=dogowner.DayInRangeDates(startdate,finishdate,semmek)
            if (count<nday or len(harta) == 0 or len1==0 ):
                parameters_for_template = { 'i_user_object': user}
                my_name_template = jinja_environment.get_template('NoDogWalkers.html')
                self.response.write(my_name_template.render(parameters_for_template))
            else:
                parameters_for_template = {'i_user_object': user,'lst': lst, 'len1': len1,'lenharta': lenharta, 'harta': harta, 'dognum': dognum,'semmek': semmek,'startdate':startdate,'finishdate': finishdate} # sending paramters to html
                my_name_template = jinja_environment.get_template('DogWalkerResults.html') # uploading the html page
                self.response.write(my_name_template.render(parameters_for_template))


class finishchoosedogwalker(webapp2.RequestHandler):
        def post(self):
            user = users.get_current_user()
            nickname = user.nickname()
            email = user.email()
            semmek = self.request.get("semmek")
            listofDW = self.request.get("harta")
            dognum = self.request.get("dognum") # collecting the details from the other page
            startdate = self.request.get("startdate")
            finishdate = self.request.get("finishdate")
            the_chosen=''
            the_chosen = self.request.get("the_chosen")
            semmek2=[]
            for i in range (len(semmek)):
                if semmek[i].isdigit():
                    semmek2.append(semmek[i])
            user=users.get_current_user()
            dogowner=DogOwner(str(user.email()))
            dogowner.TripsMaker(str(the_chosen), int(dognum), str(finishdate), str(startdate),semmek2) # making trip by using oop
            self.response.write('<script> {alert("Registration succesful!"); location.href ="/";}</script>')# jumping message of finish registration


            



# class to handle /login requests. will force the user to perform login and will show the status
class Login(webapp2.RequestHandler): #Creates login and back to HomePage
    def get(self):
        user = users.get_current_user()
        if (user):
             self.redirect('/')
        else: # force the user to login
             self.redirect(users.create_login_url('/'))


class Logout(webapp2.RequestHandler): #Creates logout and back to HomePage
    def get(self): # if the user is logged in - we will perform log out
      user = users.get_current_user()
      if user:
    # force the user to logout and redirect him afterward to show_status page afterwards
         self.redirect(users.create_logout_url('/'))
      else:
          self.redirect('/')

class AboutUs(webapp2.RequestHandler): # class for showing details aboutus adjusting menu
    def get(self):
        self.response.write(" <a style=font-size:20px;float:right; class='logout' href='/login'>Sign in</a></br>\n")
        parameter = jinja_environment.get_template('AboutUs.html')
        self.response.write(parameter.render())

class Aboutusonline(webapp2.RequestHandler): # class for showing details aboutus for users online adjusting html page
    def get(self):
        user=users.get_current_user()
        parameters_for_template = { 'i_user_object': user}
        my_name_template = jinja_environment.get_template('Aboutusonline.html')
        self.response.write(my_name_template.render(parameters_for_template))

class Aboutusdogwalker(webapp2.RequestHandler): # class for showing details aboutus for dogwalker adjusting html page
        def get(self):
                user = users.get_current_user()
                parameters_for_template = {'i_user_object': user}
                my_name_template = jinja_environment.get_template('Aboutusdogwalker.html')
                self.response.write(my_name_template.render(parameters_for_template))

class Aboutusdogowner(webapp2.RequestHandler):  # class for showing details aboutus for owner adjusting html page
            def get(self):
                user = users.get_current_user()
                parameters_for_template = {'i_user_object': user}
                my_name_template = jinja_environment.get_template('Aboutusdogowner.html')
                self.response.write(my_name_template.render(parameters_for_template))



# define which class to call according to the input URL
# if the request will have  just the regular URL  will be handled by MainPage
# if the request will have URL with /CustomerDetails  will be handled by CustomerDetails and so on for all the urls

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/dog_walker_register', dog_walker_register),
                               ('/finishchoosedogwalker', finishchoosedogwalker),
                               ('/', MainPage),
                               ('/dog_walker_thank_you', dog_walker_thank_you),
                               ('/CustomerDetails', CustomerDetails),
                               ('/registrationdogowner', DogOwnerRegistration),
                               ('/dog_owner_registration', dog_register),
                               ('/FinishRegistrationdogowner', FinishRegistrationdogowner),
                               ('/dog_register_thank_you', dog_register_thank_you),
                               ('/SearchDogWalker', SearchDogWalker),
                               ('/CustomerDetailsResults',CustomerDetailsResults ),
                                ('/DogWalkerResults',DogWalkerResults),
                                ('/AboutUs', AboutUs),
                               ('/Aboutusonline', Aboutusonline),
                               ('/Aboutusdogwalker', Aboutusdogwalker),
                               ('/Aboutusdogowner', Aboutusdogowner),
                               ('/login', Login),
                               ('/logout',Logout)],
                              debug=True)