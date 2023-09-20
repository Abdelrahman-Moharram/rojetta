from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import Specialization, Government, Doctor, Clinic, User, State
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

def SearchQuery(query):
    return Clinic.objects.filter(
        Q(doctor__user__username__contains=query.get('name')) 
        &
        Q(doctor__specialization__name__contains=query.get("specialization", None))|Q(doctor__specialization__ar_name__contains=query.get("specialization", None))
        &
        Q(government__name__contains=query.get('government', None))|Q(government__ar_name__contains=query.get('government', None))
        &
        Q(state__name__contains=query.get('state', None))|Q(state__ar_name__contains=query.get('state', None))
    )

def clinicFilter(request):
    opened = False
    if 'is_opened' in request.GET:
        opened = True
    

    clinics = Clinic.objects.filter(
         Q(government__id__in=request.GET.getlist('government', Government.objects.all()))
        &Q(doctor__specialization__id__in=request.GET.getlist('specialization', Specialization.objects.all()))
        , is_opened=opened
    ).values()

    for clinic in clinics:
        user = User.objects.get(doctor=clinic['doctor_id'])
        c=Clinic.objects.filter(doctor=clinic['doctor_id']).first()

        clinic['username'] =  user.username
        clinic['user_id'] =  user.uuid
        
        clinic['bio'] = user.DocData()['bio']
        clinic['image'] = user.DocData()['image'].url
        
        clinic['state'] =  c.state.name
        clinic['ar_state'] =  c.state.name
        clinic['government'] =  c.government.name
        clinic['ar_government'] =  c.government.ar_name
        

        
    return JsonResponse({
        "doctors":list(clinics)
    })



def advancedSearchDoctor(request):
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
    return render(request, 'home/search.html', {
        "doctors": doctors,
        "governments": Government.objects.all(),
    })





def advancedSearch(request):
    return render(request, 'home/search.html', {
        "clinics":  SearchQuery(request.GET),
        "governments": Government.objects.all(),
        "states": State.objects.all(),
        "specializations": Specialization.objects.all(),
    })

def error_404(request, exception):
    return render(request, '404.html', {})