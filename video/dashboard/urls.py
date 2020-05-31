from django.urls import path

from .views import IndexView
from .views import LoginView, LogoutView, AdminManagerView, UpdateAdminStatusView
from .views import VideoView, VideoUpdateStatus, VideoSubView, VideoStarView
from .views import StarDelete, SubDelete

app_name = 'dashboard'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('admin/manager/', AdminManagerView.as_view(), name='admin_manager'),
    path('admin/manager/update/', UpdateAdminStatusView.as_view(), name='admin_manager_update'),

    path('video/', VideoView.as_view(), name='video'),
    path('video/update_status/<int:video_id>/', VideoUpdateStatus.as_view(), name='video_update'),


    path('video/sub/<int:video_id>/', VideoSubView.as_view(), name='video_sub'),
    path('video/star/<int:video_id>/', VideoStarView.as_view(), name='video_star'),

    path('video/star/delete/<int:star_id>/<int:video_id>/', StarDelete.as_view(), name='video_star_delete'),
    path('video/sub/delete/<int:sub_id>/<int:video_id>/', SubDelete.as_view(), name='video_sub_delete'),
]
