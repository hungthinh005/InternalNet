from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('IT', views.IT, name="IT"),
    path('Marketing', views.Marketing, name="Marketing"),
    path('function/<str:pk>/', views.function, name="function"),
    path('create-meeting/', views.createMeeting, name="create-meeting"),
    path('update-meeting/<str:pk>/', views.updateMeeting, name="update-meeting"),
    path('delete-meeting/<str:pk>/', views.deleteMeeting, name="delete-meeting"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
]