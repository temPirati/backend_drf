from datetime import timedelta
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models

options = (
    ('conference', 'Conference'),
    ('meeting', 'Meeting'),
)


class ITWorks(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, email, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser duhet te jete is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser duhet te jete is_superuser=True.')

        return self.create_user(username, email, first_name, password, **other_fields)

    def create_user(self, username, email, first_name, password, **other_fields):

        if not username:
            raise ValueError('Duhet te vendosesh nje username')

        if not email:
            raise ValueError('Duhet te vendosesh nje email')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(ITWorks, AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    about = models.TextField()
    # image = model.ImageField(
    #     verbose_name= "image",
    #     help_text="Upload a property image",
    #     upload_to="images/",
    #     default="images/default.png",
    # )
    # alt_text = model.CharField(
    #     verbose_name="Alturnative text",
    #     help_text="Please add alturnative text",
    #     max_length=255,
    #     null=True,
    #     blank=True,
    # )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Room(ITWorks):

    title = models.CharField(max_length=70)
    capacity = models.IntegerField()
    description = models.TextField()
    room_type = models.CharField(max_length=20, choices=options)
    image = models.ImageField(
        verbose_name="image",
        help_text="Upload a property image",
        upload_to="images/",
        default="images/default.png",
    )

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class Reservation(ITWorks):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True)
    duration_hours = models.IntegerField()
    duration_minutes = models.IntegerField()

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def save(self, *args, **kwargs):
        self.end = self.start + timedelta(hours=self.duration_hours, minutes=self.duration_minutes)
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     queryset = Reservation.objects.filter(room_id=self.room_id)
    #     self.end = self.start + timedelta(hours=self.duration.hour, minutes=self.duration.minute)
    #     for data in queryset:
    #         if(self.start > data['start'] and self.start < data['end'] and self.end > data['start'] and self.end < data['end']):
    #             super().save(*args, **kwargs)

# class Room_reserve(ITWorks):
#     room_id = model.ForeignKey(Room, on_delete=model.CASCADE)
#     reservation_id = model.ForeignKey(Reservation, on_delete=model.CASCADE