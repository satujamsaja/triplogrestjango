from django.conf.urls import url, include
from django.contrib import admin
from triplog.models import Location, Trip, Category
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.views import obtain_auth_token


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'category_status')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'location_name', 'location_body', 'location_status')


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'trip_name', 'trip_body', 'trip_location', 'trip_status')
        depth = 1


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(category_status__exact='1')
    serializer_class = CategorySerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(location_status__exact='1')
    serializer_class = LocationSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.filter(trip_status__exact='1')
    serializer_class = TripSerializer


router = routers.DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'trips', TripViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth-token/', obtain_auth_token, name='api-auth-token')
]

