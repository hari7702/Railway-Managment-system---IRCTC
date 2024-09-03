from django.urls import path
from app.user import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("trains/availability", views.availableTrain, name="availableTrain"),
    path("trains/<int:train_id>/book", views.bookSeat, name="bookSeat"),
    path("bookings/<int:booking_id>", views.bookingDetails, name="bookingDetails")
]