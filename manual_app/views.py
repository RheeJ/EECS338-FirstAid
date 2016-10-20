from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.template import loader
from rest_framework.decorators import api_view

from rest_framework import viewsets
from rest_framework import permissions
from manual_app.serializers import *

#from parser.parser import *
from requests import *
from manual_app.models import *
from itertools import *
from urllib2 import *
from os import *
from bs4 import BeautifulSoup

START = 0
WHAT = 1
WHEN = 2

class InstructionSetViewSet(viewsets.ModelViewSet):
	queryset = InstructionSet.objects.all()
	serializer_class = InstructionSetSerializer

class StepViewSet(viewsets.ModelViewSet):
	queryset = Step.objects.all()
	serializer_class = StepSerializer

class ATViewSet(viewsets.ModelViewSet):
	queryset = AdditionalTools.objects.all()
	serializer_class = ATSerializer

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

@api_view(['POST'])
def process_request(request):

	"""
	set up parse request++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	"""
	r = request.POST.get('query')

	user = User.objects.get(username="tester")
	proxy = UserProxy.objects.get(user= user)
	ins = InstructionSet.objects.get(name="small bleeding")
	s1 = Step.objects.get(step_number=0, repeat=0, description="test step 1", InstructionSet=ins)
	s2 = Step.objects.get(step_number=1, repeat=0, description="test step 2", InstructionSet=ins)
	s3 = Step.objects.get(step_number=2, repeat=0, description="test step 3", InstructionSet=ins)
	a1 = AdditionalTools.objects.get(name="bandaid", bucket="definition", description="a gauze", Instruction=ins)

	current_set = proxy.current_instruction_set 

	words = parseOnlineStanford(r)

	"""
	start analysis tree+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	"""
	fsm = START
	object_list = []
	adj_list = []
	while words:
		tmp = words.pop(0)
		if fsm == START:
			if tmp['tag'] == "WP" or tmp['tag'] == "WDT":
				fsm = WHAT
			elif tmp['tag'] == "WRB":
				fsm = WHEN
		elif fsm == WHAT:
			if tmp['tag'] == "NN":
				if tmp['word'] == "next" or tmp['word'] == "previous":
					return HttpResponse(navigational(tmp['word'], proxy))
				else:
					if tmp['word'] not in object_list:
						object_list.append(tmp['word'])
			elif tmp['tag'] == "JJ":
				if tmp['word'] == "next" or tmp['word'] == "previous":
					return HttpResponse(navigational(tmp['word'], proxy))
				else:
					if tmp['word'] not in adj_list:
						adj_list.append(tmp['word'])
		elif fsm == WHEN:
			pass
			#FILL IN LATER
		else:
			pass
	"""
	Get and Respond++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	"""
	return_val = []
	if fsm == WHAT:
		for entry in object_list:
			try:
				val = current_set.additionaltools_set.get(bucket="definition", name=entry).description
				return_val.append("A " + entry + " is " + val + '. ')
			except:
				return_val.append("I am sorry, I do not know what a " + entry + " is. ")
	return HttpResponse(return_val)

