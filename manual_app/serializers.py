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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="myapp:user-detail")

    class Meta:
        model = User
        fields = ('username')

class ProxySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = UserProxy
		fields = ('__all__')