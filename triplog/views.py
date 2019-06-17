from triplog.models import Location, Trip, Category
from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

"""
Serializers.
"""


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'category_status')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'location_name', 'location_body', 'location_status', 'location_date')


class TripSerializer(serializers.ModelSerializer):
    trip_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    trip_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Trip
        fields = ('id', 'trip_name',  'trip_category', 'trip_body', 'trip_user', 'trip_location', 'trip_status',
                  'trip_date')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


"""
Viewsets.
"""


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(category_status__exact='1')
    serializer_class = CategorySerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(location_status__exact='1')
    serializer_class = LocationSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.filter(trip_status__exact='1')
    serializer_class = TripSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
Custom Token Obtain Auth.
"""


class ObtainAuthTokenId(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(ObtainAuthTokenId, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})