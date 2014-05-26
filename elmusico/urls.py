import os.path

from django.views.generic import TemplateView, RedirectView

from django.conf.urls import patterns, include, url

from django.contrib import admin

from bookmarks.views import *
admin.autodiscover()

site_media = os.path.join(
	os.path.dirname(__file__), '../site_media'
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'elmusico.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^$', main_page),
    # \w: alphanumeric characters with underscore
    (r'^user/(\w+)/$', user_page),
    # session manager part
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': site_media }),
    (r'^register/$', register_page),
    (r'^register/success/$',
        TemplateView.as_view(template_name='registration/register_success.html')),
    # DML part
    (r'^create_artist/$', artist_save_page),
    (r'^create_musician/$', musician_save_page),
    (r'^create_album/$', album_save_page),

    # querry part
    (r'^search/$', search_page),
    url(r'^admin/', include(admin.site.urls)),
)
