from flask import Flask, render_template, url_for, redirect, request
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import json
import pyodbc

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    params = {
        'title':'Sistema Odonto Teste'
    }
    return render_template('rafa.html', params=params)

@app.route('/consultas', methods=['GET','POST'])
def consultas():
    params = {
        'title':'Sistema Odonto Teste'
    }

    server = 'DESKTOP-JCQQMHI/SQLEXPRESS' 
    database = 'DW_TCC' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database)
    cursor = cnxn.cursor()

    cursor.execute("INSERT INTO DW_TCC.F_CONSULTAS (Name, ProductNumber, StandardCost, ListPrice, SellStartDate) OUTPUT INSERTED.ProductID VALUES ('SQL Server Express New 20', 'SQLEXPRESS New 20', 0, 0, CURRENT_TIMESTAMP )") 
    

    # cursor.execute("SELECT @@version;") 
    # row = cursor.fetchone() 
    # while row: 
    #     print (row[0] )
    #     row = cursor.fetchone()


    # while row: 
    #     print ('Inserted Product key is ' + str(row[0]))
    #     row = cursor.fetchone()

    return render_template('rafa.html', params=params)

@app.route('/dentistas', methods=['POST','GET'])
def dentistas():
    result = {}

    if request.method == 'POST':
        result = request.form

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-JCQQMHI/SQLEXPRESS;DATABASE=DW_TCC')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO DW_TCC (CRO, EMAIL_DENT) VALUES (1234,'USER@USER.COM')")
    cursor.commit()
    
    title = 'Cadastro - Dentistas'

    # params = {
    #     'title':'Cadastro - Dentistas'
    # }

    return render_template('dentistas.html', result=result, title=title)
    
@app.route('/pacientes')
def pacientes():
    return render_template('pacientes.html')

@app.route('/convenios')
def convenios():
    return render_template('convenios.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

if __name__ == '__main__':
    app.run(debug=True)
    