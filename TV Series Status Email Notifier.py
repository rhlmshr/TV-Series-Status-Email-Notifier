import sqlite3
import urllib.parse
import requests
import time
import datetime
import smtplib
import sys
import re
import logging
from yaspin import yaspin

logger = logging.Logger('catch_all')

def addToDB() :
    with yaspin(text="Adding to DB", color="cyan") as sp:
        try:
            con = sqlite3.connect(':memory:')
            c = con.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS tv_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL,
                            tv_series_list TEXT NOT NULL
                            );""")
            c.execute("INSERT INTO tv_data (email, tv_series_list) VALUES (:email, :tv_series_list);",
                    {'email': email, 'tv_series_list': ':'.join(tv_series_list)})

            sp.text = 'Added to DB'
            sp.color = 'green'
            sp.ok()

        except Exception as e:
            sp.color = 'red'
            sp.fail()

        finally:
            con.close()

    return

def findStatus() :
    mail_body = ''
    with yaspin(text="Fetching Data", color="cyan") as sp:
        try:
            for each in tv_series_list:
                api_endpoint = 'http://api.tvmaze.com/singlesearch/shows?'
                request_paramed = api_endpoint + urllib.parse.urlencode({'q': each,
                                                                    'embed': 'episodes'}) ;
                response = requests.get(request_paramed).json() ;
                show_status = ''

                if(response['status'].lower() == 'ended'):
                    show_status = 'The show has finished streaming all its episodes.'
                elif(response['status'].lower() == 'running'):

                    episode_list = response['_embedded']['episodes']
                    episode_list = sorted(episode_list, key=lambda series: series['id'], reverse=True)

                    i = 0
                    while(episode_list[i]['airdate'] == ""):
                        i += 1

                    timestamp = time.mktime(datetime.datetime.strptime(episode_list[i]['airdate'], '%Y-%m-%d').timetuple())

                    if(timestamp >= time.time()):
                        show_status = 'The next episode airs on ' + episode_list[i]['airdate']
                    else:
                        show_status = 'The show is running but airing date is not determined'

                    mail_body += '\nTv series name: ' + response['name'] + '\nStatus: ' + show_status + ' \n';

            sp.text = 'Data Fetched'
            sp.color = 'green'
            sp.ok()

            print("\n>> Fetched result:")
            print(mail_body)

            sendmail(mail_body)

        except Exception as e:
            logger.error(e)
            sp.color = 'red'
            sp.fail()

    return

def sendmail(mail_body):
    with yaspin(text="Sending Mail", color="cyan") as sp:

        #Put your credentials here:
        user = 'abc@xyz.com'
        password = 'abcd@1234'

        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(user, password)

            s.sendmail(user, email, mail_body)
            sp.text = 'Mail Sent'
            sp.ok()

        except Exception as e:
            logger.error(e)
            sp.color = 'red'
            sp.fail()

        finally:
            s.quit()

    return

while True :
    email = input("Email Address: ")
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

    if(match == None):
        print("Invalid input. Try Again.\n")
    else:
        break

while True :
    tv_series = input("TV Series: ")
    tv_series_list = tv_series.split(',')

    if(len(tv_series_list) == 0):
        print("Invalid input. Try Again.\n")
    else:
        break


addToDB()
findStatus()
