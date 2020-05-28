import hashlib
from enum import Enum

from django.db import models


def hash_password(password):
    if isinstance(password, str):
        password = password.encode('utf-8')  # 将字符串转换成'utf-8'的二进制编码
    # 返回一个md5加密的字符串 (hexdigest)16进制 (upper)大写形式
    return hashlib.md5(password).hexdigest().upper()


class ClientUser(models.Model):
    username = models.CharField(max_length=30, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    avatar = models.CharField(max_length=500, default=None)
    gender = models.CharField(max_length=10, default='')
    birthday = models.DateTimeField(null=True, blank=True, default=None)
    """
    Field.db_index¶
    If True, a database index will be created for this field.

    # 只能加速查找
    db_index=True,
    # 加速查找,限制列值唯一
    unique = True,
    # 加速查找,限制列值唯一(不能为空)
    primary = True,

    """
    status = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "username: {}".format(self.username)

    @classmethod
    def add(cls, username, password, avatar=None, gender='', birthday=''):
        return cls.objects.create(
            username=username,
            password=hash_password(password),
            avatar=avatar,
            gender=gender,
            birthday=birthday,
            status=True,
        )

    @classmethod
    def get_user(cls, username, password):
        try:
            user = cls.objects.get(
                username=username,
                password=hash_password(password),
            )
            return user
        except:
            return None

    def update_password(self, old_password, new_password):
        hash_old_password = hash_password(old_password)
        if hash_old_password != self.password:
            return False
        else:
            self.password = hash_password(new_password)
            self.save()
            return True

    def update_status(self):
        self.status = not self.status
        self.save()
        return True


# 枚举类型可以给一组标签赋予一组特定的值。
class VideoType(Enum):
    movie = 'movie'
    cartoon = 'cartoon'
    episode = 'episode'
    variety = 'variety'
    other = 'other'


VideoType.movie.label = '电影'
VideoType.cartoon.label = '卡通'
VideoType.episode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.other.label = '其他'


class FromType(Enum):
    youku = 'youku'
    custom = 'custom'


FromType.youku.label = '优酷'
FromType.custom.label = '自制'


class Video(models.Model):
    name = models.CharField(max_length=50, null=False)
    image = models.CharField(max_length=500, default=None)
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=20, default=FromType.custom.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'video_type', 'from_to')

    def __str__(self):
        return "name: {}".format(self.name)


class IdentityType(Enum):
    lead = 'lead'
    support = 'support'
    director = 'director'


IdentityType.lead.label = '主角'
IdentityType.support.label = '配角'
IdentityType.director.label = '导演'


class VideoStar(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')

    class Meta:
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return "name: {}".format(self.name)


class VideoSub(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return "video: {}, number: {}".format(self.video.name, self.number)

