from django.contrib import admin
from .models import UserInfo, ResType, Restaurant, Rate, Favourite, Menu, FoodType, FoodTypes, Avgprice

# Register your models here.

admin.site.register(UserInfo)
admin.site.register(ResType)
admin.site.register(Restaurant)
admin.site.register(Rate)
admin.site.register(Favourite)
admin.site.register(Menu)
admin.site.register(FoodType)
admin.site.register(FoodTypes)
admin.site.register(Avgprice)
