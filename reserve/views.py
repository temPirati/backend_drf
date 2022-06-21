from datetime import datetime,  timedelta
import pytz
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from model.models import Reservation, Room, User


class SerializerMapping:
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)


class ListRoom(SerializerMapping, generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_map = {
        'GET': RoomSerializerGet,
        'POST': RoomSerializerPost,
    }

    def post(self, request, format=None):
        key = 'roomArray'
        if key in request.data:
            if type(request.data['roomArray']) is list:
                count = 1
                form_error_msg = "Error in Form nr "
                form_success_msg = "Created Form nr "
                form_msg = ""
                for room in request.data['roomArray']:
                    post = RoomSerializerPost(data=room, context={'request': request})
                    if post.is_valid():
                        post.save()
                        form_msg = form_msg + form_success_msg + str(count) + ' '
                        count = count + 1
                    else:
                        form_msg = form_msg + form_error_msg + str(count) + ' '
                        count = count + 1
                return Response(form_msg, status=status.HTTP_201_CREATED)
        else:
            post = RoomSerializerPost(data=request.data, context={'request': request})
            if post.is_valid():
                post.save()
                return Response("Room Created", status=status.HTTP_201_CREATED)
            else:
                return Response(post.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRooms(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializerPost

    def pre_save(self, obj):
        obj.samplesheet = self.request.FILES.get('image')

    def post(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response("Room Created", status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetail(SerializerMapping, generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_map = {
        'GET': RoomSerializerDetail,
        'PATCH': RoomSerializerPost,
        'PUT': RoomSerializerPost,
        'DELETE': RoomSerializerPost
    }


class ReservationCreate(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializerPost(many=True)

    def post(self, request, *args, **kwargs):
        count = 1
        form_error_msg = "Error in Form nr "
        form_success_msg = "Created Form nr "
        form_msg = ""
        key = 'reservationArray'
        if key in request.data:
            if type(request.data['reservationArray']) is list:

                for reservation in request.data['reservationArray']:
                    room_id = {'room_id': request.data['room_id']}
                    res = {**room_id, **reservation}
                    reservation = ReservationSerializerPost(data=res)

                    if reservation.is_valid():
                        reservation.save()
                        form_msg = form_msg + form_success_msg + str(count) + ' '
                        count = count + 1
                    else:
                        form_msg = form_msg + form_error_msg + str(count) + ' '
                        count = count + 1

                return Response(form_msg, status=status.HTTP_201_CREATED)

        else:
            serializer = ReservationSerializerPost(data=request.data)
            rez = Reservation.objects.filter(room_id=request.data['room_id'])
            if serializer.is_valid():
                d = request.data['start'].replace('T', ' ')
                startDate = datetime.strptime(d, '%Y-%m-%d %H:%M')
                hours = int(request.data['duration_hours'])
                minutes = int(request.data['duration_minutes'])
                endDate = startDate + timedelta(hours=hours, minutes=minutes)
                utc = pytz.UTC
                startDate = utc.localize(startDate)
                endDate = utc.localize(endDate)
                count = 0
                if rez.exists():
                    for reservation in rez.iterator():
                        if (reservation.start <= startDate <= reservation.end) or (
                                reservation.start <= endDate <= reservation.end):
                            return Response("Sorry room is reserved, check for another time", status=status.HTTP_400_BAD_REQUEST)

                    serializer.save()

                    return Response("PostCreated", status=status.HTTP_201_CREATED)
                else:
                    serializer.save()

                    return Response("PostCreated", status=status.HTTP_201_CREATED)
            else:

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReservationDetailData(generics.RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationDetailData


class ReservationDetail(SerializerMapping, generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_map = {
        'GET': ReservationSerializer,
        'PATCH': ReservationSerializerPost,
        'PUT': ReservationSerializerPost,
        'DELETE': ReservationSerializer
    }
