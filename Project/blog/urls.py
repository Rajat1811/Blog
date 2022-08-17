from django.urls import path
from . import views
from django.contrib import admin
urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('emp_home/', views.home, name='emp_home'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('my_post/', views.my_post, name='my_post'),
    path('my_post/<slug:data>', views.my_post, name='my_postdata'),
    path('all_post/', views.all_post, name='all_post'),
    path('edit_post/<int:pk>', views.edit_post, name='edit_post'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('detailview/<int:pk>', views.detailview, name='detailview'),
    path('detailview/<int:pk>/comment', views.add_comment, name='add_comment'),
    path('search', views.search, name='search'),
    path('change_pass', views.change_pass, name='change_pass'),
    path('like_post', views.like_post, name='like_post'),
    ]
