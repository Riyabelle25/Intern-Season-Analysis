import requests
from bs4 import BeautifulSoup as soup
from lxml import html
import json

# Mohit's creds:-
USERNAME = "add creds here" 
PASSWORD = "add creds here"

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

	# Perform login :
	result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
	print("login successful")

	# Iterate through all companies and store their 'open-to-which-branches' urls : 	
	urls = []
	result = session_requests.get(URL, headers = dict(referer = URL))
	page = soup(result.text , "html.parser")

	for row in page.find_all('tr'):
		for data in row.find_all('td'):
			for company in data.find_all('a' , href = True):
				if ('opento' in company['href']): urls.append(("http://people.iitr.ernet.in" + company['href']))

	# Navigate to each url and store the html content :
	page_soup = []

	for Url in urls:
		result = session_requests.get(Url, headers = dict(referer = Url))
		page_soup.append(soup(result.text , "html.parser"))

	# Iterate through page_soup, and map each company to the branches they're recruiting from, into a dict :
	OpenToBranches = {}
	

	for page in page_soup:
		thisBranches = []

		for data in page.find('h3'): thisCompany = data[:-12]

		for data in page.find_all('div', class_= 'tab-pane active'):
			for branch in data.find_all('li'):
				thisBranches.append(branch.contents[0])

			OpenToBranches[thisCompany] = thisBranches


	# Dump dict to Json file: 
	with open("Open-to.json","w") as outfile:
		json.dump(OpenToBranches , outfile)


if __name__ == '__main__':
	main()

