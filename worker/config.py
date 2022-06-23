broker_url = 'redis://127.0.0.1:6379/0'
broker_pool_limit = 1000

timezone = 'Asia/Shanghai'
accept_content = ['pickle','json']
task_serializer = 'pickle'
result_expires = 3000
result_backend = 'redis://127.0.0.1:6379/0'
result_serializer = 'pickle'
result_cache_max = 10000
worker_redirect_stdouts_level = 'INFO'
