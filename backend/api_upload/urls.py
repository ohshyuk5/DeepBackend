from django.urls import path
from . import views
 
app_name = 'api_upload'
urlpatterns = [
    path('', views.FileUploadView.as_view())
    # path('(?P<filename>[^/]+)$', views.FileUploadView.as_view())
]
