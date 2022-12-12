from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin


class Genre(TimeStampedMixin, UUIDMixin):
    """Описывает жанр кинопроизведения."""

    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(
        _("description"), default='description this genre coming soon.')

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Filmwork(TimeStampedMixin, UUIDMixin):
    """Содержит основную информацию о кинопроизведении."""

    class TypeFilm(models.TextChoices):
        FRESHMAN = "movie", _("Movie")
        SOPHOMORE = "tv_show", _("Tv_show")

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"),)
    creation_date = models.DateField(auto_now=True, null=True)
    rating = models.FloatField(
        _("rating"),
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    type = models.CharField(_("type"), max_length=10, choices=TypeFilm.choices)
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = "Кинопроизведение"
        verbose_name_plural = "Кинопроизведения"

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE, related_name='genre_film_works')
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "genre_id"],
                name="genre_film_work_idx")
        ]


class Person(TimeStampedMixin, UUIDMixin):
    """Описывает участника кинопроизведения."""

    full_name = models.CharField(_("full_name"), max_length=255, unique=True)
    filmworks = models.ManyToManyField(Filmwork, through="PersonFilmwork")

    class Meta:
        db_table = "content\".\"person"
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажы"

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):

    class Role(models.TextChoices):
        actor = 'actor', _('actor')
        director = 'director', _('director')
        writer = 'writer', _('writer')

    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE, related_name="persons")
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    role = models.TextField("role", choices=Role.choices)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "person_id", "role"],
                name="film_work_person_idx")
        ]


class ProgressTransferData(models.Model):
    table_name = models.CharField(max_length=50)
    id_row = models.UUIDField()
    count_row = models.PositiveIntegerField()

    class Meta:
        db_table = "content\".\"progress_transfer_data"
        verbose_name = "Прогресс переноса данных"