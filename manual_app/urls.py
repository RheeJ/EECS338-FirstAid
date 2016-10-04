from django.conf.urls import url, include
from views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'graph', GraphViewSet, 'graph')
router.register(r'nodes', NodesViewSet, 'nodes')
router.register(r'additionals', ATViewSet, 'additionaltools')

urlpatterns = [
	url(r'^', include(router.urls)),
]