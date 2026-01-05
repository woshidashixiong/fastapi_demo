
from datetime import timedelta

from celery import Celery


app = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/1",
    backend="redis://127.0.0.1:6379/2",
)

app.conf.broker_connection_retry_on_startup = True
app.conf.worker_max_tasks_per_child = 100
app.conf.task_time_limit = 12 * 60 * 60
app.conf.timezone = "Asia/Shanghai"
app.conf.enable_utc = False

# 注册异步任务
app.autodiscover_tasks([
    'tasks1',#自动将tasks1目录下tasks.py下带有 @app.task装饰器的函数注册上
])


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    # 每隔半小时执行一次aaa函数
    sender.add_periodic_task(timedelta(minutes=30), aaa.s())


@app.task()
def aaa():
    print(1111)



cmd = "celery -A app.celery_app worker --loglevel info -E"

