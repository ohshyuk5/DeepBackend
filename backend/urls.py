"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url, include 

from .api_upload.views import FileUploadView

urlpatterns = [
    # path('.api/', include('backend.api.urls')),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    path('users/', include('backend.api_user.urls'), name='api_user'), #include 함수를 통해 api_usr의 urls.py로 라우팅 해준다.
    path('media/', include('backend.api_media.urls'), name='api_media'),
    path('upload/', include('backend.api_upload.urls'), name='api_upload')
]