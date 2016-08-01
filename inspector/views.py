# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template.context import RequestContext
from django.contrib.auth.models import User, Group

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'index.html', {}, context_instance=RequestContext(request))

@login_required()
def logout_v(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

