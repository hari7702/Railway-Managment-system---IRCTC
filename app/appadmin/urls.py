from django.urls import path
from app.appadmin import views

urlpatterns = [
    # Create or Add new train
    path("trains/create", views.addTrain, name="addTrain"),
    path("adminLogin", views.adminLogin, name="adminLogin"),
    path("adminLogout", views.adminLogout, name="adminLogout")
]