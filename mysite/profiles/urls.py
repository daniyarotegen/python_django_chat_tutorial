from django.urls import path
from .views import SignUpView, LoginView, LogoutView, ProfileListView, OtherProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('list/', ProfileListView.as_view(), name='user_list'),
    path('<str:username>/', OtherProfileView.as_view(), name='other_profile'),

]
