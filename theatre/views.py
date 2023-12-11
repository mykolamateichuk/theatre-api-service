from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from theatre.models import Actor
from theatre.paginations import ActorPagination
from theatre.serializers import ActorSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    pagination_class = ActorPagination
    serializer_class = ActorSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )


class GenreViewSet(viewsets.ModelViewSet):
    pass


class PerformanceViewSet(viewsets.ModelViewSet):
    pass


class TheatreHallViewSet(viewsets.ModelViewSet):
    pass


class PlayViewSet(viewsets.ModelViewSet):
    pass


class ReservationViewSet(viewsets.ModelViewSet):
    pass
