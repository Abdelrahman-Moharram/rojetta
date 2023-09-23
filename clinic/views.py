from django.shortcuts import render
from .models import Clinic
from accounts.views import is_doctor

# Create your views here.
def clinic(request, id):
    return render(request, "clinic/clinic.html", {'clinic':Clinic.objects.get(id=id)})

def manage_clinic(request):
    is_doctor(request)
    return render(request, "clinic/manageClinic.html", {})

