from manual_app.models import Graph, Nodes, AdditionalTools
from rest_framework import serializers

class GraphSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Graph
        fields = ('__all__')

class NodesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Nodes
		fields = ('step_number', 'instruction', 'graph')

class ATSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = AdditionalTools
		fields = ('info_name', 'info_type', 'info_path', 'node')

		