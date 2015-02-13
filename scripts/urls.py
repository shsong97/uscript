from django.conf.urls import patterns, url
from scripts import views

urlpatterns = patterns('',
    url(r'^$', views.search_page, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^short/$', views.ShortIndexView.as_view(), name='short'),
    url(r'^add/$', views.ScriptsCreate.as_view(), name='scripts_add'), 
    url(r'^add/submit/$', views.scripts_add, name='add_submit'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.ScriptsUpdateView.as_view(), name='update'),
    url(r'^(?P<scripts_id>\d+)/update/submit/$', views.scripts_update, name='update_submit'),
    url(r'^(?P<scripts_id>\d+)/delete/$', views.scripts_delete, name='delete'),
    url(r'^upload/$', views.upload_view, name='upload'),
    # session
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$',views.logout_page),
    url(r'^register/$',views.register_page,name='register'), 
    url(r'^register/success/$',views.register_success),   
) 
