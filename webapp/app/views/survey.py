import sys
import simplejson as json

from django import get_version
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, QueryDict, HttpResponse
from django.template import RequestContext, Context, loader as template_loader
from django.shortcuts import render, render_to_response
from django.middleware.csrf import get_token
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.forms.util import ErrorList

from app import forms as app_forms
from app import models as app_models


@login_required
def survey(request, template_name='survey/form.html'):
    """
    add / update survey
    """
    context = RequestContext(request)

    survey_id = request.GET.get("id", None)
    object_id = request.GET.get("object_id", None)
    try:
        survey = None
        if survey_id:
            survey = app_models.Survey.objects.get(pk=survey_id)
    except app_models.Survey.DoesNotExist, e:
        survey = None

    page_object = None
    if object_id:
        page_object = app_models.Object.objects.get(pk=object_id)
    form = app_forms.CustomSurveyForm(survey)

    if request.method == "POST":
        form = app_forms.CustomSurveyForm(data=request.POST, instance=survey)
        if form.is_valid():
            if survey:
                if form.cleaned_data.get('active'):
                    # existing
                    form.update_model_instance(survey)
                    survey.page_object = page_object
                    survey.save()
                    #messages.success(request, 'Updated survey "%s"' % survey.title)
                else:
                    # delete object
                    form.update_model_instance(survey)
                    survey.page_object = page_object
                    survey.save()
                    #messages.success(request, 'Deleted survey "%s"')
            else:
                # new object
                survey = form.get_new_model(page_object=page_object)
                survey.save()

            j = json.dumps({"id": survey.pk})
            return HttpResponse(j, content_type="application/json", status=200)
        else:
            csrf_token_value = get_token(request)
            context.update({
                'properties': True,
                'form': form,
                'csrf_token_value': csrf_token_value,
            });
            fragment = template_loader.render_to_string(template_name, context)
            return HttpResponse(fragment, content_type="text/html", status=400)

    http_response = render_to_response(
        template_name,
        {
            'properties': True,
            'form': form,
            'survey': survey,
        },
        context_instance=context,
    )
    return http_response


@login_required
def question(request, template_name='survey/form.html'):
    """
    add / update survey question
    """
    context = RequestContext(request)

    question_id = request.GET.get("id", None)
    survey_id = request.GET.get("survey_id", None)

    try:
        survey = None
        if survey_id:
            survey = app_models.Survey.objects.get(pk=survey_id)
    except app_models.Survey.DoesNotExist, e:
        survey = None

    survey_question = None
    if survey:
        if question_id:
            survey_question = survey.survey_questions.get(pk=question_id)

    form = app_forms.CustomSurveyQuestionForm(survey_question=survey_question)
    if request.method == "POST":
        form = app_forms.CustomSurveyQuestionForm(data=request.POST, instance=survey_question)
        if form.is_valid():

            # validate uniqueness of slug
            question_exists = None
            try:
                question_exists = app_models.SurveyQuestion.objects.get(survey=survey, slug=form.cleaned_data['slug'])
            except app_models.SurveyQuestion.DoesNotExist:
                question_exists = None

            if question_exists:
                errors = form._errors.setdefault("label", ErrorList())
                errors.append(u"Question already exists")
                csrf_token_value = get_token(request)
                context.update({
                    'properties': True,
                    'form': form,
                    'csrf_token_value': csrf_token_value,
                });
                fragment = template_loader.render_to_string(template_name, context)
                return HttpResponse(fragment, content_type="text/html", status=400)

            if survey_question:
                    # existing
                form.update_model_instance(survey_question)
                survey_question.save()
            else:
                # new object
                survey_question = form.get_new_model(survey=survey)
                survey_question.save()

            j = json.dumps({})
            return HttpResponse(j, content_type="application/json", status=200)
        else:
            csrf_token_value = get_token(request)
            context.update({
                'properties': True,
                'form': form,
                'csrf_token_value': csrf_token_value,
            });
            fragment = template_loader.render_to_string(template_name, context)
            return HttpResponse(fragment, content_type="text/html", status=400)

    http_response = render_to_response(
        template_name,
        {
            'properties': True,
            'form': form,
            'survey': survey,
        },
        context_instance=context,
    )
    return http_response


@login_required
def properties(request, template_name='survey/properties.html'):
    """
    list survey details
    """
    context = RequestContext(request)

    survey_id = request.GET.get("id", None)
    object_code = request.GET.get("object", None)
    page_id = request.GET.get("page", None)

    page_object = None
    try:
        page_object = app_models.Object.objects.get(page__pk=page_id, code=object_code)
    except app_models.Object.DoesNotExist, dne:
        page_object = None

    try:
        survey = None
        if survey_id:
            survey = app_models.Survey.objects.get(pk=survey_id)
    except app_models.Survey.DoesNotExist, e:
        survey = None

    http_response = render_to_response(
        template_name, 
        {
            'survey': survey,
            'page_object': page_object,
            'object_code': object_code, 
        },
        context_instance=context,
    )
    return http_response


def preview(request, template_name='survey/form.html'):
    """
    view final survey
    """
    context = RequestContext(request)

    survey_id = request.GET.get("id", None)
    form = None
    try:
        survey = app_models.Survey.objects.get(pk=survey_id, active=True)
        form = app_forms.SurveyForm(survey, context)
    except app_models.Survey.DoesNotExist, dne:
        survey = None


    print >> sys. stderr, "%s %s " % (survey, form)
    http_response = render_to_response(
        template_name, 
        {
            'form': form,
            'survey': survey,
        },
        context_instance=context,
    )
    return http_response


def handler(request, template_name='survey/form.html'):
    """
    submit survey details
    """
    context = RequestContext(request)

    survey_id = request.GET.get("id", None)
    try:
        survey = app_models.Survey.objects.get(pk=survey_id)
    except app_models.Survey.DoesNotExist:
        survey = None

    if survey is None:
        raise Http404()
    
    if request.method == "POST":
        form = app_forms.SurveyForm(survey, context, request.POST)
        if form.is_valid():
            if form.cleaned_data.keys():
                survey_result = form.get_new_model(survey=survey)
                survey_result.save()
                if survey_result:
                    form.set_related_objects(survey_result)
                    survey_result.save()

                    j = json.dumps({
                      "thank_you_message": survey.thanks,
                      "redirect_url": survey.redirect_url
                    })
                    return HttpResponse(j, content_type="application/json", status=200)

                # add error to form that saving failed

        csrf_token_value = get_token(request)
        context.update({
            'form': form,
            'survey': survey,
            'csrf_token_value': csrf_token_value,
        });
        fragment = template_loader.render_to_string(template_name, context)
        return HttpResponse(fragment, content_type="text/html", status=400)

    j = json.dumps({})
    return HttpResponse(j, content_type="application/json", status=200)


@login_required
def reports(request, template_name='survey/reports.html'):
    context = RequestContext(request)

    surveys = None
    pages = app_models.Page.objects.all()

    page = request.GET.get('page', 0)
    survey = request.GET.get('survey', 0)
    if page:
        page = int(page)
        try:
            surveys = app_models.Survey.objects.all().filter(page_object__page__pk=page)
        except Exception, e:
            surveys = None

    if survey:
        survey = int(survey)
        surveys = surveys.filter(pk=survey)

    print >> sys.stderr, "%s" % surveys

    view_context = {
        'page': page,
        'all_pages': pages,
        'survey': survey,
        'surveys': surveys,
        'export_formats': settings.EXPORT_FORMATS,
    }

    if ('export_to' in request.GET) and (request.GET.get('export_to') in settings.MIMETYPE_MAP) and surveys:
        filetype = request.GET.get('export_to')

        page_detail = pages.get(pk=page)
        report_filename = "[SURVEY REPORT] %s - %s's %s" % (page_detail.project.owner.name, page_detail.project.name, page_detail.name)
        export_template_name = "survey/reports_template.txt"
        export_template = "%s/%s" % (settings.TEMPLATE_DIRS, export_template_name)
        loader = template_loader.get_template(export_template_name)
        report_content = loader.render(Context(view_context))
        report_fullfilename = '%s.%s' % (report_filename, filetype)

        response_kwargs = {}
        key = 'content_type' if get_version().split('.')[1] > 6 else 'mimetype'
        response_kwargs[key] = settings.MIMETYPE_MAP.get(filetype, 'application/octet-stream')

        http_response = HttpResponse(**response_kwargs)
        http_response['Content-Disposition'] = 'attachment; filename="%s"' % report_fullfilename
        http_response.write(report_content)
    else:
        http_response = render_to_response(
            template_name, 
            view_context, 
            context_instance=context,
        )
    return http_response


@login_required
def switch_question(request, survey_id=None, question_id=None, switch=0):

    active = False
    if int(switch) == 1:
        active = True

    try:
        survey = app_models.Survey.objects.get(pk=survey_id)
        survey_question = survey.survey_questions.get(pk=question_id)
        survey_question.active = active 
        survey_question.save()

        j = json.dumps({})
        return HttpResponse(j, content_type="application/json", status=200)
    except:
        j = json.dumps({})
        return HttpResponse(j, content_type="application/json", status=500)

