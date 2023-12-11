from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from theatre.models import Actor, Genre, Play
from theatre.paginations import ActorPagination
from theatre.serializers import ActorSerializer, GenreSerializer, PlaySerializer, PlayListSerializer, \
    PlayDetailSerializer
from theatre.permissions import IsAdminUserOrIsAuthenticatedReadOnly


class ActorViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Actor.objects.all()
    pagination_class = ActorPagination
    serializer_class = ActorSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAdminUserOrIsAuthenticatedReadOnly, )


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrIsAuthenticatedReadOnly,)


class PlayViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Play.objects.prefetch_related("actors", "genres")
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrIsAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    pass


class TheatreHallViewSet(viewsets.ModelViewSet):
    pass


class ReservationViewSet(viewsets.ModelViewSet):
    pass
