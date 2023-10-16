from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("graphs", views.graphs, name="graphs"),
    path("disclaimers", views.disclaimers, name="disclaimers"),
    path("logout", views.logout_view),
    path("profile", views.profile)
]