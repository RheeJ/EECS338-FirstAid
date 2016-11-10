from django.conf.urls import url, include
from views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'instruction', InstructionSetViewSet, 'instruction')
router.register(r'step', StepViewSet, 'step')
router.register(r'additionals', ATViewSet, 'additionaltools')
router.register(r'questions', QuestionsViewSet, 'questions')

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^ask/$', process_request),
	url(r'^data_post/$', blackbox_2_store),
]