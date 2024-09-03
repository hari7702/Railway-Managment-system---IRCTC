from django.http import JsonResponse
from app.appadmin.models import Train
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
  

def is_admin(user):
    return user.is_staff

@csrf_exempt
def adminLogin(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if not (username and password):
            return JsonResponse({
                "status": False,
                "message": "Some fields are missing in payload!"
            }, status=400)
        
        check_user = authenticate(username=username, password=password)
        
        if not check_user:
            return JsonResponse({
                "status": False,
                "message": "Wrong username or password!"
            }, status=400)
        
        if not check_user.is_staff:
            return JsonResponse({
                "status": False,
                "message": "User is not an admin!"
            }, status=403)
        
        login(request, check_user)

        return JsonResponse(
            {
                "status": True,
                "message": "Logged In successfully!",
                "user_id": check_user.id
            }, status=200
        )


@csrf_exempt
def adminLogout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse(
            {
                "status": True,
                "message": "Successfull log out!"
            }, status=200
        )


@csrf_exempt
@user_passes_test(is_admin)
def addTrain(request):
    if request.method == "POST":
        requestBody = json.loads(request.body)
        trainName = requestBody.get("train_name")
        source = requestBody.get("source")
        destination = requestBody.get("destination")
        seatCapacity = requestBody.get("seat_capacity")
        arrivalTimeAtSource = requestBody.get("arrival_time_at_source")
        arrivalTimeAtDestination = requestBody.get("arrival_time_at_destination")

        if not (
            trainName and
            source and 
            destination and 
            seatCapacity and 
            arrivalTimeAtSource and
            arrivalTimeAtDestination):
            return JsonResponse({
                "status": False,
                "message": "Some fields are missing in payload!"
            }, status=400)
        
        train = Train.objects.create(
            trainName=trainName,
            source=source,
            destination=destination,
            seatCapacity=seatCapacity,
            availableSeat=seatCapacity,
            arrivalTimeAtSource=arrivalTimeAtSource,
            arrivalTimeAtDestination=arrivalTimeAtDestination
        )
        train.save()

        return JsonResponse({
            "status": True,
            "message": "Train added successfully!",
            "train_id": train.id
        }, status=200)


