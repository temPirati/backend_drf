from model.models import *
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


class RoomSerializerPost(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    class Meta:
        model = Room
        fields = ('title', 'capacity', 'description', 'room_type', 'image')


class RoomSerializerGet(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=150)
    capacity = serializers.IntegerField()
    description = serializers.CharField()
    room_type = serializers.ChoiceField(choices=options)
    image = serializers.ImageField()


class ReservationSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    end = serializers.DateTimeField(format='%d/%m/%Y %H:%M')

    class Meta:
        model = Reservation
        fields = ('id', 'room_id', 'user_id', 'start', 'end', 'duration_hours', 'duration_minutes')


class ReservationDetailData(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'room_id', 'user_id', 'start', 'duration_hours', 'duration_minutes')


class RoomSerializerDetail(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=150)
    reservations = ReservationSerializer(many=True, read_only=True)
    capacity = serializers.IntegerField()
    description = serializers.CharField()
    room_type = serializers.ChoiceField(choices=options)
    image = serializers.ImageField()


class SmallRoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=150)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20)


class ReservationSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('room_id', 'user_id', 'start', 'duration_hours', 'duration_minutes')