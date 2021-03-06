# -*- coding: utf-8 -*-

# Builtin Modules

# 3rd-party Modules

# Project Modules
from worker.utils import toolkit, yaml_resources

CONFIG = yaml_resources.get('CONFIG')

def before_app_create():
    APP_NAME_SERVER = CONFIG['APP_NAME'] + '-server'
    APP_NAME_WORKER = CONFIG['APP_NAME'] + '-worker'

    def get_cache_key(topic, name, tags=None, app_name=None):
        cache_key = toolkit._get_cache_key(topic, name, tags)

        # Add app name to cache key
        app_name = app_name or APP_NAME_WORKER
        cache_key_with_app_name = '{}#{}'.format(app_name, cache_key)
        return cache_key_with_app_name

    toolkit.get_cache_key = get_cache_key

    def get_server_cache_key(topic, name, tags=None):
        return toolkit.get_cache_key(topic, name, tags, APP_NAME_SERVER)

    toolkit.get_server_cache_key = get_server_cache_key

    def get_worker_queue(name):
        worker_queue = toolkit._get_worker_queue(name)

        # Add queue prefix to queue name
        worker_queue_with_prefix = '{}#{}'.format(APP_NAME_WORKER, worker_queue)
        return worker_queue_with_prefix

    toolkit.get_worker_queue = get_worker_queue

def after_app_created(celery_app):
    from worker.tasks.dataflux_func import dataflux_func_reload_scripts, dataflux_func_auto_cleaner, dataflux_func_auto_run

    # 启动时自动执行
    dataflux_func_reload_scripts.apply_async(kwargs={'sleepDelay': 10, 'isOnLaunch': True, 'force': True})
    dataflux_func_auto_cleaner.apply_async(kwargs={'sleepDelay': 30})
    dataflux_func_auto_run.apply_async(kwargs={'sleepDelay': 10})
