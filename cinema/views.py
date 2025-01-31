from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Room, Movie, Seat
from .serializers import RoomSerializer, MovieSerializer, SeatSerializer


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=True, methods=['get'])
    def movies(self, request, pk=None):
        room = self.get_object()
        movies = Movie.objects.filter(room=room)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieSeatsView(generics.ListAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Seat.objects.filter(movie_id=movie_id)


class SeatBookingView(generics.UpdateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def update(self, request, *args, **kwargs):
        seat = self.get_object()

        if seat.is_booked:
            return Response({"error": "This seat is already booked"}, status=status.HTTP_400_BAD_REQUEST)

        seat.is_booked = True
        seat.save()
        return Response({"message": "Seat successfully booked!"}, status=status.HTTP_200_OK)
