from django import forms
from .models import User


class add_user_form(forms.ModelForm):
    retypepassword=forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(
            error_messages={'invalid': 'This is my email error msg.'}, required=True)
    class Meta:
        model   = User
        fields  = '__all__'
        exclude = ("is_active", "is_staff","is_superuser","last_login", "is_admin", "is_doctor")
        

    
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already exists")
        return email
    
    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long"
            )
        return password
    def clean_retypepassword(self, *args, **kwargs):
        password = self.cleaned_data.get("password")
        retypepassword = self.cleaned_data.get("retypepassword")
        if password != retypepassword:
            raise forms.ValidationError(
                "password and confirm password does not match"
        )
        return retypepassword