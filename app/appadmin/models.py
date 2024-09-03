from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# from django.contrib.postgres.fields import ArrayField

class Train(models.Model):
    trainName = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    seatCapacity = models.IntegerField()
    availableSeat = models.IntegerField()
    arrivalTimeAtSource = models.TimeField()
    arrivalTimeAtDestination = models.TimeField()
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return self.trainName


class BookedTrainSeat(models.Model):
    user  =  models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, null=False, on_delete=models.CASCADE)
    seatNumbers = models.CharField(max_length=255)
    createdAt = models.DateTimeField(default=now)

    def get_seat_numbers(self):
        return list(map(int, self.seatNumbers.split(',')))

    def set_seat_numbers(self, seat_numbers_list):
        self.seatNumbers = ','.join(map(str, seat_numbers_list))

    def __str__(self):
        return self.id