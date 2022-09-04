from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pyautogui

username = ""
password = ""

app = Flask(__name__)

# Tela de Login-------------------------------------------------------------------

@app.route("/loginb", methods=["GET", "POST"])
def loginb():

    global username
    username = request.form.get("username")
    global password
    password = request.form.get("password")
    global resp
    resp = ""

    if (username is None) or (password is None):
        pass
    else:
        url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
        headers = {'content-type': 'text/xml'}
        body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CheckUser xmlns="http://sisteplant.com/">
      <user>""" + username + """</user>
      <password>""" + password + """</password>
      <company>MASTER2</company>
    </CheckUser>
  </soap:Body>
</soap:Envelope>"""

        response = requests.post(url, data=body, headers=headers)
        soup = BeautifulSoup(response.content, 'xml')
        resp = soup.find_all('CheckUserResult')[0].text
        print(resp)

    if resp == "OK":
        return servicos()
    elif resp == "":
        pass
    else:
        pyautogui.alert("Erro. Por favor, verifique seu login / senha.")

    return render_template("loginb.html")


# Tela de Serviços-------------------------------------------------------------------

@app.route("/servicos", methods=["GET", "POST"])
def servicos():
    global servico
    servico = request.form.get("servico")

    if (servico is None):
        pass
    else:
        return render_template(servico.lower() + ".html")

    return render_template("servicos.html")

# Tela de Serviços mens001 -------------------------------------------------------------------

mens001_quant = ""
mens001_colMat = ""
mens001_autent = ""
mens001_outR = ""

@app.route("/mens001", methods = ["GET", "POST"])
def mens001():

    global mens001_quant
    global mens001_colMat
    global mens001_autent
    global mens001_outR

    mens001_quant = request.form.get("mens001_quant")
    print(mens001_colMat)

    mens001_colMat = request.form.get("mens001_colMat")
    print(mens001_colMat)

    mens001_autent = request.form.get("mens001_autent")
    print(mens001_autent)

    mens001_outR = request.form.get("mens001_outR")
    print(mens001_outR)

    if mens002_quant == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens001.html")
    else:
        return render_template("login.html")

# Tela de Serviços mens002 -------------------------------------------------------------------

mens002_quant = ""
mens002_colMat = ""
mens002_empR = ""
mens002_endR = ""
mens002_baiR = ""
mens002_cidR = ""
mens002_estR = ""
mens002_cepR = ""
mens002_nomD = ""
mens002_cepD = ""
mens002_endD = ""
mens002_baiD = ""
mens002_cidD = ""
mens002_estD = ""
mens002_telD = ""
mens002_numD = ""

@app.route("/mens002", methods=["GET", "POST"])
def mens002():

    global mens002_quant
    global mens002_colMat
    global mens002_empR
    global mens002_endR
    global mens002_baiR
    global mens002_cidR
    global mens002_estR
    global mens002_cepR
    global mens002_nomD
    global mens002_cepD
    global mens002_endD
    global mens002_baiD
    global mens002_cidD
    global mens002_estD
    global mens002_telD
    global mens002_numD

    mens002_quant = request.form.get("mens002_quant")
    mens002_quant = request.form.get("mens002_quant")
    mens002_colMat = request.form.get("mens002_colMat")
    mens002_empR = request.form.get("mens002_empR")
    mens002_endR = request.form.get("mens002_endR")
    mens002_baiR = request.form.get("mens002_baiR")
    mens002_cidR = request.form.get("mens002_cidR")
    mens002_estR = request.form.get("mens002_estR")
    mens002_cepR = request.form.get("mens002_cepR")
    mens002_nomD = request.form.get("mens002_nomD")
    mens002_cepD = request.form.get("mens002_cepD")
    mens002_endD = request.form.get("mens002_endD")
    mens002_baiD = request.form.get("mens002_baiD")
    mens002_cidD = request.form.get("mens002_cidD")
    mens002_estD = request.form.get("mens002_estD")
    mens002_telD = request.form.get("mens002_telD")
    mens002_numD = request.form.get("mens002_numD")


    if mens002_quant == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens002.html")
    else:
        return render_template("login.html")


# Tela de Serviços mens003 -------------------------------------------------------------------

mens003_endD = ""
mens003_baiD = ""
mens003_numD = ""


@app.route("/mens003", methods=["GET", "POST"])
def mens003():

    global mens003_endD
    global mens003_baiD
    global mens003_numD

    mens003_endD = request.form.get("mens003_endD")
    mens003_baiD = request.form.get("mens003_baiD")
    mens003_numD = request.form.get("mens003_numD")

    if mens003_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens003.html")
    else:
        return render_template("login.html")


# Tela de Serviços mens004 -------------------------------------------------------------------

mens004_tipEnv = ""
mens004_tipPrd = ""
mens004_quant = ""
mens004_colMat = ""
mens004_perEnt = ""
mens004_pesoKG = ""
mens004_qbr = ""
mens004_empE = ""
mens004_empR = ""
mens004_endR = ""
mens004_baiR = ""
mens004_cidR = ""
mens004_estR = ""
mens004_cepR = ""
mens004_nomD = ""
mens004_cepD = ""
mens004_endD = ""
mens004_baiD = ""
mens004_cidD = ""
mens004_estD = ""
mens004_telD = ""
mens004_numD = ""
mens004_valor = ""
mens004_codProj = ""



@app.route("/mens004", methods=["GET", "POST"])
def mens004():
    global mens004_tipEnv
    global mens004_tipPrd
    global mens004_quant
    global mens004_colMat
    global mens004_perEnt
    global mens004_pesoKG
    global mens004_qbr
    global mens004_empE
    global mens004_empR
    global mens004_endR
    global mens004_baiR
    global mens004_cidR
    global mens004_estR
    global mens004_cepR
    global mens004_nomD
    global mens004_cepD
    global mens004_endD
    global mens004_baiD
    global mens004_cidD
    global mens004_estD
    global mens004_telD
    global mens004_numD
    global mens004_valor
    global mens004_codProj

    mens004_tipEnv = request.form.get("mens004_tipEnv")
    mens004_tipPrd = request.form.get("mens004_tipPrd")
    mens004_quant = request.form.get("mens004_quant")
    mens004_colMat = request.form.get("mens004_colMat")
    mens004_perEnt = request.form.get("mens004_perEnt")
    mens004_pesoKG = request.form.get("mens004_pesoKG")
    mens004_qbr = request.form.get("mens004_qbr")
    mens004_empE = request.form.get("mens004_empE")
    mens004_empR = request.form.get("mens004_empR")
    mens004_endR = request.form.get("mens004_endR")
    mens004_baiR = request.form.get("mens004_baiR")
    mens004_cidR = request.form.get("mens004_cidR")
    mens004_estR = request.form.get("mens004_estR")
    mens004_cepR = request.form.get("mens004_cepR")
    mens004_nomD = request.form.get("mens004_nomD")
    mens004_cepD = request.form.get("mens004_cepD")
    mens004_endD = request.form.get("mens004_endD")
    mens004_baiD = request.form.get("mens004_baiD")
    mens004_cidD = request.form.get("mens004_cidD")
    mens004_estD = request.form.get("mens004_estD")
    mens004_telD = request.form.get("mens004_telD")
    mens004_numD = request.form.get("mens004_numD")
    mens004_valor = request.form.get("mens004_valor")
    mens004_codProj = request.form.get("mens004_codProj")

    if mens004_endD == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens004.html")
    else:
        return render_template("login.html")



# Tela de Serviços mens005 -------------------------------------------------------------------

mens005_tipEnv = ""
mens005_tipPrd = ""
mens005_quant = ""
mens005_colMat = ""
mens005_pesoKG = ""
mens005_empE = ""
mens005_empR = ""
mens005_endR = ""
mens005_baiR = ""
mens005_cidR = ""
mens005_estR = ""
mens005_cepR = ""
mens005_nomD = ""
mens005_cepD = ""
mens005_endD = ""
mens005_baiD = ""
mens005_cidD = ""
mens005_estD = ""
mens005_telD = ""
mens005_numD = ""
mens005_valor = ""
mens005_codProj = ""

@app.route("/mens005", methods=["GET", "POST"])
def mens005():
    global mens005_tipEnv
    global mens005_tipPrd
    global mens005_quant
    global mens005_colMat
    global mens005_pesoKG
    global mens005_empE
    global mens005_empR
    global mens005_endR
    global mens005_baiR
    global mens005_cidR
    global mens005_estR
    global mens005_cepR
    global mens005_nomD
    global mens005_cepD
    global mens005_endD
    global mens005_baiD
    global mens005_cidD
    global mens005_estD
    global mens005_telD
    global mens005_numD
    global mens005_valor
    global mens005_codProj

    mens005_tipEnv = request.form.get("mens005_tipEnv")
    mens005_tipPrd = request.form.get("mens005_tipPrd")
    mens005_quant = request.form.get("mens005_quant")
    mens005_colMat = request.form.get("mens005_colMat")
    mens005_pesoKG = request.form.get("mens005_pesoKG")
    mens005_empE = request.form.get("mens005_empE")
    mens005_empR = request.form.get("mens005_empR")
    mens005_endR = request.form.get("mens005_endR")
    mens005_baiR = request.form.get("mens005_baiR")
    mens005_cidR = request.form.get("mens005_cidR")
    mens005_estR = request.form.get("mens005_estR")
    mens005_cepR = request.form.get("mens005_cepR")
    mens005_nomD = request.form.get("mens005_nomD")
    mens005_cepD = request.form.get("mens005_cepD")
    mens005_endD = request.form.get("mens005_endD")
    mens005_baiD = request.form.get("mens005_baiD")
    mens005_cidD = request.form.get("mens005_cidD")
    mens005_estD = request.form.get("mens005_estD")
    mens005_telD = request.form.get("mens005_telD")
    mens005_numD = request.form.get("mens005_numD")
    mens005_valor = request.form.get("mens005_valor")
    mens005_codProj = request.form.get("mens005_codProj")

    if mens005_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens005.html")
    else:
        return render_template("login.html")



# Tela de Serviços mens006 -------------------------------------------------------------------

mens006_tipEnv = ""
mens006_tipPrd = ""
mens006_quant = ""
mens006_colMat = ""
mens006_pesoKG = ""
mens006_qbr = ""
mens006_empE = ""
mens006_empR = ""
mens006_endR = ""
mens006_baiR = ""
mens006_cidR = ""
mens006_estR = ""
mens006_cepR = ""
mens006_nomD = ""
mens006_cepD = ""
mens006_endD = ""
mens006_baiD = ""
mens006_cidD = ""
mens006_estD = ""
mens006_telD = ""
mens006_numD = ""
mens006_valor = ""
mens006_codProj = ""


@app.route("/mens006", methods=["GET", "POST"])
def mens006():
    global mens006_tipEnv
    global mens006_tipPrd
    global mens006_quant
    global mens006_colMat
    global mens006_pesoKG
    global mens006_qbr
    global mens006_empE
    global mens006_empR
    global mens006_endR
    global mens006_baiR
    global mens006_cidR
    global mens006_estR
    global mens006_cepR
    global mens006_nomD
    global mens006_cepD
    global mens006_endD
    global mens006_baiD
    global mens006_cidD
    global mens006_estD
    global mens006_telD
    global mens006_numD
    global mens006_valor
    global mens006_codProj

    mens006_tipEnv = request.form.get("mens006_tipEnv")
    mens006_tipPrd = request.form.get("mens006_tipPrd")
    mens006_quant = request.form.get("mens006_quant")
    mens006_colMat = request.form.get("mens006_colMat")
    mens006_pesoKG = request.form.get("mens006_pesoKG")
    mens006_qbr = request.form.get("mens006_qbr")
    mens006_empE = request.form.get("mens006_empE")
    mens006_empR = request.form.get("mens006_empR")
    mens006_endR = request.form.get("mens006_endR")
    mens006_baiR = request.form.get("mens006_baiR")
    mens006_cidR = request.form.get("mens006_cidR")
    mens006_estR = request.form.get("mens006_estR")
    mens006_cepR = request.form.get("mens006_cepR")
    mens006_nomD = request.form.get("mens006_nomD")
    mens006_cepD = request.form.get("mens006_cepD")
    mens006_endD = request.form.get("mens006_endD")
    mens006_baiD = request.form.get("mens006_baiD")
    mens006_cidD = request.form.get("mens006_cidD")
    mens006_estD = request.form.get("mens006_estD")
    mens006_telD = request.form.get("mens006_telD")
    mens006_numD = request.form.get("mens006_numD")
    mens006_valor = request.form.get("mens006_valor")
    mens006_codProj = request.form.get("mens006_codProj")

    if mens006_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens006.html")
    else:
        return render_template("login.html")


# Tela de Serviços mens007 -------------------------------------------------------------------

mens007_tipEnv = ""
mens007_tipPrd = ""
mens007_quant = ""
mens007_colMat = ""
mens007_perEnt = ""
mens007_pesoKG = ""
mens007_empE = ""
mens007_empR = ""
mens007_endR = ""
mens007_baiR = ""
mens007_cidR = ""
mens007_estR = ""
mens007_cepR = ""
mens007_nomD = ""
mens007_cepD = ""
mens007_endD = ""
mens007_baiD = ""
mens007_cidD = ""
mens007_estD = ""
mens007_telD = ""
mens007_numD = ""
mens007_valor = ""
mens007_codProj = ""

@app.route("/mens007", methods=["GET", "POST"])
def mens007():
    global mens007_tipEnv
    global mens007_tipPrd
    global mens007_quant
    global mens007_colMat
    global mens007_perEnt
    global mens007_pesoKG
    global mens007_empE
    global mens007_empR
    global mens007_endR
    global mens007_baiR
    global mens007_cidR
    global mens007_estR
    global mens007_cepR
    global mens007_nomD
    global mens007_cepD
    global mens007_endD
    global mens007_baiD
    global mens007_cidD
    global mens007_estD
    global mens007_telD
    global mens007_numD
    global mens007_valor
    global mens007_codProj

    mens007_tipEnv = request.form.get("mens007_tipEnv")
    mens007_tipPrd = request.form.get("mens007_tipPrd")
    mens007_quant = request.form.get("mens007_quant")
    mens007_colMat = request.form.get("mens007_colMat")
    mens007_perEnt = request.form.get("mens007_perEnt")
    mens007_pesoKG = request.form.get("mens007_pesoKG")
    mens007_empE = request.form.get("mens007_empE")
    mens007_empR = request.form.get("mens007_empR")
    mens007_endR = request.form.get("mens007_endR")
    mens007_baiR = request.form.get("mens007_baiR")
    mens007_cidR = request.form.get("mens007_cidR")
    mens007_estR = request.form.get("mens007_estR")
    mens007_cepR = request.form.get("mens007_cepR")
    mens007_nomD = request.form.get("mens007_nomD")
    mens007_cepD = request.form.get("mens007_cepD")
    mens007_endD = request.form.get("mens007_endD")
    mens007_baiD = request.form.get("mens007_baiD")
    mens007_cidD = request.form.get("mens007_cidD")
    mens007_estD = request.form.get("mens007_estD")
    mens007_telD = request.form.get("mens007_telD")
    mens007_numD = request.form.get("mens007_numD")
    mens007_valor = request.form.get("mens007_valor")
    mens007_codProj = request.form.get("mens007_codProj")

    if mens007_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens007.html")
    else:
        return render_template("login.html")


# Tela de Serviços mens008 -------------------------------------------------------------------

mens008_tipEnv = ""
mens008_tipPrd = ""
mens008_quant = ""
mens008_colMat = ""
mens008_pesoKG = ""
mens008_qbr = ""
mens008_empE = ""
mens008_empR = ""
mens008_endR = ""
mens008_baiR = ""
mens008_cidR = ""
mens008_estR = ""
mens008_cepR = ""
mens008_nomD = ""
mens008_cepD = ""
mens008_endD = ""
mens008_baiD = ""
mens008_cidD = ""
mens008_estD = ""
mens008_telD = ""
mens008_numD = ""
mens008_valor = ""
mens008_codProj = ""



@app.route("/mens008", methods=["GET", "POST"])
def mens008():
    global mens008_tipEnv
    global mens008_tipPrd
    global mens008_quant
    global mens008_colMat
    global mens008_pesoKG
    global mens008_qbr
    global mens008_empE
    global mens008_empR
    global mens008_endR
    global mens008_baiR
    global mens008_cidR
    global mens008_estR
    global mens008_cepR
    global mens008_nomD
    global mens008_cepD
    global mens008_endD
    global mens008_baiD
    global mens008_cidD
    global mens008_estD
    global mens008_telD
    global mens008_numD
    global mens008_valor
    global mens008_codProj

    mens008_tipEnv = request.form.get("mens008_tipEnv")
    mens008_tipPrd = request.form.get("mens008_tipPrd")
    mens008_quant = request.form.get("mens008_quant")
    mens008_colMat = request.form.get("mens008_colMat")
    mens008_pesoKG = request.form.get("mens008_pesoKG")
    mens008_qbr = request.form.get("mens008_qbr")
    mens008_empE = request.form.get("mens008_empE")
    mens008_empR = request.form.get("mens008_empR")
    mens008_endR = request.form.get("mens008_endR")
    mens008_baiR = request.form.get("mens008_baiR")
    mens008_cidR = request.form.get("mens008_cidR")
    mens008_estR = request.form.get("mens008_estR")
    mens008_cepR = request.form.get("mens008_cepR")
    mens008_nomD = request.form.get("mens008_nomD")
    mens008_cepD = request.form.get("mens008_cepD")
    mens008_endD = request.form.get("mens008_endD")
    mens008_baiD = request.form.get("mens008_baiD")
    mens008_cidD = request.form.get("mens008_cidD")
    mens008_estD = request.form.get("mens008_estD")
    mens008_telD = request.form.get("mens008_telD")
    mens008_numD = request.form.get("mens008_numD")
    mens008_valor = request.form.get("mens008_valor")
    mens008_codProj = request.form.get("mens008_codProj")

    if mens008_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens008.html")
    else:
        return render_template("login.html")


# Tela de Serviços mens006 -------------------------------------------------------------------

mens009_tipEnv = ""
mens009_tipPrd = ""
mens009_quant = ""
mens009_colMat = ""
mens009_perEnt = ""
mens009_pesoKG = ""
mens009_empE = ""
mens009_empR = ""
mens009_endR = ""
mens009_baiR = ""
mens009_cidR = ""
mens009_estR = ""
mens009_cepR = ""
mens009_nomD = ""
mens009_cepD = ""
mens009_endD = ""
mens009_baiD = ""
mens009_cidD = ""
mens009_estD = ""
mens009_telD = ""
mens009_numD = ""
mens009_valor = ""
mens009_codProj = ""

@app.route("/mens009", methods=["GET", "POST"])
def mens009():
    global mens009_tipEnv
    global mens009_tipPrd
    global mens009_quant
    global mens009_colMat
    global mens009_perEnt
    global mens009_pesoKG
    global mens009_empE
    global mens009_empR
    global mens009_endR
    global mens009_baiR
    global mens009_cidR
    global mens009_estR
    global mens009_cepR
    global mens009_nomD
    global mens009_cepD
    global mens009_endD
    global mens009_baiD
    global mens009_cidD
    global mens009_estD
    global mens009_telD
    global mens009_numD
    global mens009_valor
    global mens009_codProj

    mens009_tipEnv = request.form.get("mens009_tipEnv")
    mens009_tipPrd = request.form.get("mens009_tipPrd")
    mens009_quant = request.form.get("mens009_quant")
    mens009_colMat = request.form.get("mens009_colMat")
    mens009_perEnt = request.form.get("mens009_perEnt")
    mens009_pesoKG = request.form.get("mens009_pesoKG")
    mens009_empE = request.form.get("mens009_empE")
    mens009_empR = request.form.get("mens009_empR")
    mens009_endR = request.form.get("mens009_endR")
    mens009_baiR = request.form.get("mens009_baiR")
    mens009_cidR = request.form.get("mens009_cidR")
    mens009_estR = request.form.get("mens009_estR")
    mens009_cepR = request.form.get("mens009_cepR")
    mens009_nomD = request.form.get("mens009_nomD")
    mens009_cepD = request.form.get("mens009_cepD")
    mens009_endD = request.form.get("mens009_endD")
    mens009_baiD = request.form.get("mens009_baiD")
    mens009_cidD = request.form.get("mens009_cidD")
    mens009_estD = request.form.get("mens009_estD")
    mens009_telD = request.form.get("mens009_telD")
    mens009_numD = request.form.get("mens009_numD")
    mens009_valor = request.form.get("mens009_valor")
    mens009_codProj = request.form.get("mens009_codProj")

    if mens009_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens009.html")
    else:
        return render_template("login.html")



# Tela de Serviços mens010 -------------------------------------------------------------------

mens010_tipEnv = ""
mens010_tipPrd = ""
mens010_quant = ""
mens010_colMat = ""
mens010_pesoKG = ""
mens010_qbr = ""
mens010_empE = ""
mens010_empR = ""
mens010_endR = ""
mens010_baiR = ""
mens010_cidR = ""
mens010_estR = ""
mens010_cepR = ""
mens010_nomD = ""
mens010_cepD = ""
mens010_endD = ""
mens010_baiD = ""
mens010_cidD = ""
mens010_estD = ""
mens010_telD = ""
mens010_numD = ""
mens010_valor = ""
mens010_codProj = ""




@app.route("/mens010", methods=["GET", "POST"])
def mens010():
    global mens010_tipEnv
    global mens010_tipPrd
    global mens010_quant
    global mens010_colMat
    global mens010_pesoKG
    global mens010_qbr
    global mens010_empE
    global mens010_empR
    global mens010_endR
    global mens010_baiR
    global mens010_cidR
    global mens010_estR
    global mens010_cepR
    global mens010_nomD
    global mens010_cepD
    global mens010_endD
    global mens010_baiD
    global mens010_cidD
    global mens010_estD
    global mens010_telD
    global mens010_numD
    global mens010_valor
    global mens010_codProj

    mens010_tipEnv = request.form.get("mens010_tipEnv")
    mens010_tipPrd = request.form.get("mens010_tipPrd")
    mens010_quant = request.form.get("mens010_quant")
    mens010_colMat = request.form.get("mens010_colMat")
    mens010_pesoKG = request.form.get("mens010_pesoKG")
    mens010_qbr = request.form.get("mens010_qbr")
    mens010_empE = request.form.get("mens010_empE")
    mens010_empR = request.form.get("mens010_empR")
    mens010_endR = request.form.get("mens010_endR")
    mens010_baiR = request.form.get("mens010_baiR")
    mens010_cidR = request.form.get("mens010_cidR")
    mens010_estR = request.form.get("mens010_estR")
    mens010_cepR = request.form.get("mens010_cepR")
    mens010_nomD = request.form.get("mens010_nomD")
    mens010_cepD = request.form.get("mens010_cepD")
    mens010_endD = request.form.get("mens010_endD")
    mens010_baiD = request.form.get("mens010_baiD")
    mens010_cidD = request.form.get("mens010_cidD")
    mens010_estD = request.form.get("mens010_estD")
    mens010_telD = request.form.get("mens010_telD")
    mens010_numD = request.form.get("mens010_numD")
    mens010_valor = request.form.get("mens010_valor")
    mens010_codProj = request.form.get("mens010_codProj")

    if mens010_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens010.html")
    else:
        return render_template("login.html")


# Tela de Serviços mens011 -------------------------------------------------------------------

mens011_tipEnv = ""
mens011_tipPrd = ""
mens011_quant = ""
mens011_colMat = ""
mens011_perEnt = ""
mens011_pesoKG = ""
mens011_empE = ""
mens011_empR = ""
mens011_endR = ""
mens011_baiR = ""
mens011_cidR = ""
mens011_estR = ""
mens011_cepR = ""
mens011_nomD = ""
mens011_cepD = ""
mens011_endD = ""
mens011_baiD = ""
mens011_cidD = ""
mens011_estD = ""
mens011_telD = ""
mens011_numD = ""
mens011_valor = ""
mens011_codProj = ""



@app.route("/mens011", methods=["GET", "POST"])
def mens011():
    global mens011_tipEnv
    global mens011_tipPrd
    global mens011_quant
    global mens011_colMat
    global mens011_perEnt
    global mens011_pesoKG
    global mens011_empE
    global mens011_empR
    global mens011_endR
    global mens011_baiR
    global mens011_cidR
    global mens011_estR
    global mens011_cepR
    global mens011_nomD
    global mens011_cepD
    global mens011_endD
    global mens011_baiD
    global mens011_cidD
    global mens011_estD
    global mens011_telD
    global mens011_numD
    global mens011_valor
    global mens011_codProj

    mens011_tipEnv = request.form.get("mens011_tipEnv")
    mens011_tipPrd = request.form.get("mens011_tipPrd")
    mens011_quant = request.form.get("mens011_quant")
    mens011_colMat = request.form.get("mens011_colMat")
    mens011_perEnt = request.form.get("mens011_perEnt")
    mens011_pesoKG = request.form.get("mens011_pesoKG")
    mens011_empE = request.form.get("mens011_empE")
    mens011_empR = request.form.get("mens011_empR")
    mens011_endR = request.form.get("mens011_endR")
    mens011_baiR = request.form.get("mens011_baiR")
    mens011_cidR = request.form.get("mens011_cidR")
    mens011_estR = request.form.get("mens011_estR")
    mens011_cepR = request.form.get("mens011_cepR")
    mens011_nomD = request.form.get("mens011_nomD")
    mens011_cepD = request.form.get("mens011_cepD")
    mens011_endD = request.form.get("mens011_endD")
    mens011_baiD = request.form.get("mens011_baiD")
    mens011_cidD = request.form.get("mens011_cidD")
    mens011_estD = request.form.get("mens011_estD")
    mens011_telD = request.form.get("mens011_telD")
    mens011_numD = request.form.get("mens011_numD")
    mens011_valor = request.form.get("mens011_valor")
    mens011_codProj = request.form.get("mens011_codProj")

    if mens011_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens011.html")
    else:
        return render_template("login.html")



# Tela de Serviços mens012 -------------------------------------------------------------------

mens012_tipEnv = ""
mens012_tipPrd = ""
mens012_quant = ""
mens012_colMat = ""
mens012_pesoKG = ""
mens012_qbr = ""
mens012_empE = ""
mens012_empR = ""
mens012_endR = ""
mens012_baiR = ""
mens012_cidR = ""
mens012_estR = ""
mens012_cepR = ""
mens012_nomD = ""
mens012_cepD = ""
mens012_endD = ""
mens012_baiD = ""
mens012_cidD = ""
mens012_estD = ""
mens012_telD = ""
mens012_numD = ""
mens012_valor = ""
mens012_codProj = ""



@app.route("/mens012", methods=["GET", "POST"])
def mens012():
    global mens012_tipEnv
    global mens012_tipPrd
    global mens012_quant
    global mens012_colMat
    global mens012_pesoKG
    global mens012_qbr
    global mens012_empE
    global mens012_empR
    global mens012_endR
    global mens012_baiR
    global mens012_cidR
    global mens012_estR
    global mens012_cepR
    global mens012_nomD
    global mens012_cepD
    global mens012_endD
    global mens012_baiD
    global mens012_cidD
    global mens012_estD
    global mens012_telD
    global mens012_numD
    global mens012_valor
    global mens012_codProj

    mens012_tipEnv = request.form.get("mens012_tipEnv")
    mens012_tipPrd = request.form.get("mens012_tipPrd")
    mens012_quant = request.form.get("mens012_quant")
    mens012_colMat = request.form.get("mens012_colMat")
    mens012_pesoKG = request.form.get("mens012_pesoKG")
    mens012_qbr = request.form.get("mens012_qbr")
    mens012_empE = request.form.get("mens012_empE")
    mens012_empR = request.form.get("mens012_empR")
    mens012_endR = request.form.get("mens012_endR")
    mens012_baiR = request.form.get("mens012_baiR")
    mens012_cidR = request.form.get("mens012_cidR")
    mens012_estR = request.form.get("mens012_estR")
    mens012_cepR = request.form.get("mens012_cepR")
    mens012_nomD = request.form.get("mens012_nomD")
    mens012_cepD = request.form.get("mens012_cepD")
    mens012_endD = request.form.get("mens012_endD")
    mens012_baiD = request.form.get("mens012_baiD")
    mens012_cidD = request.form.get("mens012_cidD")
    mens012_estD = request.form.get("mens012_estD")
    mens012_telD = request.form.get("mens012_telD")
    mens012_numD = request.form.get("mens012_numD")
    mens012_valor = request.form.get("mens012_valor")
    mens012_codProj = request.form.get("mens012_codProj")

    if mens012_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens012.html")
    else:
        return render_template("login.html")


# Tela de Serviços mens013 -------------------------------------------------------------------

mens013_tipEnv = ""
mens013_tipPrd = ""
mens013_quant = ""
mens013_colMat = ""
mens013_perEnt = ""
mens013_pesoKG = ""
mens013_empE = ""
mens013_empR = ""
mens013_endR = ""
mens013_baiR = ""
mens013_cidR = ""
mens013_estR = ""
mens013_cepR = ""
mens013_nomD = ""
mens013_cepD = ""
mens013_endD = ""
mens013_baiD = ""
mens013_cidD = ""
mens013_estD = ""
mens013_telD = ""
mens013_numD = ""
mens013_valor = ""
mens013_codProj = ""


@app.route("/mens013", methods=["GET", "POST"])
def mens013():
    global mens013_tipEnv
    global mens013_tipPrd
    global mens013_quant
    global mens013_colMat
    global mens013_perEnt
    global mens013_pesoKG
    global mens013_empE
    global mens013_empR
    global mens013_endR
    global mens013_baiR
    global mens013_cidR
    global mens013_estR
    global mens013_cepR
    global mens013_nomD
    global mens013_cepD
    global mens013_endD
    global mens013_baiD
    global mens013_cidD
    global mens013_estD
    global mens013_telD
    global mens013_numD
    global mens013_valor
    global mens013_codProj

    mens013_tipEnv = request.form.get("mens013_tipEnv")
    mens013_tipPrd = request.form.get("mens013_tipPrd")
    mens013_quant = request.form.get("mens013_quant")
    mens013_colMat = request.form.get("mens013_colMat")
    mens013_perEnt = request.form.get("mens013_perEnt")
    mens013_pesoKG = request.form.get("mens013_pesoKG")
    mens013_empE = request.form.get("mens013_empE")
    mens013_empR = request.form.get("mens013_empR")
    mens013_endR = request.form.get("mens013_endR")
    mens013_baiR = request.form.get("mens013_baiR")
    mens013_cidR = request.form.get("mens013_cidR")
    mens013_estR = request.form.get("mens013_estR")
    mens013_cepR = request.form.get("mens013_cepR")
    mens013_nomD = request.form.get("mens013_nomD")
    mens013_cepD = request.form.get("mens013_cepD")
    mens013_endD = request.form.get("mens013_endD")
    mens013_baiD = request.form.get("mens013_baiD")
    mens013_cidD = request.form.get("mens013_cidD")
    mens013_estD = request.form.get("mens013_estD")
    mens013_telD = request.form.get("mens013_telD")
    mens013_numD = request.form.get("mens013_numD")
    mens013_valor = request.form.get("mens013_valor")
    mens013_codProj = request.form.get("mens013_codProj")

    if mens013_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens013.html")
    else:
        return render_template("login.html")



# Tela de Serviços mens014 -------------------------------------------------------------------

mens014_tipEnv = ""
mens014_tipPrd = ""
mens014_quant = ""
mens014_colMat = ""
mens014_pesoKG = ""
mens014_qbr = ""
mens014_empE = ""
mens014_empR = ""
mens014_endR = ""
mens014_baiR = ""
mens014_cidR = ""
mens014_estR = ""
mens014_cepR = ""
mens014_nomD = ""
mens014_cepD = ""
mens014_endD = ""
mens014_baiD = ""
mens014_cidD = ""
mens014_estD = ""
mens014_telD = ""
mens014_numD = ""
mens014_valor = ""
mens014_codProj = ""



@app.route("/mens014", methods=["GET", "POST"])
def mens014():
    global mens014_tipEnv
    global mens014_tipPrd
    global mens014_quant
    global mens014_colMat
    global mens014_pesoKG
    global mens014_qbr
    global mens014_empE
    global mens014_empR
    global mens014_endR
    global mens014_baiR
    global mens014_cidR
    global mens014_estR
    global mens014_cepR
    global mens014_nomD
    global mens014_cepD
    global mens014_endD
    global mens014_baiD
    global mens014_cidD
    global mens014_estD
    global mens014_telD
    global mens014_numD
    global mens014_valor
    global mens014_codProj

    mens014_tipEnv = request.form.get("mens014_tipEnv")
    mens014_tipPrd = request.form.get("mens014_tipPrd")
    mens014_quant = request.form.get("mens014_quant")
    mens014_colMat = request.form.get("mens014_colMat")
    mens014_pesoKG = request.form.get("mens014_pesoKG")
    mens014_qbr = request.form.get("mens014_qbr")
    mens014_empE = request.form.get("mens014_empE")
    mens014_empR = request.form.get("mens014_empR")
    mens014_endR = request.form.get("mens014_endR")
    mens014_baiR = request.form.get("mens014_baiR")
    mens014_cidR = request.form.get("mens014_cidR")
    mens014_estR = request.form.get("mens014_estR")
    mens014_cepR = request.form.get("mens014_cepR")
    mens014_nomD = request.form.get("mens014_nomD")
    mens014_cepD = request.form.get("mens014_cepD")
    mens014_endD = request.form.get("mens014_endD")
    mens014_baiD = request.form.get("mens014_baiD")
    mens014_cidD = request.form.get("mens014_cidD")
    mens014_estD = request.form.get("mens014_estD")
    mens014_telD = request.form.get("mens014_telD")
    mens014_numD = request.form.get("mens014_numD")
    mens014_valor = request.form.get("mens014_valor")
    mens014_codProj = request.form.get("mens014_codProj")

    if mens014_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens014.html")
    else:
        return render_template("login.html")




# Tela de Serviços mens015 -------------------------------------------------------------------

mens015_tipEnv = ""
mens015_tipPrd = ""
mens015_quant = ""
mens015_colMat = ""
mens015_perEnt = ""
mens015_pesoKG = ""
mens015_empE = ""
mens015_empR = ""
mens015_endR = ""
mens015_baiR = ""
mens015_cidR = ""
mens015_estR = ""
mens015_cepR = ""
mens015_nomD = ""
mens015_cepD = ""
mens015_endD = ""
mens015_baiD = ""
mens015_cidD = ""
mens015_estD = ""
mens015_telD = ""
mens015_numD = ""
mens015_valor = ""
mens015_codProj = ""




@app.route("/mens015", methods=["GET", "POST"])
def mens015():
    global mens015_tipEnv
    global mens015_tipPrd
    global mens015_quant
    global mens015_colMat
    global mens015_perEnt
    global mens015_pesoKG
    global mens015_empE
    global mens015_empR
    global mens015_endR
    global mens015_baiR
    global mens015_cidR
    global mens015_estR
    global mens015_cepR
    global mens015_nomD
    global mens015_cepD
    global mens015_endD
    global mens015_baiD
    global mens015_cidD
    global mens015_estD
    global mens015_telD
    global mens015_numD
    global mens015_valor
    global mens015_codProj

    mens015_tipEnv = request.form.get("mens015_tipEnv")
    mens015_tipPrd = request.form.get("mens015_tipPrd")
    mens015_quant = request.form.get("mens015_quant")
    mens015_colMat = request.form.get("mens015_colMat")
    mens015_perEnt = request.form.get("mens015_perEnt")
    mens015_pesoKG = request.form.get("mens015_pesoKG")
    mens015_empE = request.form.get("mens015_empE")
    mens015_empR = request.form.get("mens015_empR")
    mens015_endR = request.form.get("mens015_endR")
    mens015_baiR = request.form.get("mens015_baiR")
    mens015_cidR = request.form.get("mens015_cidR")
    mens015_estR = request.form.get("mens015_estR")
    mens015_cepR = request.form.get("mens015_cepR")
    mens015_nomD = request.form.get("mens015_nomD")
    mens015_cepD = request.form.get("mens015_cepD")
    mens015_endD = request.form.get("mens015_endD")
    mens015_baiD = request.form.get("mens015_baiD")
    mens015_cidD = request.form.get("mens015_cidD")
    mens015_estD = request.form.get("mens015_estD")
    mens015_telD = request.form.get("mens015_telD")
    mens015_numD = request.form.get("mens015_numD")
    mens015_valor = request.form.get("mens015_valor")
    mens015_codProj = request.form.get("mens015_codProj")

    if mens015_endD == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens015.html")
    else:
        return render_template("login.html")

# Tela de Serviços mens016 -------------------------------------------------------------------

mens016_quant = ""
mens016_colMat = ""
mens016_recFir = ""
mens016_outR = ""
mens016_firm = ""

@app.route("/mens016", methods=["GET", "POST"])
def mens016():
    global mens016_quant
    global mens016_colMat
    global mens016_recFir
    global mens016_outR
    global mens016_firm

    mens016_quant = request.form.get("mens016_quant")
    mens016_colMat = request.form.get("mens016_colMat")
    mens016_recFir = request.form.get("mens016_recFir")
    mens016_outR = request.form.get("mens016_outR")
    mens016_firm = request.form.get("mens016_firm")

    if mens016_quant == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens003.html")
    else:
        return render_template("login.html")

# Tela de Serviços mens017 -------------------------------------------------------------------

mens017_cxUm = ""
mens017_cxDois = ""
mens017_cxTres = ""
mens017_cxQuat = ""



@app.route("/mens017", methods=["GET", "POST"])
def mens017():

    global mens017_cxUm
    global mens017_cxDois
    global mens017_cxTres
    global mens017_cxQuat

    mens017_cxUm = request.form.get("mens017_cxUm")
    mens017_cxDois = request.form.get("mens017_cxDois")
    mens017_cxTres = request.form.get("mens017_cxTres")
    mens017_cxQuat = request.form.get("mens017_cxQuat")

    if mens017_cxUm == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens017.html")
    else:
        return render_template("login.html")

# Tela de Serviços mens018 -------------------------------------------------------------------

mens018_envTres = ""
mens018_envQuat = ""

@app.route("/mens018", methods=["GET", "POST"])
def mens018():

    global mens018_envTres
    global mens018_envQuat

    mens018_envTres = request.form.get("mens018_envTres")
    mens018_envQuat = request.form.get("mens018_envQuat")

    if mens018_envTres == "": #and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens018.html")
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)