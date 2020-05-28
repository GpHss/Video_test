from django.urls import path

from .views import IndexView
from .views import LoginView, LogoutView, AdminManagerView, UpdateAdminStatusView
from .views import ExternalVideoView, VideoSubView, VideoStarView, StarDelete

app_name = 'dashboard'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('admin/manager', AdminManagerView.as_view(), name='admin_manager'),
    path('admin/manager/update/', UpdateAdminStatusView.as_view(), name='admin_manager_update'),

    path('video/external/', ExternalVideoView.as_view(), name='external_video'),
    path('video/sub/<int:video_id>', VideoSubView.as_view(), name='video_sub'),
    path('video/star/<int:video_id>', VideoStarView.as_view(), name='video_star'),
    path('video/star/delete/<int:star_id>/<int:video_id>', StarDelete.as_view(), name='video_star_delete'),
]
