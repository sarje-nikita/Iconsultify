from django.db import models
from django.urls import reverse


class Business(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    website = models.URLField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    reviews_count = models.IntegerField(blank=True, null=True)
    reviews_average = models.FloatField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    main_business = models.CharField(max_length=100, blank=True, null=True)
    sub_business = models.CharField(max_length=100, blank=True, null=True)
    map = models.TextField(blank=True, null=True)
    hash_value = models.CharField(max_length=64, db_index=True)    
    text = models.CharField(default="")
    # def get_absolute_url(self):
    #     return reverse('city_cost', args=[self.country_name,self.Name])
    def __str__(self):
        return self.name
    

class store(models.Model):
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    hash_value = models.CharField(max_length=64, db_index=True)    

    def __str__(self):
        return self.name




class demo0(models.Model):
    hash_value = models.CharField(max_length=64)    
    name = models.CharField(max_length=255)


class demo1(models.Model):
    hash_value = models.CharField(max_length=64, db_index=True)    
    name = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['hash_value'])
        ] 