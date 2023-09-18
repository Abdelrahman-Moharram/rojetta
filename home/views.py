from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import Specialization, Government, Doctor, Clinic, User
import json

def index(request):
    return render(request, 'home/index.html', {"specializations":Specialization.objects.all(), "governments":Government.objects.all()})

def specialization(request, id):
    specialization = Specialization.objects.get(id=id)
    
    return render(request, 'home/search.html', {
        "specialization": specialization, 
        "doctors": Doctor.objects.filter(specialization=specialization),
        "governments": Government.objects.all(),
        })



def doctorsInGoverments(request, id):
    if request.GET.getlist("government", None):
        doctors = Doctor.objects.filter(specialization__id=id).distinct().filter(clinic__government__in=request.GET.getlist("government", None)).values()
    else:
        doctors = Doctor.objects.filter(specialization__id=id).values()

    for doc in doctors:
        user = User.objects.get(uuid=doc['user_id'])
        doc['username'] =  user.username
        doc['email'] =  user.email
        doc['is_doctor'] =  user.is_doctor
        doc['joined_at'] =  user.joined_at
        
    return JsonResponse({
            "doctors":list(doctors)
    })



def error_404(request, exception):
    return render(request, '404.html', {})