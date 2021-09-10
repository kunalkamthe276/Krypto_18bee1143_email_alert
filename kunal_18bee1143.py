# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 20:28:56 2021

@author: lenovo
"""

import requests
import time
import json
import sqlite3
from sqlite3 import Error

def send_upper(tp):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox53d078ce6f804ad58ddb9b70f812c672.mailgun.org/messages",
		auth=("api", "47960c178a31158a117534b767a7c174-a3c55839-43ccf981"),
		data={"from": "Excited User <mailgun@sandbox53d078ce6f804ad58ddb9b70f812c672.mailgun.org>",
			"to": ["kunalkamthe276@gmail.com", "YOU@sandbox53d078ce6f804ad58ddb9b70f812c672.mailgun.org"],
			"subject": "Price alert ",
			"text": "the price have been increased above the trigger = {0}".format(tp)})

def send_lower(tp):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox53d078ce6f804ad58ddb9b70f812c672.mailgun.org/messages",
		auth=("api", "47960c178a31158a117534b767a7c174-a3c55839-43ccf981"),
		data={"from": "Excited User <mailgun@sandbox53d078ce6f804ad58ddb9b70f812c672.mailgun.org>",
			"to": ["kunalkamthe276@gmail.com", "YOU@sandbox53d078ce6f804ad58ddb9b70f812c672.mailgun.org"],
			"subject": "Price alert ",
			"text": "the price have been decreased below the trigger={0}".format(tp)})

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
    
connection = create_connection("F:\\sm_app.sqlite")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")



posts_table = """
CREATE TABLE IF NOT EXISTS posts(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  title TEXT,
  iftrig INTEGER 
);
"""



while True:
    
  execute_query(connection, posts_table)
  btcprice = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false", headers = {'accept': 'application/json'}).json ()
  tp=btcprice[0]["current_price"]
  print(tp)
  if int(tp)>100000 : 
    send_upper()
    create_users = """INSERT INTO posts_table(title,iftrig) VALUES (send_upper.text,1);"""
    execute_query(connection, create_users)  

  if int(tp)< 100000 :
    send_upper(tp)
    create_users = """INSERT INTO posts_table(title,iftrig) VALUES (send_upper.text,1);"""
    execute_query(connection, create_users) 


time.sleep (10)



