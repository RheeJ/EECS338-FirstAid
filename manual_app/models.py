from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class InstructionSet(models.Model):
	name = models.CharField(max_length=50)

class Step(models.Model):
	step_number = models.IntegerField(default=0)
	description = models.CharField(max_length=500)
	InstructionSet = models.ForeignKey(InstructionSet)

class AdditionalTools(models.Model):
	name = models.CharField(max_length=500)
	description = models.CharField(max_length=500)
	Step = models.ForeignKey(Step, null=True)
	Instruction = models.ForeignKey(InstructionSet)

class Warnings(models.Model):
	description = models.CharField(max_length=500)
	Instruction = models.ForeignKey(InstructionSet)

class UserProxy(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	step = models.IntegerField(default=0)
	current_instruction_set = models.ForeignKey(InstructionSet, blank=True, null=True)

class Questions(models.Model):
	question = models.CharField(max_length=500)
	instructionset = models.ForeignKey(InstructionSet)
	step = models.ForeignKey(Step, null=True)
	answer = models.ForeignKey(AdditionalTools)