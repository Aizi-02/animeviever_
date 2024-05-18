import time

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from .models import Anime,Season,Series,User
from .forms import RegistrationForm
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.hashers import make_password
from .clickhouse import client
from time import *
from datetime import *
count_main = 2




def register(request):
    if request.method == 'POST':
        # Обработка отправленной формы регистрации
        # Получите данные из формы и выполните необходимую обработку
        
        form = RegistrationForm(request.POST)

        if form.is_valid():
            
            # process form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            

            user = User.objects.create_user( username=username, email=email, password=password,is_active= True)
            

            #finally save the object in db
            user.save()
        # Дополнительная логика регистрации

            myuser = authenticate(request, username=username, password=password)
            
            login(request, myuser)
        else:
            print(form.error_messages)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request, user)
            
        
        return redirect(request.META.get('HTTP_REFERER'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def main_video_list(request):
    global count_main
    type_page = "main_page"
    print(type_page)
    count_main -=1
    favourite_ganres = None
    favourite_ganres = client.execute("SELECT "
                                      "genre,"
                                      "count(genre) AS click_count "
                                      "FROM animeviever.views  GROUP BY genre ORDER BY click_count DESC ")
    anime_set = {}
    anime = Anime.objects.all()
    anime_new = Anime.objects.filter(date_time__gte=datetime.now() - timedelta(days=30))

    for ganre in favourite_ganres:
        # print(ganre, 12)
        ganre = ganre[0].replace(' ','')
        anime_set[ganre] = []
        for ani in anime:

            if ganre in ani.genre:
                anime_set[ganre].append(ani)
    anime_list = []
    for anime_objects in anime_set.values():
        anime_list.extend(anime_objects)
    print(anime_list)

    # last_event = client.execute(
    #     "SELECT * FROM animeviever.views WHERE page = 'anime_video_page' ORDER BY created_at DESC LIMIT 2 "
    # )
    # timer = None
    # print(last_event)
    # if count_main == 1:
    #     timer = None
    #     print(timer)
    # if len(last_event) == 2:
    #     prefer_event_date = last_event[-1][3]
    #     last_event_date = last_event[0][3]
    #     print(prefer_event_date, last_event_date, sep="\n")
    #     timer = (last_event_date - prefer_event_date).seconds
    client.execute("INSERT INTO animeviever.views VALUES("
                   "generateUUIDv4(),"
                   "%(user_id)s,"
                   "%(ganres)s,"
                   "now(),"
                   "%(type_page)s,"
                   "%(num)s"
                   ")", {"user": None,
                         "ganres": "",
                         "type_page": type_page,
                         "num": 0,
                         "user_id": str(User.id)
                         })

    return render(request, 'viever/main_video_list.html',context = {"anime_list":anime_list,"anime_new":anime_new,})
    
        

def anime_detail(request,name):
    anime = Anime.objects.filter(name = name).first()
    seasons = Season.objects.filter(anime = anime)
    series_list = {}
    count = 1
    type_page = "anime_describtion"
    print(type_page)
    ganres = ""
    for i in seasons:
        series = Series.objects.filter(season = i)
        listik = []
        for j in series:
            listik.append(j)
        series_list[count] = reversed(listik)
        count+=1
        ganres = anime.genre.replace("'", " ").replace("[", " ").replace("]", " ")
    # last_event = client.execute(
    #     "SELECT * FROM animeviever.views WHERE page = 'anime_video_page' ORDER BY created_at DESC LIMIT 2 "
    # )
    # timer = None
    # print(last_event)
    # if len(last_event) == 2:
    #     prefer_event_date = last_event[-1][3]
    #     last_event_date = last_event[0][3]
    #
    #     timer = (last_event_date - prefer_event_date).seconds

    client.execute("INSERT INTO animeviever.views VALUES("
                   "generateUUIDv4(),"
                   "%(user_id)s,"
                   "%(ganres)s,"
                   "now(),"
                   "%(type_page)s,"
                   "%(num)s"
                   ")", {"user": None,
                         "ganres": ganres,
                         "type_page": type_page,
                         "num": 0,
                         "user_id": str(User.id)
                         })
   
    return render(request, 'viever/anime_profile.html',context = {"anime":anime,
                                                         "seasons":seasons,
                                                         'series_list': series_list,
                                                         "genres":ganres
                                                                   })
def profile(request):
    type_page = "profile_page"
    print(type_page)
    count_clicks = client.execute("SELECT count() FROM animeviever.views")
    favourite_ganres = None

    favourite_ganres = client.execute("SELECT "
                                      "genre,"
                                      "count(genre) AS click_count "
                                      "FROM animeviever.views  GROUP BY genre ORDER BY click_count DESC ")

    # last_event = client.execute(
    #     "SELECT * FROM animeviever.views WHERE page = 'anime_video_page' ORDER BY created_at DESC LIMIT 2 "
    # )
    # timer = None
    #
    # if len(last_event) == 2:
    #     prefer_event_date = last_event[-1][3]
    #     last_event_date = last_event[0][3]
    #     timer = last_event_date - prefer_event_date
    client.execute("INSERT INTO animeviever.views VALUES("
                   "generateUUIDv4(),"
                   "%(user_id)s,"
                   "%(ganres)s,"
                   "now(),"
                   "%(type_page)s,"
                   "%(num)s"
                   ")", {"user": None,
                         "ganres": "",
                         "type_page": type_page,
                         "num": 0,
                         "user_id": str(User.id)
                         })

    return render(request, 'person_pages/index.html',context =  {"count_clicks":count_clicks[0][0], "favourite_ganre":favourite_ganres[0][0]})



def search_anime(request):
    query = request.GET.get('query')
    print(123)
    anime_list = Anime.objects.filter(name=query)
    
    return render(request, 'viever/search.html', context ={'anime_list': anime_list,})





def video_list(request,name,season_id,series_id):
    type_page = "anime_video_page"
    print(type_page)
    anime = Anime.objects.filter(name = name).first()
    seasons = Season.objects.filter(anime = anime)
    max_seasons = len(seasons)
    max_series =1
    last_series =1
    last_event = client.execute(
        "SELECT * FROM animeviever.views ORDER BY created_at DESC LIMIT 2 "
    )
    # print(str(User.id), "           BBBBBBBBBBBBBBB")
    timer = None

    print(last_event, 222222, len(last_event), sep="\n")
    if len(last_event) == 2:
        prefer_event_date = last_event[-1][3]
        last_event_date = last_event[0][3]

        timer = last_event_date - prefer_event_date
        print(timer, "       UUUUUUUUUUUUUUU")
    if timer:
        if timer.seconds//60 > anime.mean_continiously * 0.85:
            print(str(User.id))
            print( client.execute("SELECT event_id FROM animeviever.views WHERE page = 'anime_video_page' ORDER BY created_at DESC LIMIT 1 ")[0][0])
            print(timer.seconds)
            print(str(anime.name))
            print(str(*anime.genre))
            print(str(series_id))

            client.execute("INSERT INTO animeviever.count_vie VALUES ("
                           "generateUUIDv4(),"
                           "%(user_id)s,"
                           "%(click_id)s,"
                           "%(time)s,"
                           "%(name_anime)s,"
                           "%(type_ganre)s,"
                           "%(num_seria)s"
                           ")", {"user_id": User.id,
                                 "click_id": client.execute(
                                     "SELECT event_id FROM animeviever.views WHERE page = 'anime_video_page' ORDER BY created_at DESC LIMIT 1 "
                                 )[0][0],
                                 "time": timer.seconds,
                                 "name_anime": str(anime.name),
                                 "type_ganre": anime.genre,
                                 "num_seria": str(series_id)
                                 })

    seasons = seasons.filter(season_id = season_id).first()
    series = Series.objects.filter(season = seasons)
    if max_series!= len(series):
        last_series = max_series
        max_series = len(series)

    series = series.filter(series_id = series_id).first()


    ganres = anime.genre.replace("'", " ").replace("[", " ").replace("]", " ")
    client.execute("INSERT INTO animeviever.views VALUES("
                   "generateUUIDv4(),"
                   "%(user_id)s,"
                   "%(ganres)s,"
                   "now(),"
                   "%(type_page)s,"
                   "%(num)s"
                   ")", {"ganres": str(ganres),
                         "type_page": str(type_page),
                         "num": str(series_id),
                         "user_id": str(User.id)
                         })
    

    
    
    return render(request, 'viever/video_list.html', context = {'video': series,
                                                      "id":id,
                                                      "name":name,
                                                      "now_series":series_id,
                                                      "now_season":season_id,
                                                      "max_series":max_series,
                                                      "max_seasons":max_seasons,
                                                      "last_series":last_series,
                                                        })


# создать табличку отдельную с таймером аниме серией