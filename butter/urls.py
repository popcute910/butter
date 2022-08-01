from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:username>', views.ProfileDetail.as_view(), name='profile'),
    path('profile/<slug:username>/edit/', views.UserUpdateView.as_view(), name='edit_profile'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.signup, name="signup"),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('<slug:username>/follow/', views.follow_view, name='follow'),
    path('<slug:username>/unfollow/', views.unfollow_view, name='unfollow'),
    path('<slug:username>/following/', views.FollowingList.as_view(), name='following'),
    path('<slug:username>/follower/', views.FollowerList.as_view(), name='follower'),
    path('create_post/', views.create_post, name='create_post'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)