from django.contrib import admin
from .models import Anime,Season,Series,User
from .forms import AnimeAdminForm
from django.contrib import admin


class AnimeAdmin(admin.ModelAdmin):
    form = AnimeAdminForm

admin.site.register(Anime, AnimeAdmin)

class SeriesInline(admin.TabularInline):
    model = Series

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    inlines = [SeriesInline]

# Register your models here.

admin.site.register(Series)


admin.site.register(User)