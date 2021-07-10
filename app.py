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
    #nro_delivery_agent = list_option(df_validation,column="nro_delivery_agent")

    # product_list
    product_list = list_option(df_validation,column="product")
    quantity_product_list = list_option(df_validation,column="quantity_product")
    country_type_list = list_option(df_validation,column="country_type")
    purchase_channel_list = list_option(df_validation,column="purchase_channel")
    #delivery section
    delivery_status_list = list_option(df_validation,column="delivery_status")
    delivery_type_list = list_option(df_validation,column="delivery_type")
    delivery_agent_list = list_option(df_validation,column="delivery_agent")
    checkout_status_list = list_option(df_validation,column="checkout_status")

    #nro_delivery_agent = list_option(df_validation,column="nro_delivery_agent")


    return render_template('new-order-created.html',#'form_pzr.html',
                            product_list=product_list,country_type_list=country_type_list,
                          quantity_product_list=quantity_product_list,
                          purchase_channel_list=purchase_channel_list,
                          delivery_status_list=delivery_status_list,
                          delivery_type_list=delivery_type_list,
                          delivery_agent_list=delivery_agent_list,
                          checkout_status_list=checkout_status_list                          )

@app.route("/process",methods=["GET","POST"])
def form():
    print(request.method)
    data = request.form
    data = data.to_dict()
    print(request.form)
    if request.method == "GET":
        return "Invalid action"
    if str(request.method) == "POST":
        customer_name    = data["costumer_name"]
        
        customer_phone   = data["costumer_phone"]

        product_name   = data["product_name"]
        quantity_product  = data["quantity_product"]
        purchase_channel = data["purchase_channel"]
        delivery_address = data["delivery_address"]
        link_delivery_address = data["link_delivery_address"]
        country_type = data["country_type"]

        delivery_status = data["delivery_status"]
        delivery_type = data["delivery_type"] # new
        delivery_agent = data["delivery_agent"] # new

        checkout_status = data["checkout_status"]
        print(checkout_status)
        print("hola")
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

        json_data_form = json.dumps(data)
        print(json_data_form)
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
        msg_costumer = "Pizarra Club - Detalle Pedido"
        text_agent =   """%2ANombre de cliente%2A : {}%0D%0A%2ANúmerode contacto%2A : {}%0D%0A%2AProducto%2A : {}%0D%0A%2ACantidad%2A : {}%0D%0A%2ACanal de compra%2A : {}%0D%0A%2ADirección de envío%2A : {}%0D%0A%2ALink de dirección%2A : {}%0D%0A%2ATIPO DE ENVIO%2A : {}%0D%0A%2AAgente asignado%2A : {}%0D%0A""".format(customer_name,customer_phone,
                                product_name,quantity_product,purchase_channel,
                                delivery_address,link_delivery_address,delivery_type,delivery_agent)
        text_customer =   """%2A===================%2A%0D%0A{}%0D%0A%2ACliente%2A : {}%0D%0A%2AProducto%2A : {}%0D%0A%2ACanal de compra%2A : {}%0D%0A%2ADirección de envío%2A : {}%0D%0A%2ALink de dirección%2A : {}%0D%0A%2ATIPO DE ENVIO%2A : {}%0D%0A""".format(msg_costumer,customer_name,product_name,purchase_channel,
                                delivery_address,link_delivery_address,delivery_type)


        text_agent = text_agent.replace(" ","%20")
        text_customer = text_customer.replace(" ","%20")
        print(text_customer)
        global nro_delivery_agent
        global df_validation
        #agent contact from sheets
        nro_delivery_agent_column =  "nro_delivery_agent_"+str(delivery_agent)
        nro_delivery_agent = list_option(df_validation,column=nro_delivery_agent_column)
        nro_delivery_agent = nro_delivery_agent[0]
        #customer contact from form
        customer_phone = str(customer_phone).strip()
        print(nro_delivery_agent)
        wsp_link_agent = "https://api.whatsapp.com/send?phone={}&text={}".format(nro_delivery_agent,text_agent)
        wsp_link_customer = "https://api.whatsapp.com/send?phone={}&text={}".format(customer_phone,text_customer)
        print(wsp_link_agent)
        success_msg = "Tu mensaje fue guardado con éxito, ahora a enviarlo a wsp :)"
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

        return render_template("thanks-order.html",#"success_page.html",
                               wsp_link_agent=wsp_link_agent,
                               wsp_link_customer=wsp_link_customer,
                               success_msg=success_msg,
                               delivery_type=delivery_type)






@app.route("/user/<int:user_id>/")
def user_profile(user_id):
    return "Section to user id: {}".format(user_id)

if __name__=="__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
