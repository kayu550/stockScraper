import re
import json
import csv
from io import StringIO
from bs4 import BeautifulSoup
import requests

url_stats = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'
url_profile = 'https://finance.yahoo.com/quote/{}/profile?p={}'
url_financials = 'https://finance.yahoo.com/quote/{}/financials?p={}'

stock = 'NWF.NZ'

response = requests.get(url_financials.format(stock,stock))
soup = BeautifulSoup(response.text, 'html.parser')
pattern = re.compile(r'\s--\sData\s--\s') #regex to parse through the script and find the part where the data begins. 
script_data = soup.find('script', text=pattern).contents[0] #the data that is from the list.
#print(script_data[-500:])

start_position = script_data.find("context")-2
json_data = json.loads(script_data[start_position:-12]) 
#print(json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys())
annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
#print(annual_is[0]['netIncome'])

annual_is_stats = []

for s in annual_is:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except KeyError:
            continue
        except TypeError:
            continue
    annual_is_stats.append(statement)

#print(annual_is_stats[0])


response = requests.get(url_profile.format(stock,stock))
soup = BeautifulSoup(response.text, 'html.parser')
pattern = re.compile(r'\s--\sData\s--\s') #regex to parse through the script and find the part where the data begins. 
script_data = soup.find('script', text=pattern).contents[0] #the data that is from the list.
#print(script_data[-500:])

start_position = script_data.find("context")-2
json_data1 = json.loads(script_data[start_position:-12]) 

#print(json_data1['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail'])

response = requests.get(url_stats.format(stock,stock))
soup = BeautifulSoup(response.text, 'html.parser')
pattern = re.compile(r'\s--\sData\s--\s') #regex to parse through the script and find the part where the data begins. 
script_data = soup.find('script', text=pattern).contents[0] #the data that is from the list.
start_position = script_data.find("context")-2
json_data2 = json.loads(script_data[start_position:-12]) 

#print(json_data2['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics'])

stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?'

param = {
    'period1' : '1580190947',
    'period2' : '1611813347',
    'interval' : '1d',
    'events' : 'history'
    }

param1 = {
    'range' : '5y',
    'interval' : '1wk',
    'events' : 'history'
    }

response1 = requests.get(stock_url.format(stock), params=param1)
#print(response1.text)




file = StringIO(response1.text)
reader = csv.reader(file)
data = list(reader)

for row in data[:5]:
    print(row)

