from django.contrib import admin
from .models import Graph, Nodes, AdditionalTools

admin.site.register(Graph)
admin.site.register(Nodes)
admin.site.register(AdditionalTools)