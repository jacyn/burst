from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, QueryDict, HttpResponse
from django.template import RequestContext, loader as template_loader
from django.shortcuts import render, render_to_response

@login_required
def main(request, template_name="dashboard/main.html"):
    context = RequestContext(request)

    http_response = render_to_response(
        template_name, 
        {
        },
        context_instance=context,
    )
    return http_response

def redirect_to_main(request):
    return HttpResponseRedirect(reverse('dashboard:main'))
