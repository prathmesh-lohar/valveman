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
 
 

class jw(models.Model):
    jw_no = models.IntegerField(primary_key=True)
    jw_name = models.CharField(max_length=255,blank=True,null=True)
    jw_address = models.CharField(max_length=255,blank=True,null=True)
    jw_position = models.CharField(max_length=255,blank=True,null=True)
    jw_shape = models.CharField(max_length=255,blank=True,null=True)
    jw_dimension_cm = models.CharField(max_length=255,blank=True,null=True)
    inlet_pip = models.CharField(max_length=255,blank=True,null=True)
    inlet_pip_size_cm = models.CharField(max_length=255,blank=True,null=True)
    outlet_pip = models.CharField(max_length=255,blank=True,null=True)
    outlet_pip_size_cm = models.CharField(max_length=255,blank=True,null=True)
    latitude = models.CharField(max_length=255,blank=True,null=True)
    longitude = models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self):
        return self.jw_name
 
 
 
class wtp(models.Model):
    wtp_no = models.IntegerField(primary_key=True)
    wtp_name = models.CharField(max_length=255,blank=True,null=True)
    wtp_address = models.CharField(max_length=255,blank=True,null=True)
    wtp_position = models.CharField(max_length=255,blank=True,null=True)
    wtp_shape = models.CharField(max_length=255,blank=True,null=True)
    wtp_dimension_cm = models.CharField(max_length=255,blank=True,null=True)
    inlet_pip = models.CharField(max_length=255,blank=True,null=True)
    inlet_pip_size_cm = models.CharField(max_length=255,blank=True,null=True)
    outlet_pip = models.CharField(max_length=255,blank=True,null=True)
    outlet_pip_size_cm = models.CharField(max_length=255,blank=True,null=True)
    latitude = models.CharField(max_length=255,blank=True,null=True)
    longitude = models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self):
        return self.wtp_name
    
    
class booster(models.Model):
    booster_no = models.IntegerField(primary_key=True)
    booster_name = models.CharField(max_length=255,blank=True,null=True)
    booster_address = models.CharField(max_length=255,blank=True,null=True)
    booster_position = models.CharField(max_length=255,blank=True,null=True)
    booster_shape = models.CharField(max_length=255,blank=True,null=True)
    booster_dimension_cm = models.CharField(max_length=255,blank=True,null=True)
    inlet_pip = models.CharField(max_length=255,blank=True,null=True)
    inlet_pip_size_cm = models.CharField(max_length=255,blank=True,null=True)
    outlet_pip = models.CharField(max_length=255,blank=True,null=True)
    outlet_pip_size_cm = models.CharField(max_length=255,blank=True,null=True)
    latitude = models.CharField(max_length=255,blank=True,null=True)
    longitude = models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self):
        return self.booster_name
 
 
    
    
class marker(models.Model):
     
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
     
     # a unique integer identifier for each entry
     path_id = models.IntegerField(null=True, blank=True)
     point_id = models.IntegerField(null=True, blank=True)
     
     purpose = models.CharField(max_length=255,null=True,blank=True)
     detail = models.CharField(max_length=255,null=True,blank=True)
     type = models.CharField(max_length=255,null=True,blank=True)
     
  
     
     latitude = models.FloatField(null=True,blank=True)
     longitude = models.FloatField(null=True,blank=True)
     
     pip_material = models.CharField(max_length=255,null=True, blank=True)
     pip_diameter = models.CharField(max_length=255,null=True, blank=True)
     
     valve_type = models.CharField(max_length=255,null=True, blank=True)
     valve_key_size = models.CharField(max_length=255,null=True, blank=True)
     valve_diameter = models.CharField(max_length=255,null=True, blank=True)
     
     
     # Dictionary to store markers by sequence number

     def __str__(self):
        return self.type
     
     