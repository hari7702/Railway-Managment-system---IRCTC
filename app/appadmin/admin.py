from django.contrib import admin
from app.appadmin.models import Train, BookedTrainSeat

# Register your models here.
admin.site.register(Train)
admin.site.register(BookedTrainSeat)