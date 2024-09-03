from django.http import JsonResponse
from django.core import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from app.appadmin.models import Train, BookedTrainSeat
from django.db import transaction # to handle race condition

@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if not (username and email and password):
            return JsonResponse({
                "status": False,
                "message": "Some fields are missing in payload!"
            }, status=400)

        check_user = User.objects.filter(username=username).first()
        if(check_user):
            return JsonResponse({
                "status": False,
                "message": "Already created account with this username!"
            }, status=400)
        
        create_account = User.objects.create_user(username, email, password)
        create_account.save()

        return JsonResponse({
            "status": True,
            "message": "Account successfully created!",
            "user_id": create_account.id
        }, status=200)


@csrf_exempt
def login(request):
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
        
        refresh = RefreshToken.for_user(check_user)
        access_token = str(refresh.access_token)
        return JsonResponse(
            {
                "status": True,
                "user_id": check_user.id,
                "access_token": access_token
            }
        )

@csrf_exempt
def availableTrain(request):
    if request.method == "GET":
        source = request.GET.get("source")
        destination = request.GET.get("destination")
        if not (source and destination):
            return JsonResponse({
                "status": False,
                "message": "Some fields are missing in payload!"
            }, status=400)
        
        fetchTrains = Train.objects.filter(source=source, destination=destination).values("id", "trainName", "availableSeat")
        return JsonResponse({
            "status": True,
            "data": list(fetchTrains)
        }, status=200)
    

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@transaction.atomic
def bookSeat(request, train_id):
    numberOfSeatsToBook = json.loads(request.body).get("no_of_seats")
    userId = request.user.id
    if not (numberOfSeatsToBook and userId):
        return JsonResponse({
            "status": False,
            "message": "Some fields are missing in payload!"
        }, status=400)
    
    # Lock the train row for update
    train_instance = Train.objects.select_for_update().get(id=train_id)

    if train_instance:
        if train_instance.availableSeat >= numberOfSeatsToBook:

            listOfSeatNumber = []
            for num in range(1, numberOfSeatsToBook+1):
                seatNumber = train_instance.seatCapacity - train_instance.availableSeat + num
                listOfSeatNumber.append(seatNumber)
            print(f"listOfSeatNumber : {listOfSeatNumber}")
        
            bookSeats = BookedTrainSeat.objects.create(
                user_id=userId,
                train_id=train_id,
                seatNumbers=','.join(map(str, listOfSeatNumber))
            )
            bookSeats.save()

            train_instance.availableSeat -= numberOfSeatsToBook
            train_instance.save()

            responseData = {
                "booking_id": bookSeats.id,
                "seat_numbers": bookSeats.get_seat_numbers(),
                "message": "Seat booked successfully!"
            }
            return JsonResponse({
                "status": True,
                "data": responseData
            }, status=200)
        else:
            return JsonResponse({
                "status": True,
                "message": "Seats are not available to book!"
            }, status=200)

    return JsonResponse({
            "status": False,
            "message": "Train not found!"
        }, status=400)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def bookingDetails(request, booking_id):
    userId = request.user.id
    # Lock the train row for update
    fetchBooking = BookedTrainSeat.objects.select_related('train').filter(id=booking_id, user_id=userId).first()
    if not fetchBooking:
        return JsonResponse({
                "status": False,
                "message": "No booking found!"
            }, status=400)
    
    responseData = {
        "booking_id": fetchBooking.id,
        "user_id": fetchBooking.user_id,
        "train_id": fetchBooking.train_id,
        "train_name": fetchBooking.train.trainName,
        "no_of_seats": len(fetchBooking.get_seat_numbers()),
        "seat_numbers": fetchBooking.get_seat_numbers(),
        "arrival_time_at_source": fetchBooking.train.arrivalTimeAtSource,
        "arrival_time_at_destination": fetchBooking.train.arrivalTimeAtDestination,
        "booking_date": fetchBooking.createdAt
    }
    return JsonResponse({
        "status": True,
        "data": responseData
    })