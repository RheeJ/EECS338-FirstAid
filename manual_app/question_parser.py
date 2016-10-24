from manual_app.models import *
from requests import *
from urllib2 import *
from bs4 import BeautifulSoup

def parseOnlineStanford(query):
	"""
	PARAM:
	-query => string
	OUTPUT:
	-list of dictionaries with values (tag, word)
	"""
	r = post("http://nlp.stanford.edu:8080/parser/index.jsp", { 'query' : query })
	string_html = r.text
	section = string_html.split('<h3>Tagging</h3>')[1]
	section2 = section.split('<div style="clear: left"> </div>')[0]
	soup = BeautifulSoup(section2, 'html.parser')
	ret = []
	for info in soup.findAll('div'):
		try:
			edited_string = info.string.strip('\n ')
			split_string = edited_string.split('/')
			entry = { 'word' : split_string[0], 'tag' : split_string[1] }
			ret.append(entry)
		except:
			pass
	return ret

def navigational(word, proxy):
	"""
	PARAM:
	-word => string
	-proxy => UserProxy object
	Output:
	-string
	"""
	current_step = proxy.step
	current_set = proxy.current_instruction_set
	if word == "next":
		current_step += 1
		try:
			return_val = current_set.step_set.get(step_number=current_step).description
			proxy.step = current_step
			proxy.save()
		except:
			return_val = "There are no more instructions!"
		return return_val
	elif word == "previous":
		current_step -= 1
		try:
			return_val = current_set.step_set.get(step_number=current_step).description
			proxy.step = current_step
			proxy.save()
		except:
			return_val = "This is the first instruction! " + current_set.step_set.get(step_number=0).description
		return return_val
	else:
		return 0
