from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html', {})

def error404(request):
    return render(request, 'home/404.html', {})