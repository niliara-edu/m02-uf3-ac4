# -*- coding: utf-8 -*-
"""
Created on February 2023

@author: Albert ETPX
"""

# Importación de módulos externos
import mysql.connector
from flask import Flask,render_template,request;

# Funciones de backend #############################################################################

# connectBD: conecta a la base de datos users en MySQL
def connectBD():
    db = mysql.connector.connect(
        host = "localhost",
        user = "user01",
        passwd = "admin",
        database = "users"
    )
    return db

# initBD: crea una tabla en la BD users, con un registro, si está vacía
def initBD():
    bd=connectBD()
    cursor=bd.cursor()
    
    # cursor.execute("DROP TABLE IF EXISTS users;")
    # Operación de creación de la tabla users (si no existe en BD)
    query="CREATE TABLE IF NOT EXISTS users(\
            user varchar(30) primary key,\
            password varchar(30),\
            name varchar(30), \
            surname1 varchar(30), \
            surname2 varchar(30), \
            age integer, \
            gender enum('H','D','NS/NC')); "
    cursor.execute(query)
            
    # Operación de inicialización de la tabla users (si está vacía)
    query="SELECT count(*) FROM users;"
    cursor.execute(query)
    count = cursor.fetchall()[0][0]
    if(count == 0):
        query = "INSERT INTO users \
            VALUES('user01','admin','Nil','Pernil','Cocodril',69,'H');"
        cursor.execute(query)

    bd.commit()
    bd.close()
    return

# checkUser: comprueba si el par user-contraseña existe en la BD
def checkUser(user,password):
    bd=connectBD()
    cursor=bd.cursor()

    query="""SELECT user,name,surname1,surname2,age,gender
    FROM users WHERE user=%s AND password=%s"""
    values = (user, password)
    cursor.execute(query, values)
    userData = cursor.fetchall()
    bd.close()
    
    if userData == []:
        return False
    else:
        return userData[0]

# cresteUser: crea un nuevo user en la BD
# Secuencia principal: configuración de la aplicación web ##########################################
# Instanciación de la aplicación web Flask
app = Flask(__name__)

# Declaración de rutas de la aplicación web
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    initBD()
    return render_template("login.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/newUser",methods=('GET', 'POST'))
def newUser():
    if request.method == ('POST'):
        formData = request.form
        user=formData['user']
        password=formData['password']
        name=formData['name']
        surname1=formData['surname1']
        surname2=formData['surname2']
        age=formData['age']
        gender=formData['gender']
        createUser(user,password,name,surname1,surname2,age,gender)    
        return render_template("home.html")

def createUser(user,password,name,surname1,surname2,age,gender):
    bd=connectBD()
    cursor=bd.cursor()
    query = f"INSERT INTO users \
            VALUES(%s,%s,%s,%s,%s,%s,%s);"
    age=int(age)
    values=(user,password,name,surname1,surname2,age,gender)
    print(type(user))
    print(type(age))
    cursor.execute(query,values)
    bd.commit()
    bd.close()
    return



@app.route("/results",methods=('GET', 'POST'))
def results():
    if request.method == ('POST'):
        formData = request.form
        user=formData['user']
        password=formData['password']
        userData = checkUser(user,password)

        if userData == False:
            return render_template("results.html",login=False)
        else:
            return render_template("results.html",login=True,userData=userData)
        
# Configuración y arranque de la aplicación web
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host='localhost', port=5000, debug=True)
