from django.urls import path
from . import views
 
app_name = 'api_media'
urlpatterns = [
    path('', views.MediaView.as_view()), #User에 관한 API를 처리하는 view로 Request를 넘김
    path('<int:user_id>', views.MediaView.as_view()),
    path('<int:user_id>/<int:req_id>', views.MediaView.as_view())
]
