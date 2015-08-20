from django.conf.urls import patterns, url

urlpatterns = patterns('app.views',
    url(r'^$', 'project.main', name='projects'),
    url(r'^project/$', 'project.main', name='projects'),
    url(r'^project/add/$', 'project.add', name='add_project'),
    url(r'^project/edit/(\d+)/$', 'project.edit', name='edit_project'),
    url(r'^project/read/(\d+)/$', 'project.read', name='read_project'),
    url(r'^project/switch/(\d+)/(1|0)/$', 'project.switch_status', name='switch_project'),

    url(r'^page/$', 'page.main', name='pages'),
    url(r'^page/add/$', 'page.add', name='add_page'),
    url(r'^page/edit/(\d+)/$', 'page.edit', name='edit_page'),
    url(r'^page/read/(\d+)/$', 'page.read', name='read_page'),
    url(r'^page/switch/(\d+)/(1|0)/$', 'page.switch_status', name='switch_page'),

    url(r'^layout/(\d+)/$', 'layout.main', name='layout_main'),
    url(r'^layout/objects/$', 'layout.objects', name='layout_objects'),
    url(r'^layout/object/image/$', 'layout.object_image', name='object_image'),
    url(r'^layout/object/properties/$', 'layout.object_properties', name='object_properties'),
    url(r'^layout/save/$', 'layout.save', name='save_layout'),
    url(r'^layout/preview/$', 'layout.preview', name='layout_preview'),

    url(r'^survey/$', 'survey.survey', name='survey'),
    url(r'^survey/preview/$', 'survey.preview', name='survey_preview'),
    url(r'^survey/handler/$', 'survey.handler', name='survey_handler'),
    url(r'^survey/question/$', 'survey.question', name='survey_question'),
    url(r'^survey/properties/$', 'survey.properties', name='survey_properties'),
    url(r'^survey/reports/$', 'survey.reports', name='survey_reports'),
    url(r'^survey/delete/$', 'survey.delete', name='survey_delete'),

    )
