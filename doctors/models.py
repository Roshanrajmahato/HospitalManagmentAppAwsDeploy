from django.db import models
from django.contrib.auth.models import User
# Create your models here.
specializations = [
    ('GENERAL MEDICINE','general medicine'),
    ('CARDIOLOGIST','cardiologist'),
    ('ORTHOPEDIC','orthopedic'),
    ('EYE SPECIALIST','eye specialist'),
    ('DENTIST','dentist'),
    ('OTHERS','others')
]

class ALLDOCTORS(models.Model):
    name = models.CharField(max_length=100)
    specialized = models.CharField(max_length=100,choices=specializations)
    yoe = models.IntegerField()
    license_no = models.CharField(max_length=100)
    certificate = models.ImageField(upload_to='certificates/',blank=True,null=True)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=100)
    phone = models.BigIntegerField()

    def __str__(self):
        return self.name
    
class Treatment(models.Model):
    TREATMENT_CATEGORIES = [
        ('GENERAL', 'General'),
        ('HEART', 'Heart'),
        ('ORTHO', 'Orthopedic'),
        ('EYE', 'Eye'),
        ('DENTAL', 'Dental'),
        ('OTHER', 'Other'),
    ]

    treatment_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=TREATMENT_CATEGORIES)
    doctor = models.ForeignKey('ALLDOCTORS', on_delete=models.CASCADE,related_name='treatment')
    description = models.TextField()

    def __str__(self):
        return self.treatment_name
    
class Appointment(models.Model):
    TIME_SLOTS = [
        ('10AM-12PM', '10AM-12PM'),
        ('12PM-2PM', '12PM-2PM'),
        ('4PM-6PM', '4PM-6PM'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    doctor = models.CharField(max_length=100)
    treatment = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    consultation_fee = models.CharField(max_length=100,default=500,blank=True)

    def __str__(self):
        return str(self.treatment)