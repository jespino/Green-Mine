# -*- coding: utf-8 -*-

from django.views.generic import View
from django.views.decorators.cache import cache_page
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext, loader
from django.contrib import messages
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator

class GenericView(View):
    """ Generic view with some util methods. """

    def get_context(self):
        return self.get_auth_context()

    def get_auth_context(self):
        print 1
        self.user = self.request.user
        if self.request.user.is_authenticated():
            return {'user': self.request.user}
        else:
            return {'user': None}

    def render(self, template_name, context={}, **kwargs):
        if not context:
            context = self.get_context()

        return render_to_response(template_name, context, 
            context_instance=RequestContext(self.request))

    
class ProjectGenericView(GenericView):
    """ Generic View Template for all views relationed with projects. """

    def get_context(self):
        context = super(ProjectGenericView, self).get_context()
        context['project'] = self.project
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=kwargs['projectid'])
        except Project.DoesNotExist:
            raise Http404('project does not exist')

        return super(ProjectGenericView, self).dispatch(request, *args, **kwargs)

