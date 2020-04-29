from django.contrib import admin
from .models import *
# Register your models here.

myModels = [Stat, Zakaznik, Zanr, Polozka, Interpret, Vydavatelstvi, Objednavka]  # iterable list
admin.site.register(myModels)
