from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from rest_framework.decorators import api_view

from rest_framework import viewsets
from rest_framework import permissions
from manual_app.serializers import *

from parser.parser import *
from manual_app.models import *
from itertools import *
from urllib2 import *
from os import *

S3_Library_Path = 'https://s3-us-west-2.amazonaws.com/famanual/libraries/'

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
def process_request(request):

#set up parse request++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	r = request.POST.get('query')


	"""
	SETTING UP MODELS FOR TEST. RESET ONCE DB POPULATION IS CREATED
	"""
	try:
		user = User.objects.get(username="tester")
		proxy = UserProxy.objects.get(user= user)
		ins = InstructionSet.objects.get(name="small bleeding")
		s1 = Step.objects.get(step_number=0, repeat=0, description="test step 1", InstructionSet=ins)
		s2 = Step.objects.get(step_number=1, repeat=0, description="test step 2", InstructionSet=ins)
		s3 = Step.objects.get(step_number=2, repeat=0, description="test step 3", InstructionSet=ins)
		a1 = AdditionalTools.objects.get(name="bandaid", bucket="definition", description="a gauze", Instruction=ins)
	except:
		user = User.objects.create(username="tester")
		ins = InstructionSet.objects.create(name="small bleeding")
		proxy = UserProxy.objects.create(user= user, step=0, current_instruction_set=ins)
		s1 = Step.objects.create(step_number=0, repeat=0, description="test step 1", InstructionSet=ins)
		s2 = Step.objects.create(step_number=1, repeat=0, description="test step 2", InstructionSet=ins)
		s3 = Step.objects.create(step_number=2, repeat=0, description="test step 3", InstructionSet=ins)
		a1 = AdditionalTools.objects.create(name="bandaid", bucket="definition", description="a gauze", Instruction=ins)
	"""
	FINISH SETTING MODELS
	"""
	current_step = proxy.step
	current_set = proxy.current_instruction_set
	p = Parser()
	dependencies = p.parseToStanfordDependencies(r)
	tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dependencies.dependencies]

	#finite state machine and labelling parts++++++++++++++++++++++++++++++++++++++++++++++++++++
	START = 0
	WHAT = 1
	WHEREHOWWHEN = 2

	grammar_words = {'question' : [], 'adjective' : [], 'object' : []}

	fsm = START

	for part in tupleResult:
		if fsm == START:
			if part[0] == "attr":
				grammar_words['question'] = part[2]
				fsm = WHAT
			else:
				return Response("WE ARE CURRENTLY WORKING ON MORE OPTIONS")
		elif fsm == WHAT:
			if part[0] == "amod" and part[2] not in grammar_words['adjective']:
				grammar_words['adjective'].append(part[2])
			elif part[0] == "det" and part[1] not in grammar_words['object']: 
				grammar_words['object'].append(part[1])
			elif part[0] == "nsubj" and part[2] not in grammar_words['object']:
				grammar_words['object'].append(part[2])
		else:
			return Response("WE ARE CURRENTLY WORKING ON MORE OPTIONS")

	#tree to bucket++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	if fsm == WHAT:
		#Basic Navigation
		if "next" in grammar_words['object'] or "next" in grammar_words['adjective']:
			current_step += 1
			try:
				return_val = current_set.step_set.get(step_number=current_step).description
				proxy.step = current_step
				proxy.save()
			except:
				return_val = "EOF"
			return Response(return_val)
		elif "previous" in grammar_words['object'] or "previous" in grammar_words['adjective']:
			current_step -= 1
			try:
				return_val = current_set.step_set.get(step_number=current_step).description
				proxy.step = current_step
				proxy.save()
			except:
				return_val = "BOF"
			return Response(return_val)

		#Basic Tool Description
		else:
			return_val = []
			for word in grammar_words['object']:
				try:
					tmp = current_set.additionaltools_set.get(bucket="definition", name=word)
					return_val.append({ word : tmp.description })
				except:
					pass
			return Response(return_val)
	else:
		return Response("WE ARE CURRENTLY WORKING ON MORE OPTIONS")