 # -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 20:47:01 2021

@author: Owner
"""

from  flask import Flask
from flask import render_template,request
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import re
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
# from utils import utils_data_wrangling

def list_option(df,column):
    options = df[column][df[column]!=""].to_list()
    return options

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'cursodb.cctxmwmt5coi.us-east-1.rds.amazonaws.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '11235813::'
app.config['MYSQL_DB'] = 'users'
 
# mysql = MySQL(app)


# Google Sheets Connection
sheet_file  = "Registremos Pedidos! (respuestas)"
page_validation = "validaciones"
scope       = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
         #'C:\\Users\\Owner\\Documents\\credential\\cred_mambo.json', scope) # Your json file here
            'credentials/cred_mambo.json', scope) # Your json file here
gc          = gspread.authorize(credentials)

# GSC Page
wks_preguntas = gc.open(sheet_file).worksheet(page_validation)
data = wks_preguntas.get_all_values()
headers = data.pop(0)
df_validation = pd.DataFrame(data, columns=headers)
nro_delivery_agent = list_option(df_validation,column="nro_delivery_agent")

# @app.route("/")
# def home():
#     return "Home"

@app.route("/")
def home():
    #read option google_sheets
    wks_preguntas = gc.open(sheet_file).worksheet(page_validation)
    data = wks_preguntas.get_all_values()
    headers = data.pop(0)
    df_validation = pd.DataFrame(data, columns=headers)
    nro_delivery_agent = list_option(df_validation,column="nro_delivery_agent")
    
    # product_list
    product_list = list_option(df_validation,column="product")
    country_type_list = list_option(df_validation,column="country_type")
    purchase_channel_list = list_option(df_validation,column="purchase_channel")
    delivery_status_list = list_option(df_validation,column="delivery_status")
    checkout_status_list = list_option(df_validation,column="checkout_status")
    #nro_delivery_agent = list_option(df_validation,column="nro_delivery_agent")
    
    
    return render_template('form_pzr.html',product_list=product_list,country_type_list=country_type_list,
                          purchase_channel_list=purchase_channel_list,
                          delivery_status_list=delivery_status_list,
                          checkout_status_list=checkout_status_list                          )

@app.route("/process",methods=["GET","POST"])
def form():
    if request.method == "GET":
        return "Invalid action"
    if request.method == "POST":
        costumer_name    = request.form["costumer_name"]
        costumer_phone   = request.form["costumer_phone"]
        product_name   = request.form["product_name"]
        purchase_channel = request.form["purchase_channel"]
        delivery_address = request.form["delivery_address"]
        link_delivery_address = request.form["link_delivery_address"]
        country_type = request.form["country_type"]
        delivery_status = request.form["delivery_status"]
        checkout_status = request.form["checkout_status"]
                
        
        # MYSQL INSERT
        # cursor = mysql.connection.cursor()
        # cursor.execute('SELECT * FROM account WHERE username = %s AND password = %s', (username, password,))
        # # Check if email account exist
        # account = cursor.fetchone()
        # print(account)
        # if account:
        #     msg = "Account already exist"
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address!'
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     msg = 'Username must contain only characters and numbers!'
        # elif not username or not password or not email:
        #     msg = 'Please fill out the form!'
        # else:
            # MYSQL INSERT
            
            
            # cursor.execute("""INSERT INTO account(id,username,name,phone,email,password) VALUES(NONE,%s,%s,%s,%s,MD5(%s))""",
            #            (username ,name ,phone ,email ,password))
            
            # mysql.connection.commit()
            # msg = "Registro exitoso"
            
            # Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
        webhook_url = 'https://hook.integromat.com/t4rg4pccv3mg53w7qr4xudlrmbtlu31o'
        #slack_data = {'text': "Sup! We're hacking shit together @HackSussex :spaghetti:"}
        json_data_form = json.dumps(request.form)
        response = requests.post(
            webhook_url, data=json_data_form,
            headers={'Content-Type': 'application/json'}
                )
        
        # text =   """%2ANombre de cliente%2A : {}%0D%0A
        #             %2ANúmerode contacto%2A : {}%0D%0A
        #             %2AProducto%2A : {}%0D%0A
        #             %2ACanal de compra%2A : {}%0D%0A
        #             %2ADirección de envío%2A : {}%0D%0A
        #             %2ALink de dirección%2A : {}%0D%0A
        #             """.format(costumer_name,costumer_phone,
        #                         product_name,purchase_channel,
        #                         delivery_address,link_delivery_address)
        
        text =   """%2ANombre de cliente%2A : {}%0D%0A%2ANúmerode contacto%2A : {}%0D%0A%2AProducto%2A : {}%0D%0A%2ACanal de compra%2A : {}%0D%0A%2ADirección de envío%2A : {}%0D%0A%2ALink de dirección%2A : {}%0D%0A""".format(costumer_name,costumer_phone,
                                product_name,purchase_channel,
                                delivery_address,link_delivery_address)
        
    
        text = text.replace(" ","%20")
        print(text)
        global nro_delivery_agent
        nro_delivery_agent = nro_delivery_agent[0]
        print(nro_delivery_agent)
        wsp_link = "https://api.whatsapp.com/send?phone={}&text={}".format(nro_delivery_agent,text)
        print(wsp_link)
        success_msg = "Tu mensaje fue guardado con éxito, ahora a enviarlo a wsp :)"
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
        
    return render_template("success_page.html",wsp_link=wsp_link,success_msg=success_msg)
        
        
        



@app.route("/user/<int:user_id>/")
def user_profile(user_id):
    return "Section to user id: {}".format(user_id)

if __name__=="__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)


# import psycopg2


# conn = psycopg2.connect(host = "cursodb.cctxmwmt5coi.us-east-1.rds.amazonaws.com",  port = "3306", dbname = "users",user = "admin", password = "11235813::"  )

# cur = conn.cursor()


# # def create_pandas_table(sql_query, database = conn):
# #     table = pd.read_sql_query(sql_query, database)
# #     return table

# create_pandas_table("SELECT * from account")