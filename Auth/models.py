from django.db import models
from django.contrib.auth.models import User,BaseUserManager,AbstractBaseUser




class accountManager(BaseUserManager):
    def create_user(self,username,fname, lname, email, phonenumber,password = None):
        if not username:
            raise ValueError('user must have an username')

        if not fname:
            raise ValueError('Unvalid Null Value for first name')
        
        if not lname:
            raise ValueError('Unvalid Null Value for last name')
        
        if not email:
            raise ValueError('Unvalid Null Value for email')
        
        if not phonenumber:
            raise ValueError('Unvalid Null Value for phonenumber')

        user = self.model(
            username    = username,
            fname       = fname,
            lname       = lname,
            email       = email,
            phonenumber = phonenumber,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    

    def create_superuser(self,username,fname, lname, email, phonenumber,password):
        user = self.create_user(
            username = username,
            fname = fname,
            lname = lname,
            email = email,
            phonenumber = phonenumber,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 






class User(AbstractBaseUser):
    fname           = models.CharField(max_length=90,verbose_name="Full Name",unique=False)
    lname           = models.CharField(max_length=90,verbose_name="Full Name",unique=False)
    email           = models.CharField(unique = True, max_length=60)
    phonenumber     = models.CharField(unique = True, max_length=60)
    username        = models.CharField(unique = True, max_length=60)
    password        = models.CharField(max_length=150)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    date_joined     = models.DateTimeField(auto_now=True, auto_now_add=False)


    
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['fname', 'lname', 'email', 'phonenumber']

    objects = accountManager()
    def save(self, *args, **kwargs):
        # Save the provided password in hashed format
        user = super(User, self)
        user.set_password(self.password)
        super().save(*args, **kwargs)
        return user

    def __str__(self):
        return self.username

    def has_perm(self , perm , obj = None):
        return self.is_superuser
    
    def has_module_perms(self,app_label):
        return self.is_staff








class SkillType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Skill(models.Model):
    name        = models.CharField(max_length=100)
    type        = models.ForeignKey(SkillType, on_delete=models.PROTECT)
    from_date   = models.DateTimeField(auto_now_add=False, null=True)
    to_date     = models.DateTimeField(auto_now_add=False, null=True)
    certificate = models.FileField(upload_to="media/doctors/", max_length=100)
    def __str__(self):
        return self.name
class Government(models.Model):
    name = models.CharField(max_length=100,verbose_name="المحافظة")
    def __str__(self):
        return self.name
class State(models.Model):
    name = models.CharField(max_length=100, verbose_name="المنطقة")
    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=100, verbose_name="التخصص")
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, verbose_name="الكلية")
    university = models.ForeignKey(University, on_delete=models.PROTECT, verbose_name="الجامعة")

    def __str__(self):
        return self.name



class Doctor(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    image           = models.FileField(upload_to="media/Doctors/", max_length=100, verbose_name="صورة شخصية")
    coverletter     = models.TextField(null=True, verbose_name="تفاصيل")
    bio             = models.CharField(max_length=255, verbose_name="عنوان سيرة ذاتية", blank=True)
    skills          = models.ManyToManyField(Skill, verbose_name="المهارات")
    specialization  = models.OneToOneField(Specialization, on_delete=models.CASCADE, verbose_name="التخصص")

    def __str__(self):
        return "دكتور " + self.user.username


class Clinic(models.Model):
    government      = models.ForeignKey(Government, on_delete=models.PROTECT,verbose_name="المحافظة")
    state           = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="المنطقة")
    detailLocation  = models.CharField(max_length=555, verbose_name="العنوان المفصل")
    mapsLocation    = models.CharField(max_length=555, null=True, blank=True, verbose_name="العنوان علي خرائط جوجل")
    price           = models.FloatField(verbose_name="سعر الكشف")



class Patient(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    image           = models.FileField(upload_to="media/Patients/", max_length=100, verbose_name="صورة شخصية")
    government      = models.ForeignKey(Government, on_delete=models.PROTECT,verbose_name="المحافظة")
    state           = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="المنطقة")