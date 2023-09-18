from django.shortcuts import render
from accounts.models import Specialization, Government, Doctor


def index(request):
    return render(request, 'home/index.html', {"specializations":Specialization.objects.all(), "governments":Government.objects.all()})

def specialization(request, id):
    specialization = Specialization.objects.get(id=id)
    return render(request, 'home/specialization.html', {"specialization":specialization, "doctors":Doctor.objects.filter(specialization=specialization)})


def error_404(request, exception):
    return render(request, '404.html', {})