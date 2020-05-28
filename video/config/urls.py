from django.urls import path, include

urlpatterns = [
    path('dashboard/', include('dashboard.urls')),
    path('client/', include('client.urls'))
]
