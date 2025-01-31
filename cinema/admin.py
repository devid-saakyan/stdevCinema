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
    list_filter = ('room', 'movie',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "movie":
            if "room" in request.GET:
                room_id = request.GET["room"]
                kwargs["queryset"] = models.Movie.objects.filter(room_id=room_id)
            else:
                kwargs["queryset"] = models.Movie.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)