from django.shortcuts import render
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import authenticate, login


def get_rate_limit(user):
    if user.is_authenticated:
        return "10/m"
    return "5/m"

def is_limited(request):
    """Helps to check ratelimit"""
    user_limit = get_rate_limit(request.user)
    return user_limit

@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def login_view(request):
    """
    Example login view protected by rate limiting.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse("Login Successful")
        return HttpResponse("Invalid credrentials", status=401)
    return render(requst, "login.html")
