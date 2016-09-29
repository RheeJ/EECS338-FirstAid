from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def test_function(request):
	return HttpResponse("Test Backend Function")

