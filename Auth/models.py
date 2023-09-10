from django.db import models
from django.contrib.auth.models import User,BaseUserManager,AbstractBaseUser
from django.utils.text import slugify



def imagesave(instance,filename):
    imagename , extension = filename.split(".")
    return "users/%s/%s/"%(instance.id,"images", extension)



def cap(string):
    new=string[0].upper()
    for i in range(1,len(string),1):
        if string[i-1] == '-':
            new += string[i].upper()
        else:
            new +=string[i]
    return new


class accountManager(BaseUserManager):
    def create_user(self,email,fname,lname,phone,password = None):
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
    

    def create_superuser(self,email,fname,lname,phone,password):
        user = self.create_user(
            email = self.normalize_email(email),
            phone = phone,
            fname = fname,
            lname = lname,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user 





class User(AbstractBaseUser):
    
    fname         = models.CharField(max_length=20,verbose_name="الاسم الاول",unique=False)
    lname         = models.CharField(max_length=20,verbose_name="الاسم الاخير",unique=False)
    phone         = models.CharField(max_length=12, verbose_name="رقم الهاتف",unique=True)
    email         = models.EmailField(unique = True, max_length=254)
    password      = models.CharField(max_length=150)
    # image         = models.ImageField(default="users/logo.png",upload_to=imagesave, null=True, height_field=None, width_field=None)
    joined_at     = models.DateField(auto_now_add=True,verbose_name="تاريخ الانضمام")
    username      = models.SlugField(blank=True,null=True)
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['fname','lname','phone']

    objects = accountManager()



    def save(self,*args, **kwargs):
        self.username = slugify(self.fname+"-"+self.lname)
        self.username = cap(self.username)
        super(User,self).save(*args,**kwargs)


    
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
    image           = models.ImageField(default="users/logo.png",upload_to=imagesave, null=True, height_field=None, width_field=None, verbose_name="صورة شخصية")
    coverletter     = models.TextField(null=True, verbose_name="تفاصيل")
    bio             = models.CharField(max_length=255, verbose_name="عنوان سيرة ذاتية", blank=True)
    skills          = models.ManyToManyField(Skill, verbose_name="المهارات")
    specialization  = models.OneToOneField(Specialization, on_delete=models.CASCADE, verbose_name="التخصص")

    def __str__(self):
        return "دكتور " + self.user.username


class Clinic(models.Model):
    doctor          = models.ForeignKey(Doctor, on_delete=models.CASCADE) # doctor may has more than one Clinic
    government      = models.ForeignKey(Government, on_delete=models.PROTECT,verbose_name="المحافظة")
    state           = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="المنطقة")
    detailLocation  = models.CharField(max_length=555, verbose_name="العنوان المفصل")
    mapsLocation    = models.CharField(max_length=555, null=True, blank=True, verbose_name="العنوان علي خرائط جوجل")
    price           = models.FloatField(verbose_name="سعر الكشف")
    is_opned        = models.BooleanField(verbose_name="العيادة مفتوحة", default=False)
    last_opened     = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.doctor)



class Patient(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    image           = models.ImageField(default="users/logo.png",upload_to=imagesave, verbose_name="صورة شخصية", null=True, height_field=None, width_field=None)
    government      = models.ForeignKey(Government, on_delete=models.PROTECT,verbose_name="المحافظة")
    state           = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="المنطقة")