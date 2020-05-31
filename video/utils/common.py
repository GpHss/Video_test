import os
import shutil
import time

from django.conf import settings

from .base_qiniu import video_qiniu


# from .task import video_task


def check_video_type(type_obj, type_value, message):
    try:
        type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}
    return {'code': 0, 'msg': 'success'}


def handel_video(video_file):
    base_path = os.path.join(settings.BASE_DIR, 'dashboard\\temp')
    name = "{}_{}".format(int(time.time()), video_file.name)
    path_name = '\\'.join([base_path, name])

    temp_path = video_file.temporary_file_path()

    shutil.copyfile(temp_path, path_name)

    url = video_qiniu.put(name, path_name)

    # url = video_task.delay(name, path_name)

    os.remove(path_name)
    return url
