from django.urls import path
from . import views
app_name ='User'
urlpatterns = [
    path('',views.loginpage, name='loginpage'),
    path('register/',views.registerpage, name='registerpage'),
]