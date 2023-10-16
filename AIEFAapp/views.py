from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return render(request, "home.html")
def graphs(request):
    return render(request, "graphs.html")
def disclaimers(request):
    return render(request, "disclaimers.html")
def logout_view(request):
    logout(request)
    return redirect("/")
def profile(request):
    return render(request, "profile.html")