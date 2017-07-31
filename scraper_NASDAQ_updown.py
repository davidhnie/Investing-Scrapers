#Author: David
#combine with earnings -> ticker, date, event_type-[upgrades/downgrades/initiated.. . . - from-to] / [exceeded/met/failed-percentage]

import bs4 as bs
import urllib
import urllib.request
import re 
import csv
from datetime import datetime, timedelta, date

link="http://www.nasdaq.com/earnings/daily-analyst-recommendations.aspx?type="
types=["upgraded","downgraded","initiated","reiterated"]


data=[["Company", "Symbol", "Event_type", "Market", "Brokerage", "From/Initial Recommendation", "To", "Footer Date"]]

for j in range(4):
	page = urllib.request.urlopen(link+types[j])
	soup = bs.BeautifulSoup(page,'html.parser')

	table = soup.find('div',{'class':'genTable'})
	rows=table.find_all('tr')[1:]
	for i in range(len(rows)):
		company = rows[i].td.string
		company = re.sub(r'&amp;', r'&', company)
		company = re.sub(r';', r'', company)

		symbol = rows[i].h3.a.string.strip()
		market = rows[i].find_all('td')[2].string
		brokerage = rows[i].find_all('td')[3].string
		if (j != 2):
			froms = rows[i].find_all('td')[4].string
			tos = rows[i].find_all('td')[5].string
		else:
			froms = rows[i].find_all('td')[4].string
			tos = rows[i].find_all('td')[4].string
		#print(str(i) +" "+ str(j))
		#print(company)
		footer=soup.find('div', {'class':'floatR marginT10px'}).small.contents[-1][6:]

		cols = [company, symbol, types[j], market, brokerage, froms, tos,footer]
		data.append(cols)


#add time to file name
today = datetime.combine(date.today(), datetime.min.time())
with open ('NADSAQ-updowns-'+today.strftime('%m-%d-%Y')+'.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	a.writerows(data)