from django.db import models
from accounts.models import User
# Create your models here.

class TimeTable(models.Model):
    from_date       = models.DateTimeField(auto_now=False, auto_now_add=False)
    to_date         = models.DateTimeField(auto_now=False, auto_now_add=False)
    is_full         = models.BooleanField(default=False)
    reservasions    = models.ManyToManyField("Reservasion")



class Clinic(models.Model):
    doctor          = models.ForeignKey(to='accounts.Doctor', on_delete=models.CASCADE) # doctor may has more than one Clinic
    government      = models.ForeignKey(to='accounts.Government', null=True, blank=True, on_delete=models.PROTECT,verbose_name="المحافظة")
    state           = models.ForeignKey(to='accounts.State', null=True, blank=True, on_delete=models.PROTECT, verbose_name="المنطقة")
    detailLocation  = models.CharField(max_length=555, null=True, blank=True, verbose_name="العنوان المفصل")
    mapsLocation    = models.CharField(max_length=555, null=True, blank=True, verbose_name="العنوان علي خرائط جوجل")
    price           = models.FloatField(null=True, blank=True,)
    is_opened       = models.BooleanField(default=False)
    last_opened     = models.DateTimeField(null=True, blank=True)
    phones          = models.ManyToManyField(to='accounts.Phone', blank=True)
    time_tables     = models.ManyToManyField(TimeTable, blank=True)

    def __str__(self):
        return str(self.doctor)


class Reservasion(models.Model):
    date_time       = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Reservasion Date")
    patient         = models.ForeignKey(to='accounts.Patient', on_delete=models.CASCADE)
    clinic          = models.ForeignKey(Clinic, on_delete=models.CASCADE)