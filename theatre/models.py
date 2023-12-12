from django.db import models
from rest_framework.exceptions import ValidationError

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

    actors = models.ManyToManyField(Actor, related_name="plays",
                                    null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name="plays",
                                    null=True, blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title}"


class TheatreHall(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    class Meta:
        ordering = ["name"]

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

    class Meta:
        ordering = ["-show_time"]

    def __str__(self) -> str:
        return f"{self.show_time}: {self.play.title} ({self.theatre_hall.name})"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
                             related_name="reservations",
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Reservation made: {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()

    performance = models.ForeignKey(Performance,
                                    related_name="tickets",
                                    on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation,
                                    related_name="tickets",
                                    on_delete=models.CASCADE)

    @staticmethod
    def validate_ticket(row, seat, theatre_hall):
        for ticket_attr_value, ticket_attr_name, theatre_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(theatre_hall, theatre_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise ValidationError(
                    {
                        ticket_attr_name: f"{ticket_attr_name}"
                                          f" number must be"
                                          f" in available range:"
                                          f" (1, {theatre_hall_attr_name}):"
                                          f" (1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.performance.theatre_hall,
        )

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        self.full_clean()
        return super().save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self) -> str:
        return (f"{self.performance}"
                f"Row: {self.row}, Seat: {self.seat}")
