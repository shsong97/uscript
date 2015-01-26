from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^$', hello.views.index, name='index'),
    # url(r'^db', hello.views.db, name='db'),
    url(r'^$', 'scripts.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^scripts/', include('scripts.urls',namespace='scripts')),

)
