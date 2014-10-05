import metadata_parser

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.utils import timezone


class Domain(models.Model):
    domain = models.URLField(verbose_name=_('domain'), unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    last_sync = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.domain

    def pull_meta_info(self):
        try:
            url = metadata_parser.MetadataParser(url=self.domain)
        except:
            return False

        meta = url.metadata.get('meta')
        page = url.metadata.get('page')
        data = {
            'domain': self,
            'description': meta.get('description', None),
            'keywords': meta.get('keywords', None),
            'title': page.get('title', None),
            'image': page.get('image', None),
            'last_sync': timezone.now()
        }

        try:
            meta_obj = MetaInfo.objects.get(domain=self)
            meta_obj.title = data['title']
            meta_obj.description = data['description']
            meta_obj.keywords = data['keywords']
            meta_obj.image = data['image']
            meta_obj.save()
        except ObjectDoesNotExist:
            meta_info = MetaInfo(**data)
            meta_info.save()


class MetaInfo(models.Model):
    domain = models.ForeignKey('metainfo.Domain', unique=True)
    title = models.TextField(verbose_name=_('title'), blank=True, null=True)
    description = models.TextField(verbose_name=_('description'), blank=True,
                                   null=True)
    keywords = models.TextField(verbose_name=_('keywords'), blank=True,
                                null=True)
    image = models.URLField(verbose_name=('image'), blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.domain.domain


@receiver(post_save, sender=MetaInfo)
def set_last_sync(instance, created, **kwargs):
    """
    When creating a new MetaInfo, set last_sync time for Domain
    """
    instance.domain.last_sync = timezone.now()
    instance.domain.save()


@receiver(post_delete, sender=MetaInfo)
def remove_last_sync(instance, **kwargs):
    """
    When delete MetaInfo, reset last_sync time for Domain
    """
    instance.domain.last_sync = None
    instance.domain.save()
