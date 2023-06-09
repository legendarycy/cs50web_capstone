from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class User(AbstractUser):
    pass


class Halls(models.Model):
    hall_num = models.IntegerField(blank = False, null = False)
    seat_rows = models.IntegerField()
    seat_columns = models.IntegerField()

    def __str__(self):
        return(f"hall {self.hall_num} - {self.seat_rows} rows {self.seat_columns} columns" )
    

class Movies(models.Model):
    title = models.CharField(max_length = 100, blank= False, null = False)
    release = models.DateField(blank = True, null = True)
    language = models.CharField(max_length = 100, blank= True, null = True)
    cast = models.TextField(blank = True, null = True)
    director = models.CharField(max_length = 100, blank= True, null = True)
    genre = models.CharField(max_length = 100, blank= True, null = True)
    runtime = models.IntegerField(blank = False, null = False)
    description = models.TextField(blank = True, null = True)
    thumbnail = models.ImageField(upload_to = 'thumbnails/', null = True, blank = True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "release": self.release,
            "language": self.language,
            "cast": self.cast,
            "director": self.director,
            "genre": self.genre,
            "description": self.description,
            "runtime": self.runtime,
            "thumbnail": self.thumbnail.url
        }

    def __str__(self):
        return(f"{self.title} - {self.runtime} mins")
    

class Movie_Hall_Allocation(models.Model):
    movie = models.ForeignKey('Movies', on_delete = models.CASCADE)
    hall = models.ForeignKey('Halls', on_delete = models.CASCADE)
    datetime_info = models.DateTimeField(blank = False, null = False)

    def __str__(self):
        return(f"{self.datetime_info} | {self.movie.title} in hall {self.hall.hall_num} ({self.hall.seat_rows} rows {self.hall.seat_columns} columns)")
    
    def serialize(self):
        return {
            "id": self.id,
            "movie_title": self.movie.title,
            "hall": self.hall.hall_num,
            "rows": self.hall.seat_rows,
            "columns": self.hall.seat_columns,
            "date": self.datetime_info
        }


class Reviews(models.Model):
    author = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'user_review')
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], blank = False, null = False)
    comment = models.TextField(blank = True, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey('Movies', on_delete = models.CASCADE, related_name = 'movie_review')

    def serialize(self):
        return {
            "author": self.author.username,
            "gold_stars": [i for i in range(0, self.rating)],
            "grey_stars": [] if self.rating == 5 else [i for i in range(0, 5-self.rating)],
            "comment": self.comment,
            "timestamp": self.timestamp,
            "movie": self.movie.title
        }
    
    def __str__(self):
        return(f"[{self.movie.title}] {self.author} - {self.rating}/5 - {self.timestamp}")


class Tickets(models.Model):
    choices = (
        ('unavailable', 'unavailable'),
        ('reserved', 'reserved'),
        ('sold', 'sold')
    )
    holder = models.ForeignKey('User', on_delete = models.CASCADE, related_name= 'ticket_bought')
    seat_row = models.CharField(max_length=1, blank= False, null = False)
    seat_column = models.IntegerField(blank= False, null = False)
    session = models.ForeignKey('Movie_Hall_Allocation', on_delete = models.CASCADE, blank = False, null = False, related_name = 'ticket')
    status = models.CharField(max_length = 20, choices = choices, blank = False, null = False)
    timestamp = models.DateTimeField(auto_now = True)
    transaction = models.ForeignKey("Transaction", on_delete = models.CASCADE, blank = True, null = True, related_name = 'ticket')

    def serialize(self):
        return {
            'seat_row': self.seat_row,
            'seat_column': self.seat_column,
            'status': self.status
        }
    
    def __str__(self):
        return(f"{self.holder.username} - {self.session.movie.title} - {self.status} |\
               hall {self.session.hall.hall_num} {self.seat_row} row {self.seat_column} column")


class Transaction(models.Model):
    qr_code = models.ImageField(upload_to = 'transaction_qr/', blank = False, null= False)

    def validate_user(self, username):
        return {
            "outcome": self.ticket.all().first().holder.username == username
        }


class Highlights(models.Model):
    title = models.CharField(max_length=200, blank = False, null = False)
    banner = models.ImageField(upload_to = 'banners/', blank = False, null = False)

    def __str__(self):
        return(f"{self.title}")