from django.conf.urls import patterns, include, url

from django.contrib import admin

from bookmarks.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'elmusico.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^$', main_page),
    # \w: alphanumeric characters with underscore
    (r'^user/(\w+)/$', user_page),
    url(r'^admin/', include(admin.site.urls)),
)
