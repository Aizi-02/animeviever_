
from django.contrib import admin
from django.urls import path,include
from viever.views import register,user_login
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("viever.urls")),
    


]
