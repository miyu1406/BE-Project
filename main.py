from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for
from mysqlconnection import MySQLConnector
import re
import js2py
import pandas as pd
import numpy as np
from tkinter import *
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv('food.csv')
Breakfastdata = data['Breakfast']
BreakfastdataNumpy = Breakfastdata.to_numpy()

Lunchdata = data['Lunch']
LunchdataNumpy = Lunchdata.to_numpy()

Dinnerdata = data['Dinner']
DinnerdataNumpy = Dinnerdata.to_numpy()
Food_itemsdata = data['Food_items']
import MySQLdb

import functools
import operator

conn = MySQLdb.connect("localhost", "root", "root", "rest")  #schema name=rest
cursor = conn.cursor()

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[0-9]')
PASS_REGEX = re.compile(r'.*[A-Z].*[0-9]')

app = Flask(__name__)
app.secret_key = 'rest'
mysql = MySQLConnector(app, 'rest')


@app.route('/')
def index():
    print (session)
    return render_template('index.html')


@app.route('/adm')
def admin():
    print (session)
    cursor.execute("select * from admin")
    data = cursor.fetchall()
    return render_template('admin.html', value=data)


@app.route('/use')
def user():
    print (session)
    cursor.execute("select * from userreg")
    data = cursor.fetchall()
    print (data)
    return render_template('user.html', value=data)


@app.route('/restt')
def resto():
    print (session)
    cursor.execute("select * from restreg")
    data = cursor.fetchall()
    return render_template('restaurant.html', value=data)


@app.route('/admhome')
def adminhome():
    print (session)
    return render_template('adminhome.html')


@app.route('/pred')
def pred():
    print (session)
    return render_template('Prediction.html')


@app.route('/sresti')
def search():
    print (session)
    return render_template('SearchResto.html')


@app.route('/uhome')
def usehome():
    print (session)
    cursor.execute("select * from userreg")
    data = cursor.fetchall()
    return render_template('userhome.html', value=data)


@app.route('/rhome')
def restohome():
    print (session)
    return render_template('restohome.html')


@app.route('/vuser')
def viewuser():
    print (session)
    cursor.execute("select * from userreg")
    data = cursor.fetchall()
    return render_template('viewuser.html', value=data)


@app.route('/vrest')
def viewresto():
    print (session)
    cursor.execute("select * from restreg ORDER BY rank DESC")
    data = cursor.fetchall()

    return render_template('viewrest.html', value=data)


@app.route('/vresti')
def vrestoinfo():
    print (session)
    cursor.execute("select * from restreg ")
    data = cursor.fetchall()
    print(data)
    return render_template('viewrestoinfo.html', value=data)


@app.route('/dis', methods=['POST'])
def dis():
    input_disease = request.form['disease']
    print(input_disease)
    sql_query = "select * from disease where name='%s'" % input_disease
    print(sql_query)
    cursor.execute(sql_query)
    data = cursor.fetchall()
    return render_template('Dispred.html', value=data)


@app.route('/logout')
def logoutt():
    print (session)
    cursor.execute("select * from restreg")
    data = cursor.fetchall()
    print (data)
    return render_template('viewrestoinfo.html', value=data)


@app.route('/log')
def logout():
    print (session)
    flash("You've logout!", "info")
    return redirect(url_for("index"))


@app.route('/diet')
def diet():
    print (session)
    return render_template('diet.html')


@app.route('/con')
def contact():
    print (session)

    return render_template('contactus.html')


@app.route('/ftyp', methods=['POST'])
def ftyp():
    print (session)
    bp = request.form['bp']
    sugar = request.form['sugar']
    ashthma = request.form['ashthma']
    data = [bp, sugar, ashthma]
    print(bp, sugar, ashthma)
    return render_template('ftyp.html', value=data)


@app.route('/search', methods=['POST'])
def searchresult():
    print (session)
    search = request.form['search']
    email_query = "SELECT * FROM restreg WHERE name='%s' ORDER BY rank DESC" % search
    print(email_query)
    cursor.execute(email_query)
    res = cursor.fetchall()
    for row in res:
        rank = row[9]

    print(rank)
    final_rank = int(rank) + 1

    print(final_rank)
    try:
        sql_query = "update restreg set rank= :frank where name= :name"
        print(sql_query)
        data = {
            'frank': final_rank,
            'name': search
        }

        mysql.query_db(sql_query, data)
        print("Search Successfully")
        return render_template('SearchRestoResult.html', value=res)
    except Exception as e:
        print("excpetion=", e)


@app.route('/admhome', methods=['POST'])
def adminlogin():
    input_uname = request.form['Email']
    input_password = request.form['Password']
    email_query = "SELECT * FROM admin WHERE email1 = :email and Pass = :pass"
    query_data = {'email': input_uname, 'pass': input_password}
    stored_email = mysql.query_db(email_query, query_data)

    if not EMAIL_REGEX.match(request.form['Email']):
        print("Email must be a valid email", 'error')
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
    print("signup")
    error = ""
    input_email = request.form['Email']
    email_query = "SELECT * FROM userreg WHERE email = :email_id"
    query_data = {'email_id': input_email}
    stored_email = mysql.query_db(email_query, query_data)

    age = request.form['age']

    cat = "0"

    if age <= "14":
        cat = "Children"
        print("Category Child")

    elif "15" >= age or age <= "40":
        cat = "Young"
        print("Category Young")

    else:
        cat = "Old Age"
        print("Category Old")

    print("Category=", cat)
    print (request.form['Email'])
    print (session)

    for x in request.form:
        if len(request.form[x]) < 1:
            print(x + " cannot be blank!", 'blank')
            error = "Fill all Fields"

    if len(request.form['Password']) < 5:
        print("Password must be more than 5 characters", 'pass')
        error = "Password must be greater than 5 characters"

    if not EMAIL_REGEX.match(request.form['Email']):
        print("Email must be a valid email", 'error')
        error = "Email must be a valid email"

    if stored_email:
        error = "Email already exists!"

    if error != "":
        print("error")
        return render_template('index.html', error=error)

    else:
        print("All Good!!!!", 'good')
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

        print("This email address you entered " + input_email + " is a valid email address. Thank you!")
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
    print(session['email'])

    error = None
    if not EMAIL_REGEX.match(request.form['Email']):
        print("Email must be a valid email")
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
    print("signup")
    error = ""
    input_email = request.form['Email']
    email_query = "SELECT * FROM restreg WHERE email = :email_id"
    query_data = {'email_id': input_email}
    stored_email = mysql.query_db(email_query, query_data)
    print (request.form)
    print (request.form['Email'])
    print (session)

    for x in request.form:
        if len(request.form[x]) < 1:
            print(x + " cannot be blank!", 'blank')
            error = "Fill all Fields"

    if len(request.form['Password']) < 5:
        print("Password must be more than 5 characters", 'pass')
        error = "Password must be greater than 5 characters"

    if not EMAIL_REGEX.match(request.form['Email']):
        print("Email must be a valid email", 'error')
        error = "Email must be a valid email"

    if stored_email:
        error = "Email already exists!"

    if error != "":
        print ("error")
        return render_template('index.html', error=error)

    else:
        print("All Good!!!!", 'good')
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

        print("This email address you entered " + input_email + " is a valid email address. Thank you!")
        return render_template('restaurant.html')


@app.route('/rhome', methods=['POST'])
def restolog():
    input_uname = request.form['Email']
    input_password = request.form['Password']
    email_query = "SELECT * FROM restreg WHERE email = :email and pass = :pass"
    query_data = {'email': input_uname, 'pass': input_password}
    stored_email = mysql.query_db(email_query, query_data)

    if not EMAIL_REGEX.match(request.form['Email']):
        print("Email must be a valid email", 'error')

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
    print("signup")
    error = ""
    input_email = request.form['Email']
    email_query = "SELECT * FROM book WHERE email = :email_id"
    query_data = {'email_id': input_email}
    stored_email = mysql.query_db(email_query, query_data)

    print (request.form)
    print (request.form['Email'])
    print (session)

    for x in request.form:
        if len(request.form[x]) < 1:
            print(x + " cannot be blank!", 'blank')
            error = "Fill all Fields"

    if len(request.form['Password']) < 5:
        print("Password must be more than 5 characters", 'pass')
        error = "Password must be greater than 5 characters"

    if not EMAIL_REGEX.match(request.form['Email']):
        print("Email must be a valid email", 'error')
        error = "Email must be a valid email"

    if stored_email:
        error = "Email already exists!"

    if error != "":
        print ("error")
        return render_template('radhika.html', error=error)

    else:
        print("All Good!!!!", 'good')
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

        print("This email address you entered " + input_email + " is a valid email address. Thank you!")
        return render_template('booking.html')


@app.route('/wloss', methods=['POST'])
def Weight_Loss():
    breakfastfoodseparated = []
    Lunchfoodseparated = []
    Dinnerfoodseparated = []

    breakfastfoodseparatedID = []
    LunchfoodseparatedID = []
    DinnerfoodseparatedID = []

    for i in range(len(Breakfastdata)):
        if BreakfastdataNumpy[i] == 1:
            breakfastfoodseparated.append(Food_itemsdata[i])
            breakfastfoodseparatedID.append(i)
        if LunchdataNumpy[i] == 1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if DinnerdataNumpy[i] == 1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)

    # retrieving Lunch data rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T
    # print(LunchfoodseparatedIDdata)
    val = list(np.arange(5, 15))
    Valapnd = [0] + val
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T
    # print(LunchfoodseparatedIDdata)

    # retrieving Breafast data rows by loc method
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.T
    val = list(np.arange(5, 15))
    Valapnd = [0] + val
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.T

    # retrieving Dinner Data rows by loc method
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.T
    val = list(np.arange(5, 15))
    Valapnd = [0] + val
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.T

    # calculating BMI
    age = int(request.form['age'])
    veg = float(request.form['food'])
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    bmi = weight / ((height / 100) ** 2)
    agewiseinp = 0

    for lp in range(0, 80, 20):
        test_list = np.arange(lp, lp + 20)
        for i in test_list:
            if (i == age):
                tr = round(lp / 20)
                agecl = round(lp / 20)

                # conditions
    print("Your body mass index is: ", bmi)
    if (bmi < 16):
        print("Acoording to your BMI, you are Severely Underweight")
        msg = "Acoording to your BMI, you are Severely Underweight"
        clbmi = 4
    elif (bmi >= 16 and bmi < 18.5):
        print("Acoording to your BMI, you are Underweight")
        msg = "Acoording to your BMI, you are Underweight"
        clbmi = 3
    elif (bmi >= 18.5 and bmi < 25):
        print("Acoording to your BMI, you are Healthy")
        msg = "Acoording to your BMI, you are Healthy"
        clbmi = 2
    elif (bmi >= 25 and bmi < 30):
        print("Acoording to your BMI, you are Overweight")
        msg = "Acoording to your BMI, you are Overweight"
        clbmi = 1
    elif (bmi >= 30):
        print("Acoording to your BMI, you are Severely Overweight")
        msg = "Acoording to your BMI, you are Severely Overweight"
        clbmi = 0

    # converting into numpy array
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.to_numpy()
    ti = (clbmi + agecl) / 2

    ## K-Means Based  Dinner Food
    Datacalorie = DinnerfoodseparatedIDdata[1:, 1:len(DinnerfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    XValu = np.arange(0, len(kmeans.labels_))

    # retrieving the labels for dinner food
    dnrlbl = kmeans.labels_

    ## K-Means Based  lunch Food
    Datacalorie = LunchfoodseparatedIDdata[1:, 1:len(LunchfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    XValu = np.arange(0, len(kmeans.labels_))

    # retrieving the labels for lunch food
    lnchlbl = kmeans.labels_

    ## K-Means Based  lunch Food
    Datacalorie = breakfastfoodseparatedIDdata[1:, 1:len(breakfastfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    XValu = np.arange(0, len(kmeans.labels_))

    # retrieving the labels for breakfast food
    brklbl = kmeans.labels_

    inp = []
    ## Reading of the Dataet
    datafin = pd.read_csv('nutrition_distriution.csv')

    ## train set
    dataTog = datafin.T
    bmicls = [0, 1, 2, 3, 4]
    agecls = [0, 1, 2, 3, 4]
    weightlosscat = dataTog.iloc[[1, 2, 7, 8]]
    weightlosscat = weightlosscat.T
    weightgaincat = dataTog.iloc[[0, 1, 2, 3, 4, 7, 9, 10]]
    weightgaincat = weightgaincat.T
    healthycat = dataTog.iloc[[1, 2, 3, 4, 6, 7, 9]]
    healthycat = healthycat.T
    weightlosscatDdata = weightlosscat.to_numpy()
    weightgaincatDdata = weightgaincat.to_numpy()
    healthycatDdata = healthycat.to_numpy()
    weightlosscat = weightlosscatDdata[1:, 0:len(weightlosscatDdata)]
    weightgaincat = weightgaincatDdata[1:, 0:len(weightgaincatDdata)]
    healthycat = healthycatDdata[1:, 0:len(healthycatDdata)]

    weightlossfin = np.zeros((len(weightlosscat) * 5, 6), dtype=np.float32)
    weightgainfin = np.zeros((len(weightgaincat) * 5, 10), dtype=np.float32)
    healthycatfin = np.zeros((len(healthycat) * 5, 9), dtype=np.float32)
    t = 0
    r = 0
    s = 0
    yt = []
    yr = []
    ys = []
    for zz in range(5):
        for jj in range(len(weightlosscat)):
            valloc = list(weightlosscat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightlossfin[t] = np.array(valloc)
            yt.append(brklbl[jj])
            t += 1
        for jj in range(len(weightgaincat)):
            valloc = list(weightgaincat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightgainfin[r] = np.array(valloc)
            yr.append(lnchlbl[jj])
            r += 1
        for jj in range(len(healthycat)):
            valloc = list(healthycat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            healthycatfin[s] = np.array(valloc)
            ys.append(dnrlbl[jj])
            s += 1

    X_test = np.zeros((len(weightlosscat), 6), dtype=np.float32)

    print('####################')

    # randomforest
    for jj in range(len(weightlosscat)):
        valloc = list(weightlosscat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj] = np.array(valloc) * ti

    X_train = weightlossfin  # Features
    y_train = yt  # Labels

    # Create a Gaussian Classifier
    clf = RandomForestClassifier(n_estimators=100)

    # Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train, y_train)

    # print (X_test[1])
    X_test2 = X_test
    y_pred = clf.predict(X_test)

    d1 = []
    print('SUGGESTED FOOD ITEMS ::')
    for ii in range(len(y_pred)):
        if y_pred[ii] == 2:  # weightloss
            print(Food_itemsdata[ii])
            findata = Food_itemsdata[ii]
            d1.append(findata)
            print(d1)
            if int(veg) == 1:
                datanv = ['Chicken Burger']
                for it in range(len(datanv)):
                    if findata == datanv[it]:
                        print('VegNovVeg')

    result = {'Body Mass Index': msg,

              }
    result1 = {
        'Food': d1
    }

    print('\n Thank You for taking our recommendations. :)')

    print(result)
    return render_template('thnku.html', result=result, result1=result1)


@app.route('/wgain', methods=['POST'])
def Weight_Gain():
    breakfastfoodseparated = []
    Lunchfoodseparated = []
    Dinnerfoodseparated = []

    breakfastfoodseparatedID = []
    LunchfoodseparatedID = []
    DinnerfoodseparatedID = []

    for i in range(len(Breakfastdata)):
        if BreakfastdataNumpy[i] == 1:
            breakfastfoodseparated.append(Food_itemsdata[i])
            breakfastfoodseparatedID.append(i)
        if LunchdataNumpy[i] == 1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if DinnerdataNumpy[i] == 1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)

    # retrieving rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T
    val = list(np.arange(5, 15))
    Valapnd = [0] + val
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T

    # retrieving rows by loc method
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.T
    val = list(np.arange(5, 15))
    Valapnd = [0] + val
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.T

    # retrieving rows by loc method
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.T
    val = list(np.arange(5, 15))
    Valapnd = [0] + val
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.T

    # claculating BMI
    age = int(request.form['age'])
    veg = float(request.form['food'])
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    bmi = weight / ((height / 100) ** 2)

    for lp in range(0, 80, 20):
        test_list = np.arange(lp, lp + 20)
        for i in test_list:
            if (i == age):
                tr = round(lp / 20)
                agecl = round(lp / 20)

    # conditions
    print("Your body mass index is: ", bmi)
    if (bmi < 16):
        print("Acoording to your BMI, you are Severely Underweight")
        msg = "Acoording to your BMI, you are Severely Underweight"
        clbmi = 4
    elif (bmi >= 16 and bmi < 18.5):
        print("Acoording to your BMI, you are Underweight")
        msg = "Acoording to your BMI, you are Underweight"
        clbmi = 3
    elif (bmi >= 18.5 and bmi < 25):
        print("Acoording to your BMI, you are Healthy")
        msg = "Acoording to your BMI, you are Healthy"
        clbmi = 2
    elif (bmi >= 25 and bmi < 30):
        print("Acoording to your BMI, you are Overweight")
        msg = "Acoording to your BMI, you are Overweight"
        clbmi = 1
    elif (bmi >= 30):
        print("Acoording to your BMI, you are Severely Overweight")
        msg = "Acoording to your BMI, you are Severely Overweight"
        clbmi = 0

    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.to_numpy()
    ti = (bmi + agecl) / 2

    ## K-Means Based  Dinner Food
    Datacalorie = DinnerfoodseparatedIDdata[1:, 1:len(DinnerfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    XValu = np.arange(0, len(kmeans.labels_))
    # plt.bar(XValu,kmeans.labels_)
    dnrlbl = kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")

    ## K-Means Based  lunch Food
    Datacalorie = LunchfoodseparatedIDdata[1:, 1:len(LunchfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    XValu = np.arange(0, len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    lnchlbl = kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")

    ## K-Means Based  lunch Food
    Datacalorie = breakfastfoodseparatedIDdata[1:, 1:len(breakfastfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    XValu = np.arange(0, len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    brklbl = kmeans.labels_

    # plt.title("Predicted Low-High Weigted Calorie Foods")
    inp = []
    ## Reading of the Dataet
    datafin = pd.read_csv('nutrition_distriution.csv')
    datafin.head(5)

    dataTog = datafin.T
    bmicls = [0, 1, 2, 3, 4]
    agecls = [0, 1, 2, 3, 4]
    weightlosscat = dataTog.iloc[[1, 2, 7, 8]]
    weightlosscat = weightlosscat.T
    weightgaincat = dataTog.iloc[[0, 1, 2, 3, 4, 7, 9, 10]]
    weightgaincat = weightgaincat.T
    healthycat = dataTog.iloc[[1, 2, 3, 4, 6, 7, 9]]
    healthycat = healthycat.T
    weightlosscatDdata = weightlosscat.to_numpy()
    weightgaincatDdata = weightgaincat.to_numpy()
    healthycatDdata = healthycat.to_numpy()
    weightlosscat = weightlosscatDdata[1:, 0:len(weightlosscatDdata)]
    weightgaincat = weightgaincatDdata[1:, 0:len(weightgaincatDdata)]
    healthycat = healthycatDdata[1:, 0:len(healthycatDdata)]

    weightlossfin = np.zeros((len(weightlosscat) * 5, 6), dtype=np.float32)
    weightgainfin = np.zeros((len(weightgaincat) * 5, 10), dtype=np.float32)
    healthycatfin = np.zeros((len(healthycat) * 5, 9), dtype=np.float32)
    t = 0
    r = 0
    s = 0
    yt = []
    yr = []
    ys = []
    for zz in range(5):
        for jj in range(len(weightlosscat)):
            valloc = list(weightlosscat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightlossfin[t] = np.array(valloc)
            yt.append(brklbl[jj])
            t += 1
        for jj in range(len(weightgaincat)):
            valloc = list(weightgaincat[jj])
            # print (valloc)
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightgainfin[r] = np.array(valloc)
            yr.append(lnchlbl[jj])
            r += 1
        for jj in range(len(healthycat)):
            valloc = list(healthycat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            healthycatfin[s] = np.array(valloc)
            ys.append(dnrlbl[jj])
            s += 1

    X_test = np.zeros((len(weightgaincat), 10), dtype=np.float32)

    print('####################')
    # In[287]:
    for jj in range(len(weightgaincat)):
        valloc = list(weightgaincat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj] = np.array(valloc) * ti

    X_train = weightgainfin  # Features
    y_train = yr  # Labels

    # Create a Gaussian Classifier
    clf = RandomForestClassifier(n_estimators=100)

    # Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train, y_train)

    X_test2 = X_test
    y_pred = clf.predict(X_test)

    d1 = []
    print('SUGGESTED FOOD ITEMS ::')
    for ii in range(len(y_pred)):
        if y_pred[ii] == 2:  # weightloss
            print(Food_itemsdata[ii])
            findata = Food_itemsdata[ii]
            d1.append(findata)
            print(d1)
            if int(veg) == 1:
                datanv = ['Chicken Burger']
                for it in range(len(datanv)):
                    if findata == datanv[it]:
                        print('VegNovVeg')

    result = {'Body Mass Index': msg,

              }
    result1 = {
        'Food': d1
    }

    print('\n Thank You for taking our recommendations. :)')

    print(result)
    return render_template('thnku.html', result=result, result1=result1)


@app.route('/helthy', methods=['POST'])
def Healthy():
    breakfastfoodseparated = []
    Lunchfoodseparated = []
    Dinnerfoodseparated = []

    breakfastfoodseparatedID = []
    LunchfoodseparatedID = []
    DinnerfoodseparatedID = []

    for i in range(len(Breakfastdata)):
        if BreakfastdataNumpy[i] == 1:
            breakfastfoodseparated.append(Food_itemsdata[i])
            breakfastfoodseparatedID.append(i)
        if LunchdataNumpy[i] == 1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if DinnerdataNumpy[i] == 1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)

    # retrieving rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T
    val = list(np.arange(5, 15))
    Valapnd = [0] + val
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.T

    # retrieving rows by loc method
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.T
    val = list(np.arange(5, 15))
    Valapnd = [0] + val
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.T

    # retrieving rows by loc method
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.T
    val = list(np.arange(5, 15))
    Valapnd = [0] + val
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.T

    # claculating BMI
    age = int(request.form['age'])
    veg = float(request.form['food'])
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    bmi = weight / ((height / 100) ** 2)

    for lp in range(0, 80, 20):
        test_list = np.arange(lp, lp + 20)
        for i in test_list:
            if (i == age):
                tr = round(lp / 20)
                agecl = round(lp / 20)

    # conditions
    print("Your body mass index is: ", bmi)
    if (bmi < 16):
        print("Acoording to your BMI, you are Severely Underweight")
        msg = "Acoording to your BMI, you are Severely Underweight"
        clbmi = 4
    elif (bmi >= 16 and bmi < 18.5):
        print("Acoording to your BMI, you are Underweight")
        msg = "Acoording to your BMI, you are Underweight"
        clbmi = 3
    elif (bmi >= 18.5 and bmi < 25):
        print("Acoording to your BMI, you are Healthy")
        msg = "Acoording to your BMI, you are Healthy"
        clbmi = 2
    elif (bmi >= 25 and bmi < 30):
        print("Acoording to your BMI, you are Overweight")
        msg = "Acoording to your BMI, you are Overweight"
        clbmi = 1
    elif (bmi >= 30):
        print("Acoording to your BMI, you are Severely Overweight")
        msg = "Acoording to your BMI, you are Severely Overweight"
        clbmi = 0

    DinnerfoodseparatedIDdata = DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata = LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata = breakfastfoodseparatedIDdata.to_numpy()
    ti = (bmi + agecl) / 2

    Datacalorie = DinnerfoodseparatedIDdata[1:, 1:len(DinnerfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    XValu = np.arange(0, len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    dnrlbl = kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")

    Datacalorie = LunchfoodseparatedIDdata[1:, 1:len(LunchfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    # print ('## Prediction Result ##')
    # print(kmeans.labels_)
    XValu = np.arange(0, len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    lnchlbl = kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")

    Datacalorie = breakfastfoodseparatedIDdata[1:, 1:len(breakfastfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    XValu = np.arange(0, len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    brklbl = kmeans.labels_
    # print (len(brklbl))
    # plt.title("Predicted Low-High Weigted Calorie Foods")
    inp = []
    ## Reading of the Dataet
    datafin = pd.read_csv('nutrition_distriution.csv')
    datafin.head(5)

    dataTog = datafin.T
    bmicls = [0, 1, 2, 3, 4]
    agecls = [0, 1, 2, 3, 4]
    weightlosscat = dataTog.iloc[[1, 2, 7, 8]]
    weightlosscat = weightlosscat.T
    weightgaincat = dataTog.iloc[[0, 1, 2, 3, 4, 7, 9, 10]]
    weightgaincat = weightgaincat.T
    healthycat = dataTog.iloc[[1, 2, 3, 4, 6, 7, 9]]
    healthycat = healthycat.T
    weightlosscatDdata = weightlosscat.to_numpy()
    weightgaincatDdata = weightgaincat.to_numpy()
    healthycatDdata = healthycat.to_numpy()
    weightlosscat = weightlosscatDdata[1:, 0:len(weightlosscatDdata)]
    weightgaincat = weightgaincatDdata[1:, 0:len(weightgaincatDdata)]
    healthycat = healthycatDdata[1:, 0:len(healthycatDdata)]

    weightlossfin = np.zeros((len(weightlosscat) * 5, 6), dtype=np.float32)
    weightgainfin = np.zeros((len(weightgaincat) * 5, 10), dtype=np.float32)
    healthycatfin = np.zeros((len(healthycat) * 5, 9), dtype=np.float32)
    t = 0
    r = 0
    s = 0
    yt = []
    yr = []
    ys = []
    for zz in range(5):
        for jj in range(len(weightlosscat)):
            valloc = list(weightlosscat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightlossfin[t] = np.array(valloc)
            yt.append(brklbl[jj])
            t += 1
        for jj in range(len(weightgaincat)):
            valloc = list(weightgaincat[jj])
            # print (valloc)
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightgainfin[r] = np.array(valloc)
            yr.append(lnchlbl[jj])
            r += 1
        for jj in range(len(healthycat)):
            valloc = list(healthycat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            healthycatfin[s] = np.array(valloc)
            ys.append(dnrlbl[jj])
            s += 1

    X_test = np.zeros((len(healthycat) * 5, 9), dtype=np.float32)

    for jj in range(len(healthycat)):
        valloc = list(healthycat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj] = np.array(valloc) * ti

    X_train = healthycatfin  # Features
    y_train = ys  # Labels

    # Create a Gaussian Classifier
    clf = RandomForestClassifier(n_estimators=100)

    # Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train, y_train)

    X_test2 = X_test
    y_pred = clf.predict(X_test)

    d1 = []
    print('SUGGESTED FOOD ITEMS ::')
    for ii in range(len(y_pred)):
        if y_pred[ii] == 2:  # weightloss
            print(Food_itemsdata[ii])
            findata = Food_itemsdata[ii]
            d1.append(findata)
            print(d1)
            if int(veg) == 1:
                datanv = ['Chicken Burger' 'Tuna Fish', 'Chicken Sandwich']
                for it in range(len(datanv)):
                    if findata == datanv[it]:
                        print('VegNovVeg')

    result = {'Body Mass Index': msg,

              }
    result1 = {
        'Food': d1
    }

    print('\n Thank You for taking our recommendations. :)')

    print(result)
    return render_template('thnku.html', result=result, result1=result1)


if __name__ == "__main__":
    app.run(debug=True)
