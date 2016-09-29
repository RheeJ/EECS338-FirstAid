from __future__ import unicode_literals
from django.db import models

class Graph(models.Model):
	name = models.CharField(max_length=50)

class Nodes(models.Model):
	step_number = models.IntegerField(default=0)
	instruction = models.CharField(max_length=150)
	graph = models.ForeignKey(Graph)

class AdditionalTools(models.Model):
	info_name = models.CharField(max_length=50)
	info_type = models.CharField(max_length=50)
	info_path = models.CharField(max_length=500)
	node = models.ForeignKey(Nodes, null=True)
	
