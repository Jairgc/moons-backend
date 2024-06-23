from django.db import models

# Create your models here.

class SmileCenter (models.Model):
    id = models.BigAutoField(primary_key=True)
    id_external = models.IntegerField()
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True)
    apt = models.CharField(max_length=50)
    time_table = models.CharField(max_length=150)
    region = models.CharField(max_length=100, null=True)
    cp = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=100, null=True)
    center_type_name = models.CharField(max_length=100)
    services = models.CharField(max_length=1000)
    zone = models.CharField(max_length=100)


class CenterType (models.Model):
    id = models.BigAutoField(primary_key=True)
    center_type_name = models.CharField(max_length=100)


class SmileCenterByCenterType (models.Model):
    smile_center_id = models.IntegerField()
    center_type_id = models.IntegerField()

class Service (models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id  = models.CharField(max_length=100)
    appointment_type_id = models.CharField(max_length=100)

class SmileCenterByServices (models.Model):
    smile_center_id = models.IntegerField()
    services_id = models.IntegerField()

class Zone (models.Model):
    id = models.BigAutoField(primary_key=True)
    zone = models.CharField(max_length=100)

class SmileCenterByZones (models.Model):
    smile_center_id = models.IntegerField()
    zone_id = models.IntegerField()
