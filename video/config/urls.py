from django.urls import path, include

urlpatterns = [
    path('dashboard/', include('app.dashboard.urls')),
    path('client/', include('app.client.urls'))
]
