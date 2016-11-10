from manual_app.models import *
from rest_framework import serializers

class InstructionSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstructionSet
        fields = ('name',
        			'step_set',)

class StepSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Step
		fields = ('step_number',
					'description',
					'additionaltools_set',)

class ATSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = AdditionalTools
		fields = ('name',
					'description',
					'questions_set')

class QuestionsSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Questions
		fields = ('__all__')