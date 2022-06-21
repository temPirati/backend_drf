# from django.test import TestCase
# from model.models import Room, Reservation, User
# from rest_framework.test import APIRequestFactory, APITestCase
# from django.urls import reverse
# from rest_framework import status
# from datetime import timedelta, datetime
#
#
# class TestPostRooms(APITestCase):
#
#     # test_room = Room.objects.create(title='Room_Test', capacity=1, description='Room_Test', room_type='Conferece')
#
#     def test_create_room(self):
#         url = reverse('list-create')
#         data = {'title': 'Room_Test', 'capacity': '1', 'description': 'Room_Test', 'room_type': 'Conferece'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Room.objects.count(), 1)
#         self.assertEqual(Room.objects.get().title, 'Room_Test')
#         self.assertEqual(Room.objects.get().capacity, 1)
#         self.assertEqual(Room.objects.get().description, 'Room_Test')
#         self.assertEqual(Room.objects.get().room_type, 'Conferece')
#
#
# class TestPostReservation(APITestCase):
#
#     def setUpTestData(cls):
#         cls.test_room = Room.objects.create(title='Room_Test', capacity=1, description='Room_Test', room_type='Conferece')
#         cls.test_user = User.objects.create(username='admin', email='admin@a.com', first_name='admin')
#
#     def test_create_reservation(self):
#         url = reverse('reservation_create')
#         data = {'user_id': '1', 'room_id': '1', 'start': '2022-06-23T15:46', 'duration_hours': '1', 'duration_minutes': '1'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Reservation.objects.count(), 1)
#         self.assertEqual(Reservation.objects.get().user_id, 1)
#         self.assertEqual(Reservation.objects.get().room_id, 1)
#         self.assertEqual(Reservation.objects.get().start, datetime('2022-06-23T15:46'))
#         self.assertEqual(Reservation.objects.get().duration_hours, 1)
#         self.assertEqual(Reservation.objects.get().duration_minutes, 1)
#         self.assertEqual(Reservation.objects.get().end, Reservation.objects.get().start + timedelta(hours=self.duration_hours, minutes=self.duration_minutes))
