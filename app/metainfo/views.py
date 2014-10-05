import time

from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy

from metainfo.models import Domain, MetaInfo
from metainfo.geventapps import PullMetaAsync
from metainfo.forms import DomainForm


class DomainListView(ListView):
    model = Domain
    template_name = 'metainfo/domain_list.html'


class DomainDetailView(DetailView):
    model = Domain
    template_name = 'metainfo/domain_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DomainDetailView, self).get_context_data(**kwargs)
        try:
            context['meta'] = MetaInfo.objects.get(domain=self.object)
        except ObjectDoesNotExist:
            context['meta'] = None
        return context


class DomainCreateView(CreateView):
    template_name = 'metainfo/domain_create.html'
    model = Domain
    form_class = DomainForm
    success_url = reverse_lazy('domains:list')


class DomainDetailSyncView(DetailView):
    model = Domain
    template_name = 'metainfo/sync_results.html'

    def get_context_data(self, **kwargs):
        context = super(DomainDetailSyncView, self).get_context_data(**kwargs)
        _startTime = time.time()
        self.object.pull_meta_info()
        context['meta_pulled'] = 1
        context['elapsed_time'] = time.time() - _startTime
        return context


class DomainAllSyncView(TemplateView):

    template_name = 'metainfo/sync_results.html'

    def get_context_data(self, **kwargs):
        context = super(DomainAllSyncView, self).get_context_data(**kwargs)
        _startTime = time.time()
        sync = PullMetaAsync()
        sync.start_pull()
        context['meta_pulled'] = len(sync.meta_obj_list)
        context['elapsed_time'] = time.time() - _startTime
        return context


domain_list = DomainListView.as_view()
domain_detail = DomainDetailView.as_view()
domain_create = DomainCreateView.as_view()
domain_sync_all = DomainAllSyncView.as_view()
domain_sync_detail = DomainDetailSyncView.as_view()
