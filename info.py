import requests
from bs4 import BeautifulSoup as soup
from lxml import html
import json
import pprint


# Mohit's creds:-
USERNAME =  "creds"
PASSWORD = "creds"

# URLs:-
LOGIN_URL = "http://people.iitr.ernet.in/login/?next=/internship/company/list/#all_companies"
URL = "http://people.iitr.ernet.in/internship/company/list/#all_companies"

def main():
	session_requests = requests.session()

	# Get login csrf token
	result = session_requests.get(LOGIN_URL)
	tree = html.fromstring(result.text)
	authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
	print(authenticity_token)

	# Create payload
	payload = {
		"username": USERNAME, 
		"password": PASSWORD, 
		"csrfmiddlewaretoken": authenticity_token
	}

	# Perform login
	result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
	print("login successful")

	# Iterate through all companies and store their 'more-info' html content :
	page_soup = []
	compIDs = []
	result = session_requests.get(URL, headers = dict(referer = URL))
	page = soup(result.text , "html.parser")

	for row in page.find_all('tr'):
		for data in row.find_all('td'):
			for company in data.find_all('a' , href = True):
				if ('info' in company['href']): 
					compIDs.append(list(company['href'].split('/'))[-3])
					url = "http://people.iitr.ernet.in" + company['href']
					result = session_requests.get(url, headers = dict(referer = url))
					page_soup.append(soup(result.text,"html.parser"))


	ID={}
	info={}

	for x,page in enumerate(page_soup):
		tmp = {}
		for row in page.find_all('tr'):
			ctr=0
			prop=''
			
			for data in row.find_all('td'):
					infotext = data.text

					if infotext == '-': infotext = 'N/A'

					if ctr==0:
						prop = infotext
						ctr=1
					else:
						tmp[prop]= infotext

		info[compIDs[x]] = tmp
	
	pprint.pprint(info)
					

	with open("Info.json","w") as outfile:
		json.dump(info , outfile)
	

if __name__ == '__main__':
	main()