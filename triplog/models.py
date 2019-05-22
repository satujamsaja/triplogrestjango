from django.db import models
from django.contrib.auth.models import User

"""
Category Model
"""


class Category(models.Model):
    CATEGORY_STATUS_CHOICES = (
        ('0', 'Unpublished'),
        ('1', 'Published'),
    )
    category_name = models.CharField(blank=False, max_length=255)
    category_status = models.CharField(max_length=1, choices=CATEGORY_STATUS_CHOICES, blank=False, default='1')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


"""
Location Model
"""


class Location(models.Model):
    LOCATION_STATUS_CHOICES = (
        ('0', 'Unpublished'),
        ('1', 'Published')
    )
    location_name = models.CharField(blank=False, max_length=255)
    location_body = models.TextField(blank=True)
    location_status = models.CharField(max_length=1, choices=LOCATION_STATUS_CHOICES,  blank=False, default='1')

    def __str__(self):
        return self.location_name


"""
Trip Model
"""


class Trip(models.Model):
    TRIP_STATUS_CHOICES = (
        ('0', 'Unpublished'),
        ('1', 'Published')
    )
    trip_name = models.CharField(blank=False, max_length=255)
    trip_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trip_body = models.TextField(blank=False)
    trip_user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_location = models.ManyToManyField(Location, blank=True)
    trip_status = models.CharField(max_length=1, choices=TRIP_STATUS_CHOICES, blank=False, default='1')

    def __str__(self):
        return self.trip_name