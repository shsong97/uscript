from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'scripts.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^scripts/', include('scripts.urls',namespace='scripts')),
)
