from django.urls import include, path
from rest_framework import routers

from theatre.views import ActorViewSet

router = routers.DefaultRouter()

router.register("actors", ActorViewSet)
# router.register("genres", GenreViewSet)
# router.register("performances", PerformanceViewSet)
# router.register("theatre_halls", TheatreHallViewSet)
# router.register("plays", PlayViewSet)
# router.register("reservations", ReservationViewSet)


urlpatterns = [
    path("", include(router.urls))
]

app_name = "theatre"
