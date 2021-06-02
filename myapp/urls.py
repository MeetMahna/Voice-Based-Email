from django.conf.urls import url
from django.urls import path
from .views import home_view, signup_view, login_view, logout_view, first, auth_view, compose_view, inbox_view, read_view, sent_view,read_sent_view

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
    # url(r'read/(?P<id>[0-9]+)$',read_view, name='read'),
    path('read/<id>',read_view, name='read'),
    path('read_sent/<id>',read_sent_view, name='read_sent'),

]
