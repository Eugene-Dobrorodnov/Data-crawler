from django.conf.urls import patterns, url


urlpatterns = patterns('metainfo.views',
    url(r'^$', 'domain_list', name = 'list'),
    url(r'^create$', 'domain_create', name = 'create'),
    url(r'^(?P<pk>[\d-]+)$', 'domain_detail', name = 'detail'),
    url(r'^sync$', 'domain_sync_all', name = 'sync_all'),
    url(r'^(?P<pk>[\d-]+)/sync$', 'domain_sync_detail', name = 'sync_detail'),
)
