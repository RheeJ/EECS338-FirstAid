from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from rest_framework.decorators import api_view

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

@api_view(['GET'])
def test_function(request):
	return Response("Test Backend Function")

