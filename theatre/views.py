from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from theatre.models import Actor, Genre
from theatre.paginations import ActorPagination
from theatre.serializers import ActorSerializer, GenreSerializer
from theatre.permissions import IsAdminUserOrIsAuthenticatedReadOnly


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    pagination_class = ActorPagination
    serializer_class = ActorSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAdminUserOrIsAuthenticatedReadOnly, )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrIsAuthenticatedReadOnly,)


class PerformanceViewSet(viewsets.ModelViewSet):
    pass


class TheatreHallViewSet(viewsets.ModelViewSet):
    pass


class PlayViewSet(viewsets.ModelViewSet):
    pass


class ReservationViewSet(viewsets.ModelViewSet):
    pass
