import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests
from time import sleep
from datetime import date
from datetime import datetime, timedelta


from datetime import date
from datetime import datetime, timedelta
from time import sleep
data = date.today()
hoje = datetime.strftime(data, "%d/%m/%Y")
print(hoje)
############################################################################################################
############################################################################################################
#mudar o caminho dos arquivos do chromedriver aqui
driver = webdriver.Chrome(executable_path='C:/Users/joao.basso/Downloads/chromedriver/chromedriver.exe')
############################################################################################################
############################################################################################################
link = "https://www.ccee.org.br/web/guest/precos/painel-precos"
driver.get(link)
sleep(8)

driver.find_element_by_xpath('//*[@id="tipoPreco"]/option[2]').click()
sleep(5)

data_inicial = driver.find_element_by_xpath('//*[@id="inputInitialDate"]')
data_inicial.send_keys(hoje)
sleep(2)

data_final = driver.find_element_by_xpath('//*[@id="inputFinalDate"]')
data_final.send_keys(hoje)
sleep(2)

driver.find_element_by_xpath('//*[@id="filtrarHistoricoPreco"]').click()
sleep(2)

import mysql.connector
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine

user = 'your_user' #user
password = 'password' #db password
host = 'db4free.net' #db4free was used in this case
database = 'jownne_db' #your db name
port = 3306
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=host, db=database, user=user, pw=password))

con = mysql.connector.connect(user=user, password=password, database = database, host=host, port=port)


dados = pd.read_csv('preco_horario.csv',delimiter=';', names=['Hora','Submercado','PLD','PLD2','PLD3','PLD4'])
dados = dados.drop(index=0,columns=['PLD2','PLD3','PLD4'])
dados = dados.applymap(lambda x: str(x.replace(',','.')))

dados.to_sql('dados_pld_horario', engine, index=False)

con = mysql.connector.connect(user=user, password=password, database = database, host=host, port=port)

sql = '''select submercado, avg(PLD) from dados_pld_2 group by 1 order by 1'''

cursor = con.cursor()
cursor.execute(sql)

resultado = cursor.fetchall()

con.close()
print(cursor.description)


media_pld_diario = pd.DataFrame(resultado, columns=['Média diária do PLD', 'Valor'])

import dataframe_image as dfi

dfi.export(media_pld_diario, 'media_pld.png')


import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
subject = "An email with attachment from Python"
body = "This is an email with attachment sent from Python"

############################################################################################################
############################################################################################################
sender_email = #inserir aqui um email que tenha as restrições de segurança baixas do GMAIL
receiver_email = 'receiver_email'   #str(input("Entre com o email:"))
password = #senha do email  #mail password   #str(input("Entre com a senha:"))

############################################################################################################
############################################################################################################

# Cria Multipart e os cabeçalhos
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  

# Adiciona no corpo do email
message.attach(MIMEText(body, "plain"))


filename = 'media_pld.png'
            
file_path = os.path.join('insert your file path: C:\\user\file\...', filename)
attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
attachment.add_header('Content-Disposition','attachment', filename=filename)
message.attach(attachment)
encoders.encode_base64(attachment)

message.attach(attachment)
text = message.as_string()


context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)