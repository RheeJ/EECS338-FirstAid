from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from rest_framework.decorators import api_view

from rest_framework import viewsets
from rest_framework import permissions
from manual_app.serializers import GraphSerializer, NodesSerializer, ATSerializer

from manual_app.models import Graph, Nodes, AdditionalTools

class GraphViewSet(viewsets.ModelViewSet):
	queryset = Graph.objects.all()
	serializer_class = GraphSerializer

class NodesViewSet(viewsets.ModelViewSet):
	queryset = Nodes.objects.all()
	serializer_class = NodesSerializer

class ATViewSet(viewsets.ModelViewSet):
	queryset = AdditionalTools.objects.all()
	serializer_class = ATSerializer

@api_view(['GET'])
def test_function(request):
	return Response("Test Backend Function")

