from flask import Flask, render_template, url_for, redirect, request
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import json
import pyodbc

app = Flask(__name__)
CORS(app)

# server = 'DESKTOP-6CP0SSO' 
#     database = 'TCC2' 
#     username = 'rafael'
#     password = 'root'
#     cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
#     cursor = cnxn.cursor()

class Consulta:
    def __init__(self, nomePaciente, convenio, servico,datahora,valor):
        self.nomePaciente = nomePaciente
        self.convenio = convenio
        self.servico = servico
        self.datahora = datahora
        self.valor = valor

listaConsultas = []

@app.route('/', methods=['GET','POST'])
def home():
    params = {
        'title':'Sistema Odonto Teste'
    }

    server = 'DESKTOP-6CP0SSO' 
    database = 'TCC2' 
    username = 'rafael'
    password = 'root'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    listaHome = cursor.execute("SELECT NM_PAC,p.CONVENIO,DS_SERV,c.DT_CONSULTA, c.VALOR_CONSULTA FROM F_CONSULTAS C INNER JOIN D_PACIENTES P ON P.ID_PACIENTE = C.ID_PACIENTE INNER JOIN D_SERVICOS S ON C.ID_SERVICO = S.ID_SERVICO INNER JOIN	D_CONVENIOS con ON con.ID_CONVENIO= c.ID_CONVENIO ORDER BY C.DT_CONSULTA DESC")

    for item in listaHome:  
        consulta = Consulta(item.NM_PAC, item.CONVENIO, item.DS_SERV,item.DT_CONSULTA,item.VALOR_CONSULTA)
        listaConsultas.append(consulta)

    return render_template('rafa.html', params=params, consultas = listaConsultas)

@app.route('/consultas', methods=['POST'])
def consultas():
    print('entrou metodo')

    server = 'DESKTOP-6CP0SSO' 
    database = 'TCC2' 
    username = 'rafael'
    password = 'root'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    print('conectou banco ')
    idConsulta = cursor.execute("SELECT MAX(ID_CONSULTA) FROM F_CONSULTAS").fetchval() 
    idConsulta = idConsulta + 1
    print('pegou id')
    print(idConsulta)

    nomePaciente = request.form['paciente']
    print(nomePaciente)
    #VERIFICAR SE NOME EXISTE NA BASE 
    #SE SIM BUSCAR ID E GUARDAR, SE NÃO PRINTA MENSAGEM 
    
    count = cursor.execute("SELECT COUNT(*) FROM D_PACIENTES WHERE NM_PAC LIKE ?",nomePaciente).fetchval()
    if count>=1:
        idPac = cursor.execute("SELECT ID_PACIENTE FROM D_PACIENTES WHERE NM_PAC LIKE ?",nomePaciente).fetchval()
    print('pegou nome paciente - acessou form')
    
    print(idPac)
    convenio = request.form['convenio']
    count = cursor.execute("SELECT COUNT(*) FROM D_CONVENIOS WHERE DS_CONV LIKE ?",convenio).fetchval()
    if count>=1:
        idConvenio = cursor.execute("SELECT ID_CONVENIO FROM D_CONVENIOS WHERE DS_CONV LIKE ?",convenio).fetchval()

    servico = request.form['servico']
    count = cursor.execute("SELECT COUNT(*) FROM D_SERVICOS WHERE DS_SERV LIKE ?",servico).fetchval()
    if count>=1:
        idServico = cursor.execute("SELECT ID_SERVICO FROM D_SERVICOS WHERE DS_SERV LIKE ?",servico).fetchval()

    datahora = request.form['datahora']
    valor = request.form['valor']

    p = [idConsulta, 1, idConvenio, idServico, datahora, valor, idPac]
    print(p)
    cursor.execute("INSERT INTO F_CONSULTAS (ID_CONSULTA, ID_DENTISTA, ID_CONVENIO, ID_SERVICO, DT_CONSULTA,VALOR_CONSULTA, ID_PACIENTE) VALUES(?,?,?,?,?,?,?)",idConsulta, 1, idConvenio, idServico, datahora, 0, idPac)
    cursor.commit()
    print('fez insert')
    #return render_template('rafa.html')
    return redirect('/')
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
    










########################################################################################################
# nomePaciente = request.form['paciente']
    # convenio = request.form['convenio']
    # servico = request.form['servico']
    # datahora = request.form['datahora']
    # valor = request.form['valor']
    # consulta = Consulta(nomePaciente,convenio,servico,datahora,valor)

    #listaConsultas.append(consulta)

    #cursor.execute("INSERT INTO DW_TCC.F_CONSULTAS (Name, ProductNumber, StandardCost, ListPrice, SellStartDate) OUTPUT INSERTED.ProductID VALUES ('SQL Server Express New 20', 'SQLEXPRESS New 20', 0, 0, CURRENT_TIMESTAMP )") 
    

    # cursor.execute("SELECT @@version;") 
    # row = cursor.fetchone() ,,,,,,,,,,,,,,,,,,,,,,
    # while row: 
    #     print (row[0] )
    #     row = cursor.fetchone()


    # while row: 
    #     print ('Inserted Product key is ' + str(row[0]))
    #     row = cursor.fetchone()
    #print(consulta)