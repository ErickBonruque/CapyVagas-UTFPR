from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from apps.bot.views import webhook

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('admin/', admin.site.urls),
    path('webhook/', webhook),
    path('dashboard/', include('apps.dashboard.urls')),
    path('api/', include('apps.dashboard.api_urls')),
]
