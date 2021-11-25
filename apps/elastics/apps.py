from __future__ import unicode_literals
from django.apps import AppConfig
# from elasticsearch_dsl.connections import connections
# from .utils import default_conn
# import logging
#
# log = logging.getLogger('elastic')

class ElasticsConfig(AppConfig):
    name = 'elastics'

    # def ready(self):
    #     connections.configure(default_conn.EsConnectionPool)