from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for
from mysqlconnection import MySQLConnector
import re
import js2py

import MySQLdb

import functools 
import operator


conn = MySQLdb.connect("localhost","root","root","rest" )
cursor = conn.cursor()

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[0-9]')
PASS_REGEX = re.compile(r'.*[A-Z].*[0-9]')


app = Flask(__name__)
app.secret_key= 'rest'
mysql = MySQLConnector(app,'rest')

@app.route('/')
def index():
    print (session)
    return render_template('index.html')

@app.route('/adm')    
def admin():
    print session
    cursor.execute("select * from admin")
    data = cursor.fetchall() 
    return render_template('admin.html', value=data)

@app.route('/use')  
def user():
    print session
    cursor.execute("select * from userreg")
    data = cursor.fetchall()
    print data 
    return render_template('user.html', value=data)

@app.route('/restt')  
def resto():
    print session
    cursor.execute("select * from restreg")
    data = cursor.fetchall() 
    return render_template('restaurant.html', value=data)

@app.route('/admhome')  
def adminhome():
    print session
    return render_template('adminhome.html')

@app.route('/uhome')  
def usehome():
    print session
    cursor.execute("select * from userreg")
    data = cursor.fetchall()
    return render_template('userhome.html', value=data)
    

@app.route('/rhome')    
def restohome():
    print session
    return render_template('restohome.html')


@app.route('/vuser')  
def viewuser():
    print (session
    cursor.execute("select * from userreg")
    data = cursor.fetchall()
    return render_template('viewuser.html', value=data)

@app.route('/vrest')  
def viewresto():
    print session
    cursor.execute("select * from restreg")
    data = cursor.fetchall()
   
    return render_template('viewrest.html', value=data)

@app.route('/vresti')  
def vrestoinfo():
    print session
    cursor.execute("select * from restreg")
    data = cursor.fetchall()
    print data 
    return render_template('viewrestoinfo.html', value=data)


@app.route('/logout')  
def logoutt():
    print session
    cursor.execute("select * from restreg")
    data = cursor.fetchall()
    print data 
    return render_template('viewrestoinfo.html', value=data)


@app.route('/log')  
def logout():
    print session
    flash("You've logout!","info")	
    return redirect(url_for("index"))







@app.route('/con') 
def contact():
    print session
    
    return render_template('contactus.html')






@app.route('/admhome', methods=['POST'])
def adminlogin():
    input_uname = request.form['Email']
    input_password = request.form['Password']
    email_query = "SELECT * FROM admin WHERE email1 = :email and Pass = :pass"
    query_data = {'email': input_uname, 'pass': input_password}
    stored_email = mysql.query_db(email_query, query_data)

    if not EMAIL_REGEX.match(request.form['Email']):
        print ("Email must be a valid email", 'error')
        flash("Email must be a valid email")
        
    if not stored_email:
        print("User does not exist!")
        flash("User does not exist!")
        return redirect('/')

    else:
        if request.form['Password'] == stored_email[0]['Pass']:
            print("login success")
            flash("login success")
            return render_template('adminhome.html')

        else:
            print("Wrong password, try again!")
            flash("Wrong password, try again!")
            return redirect('/')




@app.route('/use', methods=['POST'])
def userreg():
    print "signup"
    error=""
    input_email = request.form['Email']
    email_query = "SELECT * FROM userreg WHERE email = :email_id"
    query_data = {'email_id': input_email}
    stored_email = mysql.query_db(email_query, query_data)

    age= request.form['age']
    
    cat="0"

    if age <= "14":
       cat = "Children"
       print("Category Child")
    
    elif "15" >= age or age <= "40":
       cat = "Young"
       print("Category Young")
    
    else:
       cat = "Old Age"
       print("Category Old")

    print ("Category=",cat)
    print request.form['Email']
    print session

    for x in request.form:
        if len(request.form[x]) < 1:
            print (x + " cannot be blank!", 'blank')
            error="Fill all Fields"
    

    if len(request.form['Password']) < 5:
        print ("Password must be more than 5 characters", 'pass')
        error="Password must be greater than 5 characters"

    if not EMAIL_REGEX.match(request.form['Email']):
        print ("Email must be a valid email", 'error')
        error= "Email must be a valid email"
    
    if stored_email:
        error="Email already exists!"


    if error!="":
        print "error"
        return render_template('index.html',error=error)
        
    else:
        print ("All Good!!!!", 'good')
        query = "INSERT INTO userreg (name, email, pass, cpass, height, weight, age, contact, cat) VALUES(:name, :email, :pass, :cpass, :height, :weight, :age, :contact, :cat)"
        
        data = {
                'name': request.form['Name'],
                'email': request.form['Email'],
                'pass': request.form['Password'],
                'cpass': request.form['cpass'],
                'height': request.form['height'],
                'weight': request.form['weight'],
                'age': request.form['age'],
                'contact': request.form['contact'],
		'cat': cat


            }
        
        mysql.query_db(query, data)

        input_email = request.form['Email']
        email_query = "SELECT * FROM userreg WHERE email = :email"
        query_data = {'email': input_email}
        stored_email = mysql.query_db(email_query, query_data)

        
         
        print ("This email address you entered " + input_email + " is a valid email address. Thank you!")
        return render_template('user.html')



@app.route('/uhome', methods=['POST'])
def userlog():
    input_uname = request.form['Email']
    input_password = request.form['Password']
    
    email_query = "SELECT * FROM userreg WHERE email = :email and pass = :pass"
    query_data = {'email': input_uname, 'pass': input_password}
    stored_email = mysql.query_db(email_query, query_data)
    print(email_query)
    session['email'] = request.form['Email']
    print session['email']
    
    error = None
    if not EMAIL_REGEX.match(request.form['Email']):
        print ("Email must be a valid email")
        meassage = 'Email must be a valid email'
        return render_template('index.html', meassage=error)

    if not stored_email:
        print("User does not exist!")
        meassage = 'User does not exist!'
        return render_template('index.html', meassage=error)

    else:
        if request.form['Password'] == stored_email[0]['pass']: 
            print("login success")
            meassage = 'login success'
            return render_template('userhome.html', meassage=error)

        else:
            print("Wrong password, try again!")
            meassage = 'Wrong password, try again!'
            return render_template('index.html', meassage=error)


@app.route('/restt', methods=['POST'])
def restreg():
    print "signup"
    error=""
    input_email = request.form['Email']
    email_query = "SELECT * FROM restreg WHERE email = :email_id"
    query_data = {'email_id': input_email}
    stored_email = mysql.query_db(email_query, query_data)
    print request.form
    print request.form['Email']
    print session

    for x in request.form:
        if len(request.form[x]) < 1:
            print (x + " cannot be blank!", 'blank')
            error="Fill all Fields"
    

    if len(request.form['Password']) < 5:
        print ("Password must be more than 5 characters", 'pass')
        error="Password must be greater than 5 characters"

    if not EMAIL_REGEX.match(request.form['Email']):
        print ("Email must be a valid email", 'error')
        error= "Email must be a valid email"
    
    if stored_email:
        error="Email already exists!"


    if error!="":
        print "error"
        return render_template('index.html',error=error)
        
    else:
        print ("All Good!!!!", 'good')
        query = "INSERT INTO restreg (name, email, pass, cpass, address, contact, gen ) VALUES(:name, :email, :pass, :cpass, :add, :contact, :gen )"
        
        data = {
                'name': request.form['Name'],
                'email': request.form['Email'],
                'pass': request.form['Password'],
                'cpass': request.form['cpass'],
                'add': request.form['address'],
                'contact': request.form['contact'],
                'gen': request.form['gen']


            }
        
        mysql.query_db(query, data)

        input_email = request.form['Email']
        email_query = "SELECT * FROM restreg WHERE email = :email"
        query_data = {'email': input_email}
        stored_email = mysql.query_db(email_query, query_data)

        
         
        print ("This email address you entered " + input_email + " is a valid email address. Thank you!")
        return render_template('restaurant.html')



@app.route('/rhome', methods=['POST'])
def restolog():
    input_uname = request.form['Email']
    input_password = request.form['Password']
    email_query = "SELECT * FROM restreg WHERE email = :email and pass = :pass"
    query_data = {'email': input_uname, 'pass': input_password}
    stored_email = mysql.query_db(email_query, query_data)

    if not EMAIL_REGEX.match(request.form['Email']):
        print ("Email must be a valid email", 'error')

    if not stored_email:
        print("User does not exist!")
        return redirect('/')

    else:
        if request.form['Password'] == stored_email[0]['pass']:
            print("login success")
            return render_template('restohome.html')

        else:
            print("Wrong password, try again!")
            return redirect('/')



@app.route('/book', methods=['POST'])
def bookkk():
    print "signup"
    error=""
    input_email = request.form['Email']
    email_query = "SELECT * FROM book WHERE email = :email_id"
    query_data = {'email_id': input_email}
    stored_email = mysql.query_db(email_query, query_data)
	


    print request.form
    print request.form['Email']
    print session

    for x in request.form:
        if len(request.form[x]) < 1:
            print (x + " cannot be blank!", 'blank')
            error="Fill all Fields"
    

    if len(request.form['Password']) < 5:
        print ("Password must be more than 5 characters", 'pass')
        error="Password must be greater than 5 characters"

    if not EMAIL_REGEX.match(request.form['Email']):
        print ("Email must be a valid email", 'error')
        error= "Email must be a valid email"
    
    if stored_email:
        error="Email already exists!"


    if error!="":
        print "error"
        return render_template('radhika.html',error=error)
        
    else:
        print ("All Good!!!!", 'good')
        query = "INSERT INTO restreg (name, email, contact, person, date, time, food, occasion ) VALUES(:name, :email, :contact, :person, :date, :time, :food, :occasion )"
        
        data = {
                'name': request.form['Name'],
                'email': request.form['Email'],
                'contact': request.form['phone'],
                'person': request.form['person'],
                'date': request.form['date'],
                'time': request.form['time'],
                'food': request.form['food'],
                'occasion': request.form['occasion']



            }
        
        mysql.query_db(query, data)

        input_email = request.form['Email']
        email_query = "SELECT * FROM restreg WHERE email = :email"
        query_data = {'email': input_email}
        stored_email = mysql.query_db(email_query, query_data)

        
         
        print ("This email address you entered " + input_email + " is a valid email address. Thank you!")
        return render_template('booking.html')




    

if __name__ == "__main__":
    app.run(debug=True)
