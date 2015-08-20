import sys
import simplejson as json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, QueryDict, HttpResponse
from django.template import RequestContext, loader as template_loader
from django.shortcuts import render, render_to_response
from django.middleware.csrf import get_token
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt

from easy_thumbnails.files import get_thumbnailer
from filer.models import Image, File

from app import forms as app_forms
from app import models as app_models


@login_required
def main(request, page_id=None, template_name="layout/main.html"):
    context = RequestContext(request)

    page = None
    if page_id:
        page = app_models.Page.objects.get(pk=page_id)
  
    http_response = render_to_response(
        template_name, 
        {
            'page': page,
        },
        context_instance=context,
    )
    return http_response


def redirect_to_main(request, page_id=None):
    if page_id:
        return HttpResponseRedirect(reverse('app:layout_main', args=[page_id]))
    
    return HttpResponseRedirect(reverse('app:pages'))


def objects(request):

    page_id = request.GET.get("page_id", None)
    if not request.is_ajax():
        messages.error(request, 'This action requires javascript (ajax).')
        return redirect_to_main(request)

    layout_objects = [ obj.as_dict() for obj in app_models.Object.objects.filter(active=True, page__pk=page_id).order_by('sequence') ]
    return HttpResponse(json.dumps(layout_objects), content_type="application/json")

def object_image(request):

    if not request.is_ajax():
        messages.error(request, 'This action requires javascript (ajax).')
        return redirect_to_main(request)

    filename = request.GET.get("filename", None)

    try:
        # FIXME: one only; get the latest upload
        image = File.objects.get(original_filename=filename)
    except File.DoesNotExist, e:
        image = None

    url = None
    if image is not None:
        options = {"size": (image.width, image.height), "crop": True}
        url = get_thumbnailer(image).get_thumbnail(options).url

    j = json.dumps({"url": url})
    return HttpResponse(j, content_type="application/json", status=200)


@csrf_exempt
def save(request):

    if not request.is_ajax():
        messages.error(request, 'This action requires javascript (ajax).')
        return redirect_to_main(request)

    submit_status = {
        "changed": [],
        "added": [],
        "deleted": [],
        "errors": [],
        }

    errors = []
    if request.method == "POST":
        post_data = json.loads(request.POST.copy()['data'])

        for key in post_data.keys():
            data = post_data[key]

            if data["background_image"]:
                try:
                    image = File.objects.get(original_filename=data["background_image"])
                except File.DoesNotExist, e:
                    image = None
                data["background_image"] = image

            page = app_models.Page.objects.get(pk=data["page"])

            try:
                properties = app_models.Object.objects.get(code=data["code"], page=page)
            except app_models.Object.DoesNotExist, dne:
                properties = None
     
            form = app_forms.ObjectPropertiesForm(data=data)
            if form.is_valid():
                if properties:
                    if form.cleaned_data.get('active'):
                        # existing
                        form.update_model_instance(properties)
                        properties.save()

                        submit_status["changed"].append(data["name"])
                    else:
                        # delete object
                        properties.delete()
                        submit_status["deleted"].append(data["name"])
                else:
                    if form.cleaned_data.get('active'):
                        # new object
                        properties = form.get_new_model(page=page)
                        properties.save()
                        submit_status["added"].append(data["name"])

            else:
                for error in form.errors["__all__"]:
                    errors.append(error)

        status_message = dict(
            error= "",
            success= "",
            )
        if len(errors):
            status_message["error"] = "Failed to save layout. %s " % ", ".join(errors)
        else:
            status_message["success"] = "Successfully saved layout of page '%s'." % page.name

        j = json.dumps({"messages": status_message})
        return HttpResponse(j, content_type="application/json", status=200)


  
@csrf_exempt
def object_properties(request, template_name="layout/form.html"):
    context = RequestContext(request)

    if not request.is_ajax():
        messages.error(request, 'This action requires javascript (ajax).')
        return redirect_to_main(request)

    data = request.POST.copy()

    image = None
    if data["background_image"]:
        try:
            image = File.objects.get(original_filename=data["background_image"])
        except File.DoesNotExist, e:
            image = None
    data["background_image"] = image

    form = app_forms.ObjectPropertiesForm(data=data)
    context.update({
        'form': form,
    });

    fragment = template_loader.render_to_string(template_name, context)
    return HttpResponse(fragment, content_type="text/html", status=200)


def preview(request, template_name="layout/preview.html"):
    context = RequestContext(request)

    http_response = render_to_response(
        template_name, 
        {
        },
        context_instance=context,
    )
    return http_response

def view(request, project_slug=None, page_slug=None, template_name="layout/view.html"):
    context = RequestContext(request)

    if (project_slug is None) and (page_slug is None):
        raise Http404()

    page = None
    try:
        page = app_models.Page.objects.get(slug=page_slug, project__slug=project_slug)
    except app_models.Page.DoesNotExist, dne:
        page = None
        raise Http404()

    http_response = render_to_response(
        template_name, 
        {
            "page": page,
        },
        context_instance=context,
    )
    return http_response

