from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to="posters/")
    show_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="movies")

    def __str__(self):
        return f"{self.title} at {self.show_time}"


class Seat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="seats")
    row = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="booked_seats", null=True, blank=True)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ("room", "row", "seat_number", "movie")

    def __str__(self):
        return f"Row {self.row}, Seat {self.seat_number} in {self.room.name}"