from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class InstructionSet(models.Model):
	name = models.CharField(max_length=50)

class Step(models.Model):
	step_number = models.IntegerField(default=0)
	repeat = models.IntegerField(default=0)
	description = models.CharField(max_length=500)
	InstructionSet = models.ForeignKey(InstructionSet)

class AdditionalTools(models.Model):
	name = models.CharField(max_length=20)
	bucket = models.CharField(max_length=20)
	description = models.CharField(max_length=500)
	Instruction = models.ForeignKey(InstructionSet)

class UserProxy(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	step = models.IntegerField(default=0)
	current_instruction_set = models.ForeignKey(InstructionSet)