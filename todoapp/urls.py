from django.urls import path 
from .import views
urlpatterns=[
    path('',views.loginpage, name='login'),
    path('register/',views.registerpage,name='register'),
    path('home/',views.homepage,name='home'),
    path('logout/',views.LogoutView,name='logout'),
    path('delete-task/<str:name>/',views.DeleteTask,name='delete'),
    path('update/<str:name>/',views.Update,name='update'),
]