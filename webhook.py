import urllib
import json
import os
import csv
from flask import Flask , request,  make_response, render_template
import MysqlConnect as connection
from mysql.connector import Error
import re

app = Flask(__name__)

@app.route("/webhook/index")
def index():
    return render_template("index.html") 

@app.route('/webhook',methods = ['POST'])
def webhook():
    conn = connection.ConnectMySql()
    req = request.get_json(silent=True , force= True)
    res = makeWebhookResult(req)
    res = json.dumps(res , indent=4)
    print(res)
    r = make_response(res)
    print(r)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    print(req)
    if req.get("queryResult").get("action")=="order_placed":
        pizzadb = connection.ConnectMySql()
        update_table = connection.update_table(pizzadb)
        if pizzadb != False and update_table != False:
            result = req.get("queryResult")
            parameters = result.get("parameters")
            pizza_size = parameters.get("pizza_size")
            pizza_variety = parameters.get("pizza_variety")
            no_of_pizza = int(parameters.get("no_of_pizza"))
            amount = no_of_pizza*100
            name = parameters["name"]["name"]
            phone_no = parameters.get("phone_no")
            Email_id = parameters.get("Email_id")
            Address = parameters.get("Address")
            toppings = parameters.get("toppings")
            
            try:
                mycursor = pizzadb.cursor()
                sql = "INSERT INTO list_of_orders (Name, Email_Id, Address, Phone_no, No_of_pizza, pizza_size, type_of_pizza, toppings, amount, order_time,preparation_time,delivery_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW()+1,NOW()+200,NOW()+400)"
                val = (name,Email_id,Address,phone_no,no_of_pizza,pizza_size,pizza_variety,toppings,amount)
                mycursor.execute(sql,val)
                pizzadb.commit()
                id_num = mycursor.lastrowid
                speech = "Your Order is placed :)<br/> Order ID : " + str(id_num) + "<br/> Name : " + name + "<br/> Pizza ordered : " + str(no_of_pizza) + " " + pizza_size + " " + pizza_variety + "<br/> Amount : " +str(amount)+ "<br/> order status : ordered <br/> Do you want to check your status?"
                return{
                "fulfillmentText" : speech,
                "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses": {
                        "simpleResponses": [ {
                            "textToSpeech": speech
                        }]
                    }
                }]
                
            }
            except Error as err:
                print(err)
                return{
                "fulfillmentText" : "Sorry some error has occured :(",
                "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses": {
                        "simpleResponses": [ {
                            "textToSpeech": "Sorry some error has occured :("
                        }]
                    }
                }]
                
            }

            print(name)

        else:
            return{
                "fulfillmentText" : "Sorry some error has occured :(",
                "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses": {
                        "simpleResponses": [ {
                            "textToSpeech": "Sorry some error has occured :("
                        }]
                    }
                }]
                
            }


    if req.get("queryResult").get("action")=="search_order" or req.get("queryResult").get("action")=="Searchorder.Searchorder-custom":
        pizzadb = connection.ConnectMySql()
        update_table = connection.update_table(pizzadb)
        if pizzadb != False and update_table != False:
            result = req.get("queryResult")
            parameters = result.get("parameters")
            id_num = int(parameters.get("id"))
            try:
                mycursor = pizzadb.cursor()
                select_query = "select status_of_order from list_of_orders where id = %s"
                search_id = (str(id_num),)
                mycursor.execute(select_query,search_id)
                myresult = mycursor.fetchall()
                print(myresult)
                speech =""
                if len(myresult) == 0:
                    speech += "Please check your order id"
                else:
                    for i in myresult:
                        status = i[0]
                        speech += "Your Order is status :)<br/> Order ID : " + str(id_num) + "<br/> order status : " + status 
                return{
                "fulfillmentText" : speech,
                "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses": {
                        "simpleResponses": [ {
                            "textToSpeech": speech
                        }]
                    }
                }]
                
            }
            except Error as err:
                print(err)
                return{
                "fulfillmentText" : "Sorry some error has occured :(",
                "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses": {
                        "simpleResponses": [ {
                            "textToSpeech": "Sorry some error has occured :("
                        }]
                    }
                }]
                
            }
        
        else:
            return{
                "fulfillmentText" : "Sorry some error has occured :(",
                "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses": {
                        "simpleResponses": [ {
                            "textToSpeech": "Sorry some error has occured :("
                        }]
                    }
                }]
                
            }


if __name__ == "__main__":
    port = int(os.getenv('PORT', 80))
    print("starting on port %d" %(port))
    app.run(debug= True, port= 80)