from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.template import loader
from rest_framework.decorators import api_view
import json

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
from question_parser import *

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

@api_view(['POST'])
def setInstructionSet(request):

	# instruction set json object
	instructionSet = json.loads(request.body, strict=False)
	
	try:
		ins = InstructionSet.objects.get(name=instructionSet['name'])
	except:
		ins = InstructionSet.objects.create(name=instructionSet['name'])
	
	for index, step in enumerate(instructionSet['steps']):
		try:
			Step.objects.get(
				step_number = index,
				repeat = step['repeat'],
				InstructionSet=ins)
		except:
			Step.objects.create(
				step_number = index,
				repeat = step['repeat'],
				description = step['description'],
				InstructionSet=ins)

	for tool in instructionSet['additional_tools']:
		try:
			AdditionalTools.objects.get(
				name = tool['name'],
				bucket = tool['bucket'],
				Instruction = ins)
		except:
			AdditionalTools.objects.create(
				name = tool['name'],
				bucket = tool['bucket'],
				description = tool['description'],
				Instruction = ins)

	return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def process_request(request):

	"""
	set up parse request++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	"""
	r = request.POST.get('query')

	user = User.objects.get(username="tester")
	proxy = UserProxy.objects.get(user= user)
	proxy.current_instruction_set = InstructionSet.objects.get(name="Thermal Burn")
	proxy.save()
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
