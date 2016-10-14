from __future__ import unicode_literals
from django.db import models

class InstructionSet(models.Model):
	name = models.CharField(max_length=50)

class Step(models.Model):
	step_number = models.IntegerField(default=0)
	repeat = models.IntegerField(default=0)
	description = models.CharField(max_length=500)
	InsructionSet = models.ForeignKey(InstructionSet)

class AdditionalTools(models.Model):
	bucket = models.CharField(max_length=20)
	description = models.CharField(max_length=500)
	Step = models.ForeignKey(Step)
	Instruction = models.ForeignKey(InstructionSet)
