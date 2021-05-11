from django.urls import path
from .views import home_view, signup_view, login_view, logout_view, first, auth_view, compose_view, inbox_view, sent_view

app_name = 'myapp'


urlpatterns = [
    path('', first, name='first'),
    path('home/', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('auth-code/', auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('compose/', compose_view, name='compose'),
    path('inbox/', inbox_view, name='inbox'),
    path('sent/', sent_view, name='sent'),

]
