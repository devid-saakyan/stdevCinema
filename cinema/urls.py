from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, MovieSeatsView, SeatBookingView

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rooms/<int:pk>/movies/', RoomViewSet.as_view({'get': 'movies'}), name='room-movies'),
    path('seats/<int:movie_id>/', MovieSeatsView.as_view(), name='movie-seats'),
    path('seats/book/', SeatBookingView.as_view(), name='seat-booking'),
]
