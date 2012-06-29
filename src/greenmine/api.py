from tastypie.resources import ModelResource, ALL
from greenmine.models import *

#class GMAuthorization(Authorization):
#    def is_authorized(request, object):
#        pass

class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()

class MilestoneResource(ModelResource):
    class Meta:
        queryset = Milestone.objects.all()

class UserStoryResource(ModelResource):
    class Meta:
        queryset = UserStory.objects.all()

class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()

class DocumentResource(ModelResource):
    class Meta:
        queryset = Document.objects.all()

class QuestionResource(ModelResource):
    class Meta:
        queryset = Question.objects.all()

class WikiPageResource(ModelResource):
    class Meta:
        queryset = WikiPage.objects.all()
