from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # , Page
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from utils.common import check_video_type, handel_video
from utils.permission import dashboard_auth

from .models import VideoType, FromType, Video, VideoSub, VideoStar, IdentityType


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard:index'))

        return render(request, 'dashboard/auth/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        exists = User.objects.filter(username=username).exists()
        # 对比.get()方法
        # .filter().exists() 更快
        # try:
        #     User.objects.get(username=username)
        # except User.DoesNotExist:

        context = {}

        if not exists:
            # 用户名不存在
            context['error'] = '用户名不存在'
            return render(request, 'dashboard/auth/login.html', context)

        # 验证密码是否正确
        """
        django.contrib.auth.authenticate 的基础用法
        authenticate(request, username=None, password=None)¶
        Tries to authenticate username with password by calling User.check_password. 
        Returns an authenticated auth or None.
        返回一个已经被验证的用户 或者 None
        """
        user = authenticate(username=username, password=password)
        if not user:
            context['error'] = '密码错误'
            return render(request, 'dashboard/auth/login.html', context)

        # if not auth.is_superuser:
        #     context['error'] = '您无权访问'
        #     return render(request, 'dashboard/auth/login.html', context)

        login(request, user)
        next = request.GET.get('next', None)
        if not next:
            return redirect(reverse('dashboard:index'))
        else:
            return redirect(next)


class LogoutView(View):
    def get(self, request):
        next = request.GET.get('next', None)
        print(next)
        logout(request)
        if next:
            return redirect("{}?next={}".format(reverse('dashboard:login'), next))
        else:
            return redirect(reverse('dashboard:login'))


class AdminManagerView(View):
    @dashboard_auth
    def get(self, request):
        users = User.objects.all().order_by("id")
        page = int(request.GET.get('page', 1))
        p = Paginator(users, 2)
        total_page = p.num_pages
        if page < 1:
            page = 1
        elif page > total_page:
            page = total_page
        current_page = p.get_page(page)
        # Paginator.get_page() 返回一个Page对象, 其中包含当前页的user
        # Page类 重写了 __iter__() 方法
        # for auth in current_page.__iter__():
        #     print(auth)
        context = {
            'page': current_page,
            'users': current_page.__iter__(),
            'total': total_page,
        }

        return render(request, 'dashboard/auth/admin_manager.html', context)


class UpdateAdminStatusView(View):
    def get(self, request):
        username = request.GET.get('username')
        user = User.objects.get(username=username)

        status = request.GET.get('status')
        _status = True if status == 'on' else False
        print(username, _status)
        if _status:
            user.is_superuser = True
        else:
            user.is_superuser = False
        user.save()
        return redirect(reverse('dashboard:admin_manager'))


class IndexView(View):
    def get(self, request):
        return render(request, 'dashboard/index.html')


class VideoView(View):
    @dashboard_auth
    def get(self, request):
        # for item in VideoType:
        #     print(item.value, item.label)
        ex_videos = Video.objects.exclude(from_to=FromType.custom.value)
        cus_videos = Video.objects.filter(from_to=FromType.custom.value)
        context = {
            'VideoType': VideoType.__iter__,
            'FromType': FromType.__iter__,
            'ex_videos': ex_videos,
            'cus_videos': cus_videos,
        }
        return render(request, 'dashboard/video/videos.html', context=context)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        video_from = request.POST.get('video_from')
        info = request.POST.get('info')

        # 验证数据
        context = {}
        if not all([name, image, video_type, video_from, info]):
            context['error'] = '缺少必要字段'
            return render(request, 'dashboard/video/videos.html', context=context)

        result = check_video_type(VideoType, video_type, '非法的视频类型')
        if result.get('code') == -1:
            context['error'] = result.get('msg')
            return render(request, 'dashboard/video/videos.html', context=context)

        result = check_video_type(FromType, video_from, '非法的视频来源')
        if result.get('code') == -1:
            context['error'] = result.get('msg')
            return render(request, 'dashboard/video/videos.html', context=context)

        Video.objects.create(
            name=name,
            image=image,
            video_type=video_type,
            from_to=video_from,
            info=info,
        )

        return redirect(reverse('dashboard:external_video'))


class VideoUpdateStatus(View):
    @dashboard_auth
    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        video.status = not video.status
        video.save()

        return redirect(reverse('dashboard:video'))


class VideoSubView(View):
    @dashboard_auth
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)

        video_sub = VideoSub.objects.filter(video=video).order_by('number')

        sub_error = request.GET.get('sub_error', '')
        star_error = request.GET.get('star_error', '')

        stars = VideoStar.objects.filter(video=video).order_by('id')

        context = {
            'video': video,
            'subs': video_sub,
            'IdentityType': IdentityType.__iter__,
            'star_error': star_error,
            'sub_error': sub_error,
            'stars': stars,
        }
        return render(request, 'dashboard/video/video_sub.html', context)

    def post(self, request, video_id):
        number = request.POST.get('number')
        sub_id = request.POST.get('sub_id')
        video = Video.objects.get(id=video_id)

        if FromType(video.from_to) == FromType.custom:
            # 自制视频的上传
            file = request.FILES.get('url')
            if not all([file, number]):
                return redirect("{}?sub_error={}".format(reverse('dashboard:video_sub', kwargs={'video_id': video_id}),
                                                         '数据不完整'))
            # 上传到七牛云
            end_url = handel_video(file)  # 链接
            try:
                VideoSub.objects.create(video=video,url=end_url,number=number)
            except:
                return redirect("{}?sub_error={}".format(reverse('dashboard:video_sub', kwargs={'video_id': video_id}),
                                                         '上传失败'))

            return redirect(reverse('dashboard:video_sub', kwargs={'video_id': video_id}))

        else:
            # 外链视频
            url = request.POST.get('url')

            if not all([url, number]):
                return redirect("{}?sub_error={}".format(reverse('dashboard:video_sub', kwargs={'video_id': video_id}),
                                                         '数据不完整'))
            if not sub_id:
                # sub_id为空
                VideoSub.objects.create(video=video, url=url, number=number)
            else:
                video_sub = VideoSub.objects.get(id=sub_id)
                video_sub.url = url
                video_sub.number = number
                video_sub.save()
            return redirect(reverse('dashboard:video_sub', kwargs={'video_id': video_id}))


class VideoStarView(View):
    def post(self, request, video_id):
        video = Video.objects.get(id=video_id)
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        if not all([name, identity]):
            return redirect("{}?star_error={}".format(reverse('dashboard:video_sub', kwargs={'video_id': video_id}),
                                                      '数据不完整'))
            # return render(request, 'dashboard/video/video_sub.html', {'star_error': '数据不完整'})
        # print(video.name, name, IdentityType(identity).label)
        VideoStar.objects.create(
            video=video,
            name=name,
            identity=identity,
        )
        return redirect(reverse('dashboard:video_sub', kwargs={'video_id': video_id}))


class StarDelete(View):
    @dashboard_auth
    def get(self, request, star_id, video_id):
        star = VideoStar.objects.filter(id=star_id).delete()
        return redirect(reverse('dashboard:video_sub', kwargs={'video_id': video_id}))


class SubDelete(View):
    @dashboard_auth
    def get(self, request, sub_id, video_id):
        VideoSub.objects.filter(id=sub_id).delete()
        return redirect(reverse('dashboard:video_sub', kwargs={'video_id': video_id}))
