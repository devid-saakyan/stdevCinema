from django.contrib import admin
from . import models

admin.site.site_header = "stdevCinema Admin Panel"
admin.site.site_title = "stdevCinema Admin"
admin.site.index_title = "Welcome to the stdevCinema Admin Dashboard"

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(models.Movie)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_time', 'room', )


@admin.register(models.Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('room', 'row', 'seat_number', 'movie', 'is_booked',)