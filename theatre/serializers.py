from rest_framework import serializers

from theatre.models import Actor, Genre, Play, TheatreHall, Performance


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")
        read_only_fields = ("full_name", )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres")


class PlayListSerializer(PlaySerializer):
    actors = serializers.StringRelatedField(many=True, read_only=True)
    genres = serializers.StringRelatedField(many=True, read_only=True)


class PlayDetailSerializer(PlaySerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)


class TheatreHallDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class TheatreHallListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "capacity")


class PerformanceListSerializer(serializers.ModelSerializer):
    play = serializers.StringRelatedField(many=False, read_only=False)
    theatre_hall = serializers.StringRelatedField(many=False, read_only=False)

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceDetailSerializer(serializers.ModelSerializer):
    play = PlayDetailSerializer(many=False, read_only=False)
    theatre_hall = TheatreHallDetailSerializer(many=False, read_only=False)

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")
