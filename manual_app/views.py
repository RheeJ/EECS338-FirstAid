from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from rest_framework.decorators import api_view

from rest_framework import viewsets
from rest_framework import permissions
from manual_app.serializers import *

from manual_app.models import *
from itertools import *
from urllib2 import *

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
def user_question_parse(request):
	user_request = request.POST.get('query')
	f0 = urlopen(S3_Library_Path + 'definitions.txt')
	f1 = urlopen(S3_Library_Path + 'verbose.txt')
	f2 = urlopen(S3_Library_Path + 'navigation.txt')
	for row0, row1, row2 in izip(f0, f1, f2):
		if row0 in user_request:
			return Response("A")
		elif row1 in user_request:
			return Response("B")
		elif row2 in user_request:
			return Response("C")
		else:
			return Response("D")