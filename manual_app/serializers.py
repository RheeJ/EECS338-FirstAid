from manual_app.models import *
from rest_framework import serializers

class InstructionSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstructionSet
        fields = ('__all__')

class StepSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Step
		fields = ('__all__')

class ATSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = AdditionalTools
		fields = ('__all__')

		