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

from manual_app.models import *

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
	
	#try:
	ins = InstructionSet.objects.create(name=instructionSet['name'])
	
	for index, step in enumerate(instructionSet['steps']):
		Step.objects.create(
			step_number = index,
			repeat = step['repeat'],
			description = step['description'],
			InstructionSet=ins)

	for tool in instructionSet['additional_tools']:
		AdditionalTools.objects.create(
			bucket = tool['bucket'],
			description = tool['description'],
			Instruction = ins)

	return Response(status=status.HTTP_201_CREATED)
	
	#except:
		#return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

