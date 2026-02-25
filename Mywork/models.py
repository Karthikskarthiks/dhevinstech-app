from django.db import models
from django.utils import timezone

class Labour(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Site(models.Model):
    site_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
         return f"{self.site_name}\n{self.location}"
    
class Vendor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WorkDetail(models.Model):
    date = models.DateField(default=timezone.now)
    labours = models.ManyToManyField(Labour)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)   
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    work_description = models.TextField()
    material_description = models.TextField(null=True, blank=True)
    check_in = models.TimeField(null=True, blank=True) 
    check_out = models.TimeField(null=True, blank=True)

    def __str__(self):
        labour_names = ", ".join([l.name for l in self.labours.all()])
        return f"{self.date} - {labour_names}"