# Railway Management API

This is a Railway Management API similar to IRCTC (Real Time).
It can handle race condition while booking train seats.

## Database Configuration in setting.py

```json
{
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "railwaymanagement",
        "USER": "mysql username",
        "PASSWORD": "mysql password",
        "HOST": "localhost",
        "PORT": "3306"
    }
}
```

## How to Run ?

To run this api:
Step-1
```
pip install -r requirements.txt
```
Step-2
```
python manage.py runserver
```

## API Documentation

The project provides the following API endpoints:

### `POST /api/adminLogin`

Login as super user (or admin).

**Request:**

```json
{
  "username": "abhisekupa",
  "password": "abhisekupa32"
}
```

**Response:**
```json
{
  "status": true,
  "message": "Logged In successfully!",
  "user_id": 1
}
```

### `POST /api/adminLogout`

Logout as admin.

**Response:**
```json
{
    "status": true,
    "message": "Successfull log out!"
}
```

### `POST /api/trains/create`

To create a new train with a source and destination.

**Request:**

```json
{
  "train_name": "Express C",
  "source": "Old Delhi",
  "destination": "Chandigarh",
  "seat_capacity": 100,
  "arrival_time_at_source": "14:00:00",
  "arrival_time_at_destination": "20:30:00"
}
```

**Response:**
```json
{
  "status": true,
  "message": "Train added successfully!",
  "train_id": 3
}
```

### `POST /api/signup`

Create user account.

**Request:**

```json
{
  "username": "abhisek",
  "email": "abhisek0721@gmail.com",
  "password": "abhi5432"
}

```

**Response:**
```json
{
  "status": true,
  "message": "Account successfully created!",
  "user_id": 3
}
```

### `POST /api/login`

Provide the ability to the user to log into his account.

**Request:**

```json
{
  "username": "abhisek",
  "password": "abhi5432"
}
```

**Response:**
```json
{
  "status": true,
  "user_id": 2,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3MDEwMjExLCJpYXQiOjE2OTcwMDk5MTEsImp0aSI6IjhhZGU3MzRlY2UwMjQ0NDg4YmMxMjRlZjY1NDkzMmEzIiwidXNlcl9pZCI6Mn0.9Yth37RVMJpFhOk3Tkdxj3-32BqTbXqM88OYRm4KYfE"
}
```

### `GET /api/trains/availability?source={SOURCE}&destination={DESTINATION}`

Users where they can enter the source and destination and fetch all the trains between that route with their
availabilities.

**Request:**

`GET /api/trains/availability?source=Old Delhi&destination=Chandigarh`

**Response:**
```json
{
  "status": true,
  "data": [
    {
      "id": 1,
      "trainName": "Express A",
      "availableSeat": 86
    },
    {
      "id": 2,
      "trainName": "Express B",
      "availableSeat": 100
    },
    {
      "id": 3,
      "trainName": "Express C",
      "availableSeat": 100
    }
  ]
}
```

### `POST /api/trains/{train_id}/book`

To book seats on a particular train.

**Header:**
```json
{
 "Authorization": "Bearer {access_token}"
}
```

**Request:**

```json
{
  "no_of_seats": 3
}
```

**Response:**
```json
{
  "status": true,
  "data": {
    "booking_id": 18,
    "seat_numbers": [
      15,
      16,
      17
    ],
    "message": "Seat booked successfully!"
  }
}
```


### `GET /api/bookings/{booking_id}`

Get specific booking details of an user.

**Header:**
```json
{
 "Authorization": "Bearer {access_token}"
}
```

**Response:**
```json
{
  "status": true,
  "data": {
    "booking_id": 10,
    "user_id": 2,
    "train_id": 1,
    "train_name": "Express A",
    "no_of_seats": 2,
    "seat_numbers": [
      1,
      2
    ],
    "arrival_time_at_source": "14:00:00",
    "arrival_time_at_destination": "20:30:00",
    "booking_date": "2023-10-11T07:11:00.688Z"
  }
}
```


## Contact Information

```
Name: Abhisekh Upadhaya
```

```
Email: abhisek0721@gmail.com
```
