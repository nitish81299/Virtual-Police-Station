from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


CATEGORIES_OF_CRIME = (
    ('1', 'Robbery'),
    ('2', 'Murder'),
    ('3', 'Kidnapping'),
    ('4', 'Child Abuse'),
    ('5', 'Domestic Abuse'),
    ('6', 'Missing'),
    ('7', 'Other'),
)


class Report(models.Model):
    victim = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fathers_name = models.CharField(max_length=30)
    address = models.CharField(max_length=128)
    email = models.EmailField(max_length=70)
    aadhaar_regex = RegexValidator(
        regex=r'[0-9]{12}',
        message='Enter a valid aadhaar number.'
    )
    aadhaar_number = models.CharField(validators=[aadhaar_regex], max_length=12)
    contact_regex = RegexValidator(
        regex=r'^[789][0-9]{9}$',
        message='Enter a valid mobile number.'
    )

    contact = models.CharField(validators=[contact_regex], max_length=10)
    category_of_crime = models.CharField(max_length=1, choices=CATEGORIES_OF_CRIME)
    place_of_crime = models.CharField(max_length=128)
    date_time_of_crime = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    other_details = models.TextField()

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.description
