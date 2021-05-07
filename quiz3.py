import requests
import json
import sqlite3

# Declared necessary variables (url and headers to send request)

url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/covid-ovid-data/sixmonth/GEO"
headers = {
    'x-rapidapi-key': "f82a4dc724msh96b6f957df9819ep1bd155jsnef3ac0a403ad",
    'x-rapidapi-host': "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
}

# Got response from server and saved it in different variables
# Created JSON file and imported response in it

response = requests.request("GET", url, headers=headers)
data = json.loads(response.text)

with open('CoVid19.json', 'w') as f:
    json.dump(data, f, indent=4)

# Created new connection with CoVid Database

conn = sqlite3.connect('CoVid19.sqlite')
c = conn.cursor()

# Created table

query = "CREATE TABLE covid" \
        "(id VARCHAR(50) PRIMARY KEY ," \
        "date VARCHAR(10)," \
        "new_cases INTEGER," \
        "new_deaths INTEGER," \
        "new_tests INTEGER);"
c.execute(query)

# Printed information about CoVid Statistics and put data into database table
# "For" cycle helped me to get into list items (dictionaries) in JSON file

print('\n\nSARS CoV2 STATISTICS IN GEORGIA\n')

for i in data:
    print(f'\nDate:        {i["date"]}'
          f'\nNew Cases:   {i["new_cases"]}'
          f'\nNew Deaths:  {i["new_deaths"]}'
          f'\nNew Tests:   {i["new_tests"]}')
    query = f'INSERT INTO covid (id, date, new_cases, new_deaths, new_tests) ' \
            f'VALUES ("{i["id"]}","{i["date"]}", {i["new_cases"]}, {i["new_deaths"]}, {i["new_tests"]})'

    c.execute(query)
conn.commit()
conn.close()
