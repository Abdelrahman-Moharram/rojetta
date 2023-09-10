from django import forms
from .models import User


class add_user_form(forms.ModelForm):
    class Meta:
        model   = User
        fields  = '__all__'
        exclude = ("is_active", "is_stuff","is_superuser","last_login", )