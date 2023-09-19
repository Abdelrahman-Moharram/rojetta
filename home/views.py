from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import Specialization, Government, Doctor, Clinic, User
from django.db.models import Q

def index(request):
    return render(request, 'home/index.html', {"specializations":Specialization.objects.all(), "governments":Government.objects.all()})

def specialization(request, id):
    specialization = Specialization.objects.get(id=id)
    
    return render(request, 'home/search.html', {
        "specialization": specialization, 
        "doctors": Doctor.objects.filter(specialization=specialization),
        "governments": Government.objects.all(),
        })



def doctorsInGoverments(request):
    if request.GET.getlist("government", None):
        doctors = Doctor.objects.distinct().filter(clinic__government__in=request.GET.getlist("government", None)).values()
    else:
        doctors = Doctor.objects.all().values()
    for doc in doctors:
        user = User.objects.get(uuid=doc['user_id'])
        doc['username'] =  user.username
        doc['email'] =  user.email
        doc['is_doctor'] =  user.is_doctor
        doc['joined_at'] =  user.joined_at
        
    return JsonResponse({
        "doctors":list(doctors)
    })

def advancedSearch(request):
    doctors = Doctor.objects.filter(
        # specializations
        (Q(specialization__name__contains=request.GET.get("specialization", None)) | Q(specialization__ar_name__contains=request.GET.get('specialization', None)))
        # government
        &(Q(clinic__government__name__contains=request.GET.get('government', None))|Q(clinic__government__ar_name__contains=request.GET.get('government', None)))
        #state
        &(Q(clinic__state__name__contains=request.GET.get('state', None))|Q(clinic__state__ar_name__contains=request.GET.get('state', None)))
        # doctor
        &(Q(user__username__contains=request.GET.get('name', None))|Q(user__username__contains=request.GET.get('name', None)))
    )
    print("doctors>> ",doctors, request.GET.get("specialization", None))
    return render(request, 'home/search.html', {
        "doctors": doctors,
        "governments": Government.objects.all(),
    })
def error_404(request, exception):
    return render(request, '404.html', {})