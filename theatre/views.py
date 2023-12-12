from django.db.models import F, Count
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from theatre.models import Actor, Genre, Play, TheatreHall, Performance, Reservation
from theatre.paginations import ActorPagination, ReservationPagination, PlayPagination
from theatre.serializers import ActorSerializer, GenreSerializer, PlaySerializer, PlayListSerializer, \
    PlayDetailSerializer, TheatreHallListSerializer, TheatreHallDetailSerializer, PerformanceListSerializer, \
    PerformanceDetailSerializer, ReservationListSerializer, ReservationSerializer
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
    pagination_class = PlayPagination

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer

    def get_queryset(self):
        play = self.request.query_params.get("play")
        actors = self.request.query_params.get("actors")
        genres = self.request.query_params.get("genres")

        queryset = self.queryset

        if play:
            queryset = queryset.filter(title__icontains=play)

        if actors:
            actors_id = self._params_to_ints(actors)
            queryset = queryset.filter(actors__id__in=actors_id)

        if genres:
            genres_id = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres_id)

        return queryset.distinct()


class TheatreHallViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = TheatreHall.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrIsAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return TheatreHallListSerializer

        return TheatreHallDetailSerializer


class PerformanceViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = (
        Performance.objects.all()
        .prefetch_related("play", "theatre_hall")
        .annotate(
            tickets_left=(
                F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
                - Count("tickets")
            )
        )
    )
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrIsAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PerformanceDetailSerializer

        return PerformanceListSerializer


class ReservationViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Reservation.objects.prefetch_related(
        "tickets__performance__play__actors",
        "tickets__performance__play__genres",
        "tickets__performance__theatre_hall",
        "tickets__theatre_hall"
    )
    serializer_class = ReservationSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrIsAuthenticatedReadOnly,)
    pagination_class = ReservationPagination

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
