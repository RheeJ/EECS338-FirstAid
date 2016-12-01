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
	url(r'^ask1/$', process_definition),
	url(r'^ask2/$', process_navigational),
	url(r'^ask3/$', process_step_all),
	url(r'^ask4/$', process_step_question),
	url(r'^ask5/$', process_warnings),
	url(r'^data_post/$', blackbox_2_store),
]