from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.template import loader
from rest_framework.decorators import api_view
import json
import os

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
from nltk import *

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
	for idx, warnings in enumerate(data['warnings']):
		try:
			wng = Warnings.objects.get(
				Instruction = ins,
				description = warnings['description'])
		except:
			wng = Warnings.objects.create(
				description = warnings['description'],
				Instruction = ins)
		context = { 'type' : 'warning', 'name' : warnings['description'], 'sentence' : "if "+warnings['description']+", then see a doctor as soon as possible" }
		packaged_result = sentence_analyze(context)
		for result in packaged_result:
				try:
					ats = AdditionalTools.objects.get(
						name = warnings['description'],
						description = result['description'],
						Instruction = ins)
				except:
					ats = AdditionalTools.objects.create(
						name = warnings['description'],
						description = result['description'],
						Instruction = ins)
				for question in result['questions']:
					try:
						qst = Questions.objects.get(
							question = question,
							instructionset = ins,
							answer = ats)
					except:
						qst = Questions.objects.create(
							question = question,
							instructionset = ins,
							answer = ats)
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
							instructionset = ins,
							step = stp,
							answer = ats)
					except:
						qst = Questions.objects.create(
							question = question,
							instructionset = ins,
							step = stp,
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
						instructionset = ins,
						answer = ats)
				except:
					qst = Questions.objects.create(
						question = question,
						instructionset = ins,
						answer = ats)
	return HttpResponse("Posting successful")

@api_view(['POST'])
def process_definition(request):
	try:
		user = User.objects.get(username="new_user")
		proxy = UserProxy.objects.get(user= user)
		proxy.save()
	except:
		user = User.objects.create(username="new_user")
		ins = InstructionSet.objects.get(name="bruise")
		proxy = UserProxy.objects.create(user= user, step = 0, current_instruction_set = ins)
	r = request.POST.get('query')
	words = r.split(' ')
	#Layer 2 (Query the set)
	result = ""
	answer = Questions.objects.filter(question=r, instructionset=proxy.current_instruction_set)
	step_binary = 0
	if answer:
		for ans in answer:
			if not ans.step:
				step_binary = 1
				result = result + ans.answer.description + ". "
			else:
				pass
		if step_binary == 1:
			return HttpResponse(result)
		else:
			pass
	else:
		pass
	#Layer 3 (Compound definition queries)
	answer = ""
	partial = ""
	POS_words = parseOnlineStanford(r)
	for phrase in ['what is', "what's", 'how do I', 'what do you mean by', 'how to']:
		if phrase in r:
			for word in POS_words:
				if word[1] == "VB":
					question = "what is " + word[0]
					try:
						part = Questions.objects.get(question = question, instructionset = proxy.current_instruction_set).answer.description
						answer = "to " + word[0] + " is to " + part
					except:
						pass
				elif word[1] == "JJ":
					question = "what is " + word[0]
					try:
						part = Questions.objects.get(question = question, instructionset = proxy.current_instruction_set).answer.description
						partial =" which is " + word[0] + " or " + part
					except:
						pass
				elif word[1] == "NN":
					question = "what is " + word[0]
					try:
						part = Questions.objects.get(question=question, instructionset= proxy.current_instruction_set).answer.description
						if answer != "":
							answer = answer + " a " + word[0] + " or " + part
						else:
							answer = part
					except:
						pass
			answer = answer + partial
			if answer != "":
				return HttpResponse(answer)
	return HttpResponse("looking online")

@api_view(['POST'])
def process_navigational(request):
	navigational_next = ["what is the next step",
							"next",
							"what's next",
							"what is next",
							"what else"
	]
	navigational_prev = ["what is the previous step",
							"previous",
							"go back",
							"what was the last step",
							"what did you say previously",
	]
	navigational_repeat = ["can you say that again",
							"repeat",
							"what",
							"say again",
							"come again"
	]
	try:
		user = User.objects.get(username="new_user")
		proxy = UserProxy.objects.get(user= user)
		proxy.save()
	except:
		user = User.objects.create(username="new_user")
		ins = InstructionSet.objects.get(name="bruise")
		proxy = UserProxy.objects.create(user= user, step = 0, current_instruction_set = ins)
	r = request.POST.get('query')
	words = r.split(' ')

	#Layer 0 (Check Navigational or Set Instruction)
	print r
	if r in navigational_next:
		current_step = proxy.step + 1
		current_set = proxy.current_instruction_set
		try:
			return_val = current_set.step_set.get(step_number=current_step).description
			proxy.step = current_step
			proxy.save()
			return HttpResponse(return_val)
		except:
			return HttpResponse("there are no more instructions")
	elif r in navigational_prev:
		current_step = proxy.step - 1
		current_set = proxy.current_instruction_set
		try:
			return_val = current_set.step_set.get(step_number=current_step).description
			proxy.step = current_step
			proxy.save()
			return HttpResponse(return_val)
		except:
			return HttpResponse("this is the first instruction. " + current_set.step_set.get(step_number=0).description)
	elif r in navigational_repeat:
		return HttpResponse(proxy.current_instruction_set.step_set.get(step_number=proxy.step).description)
	if "how do you treat " in r:
		obj = r.replace("how do you treat ", "")
		try:
			proxy.current_instruction_set = InstructionSet.objects.get(name=obj)
			proxy.step = 0
			proxy.save()
			warns = proxy.current_instruction_set.warnings_set.all()
			result = "See a doctor immediately if you experience any of these: "
			for w in warns:
				result = result + w.description + ", "
			return HttpResponse("This is how you treat a "+proxy.current_instruction_set.name+". " + result)
		except:
			return HttpResponse("we couldn't find the manual you were looking for")
	#Layer 4 (Online query (possible elasticsearch))
	return HttpResponse("we had trouble parsing your navigational request")

@api_view(['POST'])
def process_step_question(request):
	try:
		user = User.objects.get(username="new_user")
		proxy = UserProxy.objects.get(user= user)
		proxy.save()
	except:
		user = User.objects.create(username="new_user")
		ins = InstructionSet.objects.get(name="bruise")
		proxy = UserProxy.objects.create(user= user, step = 0, current_instruction_set = ins)
	r = request.POST.get('query')
	words = r.split(' ')
	#Layer 1 (Query all steps)
	current_step = proxy.step
	result = ""
	stp = proxy.current_instruction_set.step_set.get(step_number=current_step)
	answer = Questions.objects.filter(question=r, step=stp, instructionset=proxy.current_instruction_set)
	if answer:
		for ans in answer:
			result = result + ans.answer.description + ". "
		return HttpResponse(result)
	else:
		pass
	if r not in ["what are the details for this step", "can I have more details", "what else", "what else should I know", "what more", "why"]:
		answer = Questions.objects.filter(question=r, instructionset=proxy.current_instruction_set)
		result = ""
		if answer:
			for ans in answer:
				result = result + ans.answer.description + ". "
			return HttpResponse(result)
		else:
			pass
	return HttpResponse("something else")

#FOR MORE DETAILS
@api_view(['POST'])
def process_step_all(request):
	try:
		user = User.objects.get(username="new_user")
		proxy = UserProxy.objects.get(user= user)
		proxy.save()
	except:
		user = User.objects.create(username="new_user")
		ins = InstructionSet.objects.get(name="bruise")
		proxy = UserProxy.objects.create(user= user, step = 0, current_instruction_set = ins)
	r = request.POST.get('query')
	words = r.split(' ')
	if words[-1] == 'this' or words[-1] == 'step':
		result = ""
		stp = proxy.current_instruction_set.step_set.get(step_number=current_step)
		answers = AdditionalTools.objects.filter(step = stp, instructionset=proxy.current_instruction_set)
		if answer:
			for ans in answer:
				result = result + ans.description + ". "
			return HttpResponse(result)
		else:
			pass
		return HttpResponse("there are no more details for the current step")
	else:
 		all_answers = proxy.current_instruction_set.additionaltools_set.all()
 		result = "" 
 		if all_answers:
			for answer in all_answers:
				if words[-1] in answer.name or words[-1] in answer.description:
					result = result + answer.description + ". "
			return HttpResponse(result)
		return HttpResponse("there are no details regarding your request")

#FOR WARNINGS REPEATED
@api_view(['POST'])
def process_warnings(request):
	try:
		user = User.objects.get(username="new_user")
		proxy = UserProxy.objects.get(user= user)
		proxy.save()
	except:
		user = User.objects.create(username="new_user")
		ins = InstructionSet.objects.get(name="bruise")
		proxy = UserProxy.objects.create(user= user, step = 0, current_instruction_set = ins)
	r = request.POST.get('query')
	words = r.split(' ')
	result = ""
	for tmp in proxy.current_instruction_set.warnings_set.all():
		result = result + tmp.description + ", "
	return HttpResponse(result)

def online_answers(string):
	url = "https://www.google.com/search?q="
	words = string.split(" ")
	for word in words:
		url += word
		url += "+"
		url = url[:-1]
		html = get(url).text
		soup = BeautifulSoup(html, 'html.parser')
		section = soup.find('div', {'class' : '_sPg'})
		if section != None:	
			answer = section.getText()
			break
		else:
			answer = "I don't know"
	return answer
