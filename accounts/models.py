from django.db import models
from django.contrib.auth.models import User,BaseUserManager,AbstractBaseUser
from django.utils.text import slugify
import uuid
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from clinic.models import Clinic


def imagesave(instance,filename):
    imagename , extension = filename.split(".")
    return "users/%s/%s.%s"%("images", instance.user.username, extension)



def cap(string):
    new=string[0].upper()
    for i in range(1,len(string),1):
        if string[i-1] == '-':
            new += string[i].upper()
        else:
            new +=string[i]
    return new


class accountManager(BaseUserManager):
    def create_user(self,email,fname,lname,password=None):
        if not email:
            raise ValueError('user must have an email')

        if not fname:
            raise ValueError('Invalid Null Value for fname')
        
        if not lname:
            raise ValueError('Invalid Null Value for Lname')
        
        
        user = self.model(
            email = self.normalize_email(email),
            fname = fname,
            password=password,
            lname = lname,
        )

        # user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,email,fname,lname,password):
        user = self.create_user(
            email = email,
            fname = fname,
            lname = lname,
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.set_password(password)
        user.save(using=self._db)
        return user
        
        # return user 





class User(AbstractBaseUser):
    uuid          = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    fname         = models.CharField(max_length=50,unique=False)
    lname         = models.CharField(max_length=50,unique=False)
    email         = models.EmailField(unique = True, max_length=254)
    username      = models.SlugField(blank=True,null=True)
    password      = models.CharField(max_length=150)
    # image         = models.ImageField(default="users/logo.png",upload_to=imagesave, null=True, height_field=None, width_field=None)
    phone         = models.ManyToManyField('Phone', blank=True)
    
    joined_at     = models.DateField(auto_now_add=True)
    is_active     = models.BooleanField(default= True)

    is_doctor     = models.BooleanField(default=False)
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['fname','lname']

    objects = accountManager()
    def __str__(self):
        return self.username or self.email


    def has_perm(self , perm , obj = None): # to not access admin panel
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
    


    def DocData(self):
        if self.is_doctor:
            doc = Doctor.objects.get(user=self)
            data = {}
            data['image'] = doc.image
            data['coverletter'] = doc.coverletter
            data['bio']=doc.bio 
            data['skills']=doc.skills 
            data['specialization']=doc.specialization
            data['is_completed']=doc.is_completed

            return data
        return None

    def ClinicData(self):
        if self.is_doctor :
            clinic = Clinic.objects.get(doctor=Doctor.objects.get(user=self))
            data = {}
            data['government'] = clinic.government
            data['state'] = clinic.state
            data['detailLocation'] = clinic.detailLocation
            data['mapsLocation'] = clinic.mapsLocation
            data['price'] = clinic.price
            data['is_opned'] = clinic.is_opned
            data['last_opened'] = clinic.last_opened
        
            return data
        return None
            





    def save(self, *args, **kwargs):
        # Save the provided password in hashed format
        self.username = cap(slugify(self.fname+"-"+self.lname))
        user = super(User, self)
        if not self.is_superuser:
            user.set_password(self.password)
        user.save(*args, **kwargs)
        return user


    


    

class Phone(models.Model):
    phone       = models.CharField(max_length=12)

class SkillType(models.Model):
    name        = models.CharField(max_length=100)
    ar_name     = models.CharField(max_length=100, verbose_name="نوع المهارات", null=True, blank=True)

    def __str__(self):
        return self.name



class Skill(models.Model):
    name        = models.CharField(max_length=100)
    ar_name     = models.CharField(max_length=100, verbose_name="المهارات", null=True, blank=True)
    type        = models.ForeignKey(SkillType, null=True, blank=True, on_delete=models.PROTECT)
    date        = models.DateField(default=timezone.now)
    certificate = models.FileField(upload_to="media/doctors/", max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name


class Government(models.Model):
    name        = models.CharField(max_length=100, null=True, blank=True)
    ar_name     = models.CharField(max_length=100, verbose_name="المحافظة", null=True, blank=True)

    def DocCount(self):
        return Clinic.objects.filter(government=self).count()
    def __str__(self):
        return self.name
class State(models.Model):
    name        = models.CharField(max_length=100)
    ar_name     = models.CharField(max_length=100, verbose_name="المنطقة", null=True, blank=True)
    government  = models.ForeignKey(Government, on_delete=models.PROTECT)
    def __str__(self):
        return self.name

class University(models.Model):
    name        = models.CharField(max_length=100)
    ar_name     = models.CharField(max_length=100, verbose_name="الجامعة", null=True, blank=True)

    def __str__(self):
        return self.name
class Faculty(models.Model):
    name        = models.CharField(max_length=100)
    ar_name     = models.CharField(max_length=100, verbose_name="الكلية", null=True, blank=True)

    university = models.ForeignKey(University, on_delete=models.PROTECT)
    def __str__(self):
        return self.name 


class Specialization(models.Model):
    name        = models.CharField(max_length=100)
    ar_name     = models.CharField(max_length=100, verbose_name="التخصص", null=True, blank=True)
    icon        = models.ImageField(default="specilizations/stethoscope-alt.png")
    # faculty     = models.CharField(max_length=100, null=True)
    # university  = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name



class Doctor(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    image           = models.ImageField(default="users/logo.webp",upload_to=imagesave, null=True, height_field=None, width_field=None, verbose_name="صورة شخصية")
    coverletter     = models.TextField(null=True, verbose_name="تفاصيل")
    bio             = models.CharField(max_length=255, verbose_name="عنوان سيرة ذاتية", null=True)
    skills          = models.ManyToManyField(Skill, verbose_name="المهارات")
    specialization  = models.ForeignKey(Specialization, null=True, on_delete=models.CASCADE, verbose_name="التخصص")
    is_completed    = models.BooleanField(default=False)
    # phone           = models.ManyToManyField('Phone', blank=True)
    
    def ClinicData(self):
        
        clinic = Clinic.objects.get(doctor=self)
        data = {}
        data['government'] = clinic.government
        data['state'] = clinic.state
        data['detailLocation'] = clinic.detailLocation
        data['mapsLocation'] = clinic.mapsLocation
        data['price'] = clinic.price
        data['is_opned'] = clinic.is_opned
        data['last_opened'] = clinic.last_opened
        
        return data
        
    def __str__(self):
        return "Dr." + self.user.username


@receiver(post_save, sender=User)
def create_doctor(sender, instance, **kwargs):
    if kwargs['created']:
        if instance.is_doctor:
            doc = Doctor.objects.create(user=instance)
            doc.save()
            clinic = Clinic.objects.create(doctor=doc)
            clinic.save()

        

class Patient(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    government      = models.ForeignKey(to='accounts.Government', on_delete=models.PROTECT,verbose_name="المحافظة")
    state           = models.ForeignKey(to='accounts.State', on_delete=models.PROTECT, verbose_name="المنطقة")
    phone           = models.ManyToManyField(to='accounts.Phone', blank=True)

