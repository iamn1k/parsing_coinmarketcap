# import necessary library
import requests
from bs4 import BeautifulSoup as BS 
import csv

def process_price(s):
		s = s[1:]
		return s.replace(',','')
def process_designation(s):
	try:
		s = s.replace('*','')
	except:
		pass
	finally:
		s = s.split(' ')
		s = list(filter(lambda x: x != '',s))
		return s[-1]
def write_csv(arr):
	with open('crypto.csv','a') as f:
		writer = csv.writer(f)
		writer.writerow((arr[0],arr[1],arr[2],arr[3]))
		f.close()	

def get_data(link):
	r = requests.get(link)
	soup = BS(r.text,'lxml')
	table = soup.find_all('tr',class_='cmc-table-row')
	for block in table:
		try:
			name = block.find('div',class_='sc-1kxikfi-0 fjclfm cmc-table__column-name').find('a').text
		except:
			name = ''
		try:
			price = block.find('td',class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price').find('a').text
			price = process_price(price)
		except:
			price = ''	
		try: 
			link_on_crypto = 'coinmarketcap.com' + block.find('td',class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price').find('a').get('href')
		except:
			link_on_crypto = ''
		try: 	
			designation = block.find('td',class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply').text
			designation = process_designation(designation)
		except:
			designation = ''
			data = [name,designation,price,link_on_crypto]	
			write_csv(data)
i = 1
while True:
	try:
		get_data('https://coinmarketcap.com/ru/' + str(i) + '/')
		print('current page: ',str(i))
	except:
		print('no pages more ',str(i))
		break
	i += 1

