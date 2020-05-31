from qiniu import Auth, put_data, put_file

from django.conf import settings


class Qiniu(object):
    def __init__(self, bucket_name, base_url):
        self.bucket_name = bucket_name  #要上传的空间
        self.base_url = base_url
        self.q = Auth(settings.QINIU_AK, settings.QINIU_SK)  #构建鉴权对象

    def put(self, name, path):
        token = self.q.upload_token(self.bucket_name, name, 3600)
        ret, info = put_file(token, name, path)

        if 'key' in ret:
            # 上传成功
            remote_url = '/'.join([self.base_url, ret['key']])
            return remote_url


video_qiniu = Qiniu(settings.QINIU_BUCKET, settings.QINIU_VIDEO_URL)
