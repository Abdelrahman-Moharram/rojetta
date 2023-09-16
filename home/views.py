from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html', {})

def error_404(request, exception):
    return render(request, '404.html', {})