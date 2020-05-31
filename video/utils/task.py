from celery import task


@task
def video_task(name, path_name):
    from .base_qiniu import video_qiniu
    print('=' * 30)
    print(name, path_name)
    print('=' * 30)
    url = video_qiniu.put(name, path_name)
    return url
