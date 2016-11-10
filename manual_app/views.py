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
from sentence_analyzer import *
from definition_parser import *

class InstructionSetViewSet(viewsets.ModelViewSet):
	queryset = InstructionSet.objects.all()
	serializer_class = InstructionSetSerializer

class StepViewSet(viewsets.ModelViewSet):
	queryset = Step.objects.all()
	serializer_class = StepSerializer

class ATViewSet(viewsets.ModelViewSet):
	queryset = AdditionalTools.objects.all()
	serializer_class = ATSerializer
	
class QuestionsViewSet(viewsets.ModelViewSet):
	queryset = Questions.objects.all()
	serializer_class = QuestionsSerializer

@api_view(['POST'])
def blackbox_2_store(request):
	# OUR REQUEST IS JSON DATA.
	data = json.loads(request.body, strict=False)
	try:
		ins = InstructionSet.objects.get(name=data['name'])
	except:
		ins = InstructionSet.objects.create(name=data['name'])
	for idx, step in enumerate(data['steps']):
		definition_input = []
		definition_input.append([])
		try:
			stp = Step.objects.get(
				step_number = idx,
				InstructionSet = ins,
				description = step['description'])
		except:
			try:
				stp = Step.objects.get(
					step_number = idx,
					InstructionSet = ins)
				stp.description = step['description']
				stp.save()
			except:
				stp = Step.objects.create(
					step_number = idx,
					description = step['description'],
					InstructionSet=ins)
		definition_input[0].append(step['description'])
		for sentence in step['sentences']:
			definition_input[0].append(step['description'])
			context = { 'type' : 'step', 'name' : step['description'], 'sentence' : sentence }
			packaged_result = sentence_analyze(context)
			for result in packaged_result:
				try:
					ats = AdditionalTools.objects.get(
						name = step['description'],
						description = result['description'],
						Step = stp,
						Instruction = ins)
				except:
					ats = AdditionalTools.objects.create(
						name = step['description'],
						description = result['description'],
						Step = stp,
						Instruction = ins)
				for question in result['questions']:
					try:
						qst = Questions.objects.get(
							question = question,
							answer = ats)
					except:
						qst = Questions.objects.create(
							question = question,
							answer = ats)
		definition_results = definition_finder(definition_input)
		for entry in definition_results:
			try:
				ats = AdditionalTools.objects.get(
					name = entry[0],
					description = entry[1],
					Instruction = ins)
			except:
				ats = AdditionalTools.objects.create(
					name = entry[0],
					description = entry[1],
					Instruction = ins)
			for question in entry[2]:
				try:
					qst = Questions.objects.get(
						question = question,
						answer = ats)
				except:
					qst = Questions.objects.create(
						question = question,
						answer = ats)
	return HttpResponse("Posting successful")

@api_view(['POST'])
def process_request(request):

	"""
	set up parse request++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	"""
	r = request.POST.get('query')

	user = User.objects.get(username="tester")
	proxy = UserProxy.objects.get(user= user)
	proxy.save()

	if "Instructions for" in r or "instructions for" in r:
		new = r.split("for ")
		val = new[1]
		proxy.current_instruction_set = InstructionSet.objects.get(name=val)
		proxy.step = 0
		proxy.save()
		return HttpResponse("Here are the instructions for " + proxy.current_instruction_set.name + ".")

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
			return HttpResponse("Did not understand!")
		else:
			return HttpResponse("Did not understand!")
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
	if return_val:
		return HttpResponse(return_val)
	else: 
		return HttpResponse("We could not find what you were looking for.")
