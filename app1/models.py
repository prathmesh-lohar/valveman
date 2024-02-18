from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class tanks(models.Model):
    tank_no = models.IntegerField(primary_key=True)
    owt_tank_name = models.CharField(max_length=255,blank=True,null=True)
    owt_address = models.CharField(max_length=255,blank=True,null=True)
    owt_position = models.CharField(max_length=255,blank=True,null=True)
    owt_tank_shape = models.CharField(max_length=255,blank=True,null=True)
    owt_dimension_cm = models.CharField(max_length=255,blank=True,null=True)
    inlet_pip = models.CharField(max_length=255,blank=True,null=True)
    inlet_pip_size_cm = models.CharField(max_length=255,blank=True,null=True)
    outlet_pip = models.CharField(max_length=255,blank=True,null=True)
    outlet_pip_size_cm = models.CharField(max_length=255,blank=True,null=True)
    latitude = models.CharField(max_length=255,blank=True,null=True)
    longitude = models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self):
        return self.owt_tank_name
    
    
class marker(models.Model):
     
     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
     
     # a unique integer identifier for each entry
     path_id = models.IntegerField(null=True, blank=True)
     point_id = models.IntegerField(null=True, blank=True)
     
     purpose = models.CharField(max_length=255,null=True,blank=True)
     detail = models.CharField(max_length=255,null=True,blank=True)
     type = models.CharField(max_length=255,null=True,blank=True)
     
  
     
     latitude = models.FloatField(null=True,blank=True)
     longitude = models.FloatField(null=True,blank=True)
     
     # Dictionary to store markers by sequence number

     
     
     