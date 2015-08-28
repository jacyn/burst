import sys

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager

from app import fields
from filer.fields.image import FilerImageField

from accounting import models as accounting_models

class Project(models.Model):
    owner = models.ForeignKey(
        accounting_models.Client, verbose_name=_("Project Owner"),
        related_name='projects')
    slug = models.SlugField(
        _("Slug"), max_length=64, 
        editable=True, unique=True,
        db_index=True, blank=False,
        null=False, default='')
    name = models.CharField(
        _('Name'), max_length=128,
        null=False, blank=False, 
        default='', help_text=_("Name of the Project."))
    description = models.CharField(
        _('Description'), max_length=512,
        null=True, blank=True)
    added_by = models.ForeignKey(
        User, related_name='projects')
    live_mode = models.BooleanField(
        default=False)
    datetime_added = models.DateTimeField(
        auto_now_add=True)
    last_modified = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name


class Page(models.Model):
    project = models.ForeignKey(
        Project, verbose_name=_("Project Page"),
        related_name='pages')
    slug = models.SlugField(
        _("Slug"), max_length=64,
        editable=True, db_index=True,
        blank=False, null=False, 
        default='')
    name = models.CharField(
        _('Name'), max_length=128,
        null=False, blank=False, 
        default='', help_text=_("Name of the Page."))
    added_by = models.ForeignKey(
        User, related_name='pages')
    live_mode = models.BooleanField(
        default=False)
    datetime_added = models.DateTimeField(
        auto_now_add=True)
    last_modified = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        unique_together = ('project', 'slug',)

    def __str__(self):
        return self.name


class TEXT_ALIGN:
    LEFT    = 'left'
    RIGHT   = 'right'
    CENTER  = 'center'

    CHOICES = [
            ( LEFT, 'Left' ),
            ( RIGHT, 'Right' ),
            ( CENTER, 'Center' ),
        ]

    @classmethod
    def get_choice_label(klass, choice):
        label = None
        for i in klass.CHOICES:
            if i[0] == choice:
                label = i[1]
        return label

from django.core.validators import MinValueValidator, MaxValueValidator
class Object(models.Model):
    page = models.ForeignKey(
        Page, verbose_name=_("Page"),
        related_name='page_objects')
    code = models.CharField(
        max_length=255, null=False, 
        blank=False, default="")
    sequence = models.IntegerField(
        null=False, blank=False, 
        default=0)
    name = models.CharField(
        max_length=255, null=False, 
        blank=False, default="")
    x = models.DecimalField(
        decimal_places=25, max_digits=30)
    y = models.DecimalField(
        decimal_places=25, max_digits=30)
    width = models.DecimalField(
        decimal_places=25, max_digits=30)
    height = models.DecimalField(
        decimal_places=25, max_digits=30)
    background_image = FilerImageField(
        null=True, blank=True,
        on_delete=models.SET_NULL, related_name='background_images')
    background_width = models.DecimalField(
        null=True, blank=True, 
        decimal_places=25, max_digits=30)
    background_height = models.DecimalField(
        null=True, blank=True, 
        decimal_places=25, max_digits=30)
    background_color = models.CharField(
        max_length=255, null=True, 
        blank=True)
    #SCORE_CHOICES = zip( range(1,n), range(100,n) )
    background_transparency = models.IntegerField(
        null=True, blank=True, 
        #choices=SCORE_CHOICES)
        #max_value=100, min_value=0,
        default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    font_color = models.CharField(
        max_length=255, null=True,
        blank=True)
    font_size = models.IntegerField(
        null=True, blank=True, 
        #max_value=48, min_value=8,
        default=12)
    text_align = models.CharField(
        null=False, blank=False,
        max_length=64, choices=TEXT_ALIGN.CHOICES,
        default=TEXT_ALIGN.LEFT)
    active = models.BooleanField(
        default=True)
    datetime_added = models.DateTimeField(
        auto_now_add=True)
    last_modified = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = "Object"
        verbose_name_plural = "Objects"

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "sequence": self.sequence,
            "page": self.page.pk,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "background_image": getattr( self.background_image, "original_filename", None),
            "background_image_url": getattr( self.background_image, "url", None),
            "background_width": self.background_width,
            "background_height": self.background_height,
            "background_color": self.background_color,
            "background_transparency": self.background_transparency,
            "font_color": self.font_color,
            "font_size": self.font_size,
            "text_align": self.text_align,
            "survey": list(self.survey.all().values_list('id', flat=True)),
            "active": self.active,
        }


class Survey(models.Model):
    page_object = models.ForeignKey(
        Object, null=True, 
        blank=True, related_name='survey')
    title = models.CharField(
        _('Title'), max_length=100,
        null=True, blank=True)
    thanks = models.TextField(
        _('Message displayed after submitting the survey form.'))
    redirect_url = models.CharField(
        _('Redirect URL after submitting the survey form.'), max_length=100, 
        null=True, blank=True)
    submit = models.CharField(
        _('Text for the Submit button.'), max_length=30,
        blank=True)
    active = models.BooleanField(
        default=True)
    datetime_added = models.DateTimeField(
        auto_now_add=True)
    last_modified = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        return self.title

    def copy_relations(self, oldinstance):
        for question in SurveyQuestion.objects.filter(form__pk=oldinstance.pk):
            question.pk = None
            question.save()
            self.question_set.add(
                question)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "thanks": self.thanks,
            "submit": self.submit,
            "questions": list(self.survey_questions.all().values_list('label', flat=True)),
            "active": self.active,
        }
   
    def questions_as_list(self):
        return list(self.survey_questions.all().values_list('label', flat=True))


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(
        Survey, verbose_name=_("Survey Form"),
        related_name='survey_questions')
    label = models.CharField(
        _('Question'), max_length=100)
    slug = models.SlugField(
        _("Slug"), max_length=100, 
        blank=True, editable=True,
        default='')
    field_type = models.IntegerField(
        _("Answer Type"), max_length=100, 
        choices=fields.NAMES)
    initial = models.CharField(
        _('Inital Value'), max_length=250, 
        blank=True, null=True)
    placeholder_text = models.CharField(
        _("Placeholder Text"), max_length=100,
        null=True, blank=True,
        editable=True)
    choices = models.CharField(
        _("Choices"), max_length=1000, 
        blank=True, help_text="Comma separated options where applicable. If an option "
            "itself contains commas, surround the option starting with the `"
            "character and ending with the ` character.")
    required = models.BooleanField(
        _('Required Field'), default=True)
    default = models.CharField(
        _("Default value"), max_length=2000,
        blank=True)
    help_text = models.CharField(
        _("Help text"), max_length=100, 
        blank=True)
    active = models.BooleanField(
        default=True)
    datetime_added = models.DateTimeField(
        auto_now_add=True)
    last_modified = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = "Survey Question"
        verbose_name_plural = "Survey Questions"
        unique_together = ('survey', 'slug',)

    def __str__(self):
        return self.label

    def get_choices(self):
        """
        Parse a comma separated choice string into a list of choices taking
        into account quoted choices using the ``settings.CHOICES_QUOTE`` and
        ``settings.CHOICES_UNQUOTE`` settings.
        """
        choice = ""
        quoted = False
        for char in self.choices:
            if not quoted and char == "`":
                quoted = True
            elif quoted and char == "`":
                quoted = False
            elif char == "," and not quoted:
                choice = choice.strip()
                if choice:
                    yield choice, choice
                choice = ""
            else:
                choice += char
        choice = choice.strip()
        if choice:
            yield choice, choice


class SurveyResult(models.Model):
    survey = models.ForeignKey(
        Survey, verbose_name=_("Survey Form"),
        related_name='results')
    test_mode = models.BooleanField(
        default=False)
    date_created = models.DateTimeField(
        auto_now_add=True)
    last_modified = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = "Survey Result"
        verbose_name_plural = "Survey Results"


class SurveyAnswer(models.Model):
    result = models.ForeignKey(
        SurveyResult, verbose_name=_("Survey Result"),
        related_name='answers')
    question = models.ForeignKey(
        SurveyQuestion, verbose_name=_("Survey Question"),
        related_name='answers')
    value = models.CharField(
        _('Answer'), max_length=1000,
        null=True, blank=True)
    date_created = models.DateTimeField(
        auto_now_add=True)
    last_modified = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = "Survey Answer"
        verbose_name_plural = "Survey Answers"



