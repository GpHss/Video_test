from dashboard.models import Video, FromType, VideoSub, ClientUser
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import View


class IndexView(View):
    def get(self, request):
        # 跳转到主页
        return redirect(reverse('client:external_video'))


class ExternalVideoView(View):
    def get(self, request):
        videos = Video.objects.exclude(from_to=FromType.custom.value)
        context = {
            'videos': videos,
        }
        return render(request, 'client/video/external_video.html', context)


class CustomVideoView(View):
    def get(self, request):
        videos = Video.objects.filter(from_to=FromType.custom.value)
        context = {
            'videos': videos,
        }
        return render(request, 'client/video/custom_video.html', context)


class VideoSubView(View):
    def get(self, request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        subs = VideoSub.objects.filter(video=video)
        user = request.COOKIES.get('user_cookie', None)
        is_login = True if user else False
        context = {
            'video': video,
            'subs': subs,
            'is_login': is_login,
        }
        return render(request, 'client/video/sub.html', context)


class CustomSubDetailView(View):
    def get(self, request, video_id, sub_id):
        video = get_object_or_404(Video, pk=video_id)
        sub = VideoSub.objects.get(pk=sub_id)

        context = {
            'video': video,
            'sub': sub,
        }
        return render(request, 'client/video/sub_detail.html', context)


def client_user(request):
    value = request.COOKIES.get('user_cookie')
    if not value:
        return None
    user = ClientUser.objects.filter(pk=value)
    if user:
        return user[0]
    else:
        return None


class UserView(View):
    def get(self, request):
        auth = client_user(request)
        context = {'auth': auth}
        return render(request, 'client/auth/user.html', context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            error = "缺少必要字段"
            return JsonResponse({'code': -1, 'msg': error})

        user = ClientUser.objects.filter(username=username)

        if not user:
            error = "用户不存在"
            return JsonResponse({'code': -1, 'msg': error})

        user = user[0]
        # 登录客户端用户 不能使用Django自带的 login()
        # response = render(request, 'client/auth/user.html')
        response = render(request, 'client/video/external_video.html')
        response.set_cookie('user_cookie', str(user.id))
        print('here')
        return response


class RegisterView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            error = "缺少必要字段"
            return JsonResponse({'code': -1, 'msg': error})

        exists = ClientUser.objects.filter(username=username).exists()
        if exists:
            error = "用户名已存在"
            return JsonResponse({'code': -1, 'msg': error})

        ClientUser.add(username=username, password=password)
        return JsonResponse({'code': 0, 'msg': '注册成功'})


class LogoutView(View):
    def get(self, request):
        if request.COOKIES.get('user_cookie') == None:
            return redirect(reverse('client:auth'))
        else:
            response = render(request, 'client/auth/user.html')
            response.delete_cookie('user_cookie')
            return response
