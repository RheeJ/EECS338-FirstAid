from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from rest_framework.decorators import api_view

@api_view(['GET'])
def test_function(request):
	return Response("Test Backend Function")

