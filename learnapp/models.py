from django.db import models
from django.contrib.auth.models import User # This User is inbuilt Models of Django , Have Multiple fields like 

# Create your models here.
class UserDetails(models.Model): # This UserDetails is the custom Models which we have created 
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    #additional fiels             
    phone = models.BigIntegerField()
    address = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    userpic = models.ImageField(upload_to='userimg/',blank=True,null=True)

    def __str__(self):
        return self.user.username