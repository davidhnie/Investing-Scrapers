#Author: David Nie
#to be run daily - will only return today's dividends

import bs4 as bs
import urllib
import urllib.request
import re 
import csv
import http.client

#work around the 403 error

http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

investing = "https://www.investing.com/dividends-calendar/"

req = urllib.request.Request(investing, headers={'User-Agent': 'Mozilla/5.0'})
filedescriptor = urllib.request.urlopen(req)
img = filedescriptor.read()

http.client.HTTPConnection._http_vsn = 11
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.1'

#contains data
data=[["Symbol","Date"]]

soup = bs.BeautifulSoup(img,'html.parser')
table = soup.find('table',{'id':'dividendsCalendarData'})
table_body=table.find('tbody')

#get date
daterow = table_body.find_all('tr')[0]
date = re.findall(' .*\n',daterow.getText())[0][1:-1]

#append info onto data
rows = table_body.find_all('tr')[1:]
for i in range(len(rows)):
    cols = [re.findall('[(].*?[)]', rows[i].getText())[-1][1:-1],date]
    data.append(cols)

#write data to csv
with open ('D:\\Safe_IKF\\IKF_DimaN\\Projects\\Web_data_scrapers\\Output_files\\investing_com-div-'+date+'.csv','w',newline='') as fp:
	a = csv.writer(fp,delimiter=',')
	a.writerows(data)