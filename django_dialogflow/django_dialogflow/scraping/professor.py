import requests
import re
import json
from bs4 import BeautifulSoup

BASEURL = "https://encrypted.google.com/search"

def get_prof_website(text):
	# input_text = json.loads(input_dict)['text']
	payload = {'h1':'en', 'q':text}
	soup = BeautifulSoup(requests.get(BASEURL, params=payload).text, "html5lib")

	answer = soup.findAll("a")

	print(answer)
	if not answer:
		answer = soup.findAll("span", attrs={"class": "_m3b"})
		if not answer:
			return "Sorry, google doesn't have an answer for you"
	return answer

# if __name__ == "__get_prof_website__":
string = " Stony Brook University"
print("in")
get_prof_website("Professor Zadok" + string)