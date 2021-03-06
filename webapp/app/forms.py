import sys
from datetime import date, datetime

from django import forms
from django.core.exceptions import ValidationError
from django.template import Template
from django.template.defaultfilters import slugify

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Div, Button, HTML, Hidden
from crispy_forms.bootstrap import FormActions

from app import models as app_models
from app import fields


class ProjectForm(forms.ModelForm):
    class Meta:
        model     = app_models.Project
        fields    = '__all__'
        exclude   = ( 'added_by', )

    helper = FormHelper()
    helper.form_tag = True
    helper.form_class = "form-horizontal style-form"

    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'

    helper.layout = Layout(
        Field('owner', css_class='form-control'),
        Field('name', css_class='form-control'),
        Field('slug', css_class='form-control'),
        Field('description', css_class='form-control'),
        FormActions(
            Submit('save_changes', "Save", css_class="btn btn-theme"),
            HTML("""<a class="btn btn-default" 
                      href="{% if project_detail %}{% url 'app:read_project' project_detail.pk %}{% else %}{% url 'app:projects' %}{% endif %}"
                    >Cancel</a>"""),
        ),
    )
    
    def __init__(self, project=None, *args, **kwargs):

        initial = { }
        if 'initial' in kwargs:
            initial = kwargs.get('initial')
            del kwargs['initial']

        if project:
            for fname in ProjectForm().fields.keys():
                initial[fname] = getattr(project, fname)

        super(ProjectForm, self).__init__(initial=initial, *args, **kwargs)

        
    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()

        return cleaned_data

    def get_new_model(self, **kwargs):
        d = self.cleaned_data
        defaults = dict(d)
        defaults.update({
            "added_by": kwargs.get('added_by'),
        });
        return app_models.Project(**defaults)

    def update_model_instance(self, model):
        for fname in self.cleaned_data.keys():
            setattr(model, fname, self.cleaned_data.get(fname))


class PageForm(forms.ModelForm):
    class Meta:
        model     = app_models.Page
        fields    = '__all__'
        exclude   = ( 'added_by', )

    helper = FormHelper()
    helper.form_tag = True
    helper.form_class = "form-horizontal style-form"

    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'

    helper.layout = Layout(
        Field('project', css_class='form-control'),
        Field('name', css_class='form-control'),
        Field('slug', css_class='form-control'),
        FormActions(
            Submit('save_changes', "Save", css_class="btn btn-theme"),
            HTML("""<a class="btn btn-default" 
                      href="{% if page_detail %}{% url 'app:read_page' page_detail.pk %}{% else %}{% url 'app:pages' %}{% endif %}"
                    >Cancel</a>"""),
        ),
    )
    
    def __init__(self, page=None, *args, **kwargs):

        initial = { }
        if 'initial' in kwargs:
            initial = kwargs.get('initial')
            del kwargs['initial']

        if page:
            for fname in PageForm().fields.keys():
                initial[fname] = getattr(page, fname)

        super(PageForm, self).__init__(initial=initial, *args, **kwargs)

        
    def clean(self):
        cleaned_data = super(PageForm, self).clean()

        return cleaned_data

    def get_new_model(self, **kwargs):
        d = self.cleaned_data
        defaults = dict(d)
        defaults.update({
            "added_by": kwargs.get('added_by'),
        });
        return app_models.Page(**defaults)

    def update_model_instance(self, model):
        for fname in self.cleaned_data.keys():
            setattr(model, fname, self.cleaned_data.get(fname))


class ObjectPropertiesForm(forms.ModelForm):
    class Meta:
        model     = app_models.Object
        fields    = '__all__'
        widgets   = {
                   'background_color': forms.widgets.TextInput(attrs={'type': 'color', 'value': '#000000'}),
                   'font_color': forms.widgets.TextInput(attrs={'type': 'color', 'value': '#ffffff'}),
                   }

    helper = FormHelper()
    helper.form_tag = False

    helper.layout = Layout(
        Field('name', css_class='form-control input-sm'),
        Field('background_image', css_class='form-control input-sm'),
        Field('background_color', css_class='form-control input-sm color'),
        Field('background_transparency', css_class='form-control input-sm'),
        Field('font_color', css_class='form-control input-sm color'),
        Field('font_size', css_class='form-control input-sm'),
        Field('text_align', css_class='form-control input-sm'),
    )

    def __init__(self, properties=None, *args, **kwargs):
        initial = { }
        if 'initial' in kwargs:
            initial = kwargs.get('initial')
            del kwargs['initial']
        if properties:
            for fname in ObjectPropertiesForm().fields.keys():
                initial[fname] = getattr(properties, fname)

        super(ObjectPropertiesForm, self).__init__(initial=initial, *args, **kwargs)

        
    def clean(self):
        cleaned_data = super(ObjectPropertiesForm, self).clean()

        for req_field in [ 'sequence', 'code', 'name', 
                        'x', 'y', 'width', 'height'
                        ]:
            if (len(str(cleaned_data.get(req_field, ''))) == 0):
                raise ValidationError, u"Required field: %s" % req_field

        return cleaned_data


    def get_new_model(self, **kwargs):
        d = self.cleaned_data
        defaults = dict(d)
        defaults.update({
            "page": kwargs.get('page'),
        });
        return app_models.Object(**defaults)

    def update_model_instance(self, model):
        for fname in self.cleaned_data.keys():
            setattr(model, fname, self.cleaned_data.get(fname))



class SurveyForm(forms.ModelForm):
    class Meta:
        model = app_models.Survey
        fields = '__all__'
        exclude = [ 'title', 'slug', 'submit', 'thanks', 'active', 'label', 'field_type', 'page_object', 'redirect_url', ] # exclude


    helper = FormHelper()
    helper.form_tag = False

    def __init__(self, form, context, *args, **kwargs):
        """
        Dynamically add each of the form fields for the given form model
        instance and its related field model instances.

        ref: https://github.com/stephenmcd/django-forms-builder/blob/master/forms_builder/forms/forms.py
        """

        self.form = form
        self.form_fields = form.survey_questions.all().filter(active=True).order_by("id")
        initial = kwargs.pop("initial", {})
        # If a FormEntry instance is given to edit, stores it's field
        # values for using as initial data.
        field_entries = {}
        if kwargs.get("instance"):
            for question in kwargs["instance"].survey_questions.all().filter(active=True).order_by("id"):
                field_entries[question.field_id] = question.value
        super(SurveyForm, self).__init__(*args, **kwargs)

        crispy_layout_fields = []
        # Create the form fields.
        for field in self.form_fields:
            field_key = field.slug
            field_class = fields.CLASSES[field.field_type]
            field_widget = fields.WIDGETS.get(field.field_type)
            field_args = {"label": field.label, "required": field.required,
                          "help_text": field.help_text}

            arg_names = field_class.__init__.__code__.co_varnames
            #if "max_length" in arg_names:
            #    field_args["max_length"] = settings.FIELD_MAX_LENGTH
            if "choices" in arg_names:
                choices = list(field.get_choices())
                if (field.field_type == fields.SELECT and
                        field.default not in [c[0] for c in choices]):
                    choices.insert(0, ("", field.placeholder_text))
                field_args["choices"] = choices
            if field_widget is not None:
                field_args["widget"] = field_widget
            #
            #   Initial value for field, in order of preference:
            #
            # - If a form model instance is given (eg we're editing a
            #   form response), then use the instance's value for the
            #   field.
            # - If the developer has provided an explicit "initial"
            #   dict, use it.
            # - The default value for the field instance as given in
            #   the admin.
            #
            initial_val = None
            try:
                initial_val = field_entries[field.id]
            except KeyError:
                try:
                    initial_val = initial[field_key]
                except KeyError:
                    initial_val = Template(field.default).render(context)
            if initial_val:
                if field.is_a(*fields.MULTIPLE):
                    initial_val = split_choices(initial_val)
                if field.field_type == fields.CHECKBOX:
                    initial_val = initial_val != "False"
                self.initial[field_key] = initial_val
            self.fields[field_key] = field_class(**field_args)

            if field.field_type == fields.DOB:
                now = datetime.now()
                years = list(range(now.year, now.year - 120, -1))
                self.fields[field_key].widget.years = years


            # Add identifying CSS classes to the field.
            css_class = field_class.__name__.lower()

            """
            if field.required:
                css_class += " required"
                if field.field_type not in (fields.CHECKBOX_MULTIPLE, fields.CHECKBOX):
                    self.fields[field_key].widget.attrs["required"] = ""
            """
            self.fields[field_key].widget.attrs["class"] = css_class
            if field.placeholder_text and not field.default:
                text = field.placeholder_text
                self.fields[field_key].widget.attrs["placeholder"] = text

            if field.field_type not in (fields.RADIO_MULTIPLE, fields.CHECKBOX_MULTIPLE, fields.CHECKBOX):
                self.fields[field_key].widget.attrs["class"] = "form-control input-sm"

            crispy_layout_fields.append(Field(field_key))

        crispy_layout_fields.append(
            FormActions(
                Submit('save_changes', form.submit, css_class="btn btn-theme btn-sm"),
            )
        )

        self.helper.layout = Layout(
            *crispy_layout_fields
            )

    def get_new_model(self, **kwargs):
        d = self.cleaned_data
        survey = kwargs.get('survey')
        defaults = dict()
        defaults.update({
            "survey": survey,
        });

        return app_models.SurveyResult(**defaults)

    def set_related_objects(self, model):
        d = self.cleaned_data
        for slug in d.keys():
            question = model.survey.survey_questions.get(slug=slug)
            model.answers.add( app_models.SurveyAnswer(question=question, value=d.get(slug)) )

        print >> sys.stderr, "%s" % model
        return model


class CustomSurveyForm(forms.ModelForm):
    class Meta:
        model     = app_models.Survey
        fields    = '__all__'
        widgets = {
          'thanks': forms.Textarea(attrs={'rows':3, }),
        }

    helper = FormHelper()
    helper.form_tag = False

    helper.layout = Layout(
        Field('title', css_class='form-control input-sm'),
        Field('thanks', css_class='form-control input-sm'),
        Field('redirect_url', css_class='form-control input-sm'),
        Field('submit', css_class='form-control input-sm'),
        Field('active', css_class='form-control input-sm'),
        FormActions(
            Submit('save_changes', 'Submit', css_class="btn btn-theme btn-sm"),
        ),
    )
    
    def __init__(self, survey=None, *args, **kwargs):
        initial = { }
        if 'initial' in kwargs:
            initial = kwargs.get('initial')
            del kwargs['initial']
        if survey:
            for fname in CustomSurveyForm().fields.keys():
                initial[fname] = getattr(survey, fname)

        super(CustomSurveyForm, self).__init__(initial=initial, *args, **kwargs)

    def get_new_model(self, **kwargs):
        d = self.cleaned_data
        defaults = dict(d)
        defaults.update({
            "page_object": kwargs.get('page_object'),
        });
        return app_models.Survey(**defaults)

    def update_model_instance(self, model):
        for fname in self.cleaned_data.keys():
            setattr(model, fname, self.cleaned_data.get(fname))



class CustomSurveyQuestionForm(forms.ModelForm):
    class Meta:
        model     = app_models.SurveyQuestion
        exclude = ('survey', 'active', )

    helper = FormHelper()
    helper.form_tag = False

    helper.layout = Layout(
        Field('label', css_class='form-control input-sm'),
        Field('field_type', css_class='form-control input-sm'),
        Field('choices', css_class='form-control input-sm'),
        Field('placeholder_text', css_class='form-control input-sm'),
        #Field('help_text', css_class='form-control'),
        Field('required', css_class='input-sm'),
        FormActions(
            Submit('save_changes', 'Submit', css_class="btn btn-theme btn-sm"),
        ),
    )
    
    def __init__(self, survey_question=None, *args, **kwargs):
        initial = { }
        if 'initial' in kwargs:
            initial = kwargs.get('initial')
            del kwargs['initial']

        if survey_question:
            for fname in CustomSurveyQuestionForm().fields.keys():
                initial[fname] = getattr(survey_question, fname)

        super(CustomSurveyQuestionForm, self).__init__(initial=initial, *args, **kwargs)

    def clean(self):
        cleaned_data = super(CustomSurveyQuestionForm, self).clean()

        for req_field in [ 'label', 'field_type' ]:
            if (len(str(cleaned_data.get(req_field, ''))) == 0):
                raise ValidationError, u"Required field: %s" % req_field

        slug = 'fld_' + cleaned_data.get('label')
        cleaned_data['slug'] = slugify( slug ).replace('-', '_')

        return cleaned_data

    def get_new_model(self, **kwargs):
        d = self.cleaned_data
        defaults = dict(d)
        defaults.update({
            "survey": kwargs.get('survey'),
        });
        return app_models.SurveyQuestion(**defaults)

    def update_model_instance(self, model):
        for fname in self.cleaned_data.keys():
            setattr(model, fname, self.cleaned_data.get(fname))

