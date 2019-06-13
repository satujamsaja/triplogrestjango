from django.contrib import admin
from triplog.models import Category, Location, Trip


"""
Category admin.
"""


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_status')
    list_filter = ('category_name', 'category_status')



"""
Category admin.
"""


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_body', 'location_status', 'location_date')
    list_filter = ('location_name', 'location_status')


"""
Category admin.
"""


class TripAdmin(admin.ModelAdmin):
    list_display = ('trip_name', 'trip_category', 'trip_status', 'trip_date')
    list_filter = ('trip_name', 'trip_category', 'trip_status')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Trip, TripAdmin)
