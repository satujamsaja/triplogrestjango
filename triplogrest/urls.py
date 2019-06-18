from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from triplog.views import *

router = routers.DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'trips', TripViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'users', UserViewSet)
router.register(r'all', TripAllViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth-token/', ObtainAuthTokenId.as_view(), name='api-auth-token')
]

