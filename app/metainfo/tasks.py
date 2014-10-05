from celery import task

from metainfo.geventapps import PullMetaAsync


@task()
def create_user():
    sync = PullMetaAsync
    sync.start_pull()
