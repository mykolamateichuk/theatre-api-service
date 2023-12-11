from django.db import models

from user.models import User


class Actor(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    class Meta:
        ordering = ["last_name"]

    @property
    def full_name(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Play(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField()

    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="plays")

    def __str__(self) -> str:
        return f"{self.title}"


class TheatreHall(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return f"{self.name} ({self.capacity} seats)"


class Performance(models.Model):
    play = models.ForeignKey(Play,
                             related_name="performance",
                             on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall,
                                     related_name="performance",
                                     on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.show_time}: {self.play.title} ({self.theatre_hall.name})"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
                             related_name="reservations",
                             on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Reservation made: {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()

    performance = models.ForeignKey(Performance,
                                    related_name="ticket",
                                    on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation,
                                    related_name="ticket",
                                    on_delete=models.CASCADE)

    def __str__(self) -> str:
        return (f"{self.performance}"
                f"Row: {self.row}, Seat: {self.seat}")
