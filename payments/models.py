from django.db import models

from doctors.models import ALLDOCTORS, Treatment
from learnapp.models import UserDetails


class DischargeSummary(models.Model):

    # ===============================
    # ROOM TYPES
    # ===============================

    ROOM_TYPE = [

    ('Common ward', 'Common ward'),

    ('Semi-private', 'Semi-private'),

    ('Private AC', 'Private AC'),

    ('Private Non-AC', 'Private Non-AC'),

    ('Deluxe', 'Deluxe'),
    ]

    FOOD_REQUIRED = [

        ('Yes', 'Yes'),
        ('No', 'No'),

    ]

    # ===============================
    # 🔥 HARDCODED BILLING DATA
    # (Editable Later)
    # ===============================

    ROOM_BILLING = {

    'Common ward': {
        'bed': 250,
        'nursing': 300,
        'doctor': 250,
        'misc': 100,
        'total': 900
    },

    'Semi-private': {
        'bed': 1000,
        'nursing': 1000,
        'doctor': 550,
        'misc': 250,
        'total': 2800
    },

    'Private AC': {
        'bed': 1500,
        'nursing': 1250,
        'doctor': 650,
        'misc': 350,
        'total': 3750
    },

    'Private Non-AC': {
        'bed': 1250,
        'nursing': 1150,
        'doctor': 650,
        'misc': 300,
        'total': 3350
    },

    'Deluxe': {
        'bed': 2000,
        'nursing': 1500,
        'doctor': 850,
        'misc': 500,
        'total': 4850
    }
    }

    FOOD_PER_DAY = 480
    MEDICINE_PERCENTAGE = 10

    # ===============================
    # BASIC DETAILS
    # ===============================

    patient = models.ForeignKey(
        UserDetails,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        ALLDOCTORS,
        on_delete=models.CASCADE
    )

    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    doa = models.DateField()

    dod = models.DateField()

    room_type = models.CharField(
        max_length=50,
        choices=ROOM_TYPE
    )

    food_required = models.CharField(
        max_length=10,
        choices=FOOD_REQUIRED
    )

    # ===============================
    # CALCULATED FIELDS
    # ===============================

    total_days = models.IntegerField(
        blank=True,
        null=True
    )

    bed_total = models.IntegerField(
        blank=True,
        null=True
    )

    nursing_total = models.IntegerField(
        blank=True,
        null=True
    )

    doctor_total = models.IntegerField(
        blank=True,
        null=True
    )

    misc_total = models.IntegerField(
        blank=True,
        null=True
    )

    room_total = models.IntegerField(
        blank=True,
        null=True
    )

    food_total = models.IntegerField(
        blank=True,
        null=True
    )

    medicine_total = models.IntegerField(
        blank=True,
        null=True
    )

    grand_total = models.IntegerField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # ===============================
    # 🔥 BILL CALCULATION ENGINE
    # ===============================
    def save(self, *args, **kwargs):

        # ✅ AUTO CALCULATE TOTAL DAYS
        if self.doa and self.dod:

            days = (self.dod - self.doa).days

            if days <= 0:
                days = 1   # minimum 1 day

            self.total_days = days

            print("Calculated Days:", self.total_days)

        else:
            print("DOA or DOD Missing")

        # ✅ GET ROOM DATA
        billing = self.ROOM_BILLING.get(self.room_type)

        if billing and self.total_days:

            self.bed_total = billing['bed'] * self.total_days
            self.nursing_total = billing['nursing'] * self.total_days
            self.doctor_total = billing['doctor'] * self.total_days
            self.misc_total = billing['misc'] * self.total_days

            self.room_total = (
                self.bed_total +
                self.nursing_total +
                self.doctor_total +
                self.misc_total
            )

            # Food Condition
            if self.food_required == "Yes":

                self.food_total = (

                    self.FOOD_PER_DAY *
                    self.total_days

                )

            else:

                self.food_total = 0

            # Medicine = 10%
            self.medicine_total = (
                self.room_total * 0.10
            )

            # Grand Total
            self.grand_total = (
                self.room_total +
                self.food_total +
                self.medicine_total
            )

        else:
            print("Billing NOT Found or Days Missing")

        super().save(*args, **kwargs)