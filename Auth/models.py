from django.db import models
from django.contrib.auth.models import User,BaseUserManager,AbstractBaseUser
from django.utils.text import slugify
import uuid


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
    def create_user(self,email,fname,lname,phone,password, **kwargs):
        if not email:
            raise ValueError('user must have an email')

        if not fname:
            raise ValueError('Unvalid Null Value')
        
        if not lname:
            raise ValueError('Unvalid Null Value')
        
        if not phone:
            raise ValueError('Unvalid Null Value')
        
        user = self.model(
            email = self.normalize_email(email),
            phone = phone,
            fname = fname,
            lname = lname
        )

        user.set_password(password)
        user.save(using = self._db)
        return user
    

    def create_superuser(self,email,fname,lname,phone,password, **kwargs):
        user = self.create_user(
            email = email,
            phone = phone,
            fname = fname,
            lname = lname,
            password=password,
            **kwargs
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user 





class User(AbstractBaseUser):
    uuid          = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    fname         = models.CharField(max_length=50,unique=False)
    lname         = models.CharField(max_length=50,unique=False)
    phone         = models.CharField(max_length=12, unique=True)
    email         = models.EmailField(unique = True, max_length=254)
    username      = models.SlugField(blank=True,null=True)
    password      = models.CharField(max_length=150)
    # image         = models.ImageField(default="users/logo.png",upload_to=imagesave, null=True, height_field=None, width_field=None)
    
    joined_at     = models.DateField(auto_now_add=True)
    
    is_active     = models.BooleanField(default=True)
    is_doctor     = models.BooleanField(default=False)
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)

    def DocData(self):
        if self.is_doctor:
            doc = Doctor.objects.get(user=self)
            data = {}
            data['image'] = doc.image
            data['coverletter'] = doc.coverletter
            data['bio']=doc.bio 
            data['skills']=doc.skills 
            data['specialization']=doc.specialization

            print(doc)
            return data
        return None

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['fname','lname','phone']

    objects = accountManager()



    def save(self, *args, **kwargs):
        # Save the provided password in hashed format
        self.username = cap(slugify(self.fname+"-"+self.lname))
        user = super(User, self)
        user.set_password(self.password)
        super().save(*args, **kwargs)
        return user


    
    def __str__(self):
        return self.username or self.email


    def has_perm(self , perm , obj = None): # to not access admin panel
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True

    



class SkillType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Skill(models.Model):
    name        = models.CharField(max_length=100)
    type        = models.ForeignKey(SkillType, on_delete=models.PROTECT)
    date        = models.DateField(auto_now_add=False, null=True)
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
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    def __str__(self):
        return self.name + " " + self.university.name


class Specialization(models.Model):
    name        = models.CharField(max_length=100, verbose_name="التخصص")
    faculty     = models.CharField(max_length=100)
    university  = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name + " " + str(self.faculty)



class Doctor(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    image           = models.ImageField(default="users/logo.webp",upload_to=imagesave, null=True, height_field=None, width_field=None, verbose_name="صورة شخصية")
    coverletter     = models.TextField(null=True, verbose_name="تفاصيل")
    bio             = models.CharField(max_length=255, verbose_name="عنوان سيرة ذاتية", null=True)
    skills          = models.ManyToManyField(Skill, verbose_name="المهارات")
    specialization  = models.ForeignKey(Specialization, null=True, on_delete=models.CASCADE, verbose_name="التخصص")
    is_completed    = models.IntegerField(default=0)

    def __str__(self):
        return "Dr." + self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=User)
def create_doctor(sender, instance, **kwargs):
    if kwargs['created']:
        doc = Doctor.objects.create(user=instance)
        doc.save()

        


class Clinic(models.Model):
    doctor          = models.ForeignKey(Doctor, on_delete=models.CASCADE) # doctor may has more than one Clinic
    government      = models.ForeignKey(Government, on_delete=models.PROTECT,verbose_name="المحافظة")
    state           = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="المنطقة")
    detailLocation  = models.CharField(max_length=555, verbose_name="العنوان المفصل")
    mapsLocation    = models.CharField(max_length=555, null=True, blank=True, verbose_name="العنوان علي خرائط جوجل")
    price           = models.FloatField()
    is_opned        = models.BooleanField(default=False)
    last_opened     = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.doctor)



class Patient(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    image           = models.ImageField(default="users/logo.png",upload_to=imagesave, verbose_name="صورة شخصية", null=True, height_field=None, width_field=None)
    government      = models.ForeignKey(Government, on_delete=models.PROTECT,verbose_name="المحافظة")
    state           = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="المنطقة")