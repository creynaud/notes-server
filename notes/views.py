from django.shortcuts import render


def home(request):
    response = render(request, "home.html")
    return response
