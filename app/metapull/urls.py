from django.conf.urls import patterns, include, url
from django.contrib import admin
from metainfo.views import DomainListView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'metapull.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', DomainListView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^domains/', include('metainfo.urls', namespace = 'domains')),
)
