from django.contrib import admin

from theatre.models import Actor, Genre, Play, TheatreHall, Performance, Reservation

admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Play)
admin.site.register(TheatreHall)
admin.site.register(Performance)
admin.site.register(Reservation)
