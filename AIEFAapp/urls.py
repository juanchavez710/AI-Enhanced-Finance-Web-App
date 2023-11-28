from django.urls import path
from . import views
from .views import stock_graph

urlpatterns = [
    path("", views.home, name="home"),
    path("predictions/", views.all_stocks, name="predictions"),
    path("disclaimers/", views.disclaimers, name="disclaimers"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name='profile'),
    path('associate_stock/<int:stock_id>/', views.associate_stock, name='associate_stock'),
    path('stock/<int:stock_id>/', views.stock_detail, name='stock_detail'),
    # urls.py
    path('stock-graph/<str:symbol>/', views.stock_graph, name='stock_graph'),
]