from django.db import models
from django.contrib.auth.models import User
from doctors.models import ALLDOCTORS
from learnapp.models import UserDetails
# Create your models here.

ALL_LAB_TESTS = [
    ('CBC', 'Complete Blood Count'),
    ('LFT', 'Liver Function Test'),
    ('URINE_TOTAL', 'Urine Total Test'),
    ('URINE_MICRO', 'Urine Microscopic'),
    ('SERUM', 'Serum Routine'),
    ('THYROID', 'Thyroid'),
]

TEST_STATUS = [
    ('pending', 'Pending'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
]

RESULT_RANGE = [
    ('nil', 'Nil'),
    ('positive', 'Positive'),
    ('negative', 'Negative'),
    ('normal', 'Normal'),
    ('abnormal', 'Abnormal'),
]

class LabTecnicians(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    emp_id=models.CharField(max_length=20)
    qualification=models.CharField(max_length=100)
    year_of_experience=models.IntegerField()
    address=models.CharField(max_length=100)

class LabTests(models.Model):
    reffered_by=models.ForeignKey(ALLDOCTORS,on_delete=models.CASCADE)
    patient_name=models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    lab_test=models.CharField(max_length=100,choices=ALL_LAB_TESTS)
    lab_result=models.CharField(max_length=100,choices=TEST_STATUS,default='Ongoing')
    created_at=models.DateTimeField(auto_now_add=True)
    result_range=models.CharField(max_length=100,choices=RESULT_RANGE,default='Nil')
    result_desc=models.TextField()
    test_cost=models.IntegerField()
    
     
 