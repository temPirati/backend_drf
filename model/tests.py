import pytz
from django.test import TestCase
from model.models import Reservation, Room, User
from datetime import datetime, timedelta


class Test_Create_Room(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_room = Room.objects.create(title='Room_Test', capacity=1, description='Room_Test', room_type='Conference')


    def test_room_detail(self):
        room = Room.objects.get(id=1)
        title = f'{room.title}'
        capacity = f'{room.capacity}'
        description = f'{room.description}'
        room_type = f'{room.room_type}'
        self.assertEqual(title, 'Room_Test')
        self.assertEqual(capacity, '1')
        self.assertEqual(description, 'Room_Test')
        self.assertEqual(room_type, 'Conference')


class Test_Create_User(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='admin', email='admin@a.com', first_name='admin', is_staff=False)


    def test_user_detail(self):
        user = User.objects.get(id=1)
        username = f'{user.username}'
        email = f'{user.email}'
        first_name = f'{user.first_name}'
        self.assertEqual(username, 'admin')
        self.assertEqual(email, 'admin@a.com')
        self.assertEqual(first_name, 'admin')


class Test_Create_Reservation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='admin', email='admin@a.com', first_name='admin')
        cls.test_room = Room.objects.create(title='Room_Test', capacity=1, description='Room_Test', room_type='Conference')
        cls.test_reservation = Reservation.objects.create(
            room_id=cls.test_room,
            user_id=cls.test_user,
            start=datetime.now().replace(second=0, microsecond=0),
            duration_hours=1,
            duration_minutes=1
        )

    def test_reservation_detail(self):
        utc = pytz.UTC
        reservation = Reservation.objects.get(id=1)
        user = User.objects.get(id=1)
        room = Room.objects.get(id=1)
        room_id = f'{reservation.room_id}'
        user_id = f'{reservation.user_id}'
        start = f'{reservation.start}'
        duration_hours = f'{reservation.duration_hours}'
        duration_minutes = f'{reservation.duration_minutes}'
        end = f'{reservation.end}'
        self.assertEqual(start, str(utc.localize(datetime.now().replace(second=0, microsecond=0))))
        self.assertEqual(duration_hours, '1')
        self.assertEqual(duration_minutes, '1')
        self.assertEqual(end, str(utc.localize(datetime.now().replace(second=0, microsecond=0) + timedelta(hours=int(duration_hours), minutes=int(duration_minutes)))))
