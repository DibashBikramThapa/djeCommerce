from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class IndexPage(TemplateView):
    template_name = 'index.html'
