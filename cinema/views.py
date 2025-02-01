from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Room, Movie, Seat
from django.shortcuts import get_object_or_404
from .serializers import RoomSerializer, MovieSerializer, SeatSerializer
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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


class SeatBookingView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["row_number", "seat_number", "room_id", "movie_id"],
            properties={
                "row_number": openapi.Schema(type=openapi.TYPE_INTEGER),
                "seat_number": openapi.Schema(type=openapi.TYPE_INTEGER),
                "room_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "movie_id": openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={
            200: openapi.Response("This seat is already booked", openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response("Error"),
            404: openapi.Response("Seat not found"),
        }
    )
    def post(self, request, *args, **kwargs):
        row_number = request.data.get("row_number")
        seat_number = request.data.get("seat_number")
        room_id = request.data.get("room_id")
        movie_id = request.data.get("movie_id")

        room = get_object_or_404(Room, id=room_id)
        movie = get_object_or_404(Movie, id=movie_id, room=room)

        seat = Seat.objects.filter(
            row=row_number,
            seat_number=seat_number,
            room=room,
            movie=movie
        ).first()

        if not seat:
            return Response({"error": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)

        if seat.is_booked:
            return Response({"error": "This seat is already booked"}, status=status.HTTP_400_BAD_REQUEST)

        seat.is_booked = True
        seat.save()

        return Response({"message": "Seat successfully booked!"}, status=status.HTTP_200_OK)