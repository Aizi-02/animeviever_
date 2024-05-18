from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import datetime
from .clickhouse import client


client.execute("CREATE DATABASE IF NOT EXISTS animeviever ")

client.execute("CREATE TABLE IF NOT EXISTS animeviever.views ("
               "event_id UUID,"
               "user_id UUID,"
               "genre String,"
               "created_at DateTime,"
               "page String,"
               "number_series Int64"
               ")"
               "ENGINE = MergeTree() "
               "PRIMARY KEY (event_id)")

client.execute("CREATE TABLE IF NOT EXISTS animeviever.count_vie ("
               "id UUID,"
               "user_id UUID,"
               "click_id UUID,"
               "time Int64,"
               "name_anime String,"
               "ganre_anime String,"
               "num_seria Int64"
               ")"
               "ENGINE = MergeTree() "
               "PRIMARY KEY (name_anime)")


# client.execute("CREATE VIEW IF NOT EXISTS animeviever.stat "
#                "AS SELECT cv.user_id AS user_id, cv.ganre_anime AS ganre, created_at AS time,  FROM animeviever.count_vie cv LEFT JOIN animeviever.views ON animeviever.count_vie.user_id = animeviever.views.user_id")




class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    RANK = (
        ("Новичек", "Новичек"),
        ("ученик","ученик"),
    )

    email = models.EmailField(max_length=100)
    status = models.CharField(max_length=100,default="Без статуса")
    avatar = models.ImageField(upload_to='images/',blank=True)
    date_creation = models.DateField(default=datetime.now().date())
    rank = models.CharField(max_length=50,choices=RANK,default = "Новичек")

    

class Anime(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=1500)
    description = models.CharField(max_length=1500)
    date_time = models.DateField(default=datetime.now().date())
    voise = models.CharField(default="anilibria",max_length=100)

    genre = models.CharField(max_length=1000)
    mean_continiously = models.IntegerField(default=24)
    
    def __str__(self):
        return self.name

class Season(models.Model):
    MARK = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        (6,6),
        (7,7),
        (8,8),
        (9,9),
        (10,10),
    )
    film_serier = (
        ("ТВ сериал","ТВ сериал"),
        ("Фильм","Фильм"),
    )
    STATUS = (
        ("Онгоинг","Онгоинг"),
        ("Планируется","Планируется"),
        ("Вышло","Вышло"),
        
    )
    
    id = models.AutoField(primary_key=True)
    season_id = models.IntegerField(default=1)
    anime = models.ForeignKey("Anime",on_delete=models.CASCADE)
    types = models.CharField(max_length=200,choices=film_serier)
    status = models.CharField(max_length=50,choices=STATUS)
    liked = models.IntegerField(choices=MARK)

    def __str__(self):
        return str(self.anime)+"/"+str(self.season_id)
    
    


class Series(models.Model):
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    season = models.ForeignKey("Season",on_delete=models.CASCADE)
    series_id = models.IntegerField(default=1)
    title = models.CharField(max_length=400)
    url = models.CharField(max_length=4000)
    
    
    
    
    def __str__(self):
        return self.title
    



