from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pyautogui
import pandas as pd
import pymssql

from datetime import datetime

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
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                  <soap:Body>
                    <CheckUser xmlns="http://sisteplant.com/">
                      <user>""" + username + """</user>
                      <password>""" + password + """</password>
                      <company>MRVVT-ID02</company>
                    </CheckUser>
                  </soap:Body>
                </soap:Envelope>"""

        response = requests.post(url, data=body, headers=headers)
        print(response.content)
        soup = BeautifulSoup(response.content, features="xml")
        resp = soup.find_all('CheckUserResult')[0].text
        print(resp)

    if resp == "OK":

        # Tela de solicitação ---------------------------------------------------------------

        # Acessando a base de dados do Prisma da Vivante para trazer os dados do usuário logado
        conn = pymssql.connect(server='200.196.234.14', user='VivanteDB', password='$Wvtk38n!', database='Prisma',
                               timeout=0, login_timeout=60, charset='UTF-8', as_dict=False, port='1983',
                               autocommit=False,
                               tds_version='7.1')
        cursor = conn.cursor()

        query = """select Requester.requester, Requester.requesterName, Requester.email, Requester.telephone2, Asset.assetName,
                Requester.costCenterClient, costCenterClient.costCenterClientName, costCenterClient.department, department.departmentName
                from Requester

                left join Asset on Asset.asset = Requester.asset and Asset.company = Requester.company   
                left join CostCenterClient on CostCenterClient.costCenterClient = Requester.costCenterClient and CostCenterClient.company = Requester.company
                left join Department on Department.department = costCenterClient.department and Department.company = CostCenterClient.company

                where requester.company = 'LORE' and requester.recordState = 'OP'

                order by requester.requester ASC """

        cursor.execute(query)

        # dataFrame de solicitantes criado
        df = pd.read_sql(query, conn)
        cursor.close()

        # Filtrando o data frame através do usuário logado

        # testar com o usuário do Marcelo, não esquecer de colocar uma consição caso o usuário não exista

        df_filt = df.loc[df['requester'] == username]

        # Criando as variáveis de tela e de OS
        global requester, requesterName, email, asset, assetName, costCenter, costCenterName, department, departmentName
        requester = df_filt['requester'].values.tolist()[0]
        requesterName = df_filt['requesterName'].values.tolist()[0]
        email = df_filt['email'].values.tolist()[0]
        asset = df_filt['telephone2'].values.tolist()[0]
        assetName = df_filt['assetName'].values.tolist()[0]
        costCenter = df_filt['costCenterClient'].values.tolist()[0]
        costCenterName = df_filt['costCenterClientName'].values.tolist()[0]
        department = df_filt['department'].values.tolist()[0]
        departmentName = df_filt['departmentName'].values.tolist()[0]

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

    print(servico)
    print(requester)


    if (servico is None):
        pass
    else:
        return render_template(servico.lower() + ".html")

    return render_template("servicos.html", requester=requester, requesterName=requesterName,
                           email=email, asset=asset, assetName=assetName, costCenter=costCenter,
                           costCenterName=costCenterName, department=department, departmentName=departmentName)


# Web Service de abertura de solicitação ----------------------------------------------------------------------------------

def solic():
    global servico, requester, asset, solic, solic_query, desc_servico
    global solic_url, solic_headers, solic_body, solic_soup, solic_resp, cursor_Conbras, df_Conbras
    global data, data_convert

    data = str(datetime.today())
    data_convert = data[0:19]

    # Função de descrição de serviço

    if servico == 'MENS001':
        desc_servico = 'SERVICO DE CARTORIO'
    elif servico == 'MENS002':
        desc_servico = 'ENTREGA/RETIRADA DE DOCUMENTOS'
    elif servico == 'MENS003':
        desc_servico = 'MENSAGERIA INTERNA - UNIDADE SEDE RJ'
    elif servico == 'MENS004':
        desc_servico = 'MENSAGERIA MATERIAIS PARA PUBLICIDADE - ENVIO NORMAL'
    elif servico == 'MENS005':
        desc_servico = 'MENSAGERIA MATERIAIS PARA PUBLICIDADE - ENVIO EMERGENCIAL'
    elif servico == 'MENS006':
        desc_servico = 'MENSAGERIA MATERIAIS PROMOCIONAIS - ENVIO NORMAL'
    elif servico == 'MENS007':
        desc_servico = 'MENSAGERIA MATERIAIS PROMOCIONAIS - ENVIO EMERGENCIAL'
    elif servico == 'MENS008':
        desc_servico = 'MENSAGERIA MATERIAIS PLV - ENVIO NORMAL'
    elif servico == 'MENS009':
        desc_servico = 'MENSAGERIA MATERIAIS PLV - ENVIO EMERGENCIAL'
    elif servico == 'MENS010':
        desc_servico = 'MENSAGERIA MATERIAIS PARA EXECUTIVOS OU BAs ENVIO EMERGENCIAL'
    elif servico == 'MENS010':
        desc_servico = 'MENSAGERIA MATERIAIS PARA EXECUTIVOS OU BAs ENVIO EMERGENCIAL'



    solic_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
    solic_headers = {'content-type': 'text/xml'}
    solic_body = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <SaveTableRow xmlns="http://sisteplant.com/">
          <user>{requester}</user>
          <company>MRVVT-ID02</company>
          <tableName>WorkRequest</tableName>
          <columnValues> 
            <Column> <name>workRequestName</name> <value>{desc_servico}</value> </Column>
            <Column> <name>workRequestDescription</name> <value>TESTE DE ABERTURA DE MENSAGERIA</value> </Column>
            <Column> <name>workRequestType</name> <value>MENS</value> </Column>
            <Column> <name>asset</name> <value>{asset}</value> </Column>
            <Column> <name>workRequestDate</name> <value>{data_convert}</value> </Column>
            <Column> <name>workRequestState</name> <value>00</value> </Column>
            <Column> <name>workType</name> <value>CHA</value> </Column>
            <Column> <name>defect</name> <value>SDF</value> </Column>
            <Column> <name>priority</name> <value>1</value> </Column>
            <Column> <name>requester</name> <value>{requester}</value> </Column>
            <Column> <name>job</name> <value>MENS</value> </Column>
            <Column> <name>customService</name> <value>{servico}</value> </Column>
          </columnValues>
        </SaveTableRow>
      </soap:Body>
    </soap:Envelope>"""

    response = requests.post(solic_url, data=solic_body, headers=solic_headers)
    solic_soup = BeautifulSoup(response.content, features="xml")
    solic_resp = solic_soup.find_all('SaveTableRowResult')[0].text
    print(response)
    print(response.reason)
    print(response.content)

    # Conectando BD Conbras para trazer a última OS
    conn_Conbras = pymssql.connect(server='200.196.234.14', user='dbaGPS', password='#Xrt56m7', database='GrupoGPS',
                                   timeout=0, login_timeout=60, charset='UTF-8', as_dict=False, port='1983',
                                   autocommit=False,
                                   tds_version='7.1')
    cursor_Conbras = conn_Conbras.cursor()

    query_Conbras = f"""select 
                    max(workRequest)
                    from WorkRequest where company = 'MRVVT-ID02' and requester = '{requester}'"""

    cursor_Conbras.execute(query_Conbras)

    # dataFrame de solicitantes criado
    df_Conbras = pd.read_sql(query_Conbras, conn_Conbras)
    cursor_Conbras.close()

    solic_query = df_Conbras.values.tolist()[0]
    solic = str(solic_query).strip('[]')


    # Tela de Serviços mens001 -------------------------------------------------------------------------------------

mens001_quant = ""
mens001_colMat = ""
mens001_autent = ""
mens001_outR = ""

@app.route("/mens001", methods=["GET", "POST"])
def mens001():
    global mens001_quant, mens001_colMat, mens001_autent, mens001_outR, requester
    global mens001_url, mens001_headers, mens001_body, mens001_resp
    global mens001_position, mens001_auxDataName, mens001_value, mens001_levelData, solic, mens001_auxFieldType

    mens001_quant = request.form.get("mens001_quant")
    mens001_colMat = request.form.get("mens001_colMat")
    mens001_autent = request.form.get("mens001_autent")
    mens001_outR = request.form.get("mens001_outR")

    mens001_auxFieldType = (1, 1, 1, 1)
    mens001_auxDataName = ("QUANTIDADE DE ITENS / COLETAR", "PERIODO DE COLETA DO MATERIAL / DATA HORA PARA ENVIO",
                           "AUTENTICACAO", "OUTROS")
    mens001_value = (mens001_quant, mens001_colMat, mens001_autent, mens001_outR)
    mens001_levelData = ("03", "04", "25", "26")
    mens001_position = ("1", "2", "3", "4")

    if (mens001_quant is None) and (mens001_colMat is None) and (mens001_autent is None) and (mens001_outR is None):
        return render_template("mens001.html")
    else:
        solic()
        for auxDataName, position, auxFieldType, levelData, value in zip(mens001_auxDataName, mens001_position,
                                                                         mens001_auxFieldType, mens001_levelData,
                                                                         mens001_value):
            mens001_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
            mens001_headers = {'content-type': 'text/xml'}
            mens001_body = f"""<?xml version="1.0" encoding="utf-8"?>
                            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                            xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                            xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                              <soap:Body>
                                <SaveTableRow xmlns="http://sisteplant.com/">
                                  <user>{requester}</user>
                                  <company>MRVVT-ID02</company>
                                  <tableName>WorkRequestData</tableName>
                                  <columnValues>
                                    <Column> <name>auxDataName</name> <value>{auxDataName}</value> </Column>
                                    <Column> <name>position</name> <value>{position}</value> </Column>
                                    <Column> <name>auxFieldType</name> <value>{auxFieldType}</value> </Column>
                                    <Column> <name>levelData</name> <value>{levelData}</value> </Column>
                                    <Column> <name>value</name> <value>{value}</value> </Column>
                                    <Column> <name>workRequest</name> <value>{solic}</value> </Column>
                                  </columnValues>
                                </SaveTableRow>
                              </soap:Body>
                            </soap:Envelope>"""

            response = requests.post(mens001_url, data=mens001_body, headers=mens001_headers)
            print(response.content)
            mens001_soup = BeautifulSoup(response.content, features="xml")
            mens001_resp = mens001_soup.find_all('SaveTableRowResult')[0].text

            print(response)
            print(response.reason)
            print(response.content)

            # if resp == "OK":
            #     return servicos()
            # elif resp == "":
            #     pass
            # else:
            #     pyautogui.alert("Erro. Por favor, verifique seu login / senha.")

        return render_template("loginb.html")


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
    global mens002_quant, mens002_colMat, mens002_empR, mens002_endR, mens002_baiR, mens002_cidR, mens002_estR, \
           mens002_cepR, mens002_nomD, mens002_cepD, mens002_endD, mens002_baiD, mens002_cidD, mens002_estD, mens002_telD, mens002_numD
    global mens002_url, mens002_headers, mens002_body, mens002_resp
    global mens002_position, mens002_auxDataName, mens002_value, mens002_levelData, solic, mens002_auxFieldType

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

    mens002_auxFieldType = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    mens002_auxDataName = ("QUANTIDADE DE ITENS / COLETAR", "PERÍODO DE COLETA DO MATERIAL / DATA HORA PARA ENVIO", "EMPRESA REMETENTE",
                           "CEP REMETENTE", "ENDEREÇO REMETENTE", "BAIRRO REMETENTE", "CIDADE REMETENTE", "ESTADO REMETENTE",
                           "NOME DESTINATÁRIO", "CEP DESTINATÁRIO", "ENDEREÇO DESTINATÁRIO", "BAIRRO DESTINATÁRIO", "CIDADE DESTINATÁRIO",
                           "ESTADO DESTINATÁRIO", "TELEFONE DESTINATÁRIO", "NÚMERO / COMPLEMENTO")
    mens002_value = (mens002_quant, mens002_colMat, mens002_empR, mens002_endR, mens002_baiR, mens002_cidR, mens002_estR, \
                     mens002_cepR, mens002_nomD, mens002_cepD, mens002_endD, mens002_baiD, mens002_cidD, mens002_estD, \
                     mens002_telD, mens002_numD)
    mens002_levelData = ("03","04","09","10","11","12","13","14","15","16","17","18","19","20","21","22")
    mens002_position = ("1", "2", "3", "4", "5","6","7","8","9","10","11","12","13","14","15","16")

    if (mens002_quant is None) and (mens002_colMat is None) and (mens002_empR is None) and (mens002_endR is None):
        return render_template("mens002.html")
    else:
        solic()
        for auxDataName, position, auxFieldType, levelData, value in zip(mens002_auxDataName, mens002_position,
                                                                         mens002_auxFieldType, mens002_levelData,
                                                                         mens002_value):
            mens002_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
            mens002_headers = {'content-type': 'text/xml'}
            mens002_body = f"""<?xml version="1.0" encoding="utf-8"?>
                               <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                               xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                 <soap:Body>
                                   <SaveTableRow xmlns="http://sisteplant.com/">
                                     <user>{requester}</user>
                                     <company>MRVVT-ID02</company>
                                     <tableName>WorkRequestData</tableName>
                                     <columnValues>
                                       <Column> <name>auxDataName</name> <value>{auxDataName}</value> </Column>
                                       <Column> <name>position</name> <value>{position}</value> </Column>
                                       <Column> <name>auxFieldType</name> <value>{auxFieldType}</value> </Column>
                                       <Column> <name>levelData</name> <value>{levelData}</value> </Column>
                                       <Column> <name>value</name> <value>{value}</value> </Column>
                                       <Column> <name>workRequest</name> <value>{solic}</value> </Column>
                                     </columnValues>
                                   </SaveTableRow>
                                 </soap:Body>
                               </soap:Envelope>"""

            response = requests.post(mens002_url, data=mens002_body, headers=mens002_headers)
            print(response.content)
            mens002_soup = BeautifulSoup(response.content, features="xml")
            mens002_resp = mens002_soup.find_all('SaveTableRowResult')[0].text

            print(response)
            print(response.reason)
            print(response.content)

            # if resp == "OK":
            #     return servicos()
            # elif resp == "":
            #     pass
            # else:
            #     pyautogui.alert("Erro. Por favor, verifique seu login / senha.")        

        return render_template("loginb.html")


# Tela de Serviços mens003 -------------------------------------------------------------------

mens003_endD = ""
mens003_baiD = ""
mens003_numD = ""

@app.route("/mens003", methods=["GET", "POST"])
def mens003():
    global mens003_endD, mens003_baiD, mens003_numD
    global mens003_url, mens003_headers, mens003_body, mens003_resp
    global mens003_position, mens003_auxDataName, mens003_value, mens003_levelData, solic, mens003_auxFieldType

    mens003_endD = request.form.get("mens003_endD")
    mens003_baiD = request.form.get("mens003_baiD")
    mens003_numD = request.form.get("mens003_numD")

    mens003_auxFieldType = (1, 1, 1)
    mens003_auxDataName = ("NUMERO / COMPLEMENTO", "ENDERECO DESTINATARIO", "BAIRRO DESTINATARIO")
    mens003_value = (mens003_endD, mens003_baiD, mens003_numD)
    mens003_levelData = ("22", "17", "18")
    mens003_position = ("1", "2", "3")

    if (mens003_endD is None) and (mens003_baiD is None) and (mens003_numD is None):
        return render_template("mens003.html")
    else:
        solic()
        for auxDataName, position, auxFieldType, levelData, value in zip(mens003_auxDataName, mens003_position,
                                                                         mens003_auxFieldType, mens003_levelData,
                                                                         mens003_value):
            mens003_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
            mens003_headers = {'content-type': 'text/xml'}
            mens003_body = f"""<?xml version="1.0" encoding="utf-8"?>
                                   <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                     <soap:Body>
                                       <SaveTableRow xmlns="http://sisteplant.com/">
                                         <user>{requester}</user>
                                         <company>MRVVT-ID02</company>
                                         <tableName>WorkRequestData</tableName>
                                         <columnValues>
                                           <Column> <name>auxDataName</name> <value>{auxDataName}</value> </Column>
                                           <Column> <name>position</name> <value>{position}</value> </Column>
                                           <Column> <name>auxFieldType</name> <value>{auxFieldType}</value> </Column>
                                           <Column> <name>levelData</name> <value>{levelData}</value> </Column>
                                           <Column> <name>value</name> <value>{value}</value> </Column>
                                           <Column> <name>workRequest</name> <value>{solic}</value> </Column>
                                         </columnValues>
                                       </SaveTableRow>
                                     </soap:Body>
                                   </soap:Envelope>"""

            response = requests.post(mens003_url, data=mens003_body, headers=mens003_headers)
            print(response.content)
            mens003_soup = BeautifulSoup(response.content, features="xml")
            mens003_resp = mens003_soup.find_all('SaveTableRowResult')[0].text

            print(response)
            print(response.reason)
            print(response.content)

            # if resp == "OK":
            #     return servicos()
            # elif resp == "":
            #     pass
            # else:
            #     pyautogui.alert("Erro. Por favor, verifique seu login / senha.")      
            
        return render_template("loginb.html")


# Tela de Serviços mens004 -------------------------------------------------------------------

mens004_tipEnv = ""
mens004_tipPrd = ""
mens004_quant = ""
mens004_colMat = ""
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
    global mens004_tipEnv, mens004_tipPrd, mens004_quant, mens004_colMat, mens004_pesoKG, mens004_qbr, mens004_empE, \
           mens004_empR, mens004_endR, mens004_baiR, mens004_cidR, mens004_estR, mens004_cepR, mens004_nomD, mens004_cepD,\
           mens004_endD, mens004_baiD, mens004_cidD, mens004_estD, mens004_telD, mens004_numD, mens004_valor, mens004_codProj
    global mens004_url, mens004_headers, mens004_body, mens004_resp
    global mens004_position, mens004_auxDataName, mens004_value, mens004_levelData, solic, mens004_auxFieldType

    mens004_tipEnv = request.form.get("mens004_tipEnv")
    mens004_tipPrd = request.form.get("mens004_tipPrd")
    mens004_quant = request.form.get("mens004_quant")
    mens004_colMat = request.form.get("mens004_colMat")
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

    mens004_auxFieldType = (1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1)
    mens004_auxDataName = ("TIPO DE ENVIO", "TIPO DE PRODUTO", "QUANTIDADE DE ITENS / COLETAR",
                           "PERIODO DE COLETA DO MATERIAL / DATA HORA PARA ENVIO", "PESO APROXIMADO KG", "EMPRESA PARA ENVIO",
                           "PERMITE QUEBRA DE ENVIO?", "EMPRESA REMETENTE", "CEP REMETENTE", "ENDERECO REMETENTE", "BAIRRO REMETENTE",
                           "CIDADE REMETENTE", "ESTADO REMETENTE", "NOME DESTINATARIO", "CEP DESTINATARIO", "ENDEREÇO DESTINATARIO",
                           "BAIRRO DESTINATARIO", "CIDADE DESTINATARIO", "ESTADO DESTINATARIO", "TELEFONE DESTINATARIO",
                           "NUMERO / COMPLEMENTO", "VALOR APROXIMADO DO(S) ITEN(S) A ENVIAR", "CCDIGO DE PROJETO")
    mens004_value = (mens004_tipEnv, mens004_tipPrd, mens004_quant, mens004_colMat, mens004_pesoKG, mens004_qbr, mens004_empE, \
           mens004_empR, mens004_endR, mens004_baiR, mens004_cidR, mens004_estR, mens004_cepR, mens004_nomD, mens004_cepD,\
           mens004_endD, mens004_baiD, mens004_cidD, mens004_estD, mens004_telD, mens004_numD, mens004_valor, mens004_codProj)
    mens004_levelData = ("01","02","03","04","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
    mens004_position = ("1", "2", "3", "4", "5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23")

    if (mens004_endD is None) and (mens004_baiD is None) and (mens004_numD is None):
        return render_template("mens004.html")
    else:
        solic()
        for auxDataName, position, auxFieldType, levelData, value in zip(mens004_auxDataName, mens004_position,
                                                                         mens004_auxFieldType, mens004_levelData,
                                                                         mens004_value):
            mens004_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
            mens004_headers = {'content-type': 'text/xml'}
            mens004_body = f"""<?xml version="1.0" encoding="utf-8"?>
                                   <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                     <soap:Body>
                                       <SaveTableRow xmlns="http://sisteplant.com/">
                                         <user>{requester}</user>
                                         <company>MRVVT-ID02</company>
                                         <tableName>WorkRequestData</tableName>
                                         <columnValues>
                                           <Column> <name>auxDataName</name> <value>{auxDataName}</value> </Column>
                                           <Column> <name>position</name> <value>{position}</value> </Column>
                                           <Column> <name>auxFieldType</name> <value>{auxFieldType}</value> </Column>
                                           <Column> <name>levelData</name> <value>{levelData}</value> </Column>
                                           <Column> <name>value</name> <value>{value}</value> </Column>
                                           <Column> <name>workRequest</name> <value>{solic}</value> </Column>
                                         </columnValues>
                                       </SaveTableRow>
                                     </soap:Body>
                                   </soap:Envelope>"""

            response = requests.post(mens004_url, data=mens004_body, headers=mens004_headers)
            print(response.content)
            mens004_soup = BeautifulSoup(response.content, features="xml")
            mens004_resp = mens004_soup.find_all('SaveTableRowResult')[0].text

            print(response)
            print(response.reason)
            print(response.content)

            # if resp == "OK":
            #     return servicos()
            # elif resp == "":
            #     pass
            # else:
            #     pyautogui.alert("Erro. Por favor, verifique seu login / senha.")      

        return render_template("loginb.html")


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

    if mens005_endD == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
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
    global mens006_tipEnv, mens006_tipPrd, mens006_quant, mens006_colMat, mens006_pesoKG, mens006_qbr, mens006_empE, \
           mens006_empR, mens006_endR, mens006_baiR, mens006_cidR, mens006_estR, mens006_cepR, mens006_nomD, mens006_cepD,\
           mens006_endD, mens006_baiD, mens006_cidD, mens006_estD, mens006_telD, mens006_numD, mens006_valor, mens006_codProj
    global mens006_url, mens006_headers, mens006_body, mens006_resp
    global mens006_position, mens006_auxDataName, mens006_value, mens006_levelData, solic, mens006_auxFieldType

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

    mens006_auxFieldType = (1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1)
    mens006_auxDataName = ("TIPO DE ENVIO", "TIPO DE PRODUTO", "QUANTIDADE DE ITENS / COLETAR",
                           "PERIODO DE COLETA DO MATERIAL / DATA HORA PARA ENVIO", "PESO APROXIMADO KG", "EMPRESA PARA ENVIO",
                           "PERMITE QUEBRA DE ENVIO?", "EMPRESA REMETENTE", "CEP REMETENTE", "ENDERECO REMETENTE", "BAIRRO REMETENTE",
                           "CIDADE REMETENTE", "ESTADO REMETENTE", "NOME DESTINATARIO", "CEP DESTINATARIO", "ENDEREÇO DESTINATARIO",
                           "BAIRRO DESTINATARIO", "CIDADE DESTINATARIO", "ESTADO DESTINATARIO", "TELEFONE DESTINATARIO",
                           "NUMERO / COMPLEMENTO", "VALOR APROXIMADO DO(S) ITEN(S) A ENVIAR", "CCDIGO DE PROJETO")
    mens006_value = (mens006_tipEnv, mens006_tipPrd, mens006_quant, mens006_colMat, mens006_pesoKG, mens006_qbr, mens006_empE, \
           mens006_empR, mens006_endR, mens006_baiR, mens006_cidR, mens006_estR, mens006_cepR, mens006_nomD, mens006_cepD,\
           mens006_endD, mens006_baiD, mens006_cidD, mens006_estD, mens006_telD, mens006_numD, mens006_valor, mens006_codProj)
    mens006_levelData = ("01","02","03","04","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
    mens006_position = ("1", "2", "3", "4", "5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23")

    if (mens006_endD is None) and (mens006_baiD is None) and (mens006_numD is None):
        return render_template("mens006.html")
    else:
        solic()
        for auxDataName, position, auxFieldType, levelData, value in zip(mens006_auxDataName, mens006_position,
                                                                         mens006_auxFieldType, mens006_levelData,
                                                                         mens006_value):
            mens006_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
            mens006_headers = {'content-type': 'text/xml'}
            mens006_body = f"""<?xml version="1.0" encoding="utf-8"?>
                                   <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                     <soap:Body>
                                       <SaveTableRow xmlns="http://sisteplant.com/">
                                         <user>{requester}</user>
                                         <company>MRVVT-ID02</company>
                                         <tableName>WorkRequestData</tableName>
                                         <columnValues>
                                           <Column> <name>auxDataName</name> <value>{auxDataName}</value> </Column>
                                           <Column> <name>position</name> <value>{position}</value> </Column>
                                           <Column> <name>auxFieldType</name> <value>{auxFieldType}</value> </Column>
                                           <Column> <name>levelData</name> <value>{levelData}</value> </Column>
                                           <Column> <name>value</name> <value>{value}</value> </Column>
                                           <Column> <name>workRequest</name> <value>{solic}</value> </Column>
                                         </columnValues>
                                       </SaveTableRow>
                                     </soap:Body>
                                   </soap:Envelope>"""

            response = requests.post(mens006_url, data=mens006_body, headers=mens006_headers)
            print(response.content)
            mens006_soup = BeautifulSoup(response.content, features="xml")
            mens006_resp = mens006_soup.find_all('SaveTableRowResult')[0].text

            print(response)
            print(response.reason)
            print(response.content)

            # if resp == "OK":
            #     return servicos()
            # elif resp == "":
            #     pass
            # else:
            #     pyautogui.alert("Erro. Por favor, verifique seu login / senha.")      

        return render_template("loginb.html")
    
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

    if mens007_endD == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
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
    global mens008_tipEnv, mens008_tipPrd, mens008_quant, mens008_colMat, mens008_pesoKG, mens008_qbr, mens008_empE, \
           mens008_empR, mens008_endR, mens008_baiR, mens008_cidR, mens008_estR, mens008_cepR, mens008_nomD, mens008_cepD,\
           mens008_endD, mens008_baiD, mens008_cidD, mens008_estD, mens008_telD, mens008_numD, mens008_valor, mens008_codProj
    global mens008_url, mens008_headers, mens008_body, mens008_resp
    global mens008_position, mens008_auxDataName, mens008_value, mens008_levelData, solic, mens008_auxFieldType

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

    mens008_auxFieldType = (1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1)
    mens008_auxDataName = ("TIPO DE ENVIO", "TIPO DE PRODUTO", "QUANTIDADE DE ITENS / COLETAR",
                           "PERIODO DE COLETA DO MATERIAL / DATA HORA PARA ENVIO", "PESO APROXIMADO KG", "EMPRESA PARA ENVIO",
                           "PERMITE QUEBRA DE ENVIO?", "EMPRESA REMETENTE", "CEP REMETENTE", "ENDERECO REMETENTE", "BAIRRO REMETENTE",
                           "CIDADE REMETENTE", "ESTADO REMETENTE", "NOME DESTINATARIO", "CEP DESTINATARIO", "ENDEREÇO DESTINATARIO",
                           "BAIRRO DESTINATARIO", "CIDADE DESTINATARIO", "ESTADO DESTINATARIO", "TELEFONE DESTINATARIO",
                           "NUMERO / COMPLEMENTO", "VALOR APROXIMADO DO(S) ITEN(S) A ENVIAR", "CCDIGO DE PROJETO")
    mens008_value = (mens008_tipEnv, mens008_tipPrd, mens008_quant, mens008_colMat, mens008_pesoKG, mens008_qbr, mens008_empE, \
           mens008_empR, mens008_endR, mens008_baiR, mens008_cidR, mens008_estR, mens008_cepR, mens008_nomD, mens008_cepD,\
           mens008_endD, mens008_baiD, mens008_cidD, mens008_estD, mens008_telD, mens008_numD, mens008_valor, mens008_codProj)
    mens008_levelData = ("01","02","03","04","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
    mens008_position = ("1", "2", "3", "4", "5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23")

    if (mens008_endD is None) and (mens008_baiD is None) and (mens008_numD is None):
        return render_template("mens008.html")
    else:
        solic()
        for auxDataName, position, auxFieldType, levelData, value in zip(mens008_auxDataName, mens008_position,
                                                                         mens008_auxFieldType, mens008_levelData,
                                                                         mens008_value):
            mens008_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
            mens008_headers = {'content-type': 'text/xml'}
            mens008_body = f"""<?xml version="1.0" encoding="utf-8"?>
                                   <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                     <soap:Body>
                                       <SaveTableRow xmlns="http://sisteplant.com/">
                                         <user>{requester}</user>
                                         <company>MRVVT-ID02</company>
                                         <tableName>WorkRequestData</tableName>
                                         <columnValues>
                                           <Column> <name>auxDataName</name> <value>{auxDataName}</value> </Column>
                                           <Column> <name>position</name> <value>{position}</value> </Column>
                                           <Column> <name>auxFieldType</name> <value>{auxFieldType}</value> </Column>
                                           <Column> <name>levelData</name> <value>{levelData}</value> </Column>
                                           <Column> <name>value</name> <value>{value}</value> </Column>
                                           <Column> <name>workRequest</name> <value>{solic}</value> </Column>
                                         </columnValues>
                                       </SaveTableRow>
                                     </soap:Body>
                                   </soap:Envelope>"""

            response = requests.post(mens008_url, data=mens008_body, headers=mens008_headers)
            print(response.content)
            mens008_soup = BeautifulSoup(response.content, features="xml")
            mens008_resp = mens008_soup.find_all('SaveTableRowResult')[0].text

            print(response)
            print(response.reason)
            print(response.content)

            # if resp == "OK":
            #     return servicos()
            # elif resp == "":
            #     pass
            # else:
            #     pyautogui.alert("Erro. Por favor, verifique seu login / senha.")      

        return render_template("loginb.html")
    
    
# Tela de Serviços mens009 -------------------------------------------------------------------

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

    if mens009_endD == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
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
    global mens010_tipEnv, mens010_tipPrd, mens010_quant, mens010_colMat, mens010_pesoKG, mens010_qbr, mens010_empE, \
           mens010_empR, mens010_endR, mens010_baiR, mens010_cidR, mens010_estR, mens010_cepR, mens010_nomD, mens010_cepD,\
           mens010_endD, mens010_baiD, mens010_cidD, mens010_estD, mens010_telD, mens010_numD, mens010_valor, mens010_codProj
    global mens010_url, mens010_headers, mens010_body, mens010_resp
    global mens010_position, mens010_auxDataName, mens010_value, mens010_levelData, solic, mens010_auxFieldType

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

    mens010_auxFieldType = (1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1)
    mens010_auxDataName = ("TIPO DE ENVIO", "TIPO DE PRODUTO", "QUANTIDADE DE ITENS / COLETAR",
                           "PERIODO DE COLETA DO MATERIAL / DATA HORA PARA ENVIO", "PESO APROXIMADO KG", "EMPRESA PARA ENVIO",
                           "PERMITE QUEBRA DE ENVIO?", "EMPRESA REMETENTE", "CEP REMETENTE", "ENDERECO REMETENTE", "BAIRRO REMETENTE",
                           "CIDADE REMETENTE", "ESTADO REMETENTE", "NOME DESTINATARIO", "CEP DESTINATARIO", "ENDEREÇO DESTINATARIO",
                           "BAIRRO DESTINATARIO", "CIDADE DESTINATARIO", "ESTADO DESTINATARIO", "TELEFONE DESTINATARIO",
                           "NUMERO / COMPLEMENTO", "VALOR APROXIMADO DO(S) ITEN(S) A ENVIAR", "CCDIGO DE PROJETO")
    mens010_value = (mens010_tipEnv, mens010_tipPrd, mens010_quant, mens010_colMat, mens010_pesoKG, mens010_qbr, mens010_empE, \
           mens010_empR, mens010_endR, mens010_baiR, mens010_cidR, mens010_estR, mens010_cepR, mens010_nomD, mens010_cepD,\
           mens010_endD, mens010_baiD, mens010_cidD, mens010_estD, mens010_telD, mens010_numD, mens010_valor, mens010_codProj)
    mens010_levelData = ("01","02","03","04","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
    mens010_position = ("1", "2", "3", "4", "5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23")

    if (mens010_endD is None) and (mens010_baiD is None) and (mens010_numD is None):
        return render_template("mens010.html")
    else:
        solic()
        for auxDataName, position, auxFieldType, levelData, value in zip(mens010_auxDataName, mens010_position,
                                                                         mens010_auxFieldType, mens010_levelData,
                                                                         mens010_value):
            mens010_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
            mens010_headers = {'content-type': 'text/xml'}
            mens010_body = f"""<?xml version="1.0" encoding="utf-8"?>
                                   <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                     <soap:Body>
                                       <SaveTableRow xmlns="http://sisteplant.com/">
                                         <user>{requester}</user>
                                         <company>MRVVT-ID02</company>
                                         <tableName>WorkRequestData</tableName>
                                         <columnValues>
                                           <Column> <name>auxDataName</name> <value>{auxDataName}</value> </Column>
                                           <Column> <name>position</name> <value>{position}</value> </Column>
                                           <Column> <name>auxFieldType</name> <value>{auxFieldType}</value> </Column>
                                           <Column> <name>levelData</name> <value>{levelData}</value> </Column>
                                           <Column> <name>value</name> <value>{value}</value> </Column>
                                           <Column> <name>workRequest</name> <value>{solic}</value> </Column>
                                         </columnValues>
                                       </SaveTableRow>
                                     </soap:Body>
                                   </soap:Envelope>"""

            response = requests.post(mens010_url, data=mens010_body, headers=mens010_headers)
            print(response.content)
            mens010_soup = BeautifulSoup(response.content, features="xml")
            mens010_resp = mens010_soup.find_all('SaveTableRowResult')[0].text

            print(response)
            print(response.reason)
            print(response.content)

            # if resp == "OK":
            #     return servicos()
            # elif resp == "":
            #     pass
            # else:
            #     pyautogui.alert("Erro. Por favor, verifique seu login / senha.")      

        return render_template("loginb.html")

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

    if mens011_endD == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
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
    global mens012_tipEnv, mens012_tipPrd, mens012_quant, mens012_colMat, mens012_pesoKG, mens012_qbr, mens012_empE, \
           mens012_empR, mens012_endR, mens012_baiR, mens012_cidR, mens012_estR, mens012_cepR, mens012_nomD, mens012_cepD,\
           mens012_endD, mens012_baiD, mens012_cidD, mens012_estD, mens012_telD, mens012_numD, mens012_valor, mens012_codProj
    global mens012_url, mens012_headers, mens012_body, mens012_resp
    global mens012_position, mens012_auxDataName, mens012_value, mens012_levelData, solic, mens012_auxFieldType

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

    mens012_auxFieldType = (1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1)
    mens012_auxDataName = ("TIPO DE ENVIO", "TIPO DE PRODUTO", "QUANTIDADE DE ITENS / COLETAR",
                           "PERIODO DE COLETA DO MATERIAL / DATA HORA PARA ENVIO", "PESO APROXIMADO KG", "EMPRESA PARA ENVIO",
                           "PERMITE QUEBRA DE ENVIO?", "EMPRESA REMETENTE", "CEP REMETENTE", "ENDERECO REMETENTE", "BAIRRO REMETENTE",
                           "CIDADE REMETENTE", "ESTADO REMETENTE", "NOME DESTINATARIO", "CEP DESTINATARIO", "ENDEREÇO DESTINATARIO",
                           "BAIRRO DESTINATARIO", "CIDADE DESTINATARIO", "ESTADO DESTINATARIO", "TELEFONE DESTINATARIO",
                           "NUMERO / COMPLEMENTO", "VALOR APROXIMADO DO(S) ITEN(S) A ENVIAR", "CCDIGO DE PROJETO")
    mens012_value = (mens012_tipEnv, mens012_tipPrd, mens012_quant, mens012_colMat, mens012_pesoKG, mens012_qbr, mens012_empE, \
           mens012_empR, mens012_endR, mens012_baiR, mens012_cidR, mens012_estR, mens012_cepR, mens012_nomD, mens012_cepD,\
           mens012_endD, mens012_baiD, mens012_cidD, mens012_estD, mens012_telD, mens012_numD, mens012_valor, mens012_codProj)
    mens012_levelData = ("01","02","03","04","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
    mens012_position = ("1", "2", "3", "4", "5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23")

    if (mens012_endD is None) and (mens012_baiD is None) and (mens012_numD is None):
        return render_template("mens012.html")
    else:
        solic()
        for auxDataName, position, auxFieldType, levelData, value in zip(mens012_auxDataName, mens012_position,
                                                                         mens012_auxFieldType, mens012_levelData,
                                                                         mens012_value):
            mens012_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
            mens012_headers = {'content-type': 'text/xml'}
            mens012_body = f"""<?xml version="1.0" encoding="utf-8"?>
                                   <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                     <soap:Body>
                                       <SaveTableRow xmlns="http://sisteplant.com/">
                                         <user>{requester}</user>
                                         <company>MRVVT-ID02</company>
                                         <tableName>WorkRequestData</tableName>
                                         <columnValues>
                                           <Column> <name>auxDataName</name> <value>{auxDataName}</value> </Column>
                                           <Column> <name>position</name> <value>{position}</value> </Column>
                                           <Column> <name>auxFieldType</name> <value>{auxFieldType}</value> </Column>
                                           <Column> <name>levelData</name> <value>{levelData}</value> </Column>
                                           <Column> <name>value</name> <value>{value}</value> </Column>
                                           <Column> <name>workRequest</name> <value>{solic}</value> </Column>
                                         </columnValues>
                                       </SaveTableRow>
                                     </soap:Body>
                                   </soap:Envelope>"""

            response = requests.post(mens012_url, data=mens012_body, headers=mens012_headers)
            print(response.content)
            mens012_soup = BeautifulSoup(response.content, features="xml")
            mens012_resp = mens012_soup.find_all('SaveTableRowResult')[0].text

            print(response)
            print(response.reason)
            print(response.content)

            # if resp == "OK":
            #     return servicos()
            # elif resp == "":
            #     pass
            # else:
            #     pyautogui.alert("Erro. Por favor, verifique seu login / senha.")      

        return render_template("loginb.html")


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

    if mens013_endD == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
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
    global mens014_tipEnv, mens014_tipPrd, mens014_quant, mens014_colMat, mens014_pesoKG, mens014_qbr, mens014_empE, \
           mens014_empR, mens014_endR, mens014_baiR, mens014_cidR, mens014_estR, mens014_cepR, mens014_nomD, mens014_cepD,\
           mens014_endD, mens014_baiD, mens014_cidD, mens014_estD, mens014_telD, mens014_numD, mens014_valor, mens014_codProj
    global mens014_url, mens014_headers, mens014_body, mens014_resp
    global mens014_position, mens014_auxDataName, mens014_value, mens014_levelData, solic, mens014_auxFieldType

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

    mens014_auxFieldType = (1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1)
    mens014_auxDataName = ("TIPO DE ENVIO", "TIPO DE PRODUTO", "QUANTIDADE DE ITENS / COLETAR",
                           "PERIODO DE COLETA DO MATERIAL / DATA HORA PARA ENVIO", "PESO APROXIMADO KG", "EMPRESA PARA ENVIO",
                           "PERMITE QUEBRA DE ENVIO?", "EMPRESA REMETENTE", "CEP REMETENTE", "ENDERECO REMETENTE", "BAIRRO REMETENTE",
                           "CIDADE REMETENTE", "ESTADO REMETENTE", "NOME DESTINATARIO", "CEP DESTINATARIO", "ENDEREÇO DESTINATARIO",
                           "BAIRRO DESTINATARIO", "CIDADE DESTINATARIO", "ESTADO DESTINATARIO", "TELEFONE DESTINATARIO",
                           "NUMERO / COMPLEMENTO", "VALOR APROXIMADO DO(S) ITEN(S) A ENVIAR", "CCDIGO DE PROJETO")
    mens014_value = (mens014_tipEnv, mens014_tipPrd, mens014_quant, mens014_colMat, mens014_pesoKG, mens014_qbr, mens014_empE, \
           mens014_empR, mens014_endR, mens014_baiR, mens014_cidR, mens014_estR, mens014_cepR, mens014_nomD, mens014_cepD,\
           mens014_endD, mens014_baiD, mens014_cidD, mens014_estD, mens014_telD, mens014_numD, mens014_valor, mens014_codProj)
    mens014_levelData = ("01","02","03","04","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
    mens014_position = ("1", "2", "3", "4", "5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23")

    if (mens014_endD is None) and (mens014_baiD is None) and (mens014_numD is None):
        return render_template("mens014.html")
    else:
        solic()
        for auxDataName, position, auxFieldType, levelData, value in zip(mens014_auxDataName, mens014_position,
                                                                         mens014_auxFieldType, mens014_levelData,
                                                                         mens014_value):
            mens014_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/SaveData.asmx"
            mens014_headers = {'content-type': 'text/xml'}
            mens014_body = f"""<?xml version="1.0" encoding="utf-8"?>
                                   <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                     <soap:Body>
                                       <SaveTableRow xmlns="http://sisteplant.com/">
                                         <user>{requester}</user>
                                         <company>MRVVT-ID02</company>
                                         <tableName>WorkRequestData</tableName>
                                         <columnValues>
                                           <Column> <name>auxDataName</name> <value>{auxDataName}</value> </Column>
                                           <Column> <name>position</name> <value>{position}</value> </Column>
                                           <Column> <name>auxFieldType</name> <value>{auxFieldType}</value> </Column>
                                           <Column> <name>levelData</name> <value>{levelData}</value> </Column>
                                           <Column> <name>value</name> <value>{value}</value> </Column>
                                           <Column> <name>workRequest</name> <value>{solic}</value> </Column>
                                         </columnValues>
                                       </SaveTableRow>
                                     </soap:Body>
                                   </soap:Envelope>"""

            response = requests.post(mens014_url, data=mens014_body, headers=mens014_headers)
            print(response.content)
            mens014_soup = BeautifulSoup(response.content, features="xml")
            mens014_resp = mens014_soup.find_all('SaveTableRowResult')[0].text

            print(response)
            print(response.reason)
            print(response.content)

            # if resp == "OK":
            #     return servicos()
            # elif resp == "":
            #     pass
            # else:
            #     pyautogui.alert("Erro. Por favor, verifique seu login / senha.")      

        return render_template("loginb.html")



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

    if mens015_endD == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
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

    if mens016_quant == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
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

    if mens017_cxUm == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
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

    if mens018_envTres == "":  # and (pos_b is None) and (pos_c is None) and (pos_d is None)
        return render_template("mens018.html")
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
