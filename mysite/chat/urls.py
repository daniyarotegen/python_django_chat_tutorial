from django.urls import path, re_path
from . import views
from .views import StartChatView, RoomView

urlpatterns = [
    path('', views.index, name='index'),
    path('start_chat/<str:username>/', StartChatView.as_view(), name='start_chat'),
    path('<uuid:room_uuid>/', RoomView.as_view(), name='room_view'),
    path('centrifugo/connect/', views.connect, name='connect'),
    path('centrifugo/subscribe/', views.subscribe, name='subscribe'),
    path('centrifugo/publish/', views.publish, name='publish'),

]
