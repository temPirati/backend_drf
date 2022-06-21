import pytz
from model.models import Room, Reservation, User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from datetime import datetime


class TestPostRooms(APITestCase):

    # test_room = Room.objects.create(title='Room_Test', capacity=1, description='Room_Test', room_type='Conferece')
    def text_post_room_fail(self):
        url = reverse('reserve_api:post_rooms')
        data = {'title': '', 'capacity': 'asdf', 'description': '', 'room_type': ''}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_room(self):
        url = reverse('reserve_api:post_rooms')
        data = {'title': 'Room_Test', 'capacity': 1, 'description': 'Room_Test', 'room_type': 'Conference'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(Room.objects.get().title, 'Room_Test')
        self.assertEqual(Room.objects.get().capacity, 1)
        self.assertEqual(Room.objects.get().description, 'Room_Test')
        self.assertEqual(Room.objects.get().room_type, 'Conference')


class TestPostReservation(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_room = Room.objects.create(title='Room_Test', capacity=1, description='Room_Test', room_type='Conference')
        cls.test_user = User.objects.create(username='admin', email='admin@a.com', first_name='admin')

    def test_create_reservation(self):
        utc = pytz.UTC
        url = reverse('reserve_api:reservation_create')
        date = str(datetime.now(tz=None))[0:16]
        data = {'user_id': '1', 'room_id': '1', 'start': date, 'duration_hours': '1', 'duration_minutes': '1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().user_id, self.test_user)
        self.assertEqual(Reservation.objects.get().room_id, self.test_room)
        self.assertEqual(Reservation.objects.get().start, utc.localize(datetime.now().replace(second=0, microsecond=0)))
        self.assertEqual(Reservation.objects.get().duration_hours, 1)
        self.assertEqual(Reservation.objects.get().duration_minutes, 1)

    def test_create_multiple_reservation(self):
        url = reverse('reserve_api:reservation_create')
        date = str(datetime.now(tz=None))[0:16]
        data = {
            'room_id': '1',
            'reservationArray': [
                {'user_id': '1', 'start': date, 'duration_hours': '1', 'duration_minutes': '1'},
                {'user_id': '1', 'start': date, 'duration_hours': '1', 'duration_minutes': '1'},
                {'user_id': '1', 'start': date, 'duration_hours': 'adsfads', 'duration_minutes': '1'},
            ]
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)


class TestRoomAvailability(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_room = Room.objects.create(title='Room_Test', capacity=1, description='Room_Test', room_type='Conference')
        cls.test_user = User.objects.create(username='admin', email='admin@a.com', first_name='admin')
        cls.test_reservation = Reservation.objects.create(
            room_id=cls.test_room,
            user_id=cls.test_user,
            start=datetime.now().replace(second=0, microsecond=0),
            duration_hours=1,
            duration_minutes=1
        )

    def text_room_availability(self):
        url = reverse('reserve_api:reservation_create')
        date = str(datetime.now(tz=None))[0:16]
        data = {'user_id': '1', 'room_id': '1', 'start': date, 'duration_hours': '1', 'duration_minutes': '1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestPostMultipleRooms(APITestCase):

    def test_create_room(self):
        url = reverse('reserve_api:list-create')
        data = {'roomArray': [
            {'title': 'Room_Test', 'capacity': 1, 'description': 'Room_Test', 'room_type': 'Conference'},
            {'title': 'Room_Test', 'capacity': 1, 'description': 'Room_Test', 'room_type': 'Conference'},
            {'capacity': 1, 'description': 'Room_Test', 'room_type': 'Conference'},
                              ]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 2)



    def test_create_room_single(self):

        url = reverse('reserve_api:list-create')
        data_single = {'title': 'Room_Test', 'capacity': 1, 'description': 'Room_Test', 'room_type': 'Conference'}
        response = self.client.post(url, data_single, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(Room.objects.get().title, 'Room_Test')