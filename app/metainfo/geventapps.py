import metadata_parser

from gevent import monkey, joinall, spawn
from django.utils import timezone

from metainfo.models import Domain, MetaInfo


monkey.patch_all(thread=False)


class PullMetaAsync():

    def __init__(self):
        self.meta_obj_list = []
        self.updated_domain_list = []

    def pull_meta_info(self, domain):
        try:
            url = metadata_parser.MetadataParser(url=domain.domain)
            meta = url.metadata.get('meta')
            page = url.metadata.get('page')
            meta_info_obj = MetaInfo(
                domain=domain,
                description=meta.get('description', None),
                keywords=meta.get('keywords', None),
                title=page.get('title', None),
                image=page.get('image', None)
            )
            self.meta_obj_list.append(meta_info_obj)
            self.updated_domain_list.append(domain.id)
        except:
            pass

    def start_pull(self):
        threads = [spawn(self.pull_meta_info, domain) for domain in
                   Domain.objects.filter(last_sync__isnull=True)]
        joinall(threads)

        MetaInfo.objects.bulk_create(self.meta_obj_list)
        # Update last_sync time
        Domain.objects.filter(id__in=self.updated_domain_list).update(
            last_sync=timezone.now())
