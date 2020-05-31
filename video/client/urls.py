from django.urls import path

from .views import IndexView, ExternalVideoView, CustomVideoView, VideoSubView, CustomSubDetailView, UserView, RegisterView, LogoutView

app_name = 'client'
urlpatterns = [
    path('', IndexView.as_view()),

    path('video/external/', ExternalVideoView.as_view(), name='external_video'),
    path('video/custom/', CustomVideoView.as_view(), name='custom_video'),
    path('video/custom/<int:video_id>/<int:sub_id>', CustomSubDetailView.as_view(), name='custom_video_detail'),

    path('video/sub/<int:video_id>/', VideoSubView.as_view(), name='video_sub'),

    path('video/auth/', UserView.as_view(), name='auth'),
    path('video/auth/register/', RegisterView.as_view(), name='register'),
    path('video/auth/logout/', LogoutView.as_view(), name='logout'),
]