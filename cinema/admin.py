from django.contrib import admin
from . import models


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Movie)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_time', 'room', )


@admin.register(models.Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('room', 'row', 'seat_number', 'movie', 'is_booked',)