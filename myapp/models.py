# Create your models here.
from django.db import models


# Create your models here.

class Flight(models.Model):
    flight_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    atickets = models.DecimalField(decimal_places=0, max_digits=2)    
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    tclass = models.CharField(max_length=10)

    def __str__(self):
        return self.flight_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    flightid=models.IntegerField()
    flight_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    tickets = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)
    tclass = models.CharField(max_length=10) 

    def __str__(self):
        return self.email
