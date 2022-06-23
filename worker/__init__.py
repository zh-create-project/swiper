import os
from celery import Celery
#设置环境变量,加载django的settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','swiper.settings')
celery_app = Celery('swiper')
celery_app.config_from_object('worker.config')
celery_app.autodiscover_tasks()

def call_by_worker(func):
    task = celery_app.task(func)
    return task.delay
"""celery启动   celery -A worker worker -l info -P eventlet,在启动时报了一个参数错误，这里使用-P eventlet解决"""