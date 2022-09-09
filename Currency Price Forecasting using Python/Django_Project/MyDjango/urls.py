from django.urls import path
from django.views.generic import TemplateView
from . import views
from . import example
urlpatterns = [
    path('', TemplateView.as_view(template_name = 'home.html' ) , name = 'home' ),
    path('index', TemplateView.as_view(template_name = 'index.html' ) , name = 'index' ),

   # path('index', views.index, name='myindex'),
    path('graph', views.allData.as_view(), name='graph'),
    path('getPrice', views.getPrice, name='getPrice'),
    path('Forecast', views.Forecasting.as_view(), name="Forecast"),
    path('newOrder', views.newOrder, name='newOrder'),
    path('Login', views.Login, name='Login'),
    path('autoTrade', views.autoTrade, name='autoTrade'),
    path('getNews', views.getNews, name='getNews'),
  
]