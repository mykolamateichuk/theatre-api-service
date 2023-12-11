from django.urls import include, path
from rest_framework import routers

from theatre.views import ActorViewSet, GenreViewSet, PlayViewSet, TheatreHallViewSet, PerformanceViewSet

router = routers.DefaultRouter()

router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("plays", PlayViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("performances", PerformanceViewSet)
# router.register("reservations", ReservationViewSet)


urlpatterns = [
    path("", include(router.urls))
]

app_name = "theatre"
